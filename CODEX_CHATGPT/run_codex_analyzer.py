"""CLI entrypoint for Codex Blitzcrank mirror analysis."""

import argparse
import os
import sys
from typing import List
import math

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from CODEX_CHATGPT.config import AnalyzerParameters
from CODEX_CHATGPT.mirror_matchup import MirrorMatchAnalyzer, MistakeCallout
from CODEX_CHATGPT import blitzcrank_knowledge as bk
from CODEX_CHATGPT.report_builder import (
    build_html_report,
    build_pdf_report,
    ensure_dir,
    generate_placeholder_portrait,
)
import ffmpeg
import imageio_ffmpeg


def print_mistakes(mistakes: List, limit: int) -> None:
    """Pretty-print mistake callouts."""
    if not mistakes:
        print("No mistakes detected with current heuristics.")
        return

    print("\nKey Mistakes (heuristic, low-confidence without telemetry)")
    print("-" * 60)
    for mk in mistakes[:limit]:
        recs = "; ".join(mk.get("recommendations", [])[:2]) if mk else "No tip"
        print(
            f"[{mk.get('timestamp','')}] P{mk.get('player','?')} | {mk.get('title','')} "
            f"| severity={mk.get('severity','')} | {mk.get('detail','')}"
        )
        print(f"   -> {recs}")


def timestamp_to_seconds(ts: str, fps: float) -> float:
    """Convert MM:SS:FF to seconds using FPS."""
    try:
        mm, ss, ff = ts.split(":")
        return int(mm) * 60 + int(ss) + int(ff) / (fps or 30.0)
    except Exception:
        return 0.0


def export_clip(video_path: str, ts: str, fps: float, label: str, out_path: str, pre: float = 2.5, post: float = 5.0) -> bool:
    """Export a short clip around timestamp with overlay text."""
    start = max(timestamp_to_seconds(ts, fps) - pre, 0.0)
    duration = pre + post
    font_path = "C:/Windows/Fonts/arial.ttf"
    draw_args = {
        "text": label,
        "fontsize": 24,
        "fontcolor": "white",
        "box": 1,
        "boxcolor": "black@0.6",
        "boxborderw": 8,
        "x": 20,
        "y": 20,
    }
    if os.path.exists(font_path):
        draw_args["fontfile"] = font_path

    try:
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        (
            ffmpeg
            .input(video_path, ss=start, t=duration)
            .filter("drawtext", **draw_args)
            .output(out_path, vcodec="libx264", acodec="copy", movflags="+faststart", preset="veryfast", loglevel="error")
            .overwrite_output()
            .run(cmd=ffmpeg_bin, quiet=True)
        )
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"Clip export failed for {ts}: {exc}")
        return False


