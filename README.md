# 2XKO Gameplay Analyzer

A comprehensive fighting game analysis tool for 2XKO (2v2 Fighting Game). Analyzes player gameplay footage and provides detailed feedback on mistakes, frame data awareness, playstyle assessment, and character-specific optimization tips.

## Features

### Core Analysis
- **Video Frame Analysis**: Processes MP4 gameplay footage and detects game events
- **Move Detection**: Identifies character moves and actions from video
- **Mistake Detection**: Finds unsafe moves on block, whiffed grabs, missed punishes, and more
- **Frame Data Integration**: Complete Blitzcrank frame data with analysis
- **Playstyle Assessment**: Determines player playstyle from move usage patterns

### Matchup Support
- **Mirror Matchups**: Specialized analysis for same-character vs same-character fights
- **Character Database**: Frame data for 2XKO champions (Blitzcrank focused)
- **Game Modes**: Support for Juggernaut and Standard modes

### Player Insights
- **Pros & Cons**: Identifies player strengths and weaknesses
- **Timestamps**: All mistakes and key moments timestamped for easy reference
- **Recommendations**: Character-specific tips and better move suggestions
- **Damage Analysis**: Tracks missed damage opportunities

## Installation

### Prerequisites
- Python 3.8+
- FFmpeg (for video processing)

### Setup

1. Clone or extract the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg:
   - **Windows**: `choco install ffmpeg` or download from https://ffmpeg.org/download.html
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

## Usage

### Running the Application

```bash
python main.py
```

This launches an interactive menu with options to:

1. **Analyze Gameplay Video** - Upload/select an MP4 file for analysis
2. **View Characters** - See available 2XKO characters
3. **View Frame Data** - Browse Blitzcrank's complete frame data
4. **View Tips** - Get character-specific strategy and matchup tips
5. **Exit** - Close the application

### Workflow Example

```
1. Start Application
   └─ Run: python main.py

2. Select "Analyze Gameplay Video"
   ├─ Choose video file (e.g., Blitzcrank vs Blitzcrank footage)
   ├─ Select Player 1 character (usually same as Player 2 for mirror)
   ├─ Select Player 2 character
   └─ Select game mode (Juggernaut/Standard)

3. View Analysis Report
   ├─ Detected events with timestamps
   ├─ Player 1 & 2 statistics
   ├─ Mistakes found with corrections
   ├─ Playstyle assessment
   └─ Character-specific tips

4. Export Results (Optional)
   └─ Save JSON report for documentation
```

## Blitzcrank Analysis Features

### Frame Data Available
- **Standing Normals**: 5L, 5M, 5H (including charged)
- **Crouching Normals**: 2L, 2M, 2H
- **Jumping Normals**: jL, jM, jH, j2H
- **Unique Moves**: 3L (Prod), 66H, 4H
- **Command Grabs**: 5MH, 4MH, jMH
- **Specials**: 
  - Rocket Grab line (5S1, air version, follow-ups)
  - Air Purifier (2S1, air version)
  - Rocket Punch (5S2)
  - Spinning Turbine/Prompt Disposal (6S2/2S2)
  - Garbage Collection (2S2, air version)
  - Wrecking Ball (jS2)
- **Supers**: Helping Hand (S1), Static Field (S2)
- **Ultimate**: Trash Compactor
- **Assists**: All 3 assist options

### Key Metrics Tracked
- Startup frames (how fast move comes out)
- Active frames (how many frames attack lasts)
- Recovery frames (how long until next action)
- On-block advantage/disadvantage
- Guard types (Low, High, Air, Universal)
- Cancellable moves
- Hit reactions

### Analysis Examples
- **Unsafe Detection**: Flags moves that are -7 or worse on block
- **Safe Spacing**: Identifies whiffed grabs and spacing errors
- **Combo Extensions**: Suggests better follow-ups
- **Tech Chase**: Evaluates okizeme and knockdown situations
- **Steam Management**: Tips for charging and using empowered moves

### Mirror Matchup Tips
- Grab range and spacing importance
- Mix-up timing between strikes and grabs
- Steam meter management
- Assist coverage critical for advantage
- Tech-chase heavy sequences
- When to be patient vs aggressive

## Frame Data Format

Each move includes:
```
Move Name (e.g., "5L")
├─ Damage: Hit damage (1 = grab, dummy value)
├─ Startup: Frames before move hits
├─ Active: Frames the attack lasts
├─ Recovery: Frames before next action
├─ On-Block: Frame advantage/disadvantage on block
├─ Guard Type: What guard blocks it (L/H/A/U)
├─ Description: Move properties and usage notes
└─ Special Properties: Invulnerability, cancels, special conditions
```

## Mistake Types Detected

