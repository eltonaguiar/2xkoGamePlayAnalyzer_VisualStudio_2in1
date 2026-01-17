# Enhanced HTML Report Generator - API Reference

## New Methods & Features

### 1. Player Position Management

```python
def set_player_position(self, player: int, position: str):
    """Set starting position for player (LEFT or RIGHT)"""
    report.set_player_position(1, "LEFT")
    report.set_player_position(2, "RIGHT")
```

**Effect:** Displays player position at start of round with appropriate styling

---

### 2. Move Usage Tracking

```python
def add_move_usage(self, player: int, move: str, damage: int, hit: bool = True):
    """Track move usage statistics for each player"""
    
    # Successful hit
    report.add_move_usage(1, "5H", damage=90, hit=True)
    
    # Whiffed move
    report.add_move_usage(1, "5S1", damage=0, hit=False)
```

**Tracks:**
- Usage count (how many times used)
- Hit count (successful connections)
- Whiff count (failed attempts)
- Total damage (cumulative)
- Average damage per hit

**Usage Example - Full Move Set:**
```python
# Track all of Player 1's moves
moves_used = {
    "5L": (45, 8, True),    # (damage, times_hit, had_whiff)
    "5M": (65, 5, True),
    "5H": (90, 3, True),
    "5S1": (80, 4, False),  # Grab with some whiffs
    "2M": (50, 6, True),
}

for move, (damage, times_hit, had_whiff) in moves_used.items():
    for _ in range(times_hit):
        report.add_move_usage(1, move, damage, hit=True)
    if had_whiff:
        report.add_move_usage(1, move, 0, hit=False)
```

---

### 3. Enhanced Mistake Recording

```python
def add_mistake(
    self, 
    player: int,                    # 1 or 2
    timestamp: str,                 # "MM:SS:FF" format
    move: str,                      # Move name
    mistake_type: str,              # Classification
    description: str,               # Detailed description
    severity: str,                  # "Critical", "Major", or "Minor"
    damage_at_time: int = 0,        # Cumulative damage before mistake
    range_note: str = "",           # "Should be CLOSER" or "Should be FURTHER"
    damage_value: int = 0           # Move damage value
):
```

**Full Example:**
```python
report.add_mistake(
    player=1,
    timestamp="00:15:23",
    move="5H",
    mistake_type="Unsafe on Block",
    description="Used 5H (-10f on block) - opponent had plenty of time to punish with a throw or fast normal",
    severity="Critical",
    damage_at_time=95,              # NEW: Damage before this happened
    range_note="Should be CLOSER - opponent was at max range",  # NEW: Range guidance
    damage_value=90                 # NEW: This move does 90 damage
)
```

**Mistake Types Available:**
- "Unsafe on Block"
- "Whiffed Grab"
- "Missed Punish"
- "Dropped Combo"
- "Poor Spacing"
- "Bad Blockstring"
- "Wrong Okizeme"
- "Recovery Punished"

**Severity Levels:**
- "Critical" - Major game-losing mistakes
- "Major" - Significant errors
- "Minor" - Minor issues or inefficiencies

**Range Notes Format:**
- "Should be CLOSER - [reason]"
- "Should be FURTHER - [reason]"
- "" (leave empty if not applicable)

---

### 4. Damage Tracking at Mistakes

```python
def set_damage_at_mistake(
    self, 
    mistake_index: int,     # Index of the mistake
    player1_damage: int,    # Damage on Player 1
    player2_damage: int     # Damage on Player 2
):
    """Set cumulative damage at the time of a mistake"""
    report.set_damage_at_mistake(0, player1_damage=95, player2_damage=40)
```

---

## Color System

### Player Colors (Built-in)

```python
PLAYER_COLORS = {
    1: {
        "primary": "#FF6B6B",      # Red
        "secondary": "#FFB3B3",    # Light red
        "dark": "#CC0000",         # Dark red
        "light": "#FFE8E8",        # Very light red
        "name": "Player 1",
        "position": "LEFT"
    },
    2: {
        "primary": "#4ECDC4",      # Teal
        "secondary": "#A0E7E5",    # Light teal
        "dark": "#0A9B8E",         # Dark teal
        "light": "#E0F7F5",        # Very light teal
        "name": "Player 2",
        "position": "RIGHT"
    }
}
```

