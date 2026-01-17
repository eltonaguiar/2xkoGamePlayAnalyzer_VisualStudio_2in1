"""Blitzcrank-specific matchup knowledge pulled from move data."""

from typing import Dict, List, Tuple
from src.frame_data import BLITZCRANK_FRAME_DATA, get_frame_data


def unsafe_on_block_moves(threshold: int = -10) -> List[Tuple[str, int]]:
    """Return Blitzcrank moves that are punishable on block."""
    unsafe = []
    for name, data in BLITZCRANK_FRAME_DATA.items():
        if "on_block" in data and data["on_block"] < threshold:
            unsafe.append((name, data["on_block"]))
    return sorted(unsafe, key=lambda x: x[1])


def safe_pressure_moves() -> List[str]:
    """Moves Blitzcrank can use to stay safe while applying pressure."""
    return ["5L", "2L", "5S1", "jL", "j2H"]


def juggernaut_notes() -> List[str]:
    """Quick Juggernaut-mode reminders for the mirror."""
    return [
        "Juggernaut replaces Tag Launcher with Eject; plan to burst out safely.",
        "Both players keep command grabs; whoever lands first grab controls the round.",
        "Steam meter control is huge—empowered grabs add shock and armor.",
    ]


def quick_move_lookup(move: str) -> Dict:
    """Grab frame data for a single move with an empty fallback."""
    return get_frame_data(move) or {}


def preferred_punishes() -> List[str]:
    """Fast punish options for unsafe specials."""
    return [
        "5L (8f, -2 on block)",
        "2L (9f, low, -3 on block)",
        "66H (low crush, OTG, -9 on block for knockdowns)",
    ]


def neutral_game_tips() -> List[str]:
    """Neutral pointers for Blitz mirrors."""
    return [
        "Dash-block to inch forward; avoid raw 5S2 which is -15 on block.",
        "Preemptive 2M catches jump-outs; 2H is your main anti-air (13f, -16 on block).",
        "Use 5S1 to force interaction, but cover with assist or be ready to block.",
    ]
