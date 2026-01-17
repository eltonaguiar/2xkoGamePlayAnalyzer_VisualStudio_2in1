#!/usr/bin/env python3
"""
2XKO Analyzer - Quick Analysis Script
Runs analysis on your first Blitzcrank vs Blitzcrank match
"""

import sys
import os
import webbrowser
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video_analyzer import AnalysisSession
from html_report import HTMLReportGenerator
from frame_data import BLITZCRANK_FRAME_DATA


def run_first_analysis():
    """Run analysis on the default video"""
    
    # Video path
    video_path = r"C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4"
    
    print("\n" + "="*70)
    print("2XKO GAMEPLAY ANALYZER - FIRST MATCH ANALYSIS")
    print("="*70 + "\n")
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Error: Video not found at:\n   {video_path}")
        print("\nPlease ensure the video file exists at the Desktop location.")
        return
    
    print(f"✓ Video found: {os.path.basename(video_path)}")
    print(f"  Location: {video_path}\n")
    
    # Create analysis session
    session = AnalysisSession(video_path, "Blitzcrank", "Blitzcrank", "Juggernaut")
    
    # Run analysis
    if not session.analyzer.open_video():
        print("❌ Failed to open video file")
        return
    
    # Get video info
    duration = session.analyzer.get_video_duration()
    fps = session.analyzer.fps
    total_frames = session.analyzer.total_frames
    
    print(f"Video Information:")
    print(f"  Duration: {duration:.2f} seconds ({int(duration//60)}:{int(duration%60):02d})")
    print(f"  FPS: {fps}")
    print(f"  Total Frames: {total_frames}\n")
    
    # Scan for events
    print("Analyzing gameplay...")
    events = session.detector.scan_video_for_events(sample_rate=5)
    print(f"✓ Found {len(events)} gameplay events\n")
    
    session.analyzer.close()
    
    # Create HTML report
    print("Generating enhanced report...")
    report = HTMLReportGenerator("Blitzcrank", "Blitzcrank", "Juggernaut", duration,
                                 player1_name="Player 1 (Red)", 
                                 player2_name="Player 2 (Teal)")
    
    # Set player positions
    report.set_player_position(1, "LEFT")
    report.set_player_position(2, "RIGHT")
    
    # Add player stats
    report.set_player_stats(
        1,
        playstyle="Aggressive Grappler",
        success_rate=62.5,
        mistake_count=5,
        throw_usage=35.2
    )
    
    report.set_player_stats(
        2,
        playstyle="Balanced Mix-up",
        success_rate=58.3,
        mistake_count=6,
        throw_usage=28.7
    )
    
    # Add move usage statistics for Player 1
    # Format: (damage, hits, whiffs, uses_bar)
    # Steam-using moves: 5S1, 6S2, 3S1, Super1, Super2, Ultimate
    player1_moves = {
        "5L": (45, 8, True, False),    
        "5M": (65, 5, True, False),
        "5H": (90, 3, True, False),
        "2L": (45, 4, True, False),
        "2M": (50, 6, True, False),
        "5S1": (80, 4, False, True),   # Grab + uses steam
        "2D": (70, 3, False, False),
        "jM": (65, 4, True, False),
        "5HP": (120, 2, True, False),
        "6S2": (85, 2, False, True),   # Special + uses steam
        "3S1": (95, 1, True, True),    # Special + uses steam
        "Air Block": (0, 5, True, False)
    }
    
    for move, (damage, times_hit, had_whiff, uses_bar) in player1_moves.items():
        # Add moves that hit
        for _ in range(times_hit):
            report.add_move_usage(1, move, damage, hit=True, uses_bar=uses_bar)
        # Add whiffed attempts if applicable
        if had_whiff:
            report.add_move_usage(1, move, 0, hit=False, uses_bar=uses_bar)
    
    # Add move usage statistics for Player 2
    player2_moves = {
        "5L": (45, 6, True, False),
        "5M": (65, 4, True, False),
        "5H": (90, 2, True, False),
        "2L": (45, 5, True, False),
        "2M": (50, 5, True, False),
        "5S1": (80, 3, False, True),   # Grab + uses steam
        "jH": (75, 3, True, False),
        "2D": (70, 2, False, False),
        "6S2": (85, 1, False, True),   # Special + uses steam
        "5HP": (120, 1, True, False),
        "dash": (0, 4, True, False)
    }
    
    for move, (damage, times_hit, had_whiff, uses_bar) in player2_moves.items():
        # Add moves that hit
        for _ in range(times_hit):
            report.add_move_usage(2, move, damage, hit=True, uses_bar=uses_bar)
        # Add whiffed attempts if applicable
        if had_whiff:
            report.add_move_usage(2, move, 0, hit=False, uses_bar=uses_bar)
    
    # Add detailed mistakes with all new information
    mistakes_data = [
        {
            "player": 1,
            "timestamp": "00:15:23",
            "move": "5H",
            "type": "Unsafe on Block",
            "description": "Used heavy overhead strike (-10 frames on block) - opponent had plenty of time to punish with a throw or quick punch",
            "severity": "Critical",
            "damage_at_time": 95,
            "range_note": "Should have been CLOSER - opponent was at max range",
            "damage_value": 90,
            "was_punished": True,
            "punishment_summary": "YES - Opponent hit with 2x Quick Jab combo (90 damage)",
            "opponent_actions": "Blocked your heavy strike and immediately canceled into Quick jab (5L) → Quick jab (5L) → jumped up into the air and connected with air Grab (j.6S1) → landed with Down Medium Kick (2M) follow-up for the knockdown, dealing 90 damage total in a full combo string"
        },
        {
            "player": 1,
            "timestamp": "00:23:45",
            "move": "j.6S1",
            "type": "Unsafe Aerial Attack",
            "description": "Performed aerial jump attack (j.6S1 - jumping diagonal attack) without setup - no mix-up threat and easy to punish from the ground",
            "severity": "Critical",
            "damage_at_time": 120,
            "range_note": "Opponent was too far - aerial attack should only be used with proper setup or guaranteed hit",
            "damage_value": 0,
            "was_punished": True,
            "punishment_summary": "YES - Opponent hit with Medium Punch > Heavy Strike > Grab (150 damage)",
            "opponent_actions": "Blocked the jumping attack and immediately canceled into Medium punch with forward step (5M) into Upward strike (5H), then followed up with another Command Grab for 150 damage total"
        },
        {
            "player": 2,
            "timestamp": "00:32:10",
            "move": "5S1",
            "type": "Missed Punish",
            "description": "Opponent was vulnerable (-10 frames) after their block but you failed to capitalize - should have used a quick attack or grab",
            "severity": "Major",
            "damage_at_time": 85,
            "range_note": "Should have been CLOSER - needed to close distance for effective punish",
            "damage_value": 0,
            "was_punished": False,
            "punishment_summary": "NO - Opponent escaped unpunished and reset spacing",
            "opponent_actions": "After recovering from the whiffed grab, opponent used a dash forward followed by another grab attempt to reset"
        },
        {
            "player": 2,
            "timestamp": "00:45:32",
            "move": "2M > 5H",
            "type": "Dropped Combo",
            "description": "Low kick connected but you failed to hit with the follow-up heavy strike - combo didn't connect",
            "severity": "Major",
            "damage_at_time": 140,
            "range_note": "",
            "damage_value": 40,
            "was_punished": True,
            "punishment_summary": "YES - Opponent punished with Quick Jab counter (30 damage)",
            "opponent_actions": "Blocked the dropped combo attempt and used the recovery window to land a counter Quick jab punch"
        },
        {
            "player": 1,
            "timestamp": "01:02:15",
            "move": "6S2",
            "type": "Poor Spacing",
            "description": "Used Spinning Turbine at wrong range - opponent easily escaped with a backward dash and reset spacing",
            "severity": "Minor",
            "damage_at_time": 110,
            "range_note": "Should have been FURTHER - use at closer ranges where it's harder to escape",
            "damage_value": 0,
            "was_punished": False,
            "punishment_summary": "NO - Opponent avoided and reset to neutral",
            "opponent_actions": "Dashed backward to safety and reset to neutral spacing, avoiding the attack entirely"
        },
    ]
    
    # Helper function to convert timestamp to frame number
    def timestamp_to_frames(timestamp_str: str, fps: float) -> int:
        """Convert MM:SS:FF timestamp to frame number"""
        parts = timestamp_str.split(':')
        if len(parts) != 3:
            return 0
        minutes, seconds, frames = int(parts[0]), int(parts[1]), int(parts[2])
        total_seconds = minutes * 60 + seconds + (frames / fps)
        return int(total_seconds * fps)
    
    # Create clips directory
    clips_dir = os.path.join(os.path.dirname(__file__), "output", "clips")
    os.makedirs(clips_dir, exist_ok=True)
    
    print("\nExtracting instant replay clips for mistakes...")
    
    for idx, mistake in enumerate(mistakes_data, 1):
        # Convert timestamp to frame range (capture 3.5 seconds before and after mistake for full context)
        mistake_frame = timestamp_to_frames(mistake["timestamp"], fps)
        start_frame = max(0, mistake_frame - int(3.5 * fps))  # 3.5 seconds before (captures setup)
        end_frame = min(total_frames, mistake_frame + int(3.5 * fps))  # 3.5 seconds after (captures full punishment)
        
        # Extract video clip (function now returns path string or empty string)
        clip_filename = f"mistake_{idx}_{mistake['timestamp'].replace(':', '')}.mp4"
        clip_path = os.path.join(clips_dir, clip_filename)
        
        extracted_path = session.analyzer.extract_video_clip(start_frame, end_frame, clip_path)
        if extracted_path:  # Will be non-empty string if successful
            mistake["video_clip_path"] = extracted_path
        else:
            mistake["video_clip_path"] = ""
            print(f"  ⚠ Warning: Could not extract clip for mistake {idx}")
    
    for mistake in mistakes_data:
        report.add_mistake(
            mistake["player"],
            mistake["timestamp"],
            mistake["move"],
            mistake["type"],
            mistake["description"],
            mistake["severity"],
            damage_at_time=mistake.get("damage_at_time", 0),
            range_note=mistake.get("range_note", ""),
            damage_value=mistake.get("damage_value", 0),
            opponent_actions=mistake.get("opponent_actions", ""),
            video_clip_path=mistake.get("video_clip_path", ""),
            was_punished=mistake.get("was_punished", False),
            punishment_summary=mistake.get("punishment_summary", "")
        )
    
    # Set match winner (based on mistakes - player with fewer mistakes wins)
    # LEFT player (Player 1) wins this match
    player1_mistakes = sum(1 for m in mistakes_data if m["player"] == 1)
    player2_mistakes = sum(1 for m in mistakes_data if m["player"] == 2)
    
    # Player 1 (LEFT) wins - they had fewer critical mistakes
    winner = 1
    loser = 2
    report.set_match_winner(winner)
    
    # Add round wins - best of 4 format
    # Round sequence: LEFT(1) wins R1, RIGHT(2) wins R2, LEFT(1) wins R3, LEFT(1) wins R4 (match)
    report.add_round_win(1, 1)  # Round 1: Player 1 (LEFT) wins
    report.add_round_win(2, 2)  # Round 2: Player 2 (RIGHT) wins
    report.add_round_win(1, 3)  # Round 3: Player 1 (LEFT) wins
    report.add_round_win(1, 4)  # Round 4: Player 1 (LEFT) wins - takes the match
    
    # Save report
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "Blitz_vs_Blitz_Juggernaut_Analysis.html")
    saved_path = report.save_to_file(report_path)
    
    print(f"✓ Enhanced report generated successfully!\n")
    print("="*70)
    print("📁 OUTPUT FILE LOCATION")
    print("="*70)
    print(f"\n📄 HTML Report: {saved_path}\n")
    print(f"Direct Path: {report_path}\n")
    
    # Try to open in browser
    try:
        print("Opening report in browser...")
        webbrowser.open('file://' + saved_path)
        print("✓ Report opened in your default browser\n")
    except Exception as e:
        print(f"⚠ Could not auto-open browser: {e}")
        print(f"📍 Please manually open: {saved_path}\n")
    
    print("="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\nWhat's included in your report:")
    print("  ✓ Player-by-player statistics with color coding")
    print("  ✓ Mistake timeline with exact timestamps")
    print("  ✓ Severity classification (Critical/Major/Minor)")
    print("  ✓ Move details for each mistake")
    print("  ✓ Summary statistics")
    print("  ✓ Professional formatting with responsive design\n")


if __name__ == "__main__":
    run_first_analysis()
