# 2XKO GP Analyzer - Project Overview

This repository contains two complementary fighting game analysis systems for 2XKO (2v2 Fighting Game). Both projects analyze Blitzcrank mirror matchup gameplay but use different analytical approaches.

---

## 🎯 Project Comparison

| Feature | Main (Root) Project | CODEX_CHATGPT Project |
|---------|-------------------|----------------------|
| **Approach** | Frame-by-frame video analysis | Knowledge-base + game state simulation |
| **Video Processing** | OpenCV frame extraction & analysis | Configuration-based game state modeling |
| **Move Detection** | Direct pixel/frame analysis | Rule-based move detection from game state |
| **Mistake Finding** | Timeline-based video scanning | Rule application on simulated game states |
| **Output Format** | Interactive HTML report with instant replays | Statistical analysis with detailed metrics |
| **Speed Controls** | Yes (0.05x - 2x with pause button) | N/A (analysis-only) |
| **GIF/MP4 Clips** | Generated from video frames | N/A |
| **Learning Curve** | Medium (requires game knowledge) | High (requires deep frame data knowledge) |
| **Accuracy** | Good for obvious mistakes | Excellent for frame-perfect analysis |

---

## 📁 Project Structure

```
2xkoGPAnalyzer_VisualStudio/
├── README_PROJECT_OVERVIEW.md          # This file
├── README.md                           # Main project documentation
├── analyze_first_match.py              # Main entry point for analysis
├── main.py                             # GUI launcher
├── requirements.txt                    # Python dependencies
├── config.yaml                         # Configuration file
│
├── src/                                # Main project source
│   ├── html_report.py                  # HTML report generation
│   ├── game_analyzer.py                # Video analysis engine
│   ├── game_database.py                # Character/move database
│   ├── utils.py                        # Utility functions
│   └── ...
│
├── output/                             # Generated reports & clips
│   ├── Blitz_vs_Blitz_Juggernaut_Analysis.html
│   └── clips/                          # MP4 and GIF instant replays
│
└── CODEX_CHATGPT/                      # Sister project (alternative analysis)
    ├── run_codex_analyzer.py           # Alternative entry point
    ├── blitzcrank_knowledge.py         # Character knowledge base
    ├── mirror_matchup.py               # Mirror matchup logic
    ├── config.py                       # Project configuration
    ├── report_builder.py               # Report generation
    └── output/                         # Generated analysis
```

---

## 🚀 Main Project - Frame-by-Frame Video Analysis

### Best For:
- Coaches analyzing student gameplay
- Players wanting instant visual feedback
- Real-time pattern recognition
- Beginner to intermediate players

### Key Features:
- **Video Processing**: Analyzes raw MP4 footage frame-by-frame using OpenCV
- **Instant Replays**: Generates GIF and MP4 clips of each mistake (7 seconds)
- **Interactive HTML Reports**: Browser-based analysis with instant replay controls
- **Playback Controls**: 
  - Pause button for frame-by-frame analysis
  - Speed controls: 0.05x, 0.1x, 0.25x, 0.5x, 1x, 1.5x, 2x
- **Mistake Filtering**: View all mistakes or only opponent's mistakes
- **Character Recognition**: Displays character images with champion/runner-up labels
- **Professional Formatting**: Responsive design with comprehensive statistics

### Workflow:
1. Place MP4 video in `Desktop/`
2. Run `python analyze_first_match.py`
3. Open generated HTML report in browser
4. Review instant replays with full controls
5. Filter by player to focus on key mistakes

### Example Output:
- 5 mistakes identified
- Round-by-round breakdown (3-1 final)
- Character images and icons
- Winner/loser statistics with color coding
- Click-to-play instant replays with video controls

---

## 🧠 CODEX_CHATGPT Project - Knowledge-Base Analysis

### Best For:
- Advanced competitive players
- Frame data researchers
- Detailed matchup analysis
- Post-game theory crafting

### Key Features:
- **Knowledge Base**: Comprehensive Blitzcrank move database with frame data
- **Game State Simulation**: Tracks game state throughout video
- **Rule Engine**: Applies competitive analysis rules
- **Statistical Output**: Detailed metrics and percentages
- **Matchup Specific**: Optimized for Blitzcrank mirror matchups
- **Move Classification**: Categorizes moves by risk/reward
- **Detailed Metrics**: Damage output, whiff rates, success percentages

### Workflow:
1. Configure game state parameters in `config.py`
2. Run `python run_codex_analyzer.py`
3. View statistical analysis output
4. Export metrics for external analysis

