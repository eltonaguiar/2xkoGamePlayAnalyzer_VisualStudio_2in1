"""
HTML Report Generator for 2XKO Analysis
Creates visually appealing, video-player style reports with enhanced features
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import os
import base64


class HTMLReportGenerator:
    """Generates professional HTML reports with styling"""
    
    # Player colors for visual distinction
    PLAYER_COLORS = {
        1: {
            "primary": "#FF6B6B",
            "secondary": "#FFB3B3",
            "dark": "#CC0000",
            "light": "#FFE8E8",
            "name": "Player 1",
            "position": "LEFT"
        },
        2: {
            "primary": "#4ECDC4",
            "secondary": "#A0E7E5",
            "dark": "#0A9B8E",
            "light": "#E0F7F5",
            "name": "Player 2",
            "position": "RIGHT"
        }
    }
    
    # Character images (using SVG placeholders - can be updated with actual images)
    CHARACTER_IMAGES = {
        "Blitzcrank": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%234a5568' width='100' height='100'/%3E%3Ccircle cx='50' cy='30' r='15' fill='%237f8ea3'/%3E%3Crect x='35' y='50' width='30' height='40' fill='%235a6b7f'/%3E%3Crect x='20' y='50' width='12' height='35' fill='%235a6b7f'/%3E%3Crect x='68' y='50' width='12' height='35' fill='%235a6b7f'/%3E%3Crect x='30' y='85' width='15' height='12' fill='%234a5568'/%3E%3Crect x='55' y='85' width='15' height='12' fill='%234a5568'/%3E%3C/svg%3E"
    }
    
    def __init__(self, character1: str = "Blitzcrank", character2: str = "Blitzcrank", 
                 mode: str = "Juggernaut", video_duration: float = 0,
                 player1_name: str = "Player 1", player2_name: str = "Player 2"):
        self.character1 = character1
        self.character2 = character2
        self.mode = mode
        self.video_duration = video_duration
        self.mistakes = []
        self.events = []
        self.player_stats = {}
        self.move_stats = {1: {}, 2: {}}  # Track move usage per player
        self.player_positions = {1: "LEFT", 2: "RIGHT"}  # Track starting positions
        self.round_wins = {1: 0, 2: 0}  # Track round wins
        self.match_winner = None  # Track match winner
        self.rounds_data = []  # Store per-round breakdown
        
        # Set custom player names
        self.PLAYER_COLORS[1]["name"] = player1_name
        self.PLAYER_COLORS[2]["name"] = player2_name
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.damage_at_mistake = {}  # Track cumulative damage at each mistake
    
    def _file_to_base64(self, file_path: str) -> str:
        """Convert a file to base64-encoded data URI"""
        try:
            if not os.path.exists(file_path):
                return ""
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
                base64_data = base64.b64encode(file_data).decode('utf-8')
                
                # Determine MIME type
                if file_path.lower().endswith('.gif'):
                    mime_type = 'image/gif'
                elif file_path.lower().endswith('.mp4'):
                    mime_type = 'video/mp4'
                else:
                    mime_type = 'application/octet-stream'
                
                return f"data:{mime_type};base64,{base64_data}"
        except Exception as e:
            print(f"Warning: Could not convert file to base64: {file_path}")
            return ""
        
    def add_mistake(self, player: int, timestamp: str, move: str, mistake_type: str, 
                   description: str, severity: str, damage_at_time: int = 0, 
                   range_note: str = "", damage_value: int = 0, opponent_actions: str = "", 
                   video_clip_path: str = "", was_punished: bool = False, punishment_summary: str = ""):
        """Add a mistake to the report with all enhanced details"""
        opponent_num = 2 if player == 1 else 1
        self.mistakes.append({
            "player": player,
            "player_name": self.PLAYER_COLORS[player]["name"],
            "player_color": self.PLAYER_COLORS[player]["primary"],
            "opponent": opponent_num,
            "opponent_name": self.PLAYER_COLORS[opponent_num]["name"],
            "opponent_color": self.PLAYER_COLORS[opponent_num]["primary"],
            "timestamp": timestamp,
            "move": move,
            "type": mistake_type,
            "description": description,
            "severity": severity,
            "damage_at_time": damage_at_time,
            "range_note": range_note,  # e.g., "Should be CLOSER" or "Should be FURTHER"
            "damage_value": damage_value,
            "opponent_actions": opponent_actions,  # What opponent did during this window
            "video_clip_path": video_clip_path,  # Path to instant replay video
            "was_punished": was_punished,  # Whether opponent punished this mistake
            "punishment_summary": punishment_summary  # Quick summary of punishment (or escape)
        })
    
    def add_move_usage(self, player: int, move: str, damage: int, hit: bool = True, uses_bar: bool = False):
        """Track move usage statistics for each player"""
        if move not in self.move_stats[player]:
            self.move_stats[player][move] = {
                "count": 0,
                "total_damage": 0,
                "hits": 0,
                "whiffs": 0,
                "average_damage": 0,
                "uses_bar_count": 0,
                "uses_bar": uses_bar
            }
        
        self.move_stats[player][move]["count"] += 1
        self.move_stats[player][move]["total_damage"] += damage
        if hit:
            self.move_stats[player][move]["hits"] += 1
        else:
            self.move_stats[player][move]["whiffs"] += 1
        
        if uses_bar:
            self.move_stats[player][move]["uses_bar_count"] += 1
            self.move_stats[player][move]["uses_bar"] = True
        
        # Update average damage
        if self.move_stats[player][move]["hits"] > 0:
            self.move_stats[player][move]["average_damage"] = (
                self.move_stats[player][move]["total_damage"] / 
                self.move_stats[player][move]["hits"]
            )
    
    def set_player_position(self, player: int, position: str):
        """Set starting position for player (LEFT or RIGHT)"""
        self.player_positions[player] = position
        self.PLAYER_COLORS[player]["position"] = position
    
    def add_round_win(self, player: int, round_num: int, round_data: Dict = None):
        """Track a round win for a player"""
        self.round_wins[player] += 1
        if round_data is None:
            round_data = {}
        self.rounds_data.append({
            "round": round_num,
            "winner": player,
            "winner_name": self.PLAYER_COLORS[player]["name"],
            **round_data
        })
    
    def set_match_winner(self, player: int):
        """Set the match winner"""
        self.match_winner = player
    
    def set_damage_at_mistake(self, mistake_index: int, player1_damage: int, player2_damage: int):
        """Set cumulative damage at the time of a mistake"""
        self.damage_at_mistake[mistake_index] = {
            "player1": player1_damage,
            "player2": player2_damage
        }
    
    def add_event(self, timestamp: str, event_type: str, description: str):
        """Add a game event"""
        self.events.append({
            "timestamp": timestamp,
            "type": event_type,
            "description": description
        })
    
    def set_player_stats(self, player: int, playstyle: str, success_rate: float, 
                        mistake_count: int, throw_usage: float = 0):
        """Set player statistics"""
        self.player_stats[player] = {
            "playstyle": playstyle,
            "success_rate": success_rate,
            "mistake_count": mistake_count,
            "throw_usage": throw_usage
        }
    
    @staticmethod
    def get_simple_move_description(move: str) -> str:
        """Get a simple, non-FGC description of a move"""
        simple_descriptions = {
            # Normals
            "5L": "Quick jab (light punch)",
            "5M": "Medium punch with forward step",
            "5H": "Heavy overhead strike",
            "5HP": "Strong powered-up attack",
            "2L": "Low quick kick",
            "2M": "Low medium kick (catches jumpers)",
            "2H": "Upward strike (anti-air)",
            "jL": "Jumping light punch",
            "jM": "Jumping medium punch",
            "jH": "Jumping heavy punch",
            
            # Specials
            "5S1": "Command Grab (Rocket Grab) - grab only",
            "6S2": "Spinning Turbine Spin",
            "3S1": "Steam Golem Summon",
            "214S": "Electrical Shield",
            "236S": "Static Field",
            "2D": "Dodge roll backward",
            "Air Block": "Defensive block in the air",
            "Dash": "Quick dash movement",
        }
        return simple_descriptions.get(move, move)
    
    def generate_html(self, output_path: str = None) -> str:
        """Generate complete HTML report with all enhanced features
        
        Args:
            output_path: Optional path where the HTML will be saved (used for relative paths)
        """
        if output_path:
            self.output_path = output_path
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2XKO Analysis Report - {self.character1} vs {self.character2}</title>
    <!-- GIF.js library for GIF decoding and frame control -->
    <script src="https://cdn.jsdelivr.net/npm/gif.js@0.2.0/dist/gif.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .match-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .info-card {{
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .info-label {{
            font-size: 0.85em;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .info-value {{
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .round-start-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
            color: #333;
        }}
        
        .subsection-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin: 20px 0 15px 0;
            color: #333;
            border-left: 4px solid #667eea;
            padding-left: 12px;
        }}
        
        .character-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
            align-items: start;
        }}
        
        .character-position {{
            background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
            padding: 25px;
            border-radius: 12px;
            border: 2px solid;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .character-position.left {{
            border-color: #FF6B6B;
            border-left: 5px solid #FF6B6B;
        }}
        
        .character-position.right {{
            border-color: #4ECDC4;
            border-right: 5px solid #4ECDC4;
        }}
        
        .position-label {{
            font-weight: bold;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        
        .position-label.left {{
            color: #FF6B6B;
        }}
        
        .position-label.right {{
            color: #4ECDC4;
        }}
        
        .character-image {{
            width: 150px;
            height: 150px;
            margin: 15px auto;
            border-radius: 8px;
            background: linear-gradient(135deg, #e0e0e0 0%, #f0f0f0 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .character-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 8px;
        }}
        
        .character-name {{
            font-size: 1.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .player-label {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .color-indicator {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 8px;
            vertical-align: middle;
        }}
        
        .players-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .player-card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-top: 5px solid;
            transition: transform 0.3s ease;
        }}
        
        .player-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .player-card.player1 {{
            border-top-color: {self.PLAYER_COLORS[1]["primary"]};
        }}
        
        .player-card.player2 {{
            border-top-color: {self.PLAYER_COLORS[2]["primary"]};
        }}
        
        .player-header {{
            padding: 20px;
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
            border-bottom: 2px solid #eee;
        }}
        
        .player-name {{
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .player-card.player1 .player-name {{
            color: {self.PLAYER_COLORS[1]["primary"]};
        }}
        
        .player-card.player2 .player-name {{
            color: {self.PLAYER_COLORS[2]["primary"]};
        }}
        
        .character-info {{
            font-size: 0.9em;
            color: #666;
            opacity: 0.8;
        }}
        
        .player-stats {{
            padding: 20px;
        }}
        
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .stat-row:last-child {{
            border-bottom: none;
        }}
        
        .stat-label {{
            font-weight: 600;
            color: #666;
        }}
        
        .stat-value {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .player-card.player1 .stat-value {{
            color: {self.PLAYER_COLORS[1]["primary"]};
        }}
        
        .player-card.player2 .stat-value {{
            color: {self.PLAYER_COLORS[2]["primary"]};
        }}
        
        .mistakes-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .mistake-item {{
            background: #f9f9f9;
            border-left: 5px solid;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
        }}
        
        .mistake-item.player1 {{
            border-left-color: {self.PLAYER_COLORS[1]["primary"]};
            background: {self.PLAYER_COLORS[1]["light"]};
        }}
        
        .mistake-item.player2 {{
            border-left-color: {self.PLAYER_COLORS[2]["primary"]};
            background: {self.PLAYER_COLORS[2]["light"]};
        }}
        
        .mistake-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .mistake-timestamp {{
            font-weight: bold;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            white-space: nowrap;
            padding: 6px 12px;
            background: rgba(0,0,0,0.05);
            border-radius: 4px;
        }}
        
        .player-who {{
            font-weight: bold;
            font-size: 1em;
            padding: 6px 12px;
            border-radius: 4px;
            display: inline-block;
        }}
        
        .player-who.p1 {{
            background: {self.PLAYER_COLORS[1]["primary"]};
            color: white;
        }}
        
        .player-who.p2 {{
            background: {self.PLAYER_COLORS[2]["primary"]};
            color: white;
        }}
        
        .mistake-details {{
            margin-top: 10px;
        }}
        
        .mistake-move {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 8px;
            color: #333;
        }}
        
        .mistake-type {{
            display: inline-block;
            font-size: 0.85em;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            margin-right: 8px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .mistake-type.critical {{
            background: #FF6B6B;
            color: white;
        }}
        
        .mistake-type.major {{
            background: #FFB347;
            color: white;
        }}
        
        .mistake-type.minor {{
            background: #FFD93D;
            color: #333;
        }}
        
        .mistake-description {{
            color: #555;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 10px;
        }}
        
        .mistake-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(0,0,0,0.1);
        }}
        
        .mistake-stat {{
            background: rgba(255,255,255,0.6);
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        .mistake-stat strong {{
            display: block;
            font-weight: bold;
            color: #333;
        }}
        
        .mistake-stat span {{
            color: #666;
            font-size: 0.85em;
        }}
        
        .range-note {{
            background: rgba(255,193,7,0.1);
            border-left: 3px solid #FFC107;
            padding: 10px 12px;
            border-radius: 4px;
            margin-top: 10px;
            font-weight: 500;
            color: #8B6914;
        }}
        
        .move-breakdown-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            margin-top: 30px;
        }}
        
        .move-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .move-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .move-table th {{
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: none;
        }}
        
        .move-table td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
            text-align: left;
        }}
        
        .move-table tbody tr:hover {{
            background: #f5f5f5;
        }}
        
        .move-table tbody tr:nth-child(odd) {{
            background: #fafafa;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-box-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-box-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .footer {{
            background: rgba(255,255,255,0.1);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
            margin-top: 40px;
            font-size: 0.9em;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
        
        .empty-state-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}
        
        /* GIF Animation Control */
        @keyframes gif-play {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 1; }}
        }}
        
        img[style*="animation: gif-play"] {{
            animation: gif-play 7s steps(1) infinite;
        }}
        
        @media (max-width: 768px) {{
            .players-section {{
                grid-template-columns: 1fr;
            }}
            
            .character-container {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .move-table {{
                font-size: 0.85em;
            }}
            
            .move-table th,
            .move-table td {{
                padding: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 2XKO GAMEPLAY ANALYSIS</h1>
            <p>Match Analysis Report</p>
            <div class="match-info">
                <div class="info-card">
                    <div class="info-label">Game Mode</div>
                    <div class="info-value">{self.mode}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Duration</div>
                    <div class="info-value">{self.video_duration:.1f}s</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Generated</div>
                    <div class="info-value">{datetime.now().strftime('%H:%M:%S')}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Total Mistakes</div>
                    <div class="info-value">{len(self.mistakes)}</div>
                </div>
            </div>
        </div>
        
"""
        
        # Add match results section if winner is set
        if self.match_winner:
            winner_name = self.PLAYER_COLORS[self.match_winner]["name"]
            loser = 2 if self.match_winner == 1 else 1
            loser_name = self.PLAYER_COLORS[loser]["name"]
            winner_color = self.PLAYER_COLORS[self.match_winner]["primary"]
            loser_color = self.PLAYER_COLORS[loser]["primary"]
            
            # Determine which character won
            winner_character = self.character1 if self.match_winner == 1 else self.character2
            loser_character = self.character2 if self.match_winner == 1 else self.character1
            
            html += f"""
        <div class="match-results" style="background: linear-gradient(135deg, {winner_color} 0%, rgba(0,0,0,0.2) 100%); border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <div style="text-align: center; color: #fff;">
                <div style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;">🏆 MATCH WINNER</div>
                
                <!-- Winner and Loser with character images -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                    <!-- Winner -->
                    <div style="text-align: center;">
                        <div style="font-size: 1.2em; opacity: 0.9; margin-bottom: 10px;">🥇 CHAMPION</div>
                        <div style="width: 100px; height: 100px; background: rgba(255,255,255,0.15); border-radius: 12px; margin: 0 auto 10px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                            <img src="{self.CHARACTER_IMAGES.get(winner_character, '')}" alt="{winner_character}" style="width: 90%; height: 90%; object-fit: contain;">
                        </div>
                        <div style="font-size: 1.8em; font-weight: bold;">{winner_name}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">{winner_character}</div>
                    </div>
                    
                    <!-- Loser -->
                    <div style="text-align: center; opacity: 0.85;">
                        <div style="font-size: 1.2em; opacity: 0.9; margin-bottom: 10px;">🥈 RUNNER-UP</div>
                        <div style="width: 100px; height: 100px; background: rgba(0,0,0,0.2); border-radius: 12px; margin: 0 auto 10px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                            <img src="{self.CHARACTER_IMAGES.get(loser_character, '')}" alt="{loser_character}" style="width: 90%; height: 90%; object-fit: contain;">
                        </div>
                        <div style="font-size: 1.8em; font-weight: bold;">{loser_name}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">{loser_character}</div>
                    </div>
                </div>
                
                <!-- Score -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 400px; margin: 0 auto;">
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="font-size: 0.9em; opacity: 0.8;">Rounds Won</div>
                        <div style="font-size: 2em; font-weight: bold;">{self.round_wins[self.match_winner]}</div>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;">
                        <div style="font-size: 0.9em; opacity: 0.8;"> {loser_name}'s Rounds</div>
                        <div style="font-size: 2em; font-weight: bold;">{self.round_wins[loser]}</div>
                    </div>
                </div>
            </div>
        </div>
"""
        
        # Add round breakdown if available
        if self.rounds_data:
            html += f"""
        <div class="round-breakdown" style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 30px;">
            <h2 class="section-title">📊 Round Breakdown</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
"""
            for round_data in self.rounds_data:
                round_num = round_data.get("round", 0)
                winner_player = round_data.get("winner", 0)
                winner_name = round_data.get("winner_name", "Unknown")
                winner_color = self.PLAYER_COLORS[winner_player]["primary"] if winner_player in self.PLAYER_COLORS else "#999"
                
                html += f"""
                <div style="background: linear-gradient(135deg, {winner_color} 0%, rgba(0,0,0,0.15) 100%); padding: 15px; border-radius: 8px; border-left: 4px solid {winner_color};">
                    <div style="color: #aaa; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px;">Round {round_num}</div>
                    <div style="color: #fff; font-weight: bold; margin-top: 5px; font-size: 1.1em;">✓ {winner_name} Wins</div>
                </div>
"""
            
            html += """
            </div>
        </div>
"""
        
        html += f"""
        <div class="round-start-section">
            <h2 class="section-title">🎬 Round Start Position</h2>
            <div class="character-container">
                <div class="character-position left">
                    <div class="position-label left">📍 Left Side</div>
                    <div class="character-image">
                        <img src="{self.CHARACTER_IMAGES.get(self.character1, '')}" alt="{self.character1}" onerror="this.parentElement.textContent='{self.character1}'">
                    </div>
                    <div class="player-label">
                        <span class="color-indicator" style="background: {self.PLAYER_COLORS[1]['primary']};"></span>
                        Player 1
                    </div>
                    <div class="character-name">{self.character1}</div>
                    <div class="character-info">Starting Position: LEFT</div>
                </div>
                
                <div class="character-position right">
                    <div class="position-label right">📍 Right Side</div>
                    <div class="character-image">
                        <img src="{self.CHARACTER_IMAGES.get(self.character2, '')}" alt="{self.character2}" onerror="this.parentElement.textContent='{self.character2}'">
                    </div>
                    <div class="player-label">
                        <span class="color-indicator" style="background: {self.PLAYER_COLORS[2]['primary']};"></span>
                        Player 2
                    </div>
                    <div class="character-name">{self.character2}</div>
                    <div class="character-info">Starting Position: RIGHT</div>
                </div>
            </div>
        </div>
        
        <div class="players-section">
"""
        
        # Add player cards
        for player_num in [1, 2]:
            char_name = self.character1 if player_num == 1 else self.character2
            color = self.PLAYER_COLORS[player_num]
            stats = self.player_stats.get(player_num, {})
            
            html += f"""
            <div class="player-card player{player_num}">
                <div class="player-header">
                    <div class="player-name">
                        <span style="color: {color['primary']};">●</span> {color['name']}
                    </div>
                    <div class="character-info">{char_name}</div>
                </div>
                <div class="player-stats">
                    <div class="stat-row">
                        <span class="stat-label">Playstyle</span>
                        <span class="stat-value">{stats.get('playstyle', 'N/A')}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Success Rate</span>
                        <span class="stat-value">{stats.get('success_rate', 0):.1f}%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Total Mistakes</span>
                        <span class="stat-value">{stats.get('mistake_count', 0)}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Throw Usage</span>
                        <span class="stat-value">{stats.get('throw_usage', 0):.1f}%</span>
                    </div>
                </div>
            </div>
"""
        
        html += """
        </div>
"""
        
        # Add mistakes section
        if self.mistakes:
            html += """
        <div class="mistakes-section">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 15px;">
                <h2 class="section-title" style="margin: 0;">🎯 Key Mistakes Detected</h2>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button onclick="filterMistakes('all')" id="filter_all" style="background: #4CAF50; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; transition: all 0.2s;">📋 All Mistakes</button>
                    <button onclick="filterMistakes('loser')" id="filter_loser" style="background: #444; color: #fff; padding: 8px 16px; border: 1px solid #666; border-radius: 4px; cursor: pointer; transition: all 0.2s;">🥈 Loser Only</button>
                </div>
            </div>
"""
            
            # Sort mistakes by severity
            severity_order = {"Critical": 0, "Major": 1, "Minor": 2}
            sorted_mistakes = sorted(self.mistakes, key=lambda x: (severity_order.get(x["severity"], 999), x["timestamp"]))
            
            for idx, mistake in enumerate(sorted_mistakes[:20]):  # Show top 20
                severity_lower = mistake["severity"].lower()
                player_class = f"player{mistake['player']}"
                player_badge_class = "p1" if mistake['player'] == 1 else "p2"
                opponent_badge_class = "p2" if mistake['player'] == 1 else "p1"
                
                # Get simple move description
                simple_move_desc = self.get_simple_move_description(mistake['move'])
                
                html += f"""
            <div class="mistake-item {player_class}" data-player="{mistake['player']}" style="display: block;">
                <div class="mistake-header">
                    <div class="mistake-timestamp">⏱️ {mistake['timestamp']}</div>
                    <div class="player-who {player_badge_class}">{mistake['player_name']}</div>
                    <div class="mistake-type {severity_lower}">{mistake['severity']}</div>
                </div>
"""
                
                # Add punishment status if available
                if mistake.get('punishment_summary'):
                    punishment_indicator = "✅ PUNISHED" if mistake.get('was_punished') else "❌ ESCAPED"
                    punishment_color = "#28a745" if mistake.get('was_punished') else "#dc3545"
                    html += f"""
                <div class="punishment-status" style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid {punishment_color}; padding: 10px 12px; margin: 10px 0; border-radius: 4px;">
                    <div style="color: {punishment_color}; font-weight: 600; font-size: 1.05em;">
                        {punishment_indicator}
                    </div>
                    <div style="color: #555; margin-top: 4px; font-size: 0.95em;">
                        {mistake['punishment_summary']}
                    </div>
                </div>
"""
                
                # Add instant replay video with native speed control
                if mistake.get('video_clip_path') and os.path.exists(mistake['video_clip_path']):
                    clip_path = mistake['video_clip_path']
                    
                    # Prioritize GIF for better browser compatibility (works with file:// protocol)
                    gif_path = clip_path if clip_path.endswith('.gif') else clip_path.replace('.mp4', '.gif')
                    if os.path.exists(gif_path):
                        clip_path = gif_path  # Use GIF for display
                    
                    use_video = True
                    
                    # Get filename for download
                    filename = os.path.basename(clip_path)
                    
                    # Generate unique IDs for this clip
                    clip_id = f"clip_{mistake['timestamp'].replace(':', '')}"
                    
                    # Use file path relative to HTML output location for better browser support
                    # Get relative path from output directory (use forward slashes for web compatibility)
                    clip_relative_path = os.path.relpath(clip_path, os.path.dirname(self.output_path)) if hasattr(self, 'output_path') else os.path.basename(clip_path)
                    clip_relative_path = clip_relative_path.replace('\\', '/')  # Convert backslashes to forward slashes
                    
                    # Use video tag if MP4, otherwise use img for GIF
                    if use_video:
                        html += f"""
                <div class="instant-replay" style="margin-bottom: 15px; background: #000; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; align-items: center;">
                    <!-- Playback Controls -->
                    <div style="width: 100%; background: #111; padding: 10px; display: flex; align-items: center; justify-content: center; gap: 6px; flex-wrap: wrap;">
                        <span style="color: #aaa; font-size: 0.9em;">▶️ Control:</span>
                        <button onclick="toggleVideoPause('{clip_id}')" id="{clip_id}_play_btn" style="background: #4a7f4e; color: #fff; padding: 6px 10px; border: 1px solid #6ba570; border-radius: 3px; cursor: pointer; font-size: 0.8em; transition: all 0.2s; font-weight: bold;" title="Pause/Resume">⏸️ Pause</button>
                    </div>
                    
                    <!-- Playback Speed Controls -->
                    <div style="width: 100%; background: #111; padding: 10px; display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap;">
                        <span style="color: #aaa; font-size: 0.9em;">⚡ Speed:</span>
                        <button onclick="setVideoSpeed('{clip_id}', 0.5)" data-clip-id="{clip_id}" data-speed="0.5" style="background: #444; color: #fff; padding: 5px 12px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.85em; transition: all 0.2s;">0.5x</button>
                        <button onclick="setVideoSpeed('{clip_id}', 1)" data-clip-id="{clip_id}" data-speed="1" style="background: #4CAF50; color: #fff; padding: 5px 12px; border: 1px solid #45a049; border-radius: 3px; cursor: pointer; font-size: 0.85em; transition: all 0.2s;">1x</button>
                        <button onclick="setVideoSpeed('{clip_id}', 1.5)" data-clip-id="{clip_id}" data-speed="1.5" style="background: #444; color: #fff; padding: 5px 12px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.85em; transition: all 0.2s;">1.5x</button>
                        <button onclick="setVideoSpeed('{clip_id}', 2)" data-clip-id="{clip_id}" data-speed="2" style="background: #444; color: #fff; padding: 5px 12px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.85em; transition: all 0.2s;">2x</button>
                        <span style="color: #888; font-size: 0.8em; margin-left: 10px;" id="{clip_id}_speed_display">⚡ Normal Speed (1x)</span>
                    </div>
                    
                    <div id="{clip_id}" style="width: 100%; background: #1a1a1a; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px; position: relative;">
                        <!-- HTML5 Video Player with controls -->
                        <video id="{clip_id}_video" src="{clip_relative_path}" style="max-width: 100%; height: auto; display: block;">
                            Your browser does not support HTML5 video playback.
                        </video>
                    </div>
                    
                    <div style="background: #1a1a1a; color: #fff; padding: 10px; font-size: 0.9em; text-align: center; width: 100%;">
                        🎬 Instant Replay - Use the speed controls above to slow down or speed up
                    </div>
                </div>
"""
                    else:
                        # Fallback to GIF display  
                        gif_relative_path = os.path.relpath(clip_path, os.path.dirname(self.output_path)) if hasattr(self, 'output_path') else os.path.basename(clip_path)
                        gif_relative_path = gif_relative_path.replace('\\', '/')  # Convert backslashes to forward slashes
                        html += f"""
                <div class="instant-replay" style="margin-bottom: 15px; background: #000; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; align-items: center;">
                    <!-- Playback Controls -->
                    <div style="width: 100%; background: #111; padding: 10px; display: flex; align-items: center; justify-content: center; gap: 6px; flex-wrap: wrap;">
                        <span style="color: #aaa; font-size: 0.9em;">▶️ Control:</span>
                        <button onclick="toggleGifPause('{clip_id}')" id="{clip_id}_play_btn" style="background: #4a7f4e; color: #fff; padding: 6px 10px; border: 1px solid #6ba570; border-radius: 3px; cursor: pointer; font-size: 0.8em; transition: all 0.2s; font-weight: bold;" title="Pause/Resume">⏸️ Pause</button>
                    </div>
                    
                    <!-- Speed Controls -->
                    <div style="width: 100%; background: #111; padding: 10px; display: flex; align-items: center; justify-content: center; gap: 6px; flex-wrap: wrap;">
                        <span style="color: #aaa; font-size: 0.9em;">⚡ Speed:</span>
                        <button onclick="setGifSpeed('{clip_id}', 0.05)" data-clip-id="{clip_id}" data-speed="0.05" style="background: #444; color: #fff; padding: 5px 8px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s;" title="Ultra Slow - 5% speed">🐢 0.05x</button>
                        <button onclick="setGifSpeed('{clip_id}', 0.1)" data-clip-id="{clip_id}" data-speed="0.1" style="background: #444; color: #fff; padding: 5px 8px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s;" title="Very Slow - 10% speed">🐌 0.1x</button>
                        <button onclick="setGifSpeed('{clip_id}', 0.25)" data-clip-id="{clip_id}" data-speed="0.25" style="background: #444; color: #fff; padding: 5px 8px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s;" title="Slow - 25% speed">📉 0.25x</button>
                        <button onclick="setGifSpeed('{clip_id}', 0.5)" data-clip-id="{clip_id}" data-speed="0.5" style="background: #444; color: #fff; padding: 5px 8px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s;" title="Slow - 50% speed">📉 0.5x</button>
                        <button onclick="setGifSpeed('{clip_id}', 1)" data-clip-id="{clip_id}" data-speed="1" style="background: #4CAF50; color: #fff; padding: 5px 8px; border: 1px solid #45a049; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s; font-weight: bold;" title="Normal - 100% speed">⚡ 1x</button>
                        <button onclick="setGifSpeed('{clip_id}', 1.5)" data-clip-id="{clip_id}" data-speed="1.5" style="background: #444; color: #fff; padding: 5px 8px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s;" title="Fast - 150% speed">🔥 1.5x</button>
                        <button onclick="setGifSpeed('{clip_id}', 2)" data-clip-id="{clip_id}" data-speed="2" style="background: #444; color: #fff; padding: 5px 8px; border: 1px solid #666; border-radius: 3px; cursor: pointer; font-size: 0.75em; transition: all 0.2s;" title="Very Fast - 200% speed">⚡⚡ 2x</button>
                        <span style="color: #888; font-size: 0.75em; margin-left: 10px;" id="{clip_id}_speed_display">⚡ Normal (1x)</span>
                        <span style="color: #FFD700; font-size: 0.7em; margin-left: 5px; display: none;" id="{clip_id}_speed_indicator"></span>
                    </div>
                    
                    <div id="{clip_id}" style="width: 100%; background: #1a1a1a; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px; position: relative;">
                        
                        <!-- GIF display with CSS animation control -->
                        <img id="{clip_id}_gif" src="{gif_relative_path}" style="max-width: 100%; height: auto; animation: gif-play 7s steps(1) infinite;" alt="Instant Replay">
                        
                        <!-- Fallback message if GIF can't load -->
                        <div id="{clip_id}_fallback" style="display: none; text-align: center; padding: 20px; color: #fff; width: 100%;">
                            <p style="margin: 10px 0; font-size: 0.95em;">⚠️ Video playback unavailable in this view</p>
                            <p style="margin: 10px 0; font-size: 0.85em; color: #aaa;">The replay file exists but cannot be displayed here</p>
                            <button onclick="downloadReplayFile('{clip_id}', '{filename}')" style="background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.95em; margin: 10px 0;">
                                📥 Download & View Replay
                            </button>
                            <p style="margin: 10px 0; font-size: 0.8em; color: #999;">Your media player will open with the full resolution video</p>
                        </div>
                    </div>
                    
                    <div style="background: #1a1a1a; color: #fff; padding: 10px; font-size: 0.85em; text-align: center; width: 100%;">
                        🎬 Try 0.05x or 0.1x speed + Pause to see every frame of fast attacks
                    </div>
                </div>
"""

                html += f"""
                <div class="mistake-details">
                    <div class="mistake-move">Move: <strong>{mistake['move']}</strong></div>
                    <div class="mistake-move-description" style="font-size: 0.9em; color: #555; margin-bottom: 10px; font-style: italic;">
                        → {simple_move_desc}
                    </div>
                    <div class="mistake-description">{mistake['description']}</div>
                    
                    <div class="mistake-stats">
                        <div class="mistake-stat">
                            <strong>Mistake Type</strong>
                            <span>{mistake['type']}</span>
                        </div>
                        <div class="mistake-stat">
                            <strong>Damage at Time</strong>
                            <span>{mistake['damage_at_time']} damage</span>
                        </div>
                        <div class="mistake-stat">
                            <strong>Move Damage</strong>
                            <span>{mistake['damage_value']} damage</span>
                        </div>
                    </div>
"""
                
                # Add opponent actions if provided
                if mistake.get('opponent_actions'):
                    opponent_color = mistake['opponent_color']
                    html += f"""
                    <div class="opponent-actions" style="background: rgba({int(opponent_color[1:3], 16)}, {int(opponent_color[3:5], 16)}, {int(opponent_color[5:7], 16)}, 0.1); border-left: 3px solid {opponent_color}; padding: 12px; border-radius: 4px; margin-top: 12px;">
                        <strong style="color: {opponent_color};">What {mistake['opponent_name']} Did:</strong>
                        <div style="margin-top: 8px; color: #555; line-height: 1.6;">
                            {mistake['opponent_actions']}
                        </div>
                    </div>
"""
                
                if mistake['range_note']:
                    html += f"""
                    <div class="range-note">
                        📏 Range Note: <strong>{mistake['range_note']}</strong>
                    </div>
"""
                
                html += """
                </div>
            </div>
"""
            
            html += """
        </div>
"""
        else:
            html += """
        <div class="mistakes-section">
            <div class="empty-state">
                <div class="empty-state-icon">✓</div>
                <p>No significant mistakes detected</p>
            </div>
        </div>
"""
        
        # Add move breakdown sections for each player
        for player_num in [1, 2]:
            player_name = self.PLAYER_COLORS[player_num]["name"]
            moves = self.move_stats.get(player_num, {})
            
            if moves:
                html += f"""
        <div class="move-breakdown-section">
            <h2 class="section-title">📊 {player_name} - Move Variety Breakdown</h2>
"""
                
                # Sort by usage count
                sorted_moves = sorted(moves.items(), key=lambda x: x[1]["count"], reverse=True)
                
                html += """
            <table class="move-table">
                <thead>
                    <tr>
                        <th>Move</th>
                        <th>Usage Count</th>
                        <th>Hits</th>
                        <th>Whiffs</th>
                        <th>Hit Rate</th>
                        <th>Total Damage</th>
                        <th>Avg Damage/Hit</th>
                        <th>Steam/Bar</th>
                    </tr>
                </thead>
                <tbody>
"""
                
                for move, stats in sorted_moves[:15]:  # Show top 15 moves
                    total_attempts = stats["hits"] + stats["whiffs"]
                    hit_rate = (stats["hits"] / total_attempts * 100) if total_attempts > 0 else 0
                    bar_indicator = f"⚡ {stats['uses_bar_count']}x" if stats.get("uses_bar") else "—"
                    bar_color = "color: #FFD700; font-weight: bold;" if stats.get("uses_bar") else ""
                    
                    html += f"""
                    <tr>
                        <td><strong>{move}</strong></td>
                        <td>{stats['count']}</td>
                        <td><span style="color: green; font-weight: bold;">{stats['hits']}</span></td>
                        <td><span style="color: red; font-weight: bold;">{stats['whiffs']}</span></td>
                        <td><strong>{hit_rate:.1f}%</strong></td>
                        <td><strong>{stats['total_damage']}</strong></td>
                        <td><strong>{stats['average_damage']:.1f}</strong></td>
                        <td><span style="{bar_color}">{bar_indicator}</span></td>
                    </tr>
"""
                
                html += """
                </tbody>
            </table>
        </div>
"""
        
        # Add summary stats
        critical_count = len([m for m in self.mistakes if m["severity"] == "Critical"])
        major_count = len([m for m in self.mistakes if m["severity"] == "Major"])
        minor_count = len([m for m in self.mistakes if m["severity"] == "Minor"])
        
        html += f"""
        <div class="mistakes-section">
            <h2 class="section-title">📈 Analysis Summary</h2>
            <div class="stats-grid">
                <div class="stat-box" style="background: linear-gradient(135deg, #FF6B6B 0%, #ff8e8e 100%);">
                    <div class="stat-box-label">Critical Mistakes</div>
                    <div class="stat-box-value">{critical_count}</div>
                </div>
                <div class="stat-box" style="background: linear-gradient(135deg, #FFB347 0%, #ffc966 100%);">
                    <div class="stat-box-label">Major Mistakes</div>
                    <div class="stat-box-value">{major_count}</div>
                </div>
                <div class="stat-box" style="background: linear-gradient(135deg, #FFD93D 0%, #ffe66d 100%);">
                    <div class="stat-box-label">Minor Issues</div>
                    <div class="stat-box-value">{minor_count}</div>
                </div>
                <div class="stat-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="stat-box-label">Total Events</div>
                    <div class="stat-box-value">{len(self.events)}</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>2XKO Gameplay Analyzer v2.0 | Enhanced Report with Move Breakdown & Range Analysis</p>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    
    <!-- Global JavaScript Functions for Replay Controls -->
    <script>
    // Store loser player number (Player 2 in this match)
    const loserPlayer = 2;
    
    // Filter mistakes by player
    function filterMistakes(filter) {{
        const allItems = document.querySelectorAll('.mistake-item');
        const filterAllBtn = document.getElementById('filter_all');
        const filterLoserBtn = document.getElementById('filter_loser');
        
        allItems.forEach(item => {{
            const playerNum = parseInt(item.getAttribute('data-player'));
            if (filter === 'all') {{
                item.style.display = 'block';
            }} else if (filter === 'loser' && playerNum === loserPlayer) {{
                item.style.display = 'block';
            }} else if (filter === 'loser') {{
                item.style.display = 'none';
            }}
        }});
        
        // Update button styles
        if (filter === 'all') {{
            filterAllBtn.style.background = '#4CAF50';
            filterAllBtn.style.borderColor = '#45a049';
            filterLoserBtn.style.background = '#444';
            filterLoserBtn.style.borderColor = '#666';
        }} else if (filter === 'loser') {{
            filterAllBtn.style.background = '#444';
            filterAllBtn.style.borderColor = '#666';
            filterLoserBtn.style.background = '#4CAF50';
            filterLoserBtn.style.borderColor = '#45a049';
        }}
    }}
    
    // GIF animation control for pause functionality
    const gifAnimationStates = {{}};
    
    // Note: GIF pause via CSS is browser-limited, but we provide UI feedback
    // Users can download MP4 versions for full playback control
    function toggleGifPause(clipId) {{
        const gifImg = document.getElementById(clipId + '_gif');
        const playBtn = document.getElementById(clipId + '_play_btn');
        
        if (!gifImg || !playBtn) return;
        
        gifAnimationStates[clipId] = !gifAnimationStates[clipId];
        
        if (gifAnimationStates[clipId]) {{
            // Paused
            gifImg.style.animationPlayState = 'paused';
            playBtn.innerHTML = '▶️ Play';
            playBtn.style.background = '#2196F3';
            playBtn.style.borderColor = '#1976D2';
        }} else {{
            // Playing
            gifImg.style.animationPlayState = 'running';
            playBtn.innerHTML = '⏸️ Pause';
            playBtn.style.background = '#ff9800';
            playBtn.style.borderColor = '#f57c00';
        }}
    }}
    
    function setGifSpeed(clipId, speed) {{
        const gifImg = document.getElementById(clipId + '_gif');
        const speedBtn = document.querySelector('[data-clip-id="' + clipId + '"][data-speed="' + speed + '"]');
        const speedDisplay = document.getElementById(clipId + '_speed_display');
        
        if (!gifImg) return;
        
        // Calculate animation duration (lower speed = longer duration)
        const duration = 7 / speed;  // Base is 7 seconds for full clip
        gifImg.style.animationDuration = duration + 's';
        
        // Update speed display text
        if (speedDisplay) {{
            const speedLabels = {{
                0.05: '🐢 Ultra Slow (0.05x)',
                0.1: '🐌 Very Slow (0.1x)',
                0.25: '📉 Slow (0.25x)',
                0.5: '📉 Slow (0.5x)',
                1: '⚡ Normal (1x)',
                1.5: '🔥 Fast (1.5x)',
                2: '⚡⚡ Very Fast (2x)'
            }};
            speedDisplay.textContent = speedLabels[speed] || speed + 'x';
        }}
    }}
    
    // Video player control functions
    function toggleVideoPause(clipId) {{
        const video = document.getElementById(clipId + '_video');
        const playBtn = document.getElementById(clipId + '_play_btn');
        
        if (!video || !playBtn) return;
        
        if (video.paused) {{
            video.play();
            playBtn.innerHTML = '⏸️ Pause';
            playBtn.style.background = '#ff9800';
            playBtn.style.borderColor = '#f57c00';
        }} else {{
            video.pause();
            playBtn.innerHTML = '▶️ Play';
            playBtn.style.background = '#2196F3';
            playBtn.style.borderColor = '#1976D2';
        }}
    }}
    
    function setVideoSpeed(clipId, speed) {{
        const video = document.getElementById(clipId + '_video');
        const speedBtn = document.querySelector('[data-clip-id="' + clipId + '"][data-speed="' + speed + '"]');
        const speedDisplay = document.getElementById(clipId + '_speed_display');
        
        if (!video) return;
        
        video.playbackRate = speed;
        
        // Update speed display text
        if (speedDisplay) {{
            const speedLabels = {{
                0.5: '📉 Slow (0.5x)',
                1: '⚡ Normal (1x)',
                1.5: '🔥 Fast (1.5x)',
                2: '⚡⚡ Very Fast (2x)'
            }};
            speedDisplay.textContent = speedLabels[speed] || speed + 'x';
        }}
        
        // Update button styling
        const allSpeedBtns = document.querySelectorAll('[data-clip-id="' + clipId + '"]');
        allSpeedBtns.forEach(btn => {{
            btn.style.background = '#444';
            btn.style.borderColor = '#666';
        }});
        
        if (speedBtn) {{
            speedBtn.style.background = '#4CAF50';
            speedBtn.style.borderColor = '#45a049';
        }}
    }}
        
        // Update button styling
        const allSpeedBtns = document.querySelectorAll('[data-clip-id="' + clipId + '"]');
        allSpeedBtns.forEach(btn => {{
            btn.style.background = '#444';
            btn.style.borderColor = '#666';
        }});
        
        if (speedBtn) {{
            speedBtn.style.background = '#4CAF50';
            speedBtn.style.borderColor = '#45a049';
        }}
    }}
    
    // Global speed storage for video elements
    const videoSpeeds = {{}};
    
    // Global function - Handle GIF load failure with fallback
    function handleGifLoadError(clipId, gifPath) {{
        console.warn("GIF failed to load:", gifPath);
        const gifElement = document.getElementById(clipId + "_gif");
        const fallbackElement = document.getElementById(clipId + "_fallback");
        
        if (gifElement) {{
            gifElement.style.display = "none";
        }}
        if (fallbackElement) {{
            fallbackElement.style.display = "block";
        }}
    }}
    
    // Global function - Download replay file from base64
    function downloadReplayFile(clipId, filename) {{
        const video = document.getElementById(clipId + '_video');
        const img = document.getElementById(clipId + '_gif');
        const src = video ? video.src : (img ? img.src : null);
        
        if (!src) {{
            console.error('No playable media found for:', clipId);
            return;
        }}
        
        const link = document.createElement('a');
        link.href = src;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }}
    
    // On page load, ensure all videos have speed controls initialized
    window.addEventListener('load', function() {{
        // Initialize all speed displays with 1x
        const speedDisplays = document.querySelectorAll('[id$="_speed_display"]');
        speedDisplays.forEach(display => {{
            if (display.textContent === '' || !display.textContent) {{
                display.textContent = '⚡ Normal Speed (1x)';
            }}
        }});
    }});
    </script>
</body>
</html>
```"""
        
        return html
    
    def save_to_file(self, filename: str) -> str:
        """Save HTML report to file"""
        html_content = self.generate_html(output_path=filename)
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return os.path.abspath(filename)
