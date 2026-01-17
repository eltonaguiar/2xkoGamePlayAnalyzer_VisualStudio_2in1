"""Configuration helpers for Codex matchup analysis."""

from dataclasses import dataclass
from typing import Literal


MatchupType = Literal["mirror", "cross"]


@dataclass
class AnalyzerParameters:
    """Runtime parameters for video analysis."""

    video_path: str
    player1_name: str = "Player 1"
    player2_name: str = "Player 2"
    character1: str = "Blitzcrank"
    character2: str = "Blitzcrank"
    matchup: MatchupType = "mirror"
    mode: str = "Juggernaut"
    sample_rate: int = 3  # analyze every N frames
    flash_threshold: float = 24.0  # brightness delta to flag an event
    major_flash_threshold: float = 55.0  # bigger flashes = supers/whiffs
    motion_threshold: float = 4.5  # optical flow magnitude to treat as scramble
    max_events: int = 120  # trim report noise
    round_length_sec: int = 40  # approximate per-round length for grouping (heuristic)
    min_event_second: float = 2.0  # ignore detections earlier than this to avoid round-start noise
    top_punished_clips_per_player: int = 2

    def describe(self) -> str:
        """Human-readable description for logs."""
        return (
            f"{self.character1} vs {self.character2} "
            f"({self.matchup}, {self.mode}, sample={self.sample_rate})"
        )
