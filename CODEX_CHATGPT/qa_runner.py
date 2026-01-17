"""Automated QA checks to sanity-check analyzer outputs and health-based damage.

Usage:
  python CODEX_CHATGPT/qa_runner.py --video <path> --p1-name P1 --p2-name Bot

What it does:
  - Runs the analyzer with supplied params.
  - Samples health bars shortly before and after each mistake timestamp.
  - Estimates health delta and compares to our punish damage estimate.
  - Writes a QA summary JSON and CSV under CODEX_CHATGPT/output/qa/.

NOTE: You must configure health bar regions/colors below to match your capture.
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Dict, Tuple, List
import cv2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from CODEX_CHATGPT.config import AnalyzerParameters
from CODEX_CHATGPT.mirror_matchup import MirrorMatchAnalyzer
from CODEX_CHATGPT.report_builder import ensure_dir


@dataclass
class HealthBarConfig:
    bbox: Tuple[int, int, int, int]  # x, y, w, h
    hsv_low: Tuple[int, int, int]
    hsv_high: Tuple[int, int, int]


def estimate_health(frame, cfg: HealthBarConfig) -> float:
    x, y, w, h = cfg.bbox
    crop = frame[y : y + h, x : x + w]
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, cfg.hsv_low, cfg.hsv_high)
    filled = cv2.countNonZero(mask)
    total = mask.size
    if total == 0:
        return 0.0
    return filled / total


def sample_health(video_path: str, seconds: float, fps: float, cfg_left: HealthBarConfig, cfg_right: HealthBarConfig) -> Dict[str, float]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"p1": 0.0, "p2": 0.0}
    frame_idx = max(0, int(seconds * fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return {"p1": 0.0, "p2": 0.0}
    h1 = estimate_health(frame, cfg_left)
    h2 = estimate_health(frame, cfg_right)
    cap.release()
    return {"p1": h1, "p2": h2}


def run_qa(video: str, args) -> Dict:
    params = AnalyzerParameters(
        video_path=video,
        player1_name=args.p1_name,
        player2_name=args.p2_name,
        sample_rate=args.sample_rate,
        flash_threshold=args.flash_threshold,
        major_flash_threshold=args.major_flash_threshold,
        motion_threshold=args.motion_threshold,
        max_events=args.max_events,
    )
    analyzer = MirrorMatchAnalyzer(params)
    result = analyzer.run()
    mistakes = result.get("mistakes", [])
    fps = result.get("fps", 30.0)

    # Health bar configs (edit to your capture)
    left_bar = HealthBarConfig(bbox=tuple(map(int, args.p1_bbox.split(","))), hsv_low=(20, 50, 180), hsv_high=(40, 255, 255))
    right_bar = HealthBarConfig(bbox=tuple(map(int, args.p2_bbox.split(","))), hsv_low=(20, 50, 180), hsv_high=(40, 255, 255))

    qa_rows: List[Dict] = []
    for mk in mistakes:
        sec = mk.get("seconds", 0.0)
        pre = max(0.0, sec - args.health_pre)
        post = sec + args.health_post
        pre_h = sample_health(video, pre, fps, left_bar, right_bar)
        post_h = sample_health(video, post, fps, left_bar, right_bar)
        delta_p1 = pre_h["p1"] - post_h["p1"]
        delta_p2 = pre_h["p2"] - post_h["p2"]
        qa_rows.append({
            "round": mk.get("round", 0),
            "time": mk.get("timestamp", ""),
            "player": mk.get("player", ""),
            "severity": mk.get("severity", ""),
            "punished": mk.get("punished", False),
            "punish_damage_est": mk.get("punish_damage", 0),
            "p1_health_pre": round(pre_h["p1"], 3),
            "p1_health_post": round(post_h["p1"], 3),
            "p2_health_pre": round(pre_h["p2"], 3),
            "p2_health_post": round(post_h["p2"], 3),
            "p1_health_delta": round(delta_p1, 3),
            "p2_health_delta": round(delta_p2, 3),
            "title": mk.get("title", ""),
            "opponent_string": mk.get("opponent_string", ""),
        })

    outdir = ensure_dir(os.path.join("CODEX_CHATGPT", "output", "qa"))
    json_path = os.path.join(outdir, "qa_summary.json")
    csv_path = os.path.join(outdir, "qa_health_checks.csv")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump({"mistakes": qa_rows}, jf, indent=2)
    headers = ["round", "time", "player", "severity", "punished", "punish_damage_est", "p1_health_pre", "p1_health_post", "p2_health_pre", "p2_health_post", "p1_health_delta", "p2_health_delta", "title", "opponent_string"]
    with open(csv_path, "w", encoding="utf-8") as cf:
        cf.write(",".join(headers) + "\n")
        for r in qa_rows:
            cf.write(",".join(str(r[h]) for h in headers) + "\n")
    return {"json": json_path, "csv": csv_path, "rows": qa_rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QA checker for mistakes vs health deltas.")
    parser.add_argument("--video", required=False, default=r"C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4")
    parser.add_argument("--p1-name", default="P1")
    parser.add_argument("--p2-name", default="Bot")
    parser.add_argument("--sample-rate", type=int, default=3)
    parser.add_argument("--flash-threshold", type=float, default=24.0)
    parser.add_argument("--major-flash-threshold", type=float, default=60.0)
    parser.add_argument("--motion-threshold", type=float, default=4.5)
    parser.add_argument("--max-events", type=int, default=80)
    parser.add_argument("--p1-bbox", default="50,20,300,20", help="x,y,w,h for P1 health bar")
    parser.add_argument("--p2-bbox", default="530,20,300,20", help="x,y,w,h for P2 health bar")
    parser.add_argument("--health-pre", type=float, default=0.5, help="seconds before mistake to sample health")
    parser.add_argument("--health-post", type=float, default=1.5, help="seconds after mistake to sample health")
    args = parser.parse_args()

    outputs = run_qa(args.video, args)
    print("QA outputs:")
    print(" JSON:", outputs["json"])
    print(" CSV :", outputs["csv"])