def export_top_clips(mistakes: List, video_path: str, fps: float, outdir: str, limit: int = 3, pre: float = 2.5, post: float = 5.0) -> List[str]:
    """Create clips for top mistakes, preferring critical/major, falling back to highest damage."""
    ensure_dir(outdir)
    pool = [m for m in mistakes if m.get("severity") in ("critical", "major")]
    if not pool:
        pool = mistakes  # fallback to top damage across all
    sorted_mks = sorted(
        pool,
        key=lambda m: -(m.get("punish_damage") or m.get("damage_estimate", 0)),
    )[: max(limit, 1)]
    saved = []
    per_player_limit = limit  # allow multiple from same player when needed
    used_per_player = {}
    for mk in sorted_mks:
        pid = mk.get("player", "?")
        used_per_player[pid] = used_per_player.get(pid, 0)
        if used_per_player[pid] >= per_player_limit:
            continue
        recs = mk.get("recommendations", [])
        fix = recs[0] if recs else "Punish with 5L/2L."
        overlay = (
            f"{mk.get('player_name','')} (P{mk.get('player','?')}) [{mk.get('severity','').upper()}]: {mk.get('title','')}. "
            f"{mk.get('detail','')} | Punish: {mk.get('opponent_string','')} (~{mk.get('punish_damage','~')} dmg) | Fix: {fix}"
        )
        clip_idx = len(saved) + 1
        out_path = os.path.join(outdir, f"mistake_{clip_idx:02d}_P{pid}.mp4")
        if export_clip(video_path, mk.get("timestamp", "00:00:00"), fps, overlay, out_path, pre=pre, post=post):
            saved.append(out_path)
            used_per_player[pid] += 1
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Codex helper: analyze 2XKO Blitz mirror gameplay."
    )
    parser.add_argument("--video", required=True, help="Path to gameplay MP4")
    parser.add_argument("--char1", default="Blitzcrank")
    parser.add_argument("--char2", default="Blitzcrank")
    parser.add_argument("--matchup", choices=["mirror", "cross"], default="mirror")
    parser.add_argument("--mode", default="Juggernaut")
    parser.add_argument("--sample-rate", type=int, default=3)
    parser.add_argument("--flash-threshold", type=float, default=24.0)
    parser.add_argument("--major-flash-threshold", type=float, default=55.0)
    parser.add_argument("--motion-threshold", type=float, default=4.5)
    parser.add_argument("--max-events", type=int, default=120)
    parser.add_argument("--top-mistakes", type=int, default=12)
    parser.add_argument("--outdir", default=os.path.join("CODEX_CHATGPT", "output"))
    parser.add_argument("--player1-name", default="Player 1")
    parser.add_argument("--player2-name", default="Player 2")
    parser.add_argument("--player1-color", default="#1f77b4")
    parser.add_argument("--player2-color", default="#d62728")
    parser.add_argument("--player1-start", default="Left")
    parser.add_argument("--player2-start", default="Right")
    parser.add_argument("--round-length", type=int, default=90)
    parser.add_argument("--clip-limit", type=int, default=3)
    parser.add_argument("--clip-pre", type=float, default=2.5, help="seconds before timestamp")
    parser.add_argument("--clip-post", type=float, default=8.0, help="seconds after timestamp (extend to capture full punish)")
    parser.add_argument("--char1-img", default=os.path.join("CODEX_CHATGPT", "assets", "blitz_p1.png"))
    parser.add_argument("--char2-img", default=os.path.join("CODEX_CHATGPT", "assets", "blitz_p2.png"))
    args = parser.parse_args()

    params = AnalyzerParameters(
        video_path=args.video,
        player1_name=args.player1_name,
        player2_name=args.player2_name,
        character1=args.char1,
        character2=args.char2,
        matchup=args.matchup,
        mode=args.mode,
        sample_rate=args.sample_rate,
        flash_threshold=args.flash_threshold,
        major_flash_threshold=args.major_flash_threshold,
        motion_threshold=args.motion_threshold,
        max_events=args.max_events,
        round_length_sec=args.round_length,
    )

    print(f"Running analyzer with: {params.describe()}")
    analyzer = MirrorMatchAnalyzer(params)
    result = analyzer.run()
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    events = result.get("events", [])
    mistakes = result.get("mistakes", [])
    player_summary = result["player_summary"]
    knowledge = result["knowledge"]

    print(f"Detected events: {len(events)} (trimmed to {params.max_events})")
    print_mistakes(mistakes, args.top_mistakes)

    print("\nPlayer Tendencies (very rough due to video-only cues)")
    print("-" * 60)
    for pid, data in player_summary.items():
        print(
            f"P{pid}: {data.get('style', 'Unknown')} | "
            f"spikes={data.get('events', 0)} | big_commits={data.get('big_commits', 0)}"
        )

    print("\nFast Reference")
    print("-" * 60)
    print(f"Unsafe on block: {knowledge['unsafe_moves'][:6]}")
    print(f"Safe pressure: {knowledge['safe_pressure']}")
    print(f"Preferred punishes: {knowledge['preferred_punishes']}")
    print(f"Juggernaut notes: {knowledge['juggernaut_notes']}")
    print("\nReminder: tag clips around shown timestamps for manual review.")

    # Reports
    outdir = ensure_dir(args.outdir)
    img1 = generate_placeholder_portrait(
        os.path.join(outdir, "p1_portrait.png"), args.player1_name, args.player1_color
    )
    img2 = generate_placeholder_portrait(
        os.path.join(outdir, "p2_portrait.png"), args.player2_name, args.player2_color
    )
    clip_dir = ensure_dir(os.path.join(outdir, "clips"))
    clip_paths = export_top_clips(
        mistakes,
        args.video,
        result.get("fps", 30.0),
        clip_dir,
        limit=args.clip_limit,
        pre=args.clip_pre,
        post=args.clip_post,
    )
    html_path = build_html_report(
        result,
        outdir,
        args.video,
        args.player1_name,
        args.player2_name,
        args.player1_color,
        args.player2_color,
        args.player1_start,
        args.player2_start,
        img1,
        img2,
        result.get("fps", 30.0),
        args.char1_img,
        args.char2_img,
        clip_paths,
    )
    pdf_path = build_pdf_report(result, outdir, args.player1_name, args.player2_name)
    print(f"\nReports saved:")
    print(f" - HTML: {html_path}")
    print(f" - PDF:  {pdf_path}")
    if clip_paths:
        print(" - Clips:")
        for c in clip_paths:
            print(f"    {c}")
    else:
        print(" - Clips: none exported (no mistakes or ffmpeg issue)")


if __name__ == "__main__":
    main()
