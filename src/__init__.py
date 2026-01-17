"""
2XKO Gameplay Analyzer - Core Package
Modules for video analysis, frame data, and gameplay assessment
"""

__version__ = "1.0"
__author__ = "2XKO Analyzer Team"
__description__ = "Fighting game video analysis tool for 2XKO"

from . import frame_data
from . import video_analyzer
from . import analysis_engine

__all__ = [
    "frame_data",
    "video_analyzer", 
    "analysis_engine"
]
