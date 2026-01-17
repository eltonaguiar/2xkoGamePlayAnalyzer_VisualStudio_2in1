"""
Gameplay Analysis Engine
Identifies mistakes, playstyles, and provides recommendations
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class MistakeType(Enum):
    """Types of mistakes"""
    UNSAFE_MOVE_ON_BLOCK = "Unsafe on Block"
    MISSED_PUNISH = "Missed Punish Opportunity"
    POOR_SPACING = "Poor Spacing"
    WHIFFED_GRAB = "Whiffed Grab"
    BAD_BLOCKSTRING = "Broken Blockstring"
    TECH_CHASE_FAIL = "Failed Tech Chase"
    WRONG_OKIZEME = "Poor Okizeme"
    DROPPED_COMBO = "Dropped Combo"
    OVERZEALOUS_APPROACH = "Risky Approach"
    RECOVERY_PUNISHED = "Recovery Punished"


@dataclass
class PlayerAnalysis:
    """Analysis of a single player's performance"""
    character: str
    playstyle: str  # e.g., "Aggressive", "Defensive", "Grab-Heavy"
    strengths: List[str]
    weaknesses: List[str]
    mistake_count: int
    missed_damage_total: float
    average_combo_damage: float
    throw_usage_percent: float
    success_rate: float


@dataclass
class Mistake:
    """A detected mistake in gameplay"""
    frame_number: int
    timestamp: str
    player: int  # 1 or 2
    move_used: str
    mistake_type: MistakeType
    description: str
    frame_data: Dict
    correction: str
    damage_lost: float
    severity: str  # "Minor", "Major", "Critical"


class PlaystyleAnalyzer:
    """Analyzes player playstyle from move usage"""
    
    def __init__(self):
        self.move_frequency = {}
        self.throw_attempts = 0
        self.grab_success_rate = 0.0
        self.pressure_strings = []
        self.defensive_options = []
        
    def analyze_playstyle(self, move_log: List[Dict]) -> str:
        """Determine playstyle from move history"""
        
        grab_count = sum(1 for m in move_log if "S1" in m.get("move", ""))
        strike_count = sum(1 for m in move_log if any(x in m.get("move", "") for x in ["L", "M", "H", "5", "2", "j"]))
        special_count = sum(1 for m in move_log if "S2" in m.get("move", ""))
        
        if len(move_log) == 0:
            return "Unknown"
        
        grab_percentage = grab_count / len(move_log) * 100
        special_percentage = special_count / len(move_log) * 100
        
        if grab_percentage > 40:
            return "Grab-Heavy / Aggressive Grappler"
        elif special_percentage > 30:
            return "Special-Focused / Combo-Heavy"
        elif grab_percentage > 20 and strike_count > grab_count:
            return "Balanced Mix-up Player"
        elif grab_percentage < 10:
            return "Strike-Focused / Footsies-Heavy"
        else:
            return "Balanced"


class MistakeDetector:
    """Identifies mistakes in gameplay"""
    
    @staticmethod
    def check_unsafe_move(move_name: str, blocked: bool, frame_data: Dict) -> Optional[Mistake]:
        """Check if a move is unsafe on block"""
        if not blocked or not frame_data:
            return None
        
        on_block = frame_data.get("on_block", 0)
        
        # Moves that are -10 or worse are very unsafe
        if on_block < -7:
            return {
                "type": MistakeType.UNSAFE_MOVE_ON_BLOCK,
                "severity": "Critical" if on_block < -15 else "Major",
                "frame_disadvantage": on_block,
                "risk_level": "High"
            }
        
        return None
    
    @staticmethod
    def detect_whiffed_grab(move_name: str, hit: bool, character_spacing: str) -> Optional[Mistake]:
        """Detect whiffed grab attempt"""
        is_grab = "S1" in move_name or "2S2" in move_name or "6S2_2S2" in move_name
        
        if is_grab and not hit and character_spacing == "too_far":
            return {
                "type": MistakeType.WHIFFED_GRAB,
                "severity": "Major",
                "reason": "Used grab outside of range",
                "recovery_frames": 60  # Typical grab recovery
            }
        
        return None
    
    @staticmethod
    def detect_missed_punish(opponent_move: str, recovery_frames: int, player_action_delay: int, opponent_frame_data: Dict) -> Optional[Mistake]:
        """Detect when player could have punished but didn't"""
        
        on_block = opponent_frame_data.get("on_block", 0)
        
        # If opponent is -7 or worse and player didn't punish
        if on_block < -7 and player_action_delay > 10:
            return {
                "type": MistakeType.MISSED_PUNISH,
                "severity": "Major",
                "opportunity": f"Opponent move was {on_block}f",
                "optimal_punish": "Use fastest startup move (5L: 8f startup)",
                "damage_lost": 45  # At least light punch damage
            }
        
        return None


