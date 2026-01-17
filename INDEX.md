# 2XKO Analyzer - Project Index

## 📂 Project Files & Directory Guide

### 🎯 **START HERE**
1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ (5-minute setup guide)
   - Installation steps
   - First analysis walkthrough
   - FAQ and troubleshooting
   - **👉 Read this first!**

2. **[main.py](main.py)** 🚀 (Application entry point)
   - Run with: `python main.py`
   - Interactive CLI menu
   - All features accessible from here

### 📚 **DOCUMENTATION**

3. **[README.md](README.md)** (Comprehensive guide)
   - Feature overview
   - Installation instructions
   - Usage examples
   - Frame data explanations
   - Blitzcrank strategy notes
   - Limitations and future work

4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** (This project overview)
   - Complete project details
   - Architecture explanation
   - Implementation highlights
   - Statistics and metrics
   - Testing & quality info
   - Roadmap for enhancements

### ⚙️ **CONFIGURATION & TESTING**

5. **[requirements.txt](requirements.txt)** (Python dependencies)
   - Lists all required packages
   - Run: `pip install -r requirements.txt`

6. **[config.yaml](config.yaml)** (Configuration settings)
   - Video analysis parameters
   - Game mode definitions
   - Frame data thresholds
   - Character metadata

7. **[tests.py](tests.py)** (Unit tests)
   - Run: `python tests.py`
   - Tests frame data accuracy
   - Validates core functionality
   - 12+ test cases

### 💻 **SOURCE CODE** (src/ directory)

8. **[src/frame_data.py](src/frame_data.py)** (Blitzcrank move database)
   - 90+ moves with complete frame data
   - Helper functions for data queries
   - Combo detection utilities
   - Constants and mechanics

9. **[src/video_analyzer.py](src/video_analyzer.py)** (Video processing)
   - VideoFrameAnalyzer: Frame extraction and analysis
   - GameStateDetector: Event detection
   - MoveDetector: Move identification
   - AnalysisSession: Orchestration

10. **[src/analysis_engine.py](src/analysis_engine.py)** (Analysis logic)
    - PlaystyleAnalyzer: Player behavior classification
    - MistakeDetector: Error identification
    - RecommendationEngine: Strategy suggestions
    - AnalysisReport: Report generation

---

## 🚀 Quick Navigation Guide

### I want to...

**Analyze a video**
→ Run `python main.py` → Select option 1

**Learn about Blitzcrank moves**
→ Run `python main.py` → Select option 3 (Frame Data Browser)

**Get strategy tips**
→ Run `python main.py` → Select option 4 (Tips)

**Set up the project**
→ Read [QUICKSTART.md](QUICKSTART.md)

**Understand the architecture**
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**Add a new character**
→ Edit [src/frame_data.py](src/frame_data.py)

**Change analysis settings**
→ Edit [config.yaml](config.yaml)

**Run tests**
→ Run `python tests.py`

---

## 📊 File Statistics

| File | Type | Size | Purpose |
|------|------|------|---------|
| main.py | Python | ~600 lines | CLI & orchestration |
| frame_data.py | Python | ~500 lines | Move database |
| video_analyzer.py | Python | ~400 lines | Video processing |
| analysis_engine.py | Python | ~500 lines | Analysis logic |
| tests.py | Python | ~250 lines | Unit tests |
| README.md | Markdown | ~400 lines | Main documentation |
| QUICKSTART.md | Markdown | ~300 lines | Setup guide |
| PROJECT_SUMMARY.md | Markdown | ~400 lines | Project overview |
| config.yaml | YAML | ~40 lines | Configuration |

**Total Code**: 2,500+ lines  
**Documentation**: 1,100+ lines  
**Tests**: 250+ lines

---

## 🎮 Feature Checklist

### Video Analysis
- ✅ MP4 file processing
- ✅ Frame extraction
- ✅ Event detection (hits, flashes)
- ✅ Motion analysis
- ✅ Timestamp generation

### Frame Data
- ✅ 90+ Blitzcrank moves
- ✅ Complete metrics (startup, recovery, on-block, etc.)
- ✅ Move categorization
- ✅ Combo starter detection
- ✅ Safety analysis

### Gameplay Analysis
- ✅ Mistake detection (8 types)
- ✅ Playstyle assessment
- ✅ Move recommendations
- ✅ Character-specific tips
- ✅ Severity classification

### User Interface
- ✅ Interactive menu system
- ✅ Character selection
- ✅ Frame data browser
- ✅ Search functionality
- ✅ Report generation
- ✅ JSON export

### Documentation
- ✅ Installation guide
- ✅ Usage examples
- ✅ Frame data explanations
- ✅ Strategy tips
- ✅ Troubleshooting guide
- ✅ Quick start guide

---

## 🔧 Installation Checklist

- [ ] Python 3.8+ installed
- [ ] `pip install -r requirements.txt` completed
- [ ] FFmpeg installed and in PATH
- [ ] `python tests.py` passes
- [ ] `python main.py` launches successfully

---

## 📈 Next Steps After Installation

1. **Read QUICKSTART.md** (5 min)
2. **Run main.py** and explore menus (10 min)
3. **View Frame Data** for Blitzcrank (15 min)
4. **Analyze a video** with your match (10 min)
5. **Review recommendations** from the report (10 min)

**Total time**: ~50 minutes to be fully up to speed!

---

## 🎯 Feature Highlights

### Most Useful Functions

**Find if a move is safe**
```
Main Menu → 3 (Frame Data) → Search for move → Check "Block: " value
Negative = unsafe, Zero or Positive = safe
```

**Get tips for your character**
```
Main Menu → 4 (Tips) → Read Blitzcrank section for your situation
```

**Analyze a match**
```
Main Menu → 1 (Analyze Video) → Follow prompts → Review report
```

**Export for sharing**
```
During/after analysis → Select "Export to JSON" → Share report
```

---

## 📞 Help & Support

### Common Questions

**Q: Where do I put my video file?**  
A: Anywhere on your computer. The tool will ask you to select it.

**Q: What video format works?**  
A: MP4 files work best. Must be readable by FFmpeg.

**Q: Can I analyze other characters?**  
A: Yes! The framework supports all 11 2XKO champions. Add their frame data to `src/frame_data.py`.

**Q: How do I interpret frame data?**  
A: Read "Understanding Frame Data" section in QUICKSTART.md

**Q: What if analysis doesn't work?**  
A: Check QUICKSTART.md troubleshooting section or README.md FAQ

---

## 🔗 External Resources

- **2XKO Official**: https://2xko.riotgames.com/
- **2XKO Wiki**: https://wiki.play2xko.com/
- **Blitzcrank Page**: https://wiki.play2xko.com/en-us/Blitzcrank

---

## 📋 Version Information

- **Project**: 2XKO Gameplay Analyzer
- **Version**: 1.0
- **Release Date**: January 2026
- **Python**: 3.8+
- **Status**: ✅ Complete & Ready to Use

---

## 🏆 What This Tool Does

```
Your Gameplay Video
        ↓
    [Analyzer]
        ↓
   Video Processing → Event Detection → Move Identification
        ↓
   Frame Data Lookup → Mistake Detection → Analysis
        ↓
    Report Generation → Recommendations → Export
        ↓
    Your Personalized Analysis
```

---

**Everything is ready to use! Start with QUICKSTART.md, then run `python main.py`** 🚀