1. **UNSAFE_MOVE_ON_BLOCK** - Used unsafe move and opponent blocked
2. **MISSED_PUNISH** - Could have punished opponent's unsafe move but didn't
3. **WHIFFED_GRAB** - Grab attempt outside of range
4. **POOR_SPACING** - Used move at wrong distance
5. **DROPPED_COMBO** - Failed to continue combo
6. **RECOVERY_PUNISHED** - Recovery from move was punished
7. **BAD_BLOCKSTRING** - Broke blockstring allowing escape
8. **WRONG_OKIZEME** - Poor choice after knockdown

## Playstyle Categories

- **Aggressive Grappler**: High grab usage (40%+), risky approaches
- **Grab-Heavy**: Focused on mix-ups between strikes and grabs (20-40%)
- **Balanced Mix-up**: Equal distribution of strikes and grabs
- **Strike-Focused**: Prefers normals and spacing (low grab usage)
- **Special-Focused**: Heavy reliance on special moves and combos

## Output

### Console Report
- Video metadata (duration, FPS)
- Player statistics (success rate, playstyle, mistakes)
- Detailed mistake list with timestamps
- Character-specific recommendations
- Combo suggestions

### JSON Export (Optional)
```json
{
  "player1": {
    "character": "Blitzcrank",
    "playstyle": "Aggressive Grappler",
    "success_rate": 62.5,
    "mistakes": 8
  },
  "total_mistakes": 12,
  "critical_mistakes": 2,
  "recommendations": {...}
}
```

## Project Structure

```
2xkoGPAnalyzer/
├── main.py                 # Entry point and CLI
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── frame_data.py      # Blitzcrank frame data database
│   ├── video_analyzer.py  # Video processing engine
│   └── analysis_engine.py # Gameplay analysis logic
├── data/                  # Frame data and config files (expandable)
├── output/                # Analysis reports and exports
└── tests/                 # Unit tests (optional)
```

## Current Limitations & Future Work

### Current
- Video analysis currently detects frame-level events (hits, flashes)
- Frame-by-frame manual analysis possible with extracted frames
- Character database focused on Blitzcrank (others can be added)

### Future Enhancements
- **Machine Learning**: Train model on move patterns for automatic detection
- **Character Expansion**: Add frame data for all 11 champions
- **Advanced Metrics**: Damage scaling, reset timing, priority systems
- **Assist Synergy**: Dedicated assist-specific analysis
- **Web Interface**: Browser-based analyzer
- **Real-time Analysis**: Live streaming support
- **Replay Integration**: Connect to 2XKO replay files directly
- **Tournament Stats**: Compare against professional players

## Blitzcrank Strategy Notes

### Neutral Game
- Rocket Grab (5S1) is your main neutral tool - near-fullscreen range
- Use grab to force opponent in, then mixup with strikes vs command grab
- Build Steam gauge (10% movement speed buff at full) with successful grabs
- 2H is your anti-air but risky (-16f on block) - rely on good spacing

### Mix-up Game
- Once close: Loop 2M (catches fuzzy jumps), throws, and 2S2 (command grab)
- After successful grab: Forward throw for hard knockdown, back throw for bounce
- Use 5H/5H charged to beat opponent normals
- Rocket Grab on block is +4f - gives you turn advantage

### Steam System
- Rocket Grab line (5S1, 2S1, jS1) generates Steam
- Empowered versions are multi-hit with shock state (better combo potential)
- 6S2 (Spinning Turbine) also charges Steam while repositioning
- Spinning Turbine into 2S2 (Prompt Disposal) is strong pressure/mixup tool

### Okizeme (Oki)
- Forward throw → 66H, assist, or tech-chase 2M mix
- Back throw → Ground bounce for aerial combo continuation
- Hard Knockdown situations vulnerable to tech-chase loops
- Watch out for assist okizeme - proper defense critical

### Mirror Matchup Notes
- Both characters want close range - patience is key
- First successful grab often swings momentum (lots of throw loops)
- Tech-chase heavy - be good at 2M loops and throw spacing
- Assist choice becomes critical - good assist can win matchup
- Steam management key - charge at right times, don't waste empowered moves

## Documentation

- **Frame Data**: See `src/frame_data.py` for complete move list
- **Video Analysis**: See `src/video_analyzer.py` for detection methods
- **Analysis Logic**: See `src/analysis_engine.py` for mistake detection

## Contributing

To add support for other characters:
1. Research character frame data from wiki.play2xko.com
2. Add character dictionary to `src/frame_data.py`
3. Update character list in `main.py`
4. Test analysis with sample footage

## Resources

- **2XKO Wiki**: https://wiki.play2xko.com/en-us/
- **Official Game**: https://2xko.riotgames.com/
- **Community**: Discord & fighting game communities

## License

This tool is created for educational and personal analysis purposes.

## Support

For issues or feature requests:
1. Check README and in-app tips first
2. Review frame data notes in code comments
3. Test with different video files/matches

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Focus Character**: Blitzcrank (Juggernaut Mode)
