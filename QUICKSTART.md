# Quick Start Guide - 2XKO Analyzer

## Installation (5 minutes)

### 1. Install Python
- Download Python 3.8+ from https://www.python.org/
- Make sure "Add Python to PATH" is checked during installation

### 2. Install FFmpeg
**Windows:**
```powershell
# Using Chocolatey (if installed)
choco install ffmpeg

# OR download from https://ffmpeg.org/download.html
```

### 3. Install Project Dependencies
```bash
cd 2xkoGPAnalyzer_VisualStudio
pip install -r requirements.txt
```

## Your First Analysis (10 minutes)

### Step 1: Prepare Your Video
- Make sure you have a 2XKO gameplay MP4 video
- Default location: `C:\Users\<YourName>\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4`
- Or have the file path ready

### Step 2: Launch the Analyzer
```bash
python main.py
```

### Step 3: Navigate Menu
```
Main Menu will appear:
1. Analyze Gameplay Video  ← Select this first
2. View Available Characters
3. View Blitzcrank Frame Data
4. View Blitzcrank Tips
5. Exit
```

### Step 4: Analysis Workflow
```
1. Select "1" → Analyze Gameplay Video
2. Choose your video file (can use default or browse)
3. Select Player 1 character (e.g., Blitzcrank)
4. Select Player 2 character (e.g., Blitzcrank for mirror)
5. Select mode (Juggernaut or Standard)
6. Wait for analysis to complete
7. Review the analysis report
8. (Optional) Export to JSON
```

## Understanding the Report

### Video Information
- **Characters**: Shows both characters being analyzed
- **Duration**: Total video length in seconds
- **FPS**: Frames per second

### Detected Events
- **Hits**: Impact flashes detected
- **Blockstrings**: Guard states identified
- **Timestamps**: MM:SS:FF format for easy reference in video

### Player Analysis
- **Playstyle**: How they play (Aggressive, Defensive, Grab-Heavy, etc.)
- **Success Rate**: Percentage of successful moves/combos
- **Mistakes**: Total errors detected

### Mistakes Breakdown
- **🔴 Critical**: Game-changing errors (huge punish opportunities missed)
- **🟠 Major**: Significant damage loss or positioning errors
- **🟡 Minor**: Small optimizations or spacing issues

### Corrections
Each mistake shows:
- **What happened**: The move used
- **What was wrong**: Why it's a mistake
- **Better option**: Suggested correction
- **Damage Lost**: How much health was wasted

## Using the Frame Data Browser

### Option 1: Browse by Category
```
Main Menu → 3. View Blitzcrank Frame Data
→ Select category (Standing Normals, Specials, etc.)
→ See all moves in that category with data
```

### Option 2: Search for Specific Move
```
Main Menu → 3. View Blitzcrank Frame Data
→ Select "Search Move"
→ Type move name (e.g., "5H", "Rocket", "grab")
```

### Reading Frame Data
```
5L | Damage: 45 | Startup: 8f | Recovery: 12f | Block: -2f

Breaking it down:
- 5L = Standing Light punch
- Damage: 45 = How much health it removes
- Startup: 8f = Takes 8 frames to come out
- Recovery: 12f = Takes 12 frames to recover and do next action
- Block: -2f = Opponent has +2 frame advantage if they block
```

## Frame Advantage Explained

### Positive (+) = Your Turn
- Example: "+4f" means you get 4 free frames to act
- Good for continuing combos or blockstrings

### Negative (-) = Their Turn
- Example: "-7f" means opponent gets 7 free frames
- Dangerous if they can use it for combo/throw

### Safe vs Unsafe
- **Safe**: 0f or better (you at worst, neutral)
- **Unsafe**: -1f to -6f (risky but sometimes necessary)
- **Very Unsafe**: -7f or worse (can be heavily punished)

## Quick Reference: Blitzcrank Tips

### Neutral Game (Before Getting Close)
✓ Use Rocket Grab (5S1) to force opponent in - it's your "fullscreen poke"
✓ Build Steam gauge for powered-up moves
✗ Don't approach carelessly - slow dash speed is a weakness

### Close Range Game (Mix-ups)
✓ Mix between strikes (5L, 5M, 2M) and grabs (2S2)
✓ After successful grab: forward throw → hard knockdown
✗ Don't whiff grabs - huge recovery penalty

### Against Another Blitzcrank
✓ First to land grab often wins - lots of throw loops  
✓ Good spacing is critical for both players
✓ Assist choice can swing entire match
✗ Don't be too predictable with grab patterns

## Keyboard Shortcuts
- `Ctrl+C`: Exit program anytime
- `Enter`: Confirm selections and continue
- Type numbers to navigate menus

## Troubleshooting

### "Video file not found"
- Check file path is correct
- Make sure file isn't being used by another program
- Try absolute path instead of relative

### "FFmpeg not found"
- You need to install FFmpeg (see Installation above)
- Or add FFmpeg to Windows PATH

### "No events detected"
- Video might be too short or low contrast
- Try adjusting brightness in video settings
- Ensure it's actual gameplay footage

### "Analysis seems incomplete"
- This is normal - ML analysis coming in future versions
- Current version detects frame events and flashes
- Manual review of highlighted frames recommended

## Next Steps

1. **Learn Frame Data**: Spend 5 minutes in the Frame Data browser
2. **Watch Tips**: Review Blitzcrank tips section for your character
3. **Analyze Matches**: Get comfortable with the workflow
4. **Export Reports**: Save JSON reports for comparison over time

## Advanced Usage

### Command Line
```bash
# Run tests
python tests.py

# Future: Batch analysis
python main.py --batch-analyze videos/
```

### Custom Analysis
Edit `src/frame_data.py` to:
- Add more characters
- Adjust frame values based on patches
- Add new move properties

## Resources

- **2XKO Official**: https://2xko.riotgames.com/
- **2XKO Wiki**: https://wiki.play2xko.com/
- **Frame Data**: https://wiki.play2xko.com/en-us/Blitzcrank

## Tips for Best Results

1. **Clear Footage**: Use high-quality video (1080p+ recommended)
2. **Frame Timing**: Game running at 60 FPS gives most accurate analysis
3. **Full Rounds**: Analyze complete matches for best patterns
4. **Multiple Matches**: Compare trends across multiple videos
5. **Note Taking**: Have pen+paper for manual notes during review

## FAQ

**Q: Can this analyze other characters?**  
A: Yes! Blitzcrank is primary, but framework supports all 11 champions. Frame data can be added.

**Q: Does it work with streams/recordings?**  
A: Yes! Any MP4 file works. Replay data support coming later.

**Q: Can it detect combos automatically?**  
A: Current version flags combo starters and reads hitstun. Full combo detection coming.

**Q: How accurate is the analysis?**  
A: Frame events are detected reliably. ML model for move detection in development.

**Q: Can I share the reports?**  
A: Yes! JSON exports are designed for sharing with teammates.

---

**Need help?** Check README.md for more details or review the tips in-application!