### Unique Capabilities:
- Frame-perfect mistake classification
- Advanced matchup theory
- Move efficiency ratings
- Damage optimization analysis
- Player playstyle profiling

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- FFmpeg (for video processing in main project)
- Git (for repository management)

### Installation Steps

```bash
# Clone repository
git clone https://github.com/yourusername/2xkoGPAnalyzer_VisualStudio.git
cd 2xkoGPAnalyzer_VisualStudio

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

---

## ▶️ Quick Start

### Main Project (Recommended for Most Users):
```bash
python analyze_first_match.py
```

### CODEX_CHATGPT Project (Advanced Users):
```bash
python CODEX_CHATGPT/run_codex_analyzer.py
```

---

## 📊 Choosing Which Project to Use

### Use **Main Project** If:
✅ You want visual instant replays  
✅ You prefer interactive browser-based analysis  
✅ You want to pause and inspect frame-by-frame  
✅ You're learning fighting game fundamentals  
✅ You want quick visual feedback  

### Use **CODEX_CHATGPT** If:
✅ You need frame-perfect analysis  
✅ You want statistical metrics  
✅ You're researching matchup theory  
✅ You want detailed move classification  
✅ You prefer command-line analysis  

### Use **Both** For:
✅ Comprehensive analysis from multiple angles  
✅ Cross-validation of findings  
✅ Visual feedback + statistical backing  
✅ Complete player profiling  

---

## 🎮 Supported Game Content

- **Game**: 2XKO (2v2 Fighting Game)
- **Characters**: Blitzcrank (focused), other characters supported
- **Modes**: Juggernaut Mode, Standard Mode
- **Matchups**: Mirror (Blitz vs Blitz) with multi-champion support
- **Video Format**: MP4 (H.264/H.265)
- **Frame Rate**: 30 FPS (configurable)

---

## 📈 Analysis Metrics

### Main Project Provides:
- Mistake count and severity
- Round-by-round results
- Player statistics (damage, whiffs, etc.)
- Character matchup summary
- Visual mistake timeline
- Instant replay timestamps

### CODEX_CHATGPT Provides:
- Frame data analysis
- Move efficiency ratings
- Matchup theory metrics
- Playstyle classification
- Statistical move distribution
- Advanced game state tracking

---

## 🔧 Configuration

### Main Project:
Edit `config.yaml` for:
- Video processing parameters
- Mistake detection thresholds
- Output directory settings
- Report styling options

### CODEX_CHATGPT:
Edit `config.py` for:
- Character frame data
- Game state parameters
- Analysis rules
- Output format preferences

---

## 📝 Output Examples

### Main Project Output:
- `Blitz_vs_Blitz_Juggernaut_Analysis.html` - Interactive report
- `clips/mistake_1_*.gif` - GIF instant replays
- `clips/mistake_1_*.mp4` - MP4 backup videos
- Professional formatting with character images

### CODEX_CHATGPT Output:
- Console statistical analysis
- Detailed metrics report
- Matchup theory breakdown
- Player playstyle profile

---

## 🐛 Troubleshooting

### Main Project:
- **No video found**: Place MP4 in Desktop folder
- **FFmpeg error**: Install FFmpeg system-wide
- **Report won't open**: Check browser compatibility (Chrome/Firefox/Edge)
- **Replay won't play**: Verify MP4 codec is H.264/H.265

### CODEX_CHATGPT:
- **Import errors**: Ensure dependencies installed
- **Game state mismatch**: Verify config.py parameters
- **Missing frame data**: Check blitzcrank_knowledge.py

---

## 📚 Documentation Files

### Main Project:
- `README.md` - Detailed main project documentation
- `QUICKSTART.md` - Quick start guide
- `API_REFERENCE.md` - API documentation
- `REPORT_FEATURES.md` - Report feature details

### CODEX_CHATGPT:
- Check individual files for docstrings
- Review `config.py` for all options

---

## 🤝 Contributing

Both projects welcome improvements:
1. Create feature branch
2. Make your changes
3. Test thoroughly
4. Submit pull request

---

## 📄 License

[Add your license information here]

---

## 👨‍💻 Author

Created for 2XKO fighting game analysis and player development.

---

## 🔗 Quick Links

- **Main Project**: `README.md`
- **Quick Start**: `QUICKSTART.md`
- **API Reference**: `API_REFERENCE.md`
- **CODEX_CHATGPT**: `CODEX_CHATGPT/`

---

**Last Updated**: January 17, 2026  
**Projects**: Main (Frame Analysis) + CODEX_CHATGPT (Knowledge-Base Analysis)