class RecommendationEngine:
    """Generates recommendations for improvement"""
    
    @staticmethod
    def get_move_recommendations(move_used: str, situation: str, frame_data: Dict) -> List[str]:
        """Get better move options for a situation"""
        
        recommendations = []
        on_block = frame_data.get("on_block", 0)
        
        # Unsafe on block
        if on_block < -7:
            recommendations.append(f"❌ {move_used} is {on_block}f on block - TOO UNSAFE! Use safer options like 5L(-2f) or 2L(-3f)")
        
        # Can't combo after this
        if "on_block" in frame_data and on_block < 0:
            recommendations.append(f"✓ After blocking, opponent can punish - be ready to defend or block again")
        
        # Grab spacing
        if "S1" in move_used or "2S2" in move_used:
            recommendations.append("💡 Grab spacing: Ensure opponent is in range - too close = won't connect, too far = whiff recovery")
        
        return recommendations
    
    @staticmethod
    def get_blitzcrank_tips() -> Dict:
        """Get character-specific tips for Blitzcrank"""
        return {
            "neutral_game": [
                "Use 5S1 (Rocket Grab) to force opponent into close range - fullscreen reach is your strength",
                "Rocket Grab is +4f on block, giving you turn advantage to continue pressure",
                "Build Steam gauge with grab hits - empowered versions are much stronger"
            ],
            "mixup_game": [
                "Once close: condition opponent between strikes and 2S2 (Garbage Collection) command grab",
                "2S2 is 0-startup but has startup/active frames - careful of clash",
                "2M catches fuzzy jumps - excellent for anti-escape",
                "After successful grab: forward throw puts opponent in Hard Knockdown - follow with assist or 66H"
            ],
            "neutral_tools": [
                "2H: Main anti-air (13f startup, -16f on block) - risky but necessary",
                "5H: Can be charged for ground bounce, good for beating other normals",
                "66H: Hits low, crushing lows - useful for catching crouch tech",
                "5L: -2f on block but disjointed, can stop opponent approaches"
            ],
            "steam_mechanic": [
                "Rocket Grab variants (5S1/2S1/jS1) generate Steam and enhance to multi-hit with shock",
                "Empowered grabs and specials deal more damage and have better properties",
                "At full Steam: gain 10% movement speed buff (helps with mobility issue)",
                "Spinning Turbine (6S2) also charges Steam - use to build meter while repositioning"
            ],
            "okizeme": [
                "After forward throw: can combo into 66H or assist into mixup",
                "Back throw creates Ground Bounce - use to continue combo",
                "Hard Knockdown situations: opponent vulnerable to 66H and tech chase setups"
            ],
            "matchup_tips_blitzcrank_mirror": [
                "Whoever lands grab first has advantage - be careful with commit",
                "Both characters want close range - be patient, don't whiff",
                "Tech chase heavy character - use 2M and throw mixups extensively",
                "Be wary of opponent's Rocket Grab - respect its range and don't approach recklessly",
                "Assist coverage becomes critical - good assist can swing entire matchup",
                "Steam management is key - charge intelligently and use empowered moves when it matters"
            ]
        }
    
    @staticmethod
    def generate_combo_suggestions(character: str, situation: str) -> List[str]:
        """Generate combo suggestions"""
        if character.lower() != "blitzcrank":
            return []
        
        suggestions = []
        
        if "ground_bounce" in situation:
            suggestions.append("After Ground Bounce: 2M > [continue juggle] > 2H > air combo")
            suggestions.append("Alternative: Dash > 5H > jM > jH > land combo")
        
        if "air_tailspin" in situation:
            suggestions.append("After Air Tailspin: jump > jM > jH > etc (air series)")
            suggestions.append("Or: land > 5M > 2M for reset")
        
        if "hard_knockdown" in situation:
            suggestions.append("Okizeme options: 66H (hits OTG), assist setup, or tech chase with 2M/throw mix")
        
        if "grab_hit" in situation:
            suggestions.append("After grab: 5S1~S1 (Power Fist follow-up) into air combo")
            suggestions.append("Or: 66H > assist/tag for resets")
        
        return suggestions