All styling is automatically color-coded based on player:
- Mistake backgrounds
- Player badges
- Borders and accents
- Statistics displays

---

## Report Output

### Automatic Sections Generated

1. **🎬 Round Start Position**
   - Character images (customizable)
   - Player colors and positions
   - Character names

2. **Player Statistics**
   - Playstyle classification
   - Success rate (%)
   - Total mistakes
   - Throw usage (%)

3. **🎯 Key Mistakes Detected**
   - Timestamp
   - Player identification (color-coded)
   - Mistake type badge
   - Move details
   - **NEW:** Damage at time of mistake
   - **NEW:** Move damage value
   - **NEW:** Range guidance (CLOSER/FURTHER)

4. **📊 Player 1/2 - Move Variety Breakdown**
   - Move name
   - Usage count
   - Hit count (green)
   - Whiff count (red)
   - Hit rate (%)
   - Total damage
   - Average damage per hit

5. **📈 Analysis Summary**
   - Critical mistakes count
   - Major mistakes count
   - Minor issues count
   - Total events count

---

## Complete Report Generation Example

```python
from src.html_report import HTMLReportGenerator

# Create report
report = HTMLReportGenerator(
    character1="Blitzcrank",
    character2="Blitzcrank",
    mode="Juggernaut",
    video_duration=156.90
)

# Set positions
report.set_player_position(1, "LEFT")
report.set_player_position(2, "RIGHT")

# Add player stats
report.set_player_stats(
    player=1,
    playstyle="Aggressive Grappler",
    success_rate=62.5,
    mistake_count=5,
    throw_usage=35.2
)

report.set_player_stats(
    player=2,
    playstyle="Balanced Mix-up",
    success_rate=58.3,
    mistake_count=6,
    throw_usage=28.7
)

# Track moves
report.add_move_usage(1, "5L", damage=45, hit=True)
report.add_move_usage(1, "5H", damage=90, hit=True)
report.add_move_usage(1, "5S1", damage=0, hit=False)  # Whiff

# Add mistakes
report.add_mistake(
    player=1,
    timestamp="00:15:23",
    move="5H",
    mistake_type="Unsafe on Block",
    description="Move was unsafe",
    severity="Critical",
    damage_at_time=95,
    range_note="Should be CLOSER",
    damage_value=90
)

# Save report
output_file = report.save_to_file("output/analysis.html")
print(f"Report saved to: {output_file}")
```

---

## Data Structure Reference

### Move Stats Structure
```python
move_stats = {
    1: {  # Player 1
        "5H": {
            "count": 5,              # Total times used
            "total_damage": 450,     # 90 * 5 hits
            "hits": 5,               # Successful connections
            "whiffs": 0,             # Failed attempts
            "average_damage": 90.0   # 450 / 5
        },
        "5S1": {
            "count": 5,
            "total_damage": 320,
            "hits": 4,
            "whiffs": 1,
            "average_damage": 80.0
        }
    },
    2: { ... }  # Player 2 moves
}
```

### Mistake Structure
```python
mistake = {
    "player": 1,
    "player_name": "Player 1",
    "player_color": "#FF6B6B",
    "timestamp": "00:15:23",
    "move": "5H",
    "type": "Unsafe on Block",
    "description": "Detailed description...",
    "severity": "Critical",
    "damage_at_time": 95,
    "range_note": "Should be CLOSER - opponent was at max range",
    "damage_value": 90
}
```

---

## Responsive Design

The generated report automatically adapts to:
- ✅ Desktop (full width)
- ✅ Tablet (2-column layouts adjust to single column)
- ✅ Mobile (tables become scrollable, readable on small screens)

---

## File Output

```python
# Save to file
saved_path = report.save_to_file("output/my_analysis.html")

# Returns: Absolute path to saved file
# File: ~1,100 lines of styled HTML
# Size: ~100-200 KB (depending on mistake count)
```

---

## Version

**2.0 - Enhanced Report Generator**

Features:
- ✅ Round start position with character images
- ✅ Player color and position distinction
- ✅ Clear player identification for each mistake
- ✅ Damage tracking (cumulative + move damage)
- ✅ Range analysis with guidance
- ✅ Complete move variety breakdown
- ✅ Professional responsive design

