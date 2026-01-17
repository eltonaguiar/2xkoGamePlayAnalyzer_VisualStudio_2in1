"""Lightweight Blitzcrank mirror-match analyzer and helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np

from src.video_analyzer import VideoFrameAnalyzer
from src.analysis_engine import MistakeType, RecommendationEngine
from .config import AnalyzerParameters
from . import blitzcrank_knowledge as bk


@dataclass
class DetectedEvent:
    """Single flash/scramble detected in the video."""

    frame: int
    seconds: float
    timestamp: str
    intensity: float
    motion: float
    tag: str
    confidence: float


@dataclass
class MistakeCallout:
    """Heuristic mistake detection for reporting."""

    player: int
    character: str
    player_name: str
    round: int
    timestamp: str
    seconds: float
    title: str
    detail: str
    range_note: str
    damage_estimate: int
    opponent_response: str
    punished: bool
    punish_damage: int
    opponent_string: str
    recommendations: List[str] = field(default_factory=list)
    severity: str = "info"
    impact: str = "low"


class MirrorMatchAnalyzer:
    """Mirror-match specific analyzer with Blitzcrank heuristics."""

    def __init__(self, params: AnalyzerParameters):
        self.params = params
        self.events: List[DetectedEvent] = []
        self.mistakes: List[MistakeCallout] = []
        self.fps: float = 30.0
        self.total_seconds: float = 0.0
        self.player_names = {
            1: params.player1_name,
            2: params.player2_name,
        }

    def _downscale_gray(self, frame: np.ndarray) -> np.ndarray:
        """Downscale to speed up math-heavy operations."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.resize(gray, (320, 180), interpolation=cv2.INTER_AREA)

    def scan_video(self) -> bool:
        """Walk the video and collect flashes + motion spikes."""
        analyzer = VideoFrameAnalyzer(self.params.video_path)
        if not analyzer.open_video():
            return False
        self.fps = analyzer.fps or 30.0
        self.total_seconds = analyzer.get_video_duration()

        prev_gray: Optional[np.ndarray] = None
        cap = analyzer.cap
        step = max(1, self.params.sample_rate)
        major = self.params.major_flash_threshold
        minor = self.params.flash_threshold
        motion_thresh = self.params.motion_threshold

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % step != 0:
                frame_idx += 1
                continue

            gray = self._downscale_gray(frame)
            motion_score = 0.0
            intensity = 0.0

            if prev_gray is not None:
                diff = cv2.absdiff(prev_gray, gray)
                intensity = float(np.mean(diff))
                # lighter-weight motion proxy: average absolute gradient
                motion_score = float(np.mean(np.gradient(gray.astype(np.float32))))

                if intensity > minor or motion_score > motion_thresh:
                    tag = "heavy_commit" if intensity >= major else "scramble"
                    # Heuristic grab detection: low motion but medium flash near threshold
                    if motion_score < 0.8 and intensity > (minor + 3):
                        tag = "grab_punish"
                    ts_sec = frame_idx / self.fps
                    if ts_sec < self.params.min_event_second:
                        frame_idx += 1
                        prev_gray = gray
                        continue
                    ts = self._format_timestamp(ts_sec)
                    confidence = min(1.0, max(intensity / 100.0, 0.35))
                    self.events.append(
                        DetectedEvent(
                            frame=frame_idx,
                            seconds=ts_sec,
                            timestamp=ts,
                            intensity=round(intensity, 2),
                            motion=round(motion_score, 2),
                            tag=tag,
                            confidence=confidence,
                        )
                    )

            prev_gray = gray
            frame_idx += 1

            if len(self.events) > self.params.max_events:
                break

        analyzer.close()
        return True

    def _timestamp_to_seconds(self, timestamp: str) -> float:
        """Convert MM:SS(.ms or :ff) timestamp to seconds."""
        try:
            if "." in timestamp:
                mm_ss, ms = timestamp.split(".")
                minutes, seconds = map(int, mm_ss.split(":"))
                return minutes * 60 + seconds + int(ms) / 1000.0
            parts = timestamp.split(":")
            if len(parts) == 3:
                minutes, seconds, frames = map(int, parts)
                return minutes * 60 + seconds + frames / (self.fps or 30.0)
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            return 0.0
        except Exception:
            return 0.0

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds -> MM:SS for user clarity (rounded to tenths)."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        tenths = int(((seconds - int(seconds)) * 10))
        if tenths:
            return f"{minutes:02d}:{secs:02d}.{tenths}"
        return f"{minutes:02d}:{secs:02d}"

    def _format_full_timestamp(self, seconds: float) -> str:
        """Full HH:MM:SS.mmm string for tooltips."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"

    def _guess_player(self, idx: int) -> int:
        """Alternate players when we cannot fully disambiguate POV."""
        return 1 if idx % 2 == 0 else 2

    def _describe_event(self, event: DetectedEvent) -> str:
        """Attach matchup-aware description to a detected spike."""
        if event.tag == "grab_punish":
            return "Likely got grabbed/command grabbed; you were stuck until throw ended."
        if event.intensity >= self.params.major_flash_threshold:
            return (
                "Likely big commit (raw 5S2/Super/Ultimate). "
                "If blocked, this is punishable—dash 5L/2L."
            )
        if event.motion < 1.0:
            return "Low-motion spike; often a whiffed grab or slow special."
        return "General scramble/hit exchange."

    def _build_recommendations(self, event: DetectedEvent) -> List[str]:
        tips = []
        if event.tag == "grab_punish":
            tips.append("Delay tech or jump pre-emptively to avoid grab; buffer 5L/2L after block to stop dash-in grab attempts.")
            tips.append("Use backdash/neutral jump when you see run-up to force whiff and punish recovery.")
            return tips
        if event.intensity >= self.params.major_flash_threshold:
            tips.append(
                "On block, punish with 5L (-2 on block) into confirm; 5S2 is -15f."
            )
            tips.append("If this was Super2, roll or jump to avoid lingering field.")
        elif event.motion < 1.0:
            tips.append(
                "If grab whiffed, buffer 66H or 5L starter to punish 50f+ recovery."
            )
        else:
            tips.extend(bk.neutral_game_tips()[:2])
        return tips

    def _damage_estimate(self, severity: str, intensity: float, motion: float, punished: bool) -> int:
        """Coarse damage estimate scaled by visual intensity/motion and punish flag."""
        if not punished:
            return 0
        base = 70 if severity == "minor" else 120
        scaled = base + int(intensity * 2.5) + int(motion * 18)
        return max(60, min(320, scaled))

    def _range_note(self, event: DetectedEvent) -> str:
        """Guidance on spacing if we suspect a whiff."""
        if event.motion < 1.0:
            return "Too far for grab/special—step closer before committing."
        if event.intensity >= self.params.major_flash_threshold:
            return "Likely too close when throwing unsafe special; stay further or cover with assist."
        return "Spacing unclear."

    def produce_mistakes(self) -> None:
        """Convert raw events into human-readable mistakes."""
        if not self.events:
            return

        for idx, event in enumerate(self.events):
            if event.seconds < self.params.min_event_second:
                continue
            player = self._guess_player(idx)
            title = (
                "Over-commit without cover"
                if event.intensity >= self.params.major_flash_threshold
                else "Scramble / possible dropped confirm"
            )
            detail = self._describe_event(event)
            severity = "minor"
            timestamp_sec = event.seconds
            round_num = int(timestamp_sec // self.params.round_length_sec) + 1
            # Punish if clear commitment (major) or notable motion/flash
            punished = True if severity == "major" or event.motion > 1.2 or event.intensity > (self.params.major_flash_threshold * 0.8) or event.tag == "grab_punish" else False
            if punished:
                if event.tag == "grab_punish":
                    opponent_response = "Opponent landed a grab/command grab and took guaranteed damage."
                    opponent_string = "Throw / Command Grab > knockdown (you were stuck until recovery)."
                else:
                    opponent_response = "Opponent punished the opening (jab/2L into confirm)."
                    opponent_string = "5L (jab) > 5M (mid) > 2H (launcher) into knockdown/okizeme."
                punish_damage = self._damage_estimate(severity, event.intensity, event.motion, True)
            else:
                opponent_response = "Likely scramble; limited punish observed."
                opponent_string = "No clear string; scramble/neutral reset."
                punish_damage = 0
            impact = "low"
            self.mistakes.append(
                MistakeCallout(
                    player=player,
                    character="Blitzcrank",
                    player_name=self.player_names.get(player, f"P{player}"),
                    timestamp=event.timestamp,
                    seconds=timestamp_sec,
                    title=title,
                    detail=detail,
                    range_note=self._range_note(event),
                    damage_estimate=self._damage_estimate(severity, event.intensity, event.motion, punished),
                    opponent_response=opponent_response,
                    punished=punished,
                    punish_damage=punish_damage,
                    opponent_string=opponent_string,
                    recommendations=self._build_recommendations(event),
                    severity=severity,
                    impact=impact,
                    round=round_num,  # type: ignore
                )
            )

        # Re-rank severities based on top damage only
        if self.mistakes:
            ranked = sorted(self.mistakes, key=lambda m: m.punish_damage, reverse=True)
            top_count = max(1, int(len(ranked) * 0.2))
            for i, mk in enumerate(ranked):
                if mk.punish_damage <= 0:
                    mk.severity = "minor"
                    mk.impact = "low"
                elif i == 0 and mk.punish_damage >= 180:
                    mk.severity = "critical"
                    mk.impact = "high"
                elif i < top_count or mk.punish_damage >= 130:
                    mk.severity = "major"
                    mk.impact = "medium" if mk.punish_damage < 180 else "high"
                else:
                    mk.severity = "minor"
                    mk.impact = "low"
            # Sort by severity then punish damage then time
            severity_order = {"critical": 3, "major": 2, "minor": 1}
            self.mistakes.sort(
                key=lambda m: (
                    severity_order.get(m.severity, 1) * -1,
                    -m.punish_damage,
                    -self._timestamp_to_seconds(m.timestamp),
                )
            )

    def summarize_players(self) -> Dict[int, Dict]:
        """Crude playstyle summary per player."""
        if not self.events:
            return {}

        players = {1: {"events": 0}, 2: {"events": 0}}
        for idx, event in enumerate(self.events):
            p = self._guess_player(idx)
            players[p]["events"] += 1
            players[p]["big_commits"] = players[p].get("big_commits", 0) + (
                1 if event.intensity >= self.params.major_flash_threshold else 0
            )

        for pid, data in players.items():
            big = data.get("big_commits", 0)
            if big >= max(2, data["events"] // 3):
                style = "Aggressive / commit-heavy"
            elif data["events"] > 8:
                style = "Active neutral / poke-heavy"
            else:
                style = "Low-activity (likely defensive or mis-detected)"
            data["style"] = style
        return players

    def _estimate_round_winners(self, player_summary: Dict[int, Dict]) -> Dict:
        """Heuristic round winner estimate using event density (video-only placeholder)."""
        # With no HUD data, approximate by counting events per round per player and force at least 4 rounds.
        round_events = {}
        for idx, event in enumerate(self.events):
            if event.seconds < self.params.min_event_second:
                continue
            rnd = int(event.seconds // self.params.round_length_sec) + 1
            p = self._guess_player(idx)
            round_events.setdefault(rnd, {1: 0, 2: 0})
            round_events[rnd][p] += 1

        # Ensure at least 4 rounds in the heuristic output
        total_rounds = max(4, int((self.total_seconds or 0) // self.params.round_length_sec) + 1)
        for r in range(1, total_rounds + 1):
            round_events.setdefault(r, {1: 0, 2: 0})

        winners = {}
        for rnd, data in round_events.items():
            if data[1] > data[2]:
                winners[rnd] = 1
            elif data[2] > data[1]:
                winners[rnd] = 2
            else:
                winners[rnd] = 0  # tie/unknown
        # Overall winner guess
        p1_rounds = sum(1 for w in winners.values() if w == 1)
        p2_rounds = sum(1 for w in winners.values() if w == 2)
        overall = 1 if p1_rounds > p2_rounds else 2 if p2_rounds > p1_rounds else 0
        return {"round_winners": winners, "overall_winner": overall, "p1_rounds": p1_rounds, "p2_rounds": p2_rounds}

    def _mock_move_variety(self, player_summary: Dict[int, Dict]) -> Dict[int, List[Dict]]:
        """Placeholder move variety stats (video-only; needs telemetry to be precise)."""
        base_moves = ["5L", "2L", "5S1", "2S2", "66H", "2H", "5S2", "Super1", "Super2"]
        variety = {}
        for pid in (1, 2):
            events = player_summary.get(pid, {}).get("events", 0)
            big = player_summary.get(pid, {}).get("big_commits", 0)
            # distribute counts heuristically across common moves
            counts = []
            for mv in base_moves:
                weight = 1
                if mv in ("5L", "2L"):
                    weight = 3
                elif mv in ("5S1", "66H"):
                    weight = 2
                count = max(0, events // (8 + base_moves.index(mv))) // weight
                counts.append({"move": mv, "uses": count})
            if big:
                counts.append({"move": "Meter/Bar Spend", "uses": big})
            variety[pid] = counts
        return variety

    def run(self) -> Dict:
        """Entry point: scan video then build high-level notes."""
        ok = self.scan_video()
        if not ok:
            return {"error": "Failed to open video"}

        self.produce_mistakes()
        player_summary = self.summarize_players()
        winners = self._estimate_round_winners(player_summary)

        event_rows = [
            {
                "frame": e.frame,
                "seconds": e.seconds,
                "timestamp": e.timestamp,
                "full_timestamp": self._format_full_timestamp(e.seconds),
                "intensity": e.intensity,
                "motion": e.motion,
                "tag": e.tag,
                "confidence": e.confidence,
            }
            for e in self.events
        ]
        mistake_rows = [
            {
                "player": m.player,
                "character": m.character,
                "player_name": m.player_name,
                "round": m.round,
                "timestamp": m.timestamp,
                "seconds": m.seconds,
                "full_timestamp": self._format_full_timestamp(m.seconds),
                "title": m.title,
                "detail": m.detail,
                "range_note": m.range_note,
                "damage_estimate": m.damage_estimate,
                "opponent_response": m.opponent_response,
                "punished": m.punished,
                "punish_damage": m.punish_damage,
                "opponent_string": m.opponent_string,
                "recommendations": m.recommendations,
                "severity": m.severity,
            }
            for m in self.mistakes
        ]

        return {
            "parameters": self.params,
            "events": event_rows,
            "mistakes": mistake_rows,
            "player_summary": player_summary,
            "fps": self.fps,
            "winners": winners,
            "move_variety": self._mock_move_variety(player_summary),
            "knowledge": {
                "unsafe_moves": bk.unsafe_on_block_moves(),
                "safe_pressure": bk.safe_pressure_moves(),
                "preferred_punishes": bk.preferred_punishes(),
                "juggernaut_notes": bk.juggernaut_notes(),
            },
        }