class AnalysisReport:
    """Generates final analysis report"""
    
    def __init__(self):
        self.player1_analysis: Optional[PlayerAnalysis] = None
        self.player2_analysis: Optional[PlayerAnalysis] = None
        self.mistakes: List[Mistake] = []
        self.key_moments: List[Dict] = []
        self.recommendations: Dict = {}
        
    def generate_summary(self) -> str:
        """Generate text summary of analysis"""
        summary = []
        summary.append("\n" + "="*60)
        summary.append("ANALYSIS SUMMARY")
        summary.append("="*60 + "\n")
        
        if self.player1_analysis:
            summary.append(f"PLAYER 1 - {self.player1_analysis.character}")
            summary.append(f"Playstyle: {self.player1_analysis.playstyle}")
            summary.append(f"Success Rate: {self.player1_analysis.success_rate:.1f}%")
            summary.append(f"Mistakes: {self.player1_analysis.mistake_count}")
            summary.append(f"Avg Combo Damage: {self.player1_analysis.average_combo_damage:.0f}")
            summary.append(f"Grab Usage: {self.player1_analysis.throw_usage_percent:.1f}%")
            summary.append("Strengths:")
            for strength in self.player1_analysis.strengths:
                summary.append(f"  ✓ {strength}")
            summary.append("Weaknesses:")
            for weakness in self.player1_analysis.weaknesses:
                summary.append(f"  ✗ {weakness}")
            summary.append("")
        
        if self.player2_analysis:
            summary.append(f"PLAYER 2 - {self.player2_analysis.character}")
            summary.append(f"Playstyle: {self.player2_analysis.playstyle}")
            summary.append(f"Success Rate: {self.player2_analysis.success_rate:.1f}%")
            summary.append(f"Mistakes: {self.player2_analysis.mistake_count}")
            summary.append(f"Avg Combo Damage: {self.player2_analysis.average_combo_damage:.0f}")
            summary.append(f"Grab Usage: {self.player2_analysis.throw_usage_percent:.1f}%")
            summary.append("Strengths:")
            for strength in self.player2_analysis.strengths:
                summary.append(f"  ✓ {strength}")
            summary.append("Weaknesses:")
            for weakness in self.player2_analysis.weaknesses:
                summary.append(f"  ✗ {weakness}")
            summary.append("")
        
        return "\n".join(summary)
    
    def generate_mistakes_report(self) -> str:
        """Generate detailed mistakes report"""
        if not self.mistakes:
            return "No mistakes detected.\n"
        
        report = []
        report.append("\nKEY MISTAKES DETECTED")
        report.append("-" * 60)
        
        # Sort by severity
        critical = [m for m in self.mistakes if m.severity == "Critical"]
        major = [m for m in self.mistakes if m.severity == "Major"]
        minor = [m for m in self.mistakes if m.severity == "Minor"]
        
        if critical:
            report.append(f"\n🔴 CRITICAL ({len(critical)} mistakes)")
            for mistake in critical[:5]:  # Show top 5
                report.append(f"\n  [{mistake.timestamp}] {mistake.move_used}")
                report.append(f"  Type: {mistake.mistake_type.value}")
                report.append(f"  {mistake.description}")
                report.append(f"  Correction: {mistake.correction}")
                report.append(f"  Damage Lost: {mistake.damage_lost:.0f}")
        
        if major:
            report.append(f"\n🟠 MAJOR ({len(major)} mistakes)")
            for mistake in major[:5]:
                report.append(f"\n  [{mistake.timestamp}] {mistake.move_used}")
                report.append(f"  Type: {mistake.mistake_type.value}")
                report.append(f"  {mistake.description}")
                report.append(f"  Correction: {mistake.correction}")
        
        if minor:
            report.append(f"\n🟡 MINOR ({len(minor)} mistakes)")
            for mistake in minor[:3]:
                report.append(f"\n  [{mistake.timestamp}] {mistake.move_used}")
                report.append(f"  Type: {mistake.mistake_type.value}")
        
        return "\n".join(report)
    
    def export_json(self, filename: str) -> None:
        """Export analysis as JSON"""
        data = {
            "player1": {
                "character": self.player1_analysis.character if self.player1_analysis else "Unknown",
                "playstyle": self.player1_analysis.playstyle if self.player1_analysis else "Unknown",
                "success_rate": self.player1_analysis.success_rate if self.player1_analysis else 0,
                "mistakes": self.player1_analysis.mistake_count if self.player1_analysis else 0
            },
            "player2": {
                "character": self.player2_analysis.character if self.player2_analysis else "Unknown",
                "playstyle": self.player2_analysis.playstyle if self.player2_analysis else "Unknown",
                "success_rate": self.player2_analysis.success_rate if self.player2_analysis else 0,
                "mistakes": self.player2_analysis.mistake_count if self.player2_analysis else 0
            },
            "total_mistakes": len(self.mistakes),
            "critical_mistakes": sum(1 for m in self.mistakes if m.severity == "Critical"),
            "recommendations": self.recommendations
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✓ Analysis exported to {filename}")
