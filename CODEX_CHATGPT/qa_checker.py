"""QA routine to cross-check damage/health per round against detected mistakes.

This script runs the analyzer, then samples health bars at mistake timestamps
to sanity-check whether a punish actually removed health.

Note: You must configure the health bar regions and colors for your capture.
Defaults are placeholders.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple
import cv2
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from CODEX_CHATGPT.config import AnalyzerParameters
from CODEX_CHATGPT.mirror_matchup import MirrorMatchAnalyzer
from CODEX_CHATGPT.report_builder import ensure_dir


@dataclass
class HealthBarConfig:
    """Health bar region and color range (HSV)."""

    bbox: Tuple[int, int, int, int]  # x, y, w, h
    hsv_low: Tuple[int, int, int]
    hsv_high: Tuple[int, int, int]


def estimate_health(frame, cfg: HealthBarConfig) -> float:
    """Return health fill percentage within the configured box."""
    x, y, w, h = cfg.bbox
    crop = frame[y : y + h, x : x + w]
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, cfg.hsv_low, cfg.hsv_high)
    filled = cv2.countNonZero(mask)
    total = mask.size
    if total == 0:
        return 0.0
    return filled / total


def sample_health_at(video_path: str, seconds: float, fps: float, left_cfg: HealthBarConfig, right_cfg: HealthBarConfig) -> Dict[str, float]:
    """Seek to a timestamp and sample both health bars."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"p1": 0.0, "p2": 0.0}
    frame_idx = int(seconds * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return {"p1": 0.0, "p2": 0.0}
    p1_health = estimate_health(frame, left_cfg)
    p2_health = estimate_health(frame, right_cfg)
    cap.release()
    return {"p1": p1_health, "p2": p2_health}


def run_qa(video_path: str, left_cfg: HealthBarConfig, right_cfg: HealthBarConfig, outdir: str = "CODEX_CHATGPT/output") -> str:
    """Run analyzer, then sample health at each mistake."""
    params = AnalyzerParameters(video_path=video_path)
    analyzer = MirrorMatchAnalyzer(params)
    result = analyzer.run()
    mistakes = result.get("mistakes", [])
    fps = result.get("fps", 30.0)

    rows = []
    for m in mistakes:
        sec = m.get("seconds", 0.0)
        health = sample_health_at(video_path, sec, fps, left_cfg, right_cfg)
        rows.append({
            "round": m.get("round", 0),
            "time": m.get("timestamp", ""),
            "full_time": m.get("full_timestamp", ""),
            "player": m.get("player", ""),
            "severity": m.get("severity", ""),
            "punish_damage_est": m.get("punish_damage", 0),
            "p1_health": round(health["p1"], 3),
            "p2_health": round(health["p2"], 3),
            "title": m.get("title", ""),
            "tag": m.get("opponent_string", ""),
        })

    ensure_dir(outdir)
    csv_path = os.path.join(outdir, "qa_health_checks.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        headers = ["round", "time", "full_time", "player", "severity", "punish_damage_est", "p1_health", "p2_health", "title", "tag"]
        f.write(",".join(headers) + "\n")
        for r in rows:
            f.write(",".join(str(r[h]) for h in headers) + "\n")
    return csv_path


if __name__ == "__main__":
    # TODO: set these to your HUD bar positions/colors
    left_bar = HealthBarConfig(bbox=(50, 20, 300, 20), hsv_low=(20, 50, 180), hsv_high=(40, 255, 255))
    right_bar = HealthBarConfig(bbox=(530, 20, 300, 20), hsv_low=(20, 50, 180), hsv_high=(40, 255, 255))
    video = r"C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4"
    out_csv = run_qa(video, left_bar, right_bar)
    print(f"QA report written to {out_csv}")
