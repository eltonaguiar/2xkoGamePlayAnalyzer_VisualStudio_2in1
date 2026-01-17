"""
2XKO Frame Data Database
Contains all character move data for analysis
"""

BLITZCRANK_FRAME_DATA = {
    # Standing Normals
    "5L": {
        "damage": 45,
        "startup": 8,
        "active": 5,
        "recovery": 12,
        "on_block": -2,
        "guardType": ["L", "H", "A"],
        "cancel": ["N", "SP", "SU"],
        "description": "Standard light strike"
    },
    "5M": {
        "damage": 65,
        "startup": 11,
        "active": 5,
        "recovery": 18,
        "on_block": -5,
        "guardType": ["L", "H", "A"],
        "cancel": ["N", "SP", "SU"],
        "description": "Forward advancing medium",
        "properties": ["forward_moving"]
    },
    "5H": {
        "damage": 90,
        "startup": 16,
        "active": 4,
        "recovery": 31,
        "on_block": -10,
        "guardType": ["L", "H", "A"],
        "cancel": ["N", "SP", "SU"],
        "description": "Can be charged for ground bounce",
        "hitReaction": "Ground Bounce"
    },
    "5H_charged": {
        "damage": 110,
        "startup": 28,  # Charge frames
        "active": 4,
        "recovery": 31,
        "on_block": -9,
        "guardType": ["L", "H", "A"],
        "cancel": ["N", "SP", "SU", "D"],
        "description": "Charged version with dash cancel",
        "properties": ["dash_cancel_on_hit", "dash_cancel_on_block"]
    },
    
    # Crouching Normals
    "2L": {
        "damage": 45,
        "startup": 9,
        "active": 4,
        "recovery": 12,
        "on_block": -3,
        "guardType": ["L"],
        "cancel": ["N", "SP", "SU"],
        "description": "Fastest low"
    },
    "2M": {
        "damage": 50,  # First hit
        "startup": 11,
        "active": 11,
        "recovery": 20,
        "on_block": -5,
        "guardType": ["L"],
        "cancel": ["N", "SP", "SU", "!J"],
        "description": "Multi-hit launcher, catches fuzzy jumps",
        "hits": 2,
        "vacuum": True
    },
    "2H": {
        "damage": 90,
        "startup": 13,
        "active": 4,
        "recovery": 33,
        "on_block": -16,
        "guardType": ["L", "H", "A"],
        "cancel": ["N", "SP", "SU", "!J"],
        "invulnerable": "Air 17",
        "description": "Main anti-air launcher",
        "hitReaction": "Air Tailspin (on Counter Hit)"
    },
    
    # Jumping Normals
    "jL": {
        "damage": 45,
        "startup": 7,
        "active": 12,
        "recovery": 17,
        "on_block": -15,  # vs grounded, -15 to +12
        "guardType": ["H"],
        "cancel": ["N", "SP", "SU"],
        "description": "Second fastest air option"
    },
    "jM": {
        "damage": 65,
        "startup": 9,
        "active": 7,
        "recovery": 24,
        "on_block": -15,  # vs grounded, -15 to +15
        "guardType": ["H"],
        "cancel": ["N", "SP", "SU"],
        "description": "Good combo filler"
    },
    "jH": {
        "damage": 90,
        "startup": 14,
        "active": 3,
        "recovery": 23,
        "on_block": -5,  # vs grounded, -5 to +19
        "guardType": ["H"],
        "cancel": ["N", "SP", "SU"],
        "description": "Can be charged",
        "hitReaction": "Wall Bounce (if charged)"
    },
    "j2H": {
        "damage": 90,
        "startup": 17,
        "active": 7,
        "recovery": 18,
        "on_block": -2,  # vs grounded, -2 to +15
        "guardType": ["H"],
        "cancel": ["SP", "SU"],
        "description": "Crossup belly flop",
        "properties": ["can_crossup"]
    },
    
    # Unique Moves
    "3L": {  # Prod
        "damage": 50,
        "startup": 9,
        "active": 4,
        "recovery": 12,
        "on_block": -1,
        "guardType": ["L"],
        "cancel": ["N", "SP", "SU"],
        "description": "Low normal, no chain to itself"
    },
    "66H": {  # Rear Compression
        "damage": 90,
        "startup": 18,
        "active": 3,
        "recovery": 29,
        "on_block": -9,
        "guardType": ["L", "H", "A"],
        "cancel": ["SP", "SU"],
        "description": "Running strike, hits OTG",
        "properties": ["low_crush", "hits_OTG"],
        "hitReaction": "Air Tailspin (on Counter Hit)"
    },
    "4H": {  # Uplift
        "damage": 90,
        "startup": 15,
        "active": 3,
        "recovery": 28,
        "on_block": -10,
        "guardType": ["L", "H", "A"],
        "cancel": ["SP", "SU", "!J"],
        "invulnerable": "Air 18",
        "description": "Vertical launcher, anti-air vs crossups"
    },
    
    # Throws
    "5MH": {  # Forward Throw
        "damage": 190,
        "startup": 6,
        "active": 5,
        "recovery": 36,
        "guardType": ["U"],
        "description": "Puts opponent in Hard Knockdown",
        "hits": 3,  # Three punches + steam burst
        "knockdown": "Hard"
    },
    "4MH": {  # Back Throw
        "damage": 210,
        "startup": 6,
        "active": 5,
        "recovery": 36,
        "guardType": ["U"],
        "description": "Ground Bounce",
        "knockdown": "Hard",
        "hitReaction": "Ground Bounce"
    },
    "jMH": {  # Air Throw
        "damage": 210,
        "startup": 4,
        "active": 2,
        "recovery": 0,  # Until landing
        "guardType": ["U"],
        "description": "Can throw backwards with 4MH",
        "knockdown": "Hard"
    },
    
    # Tag Launcher
    "2T": {
        "damage": 80,
        "startup": 14,
        "active": 3,
        "recovery": 29,
        "on_block": -5,
        "guardType": ["L", "H", "A"],
        "description": "Launches for assist combo"
    },
    
    # Specials - Rocket Grab line
    "5S1": {  # Rocket Grab
        "damage": 1,  # Grab, pulls on hit or block
        "startup": 25,
        "active": 23,
        "recovery": 30,
        "on_block": 4,
        "guardType": ["L", "H"],
        "cancel": ["F", "SU"],
        "description": "Near-fullscreen hit grab",
        "range": "Fullscreen",
        "properties": ["long_range", "can_be_punished"]
    },
    "5S1_steam": {  # Rocket Grab Empowered
        "damage": 121,
        "startup": 20,
        "active": 23,
        "recovery": 44,
        "on_block": 6,
        "guardType": ["L", "H"],
        "cancel": ["SU"],
        "description": "Steam version - multi hit with shock",
        "hits": 2,
        "hitReaction": "Shock State",
        "properties": ["destroys_projectiles"]
    },
    "5S1S1": {  # Power Fist (follow-up)
        "damage": 120,
        "startup": 16,
        "active": 3,
        "recovery": 19,
        "cancel": ["SU"],
        "description": "Uppercut follow-up after Rocket Grab"
    },
    
    # Specials - Air Purifier line
    "2S1": {  # Air Purifier
        "damage": 1,  # Grab
        "startup": 20,
        "active": 11,
        "recovery": 43,
        "on_block": 5,
        "guardType": ["A"],
        "cancel": ["F", "SU"],
        "description": "Anti-air grab",
        "properties": ["airborne_only"]
    },
    "2S1_steam": {  # Air Purifier Empowered
        "damage": 121,
        "startup": 19,
        "active": 12,
        "recovery": 43,
        "on_block": 6,
        "guardType": ["A"],
        "cancel": ["SU"],
        "description": "Steam version",
        "hits": 2,
        "hitReaction": "Shock State"
    },
    "2S1S1": {  # Waste Disposal (follow-up)
        "damage": 130,
        "startup": 11,
        "active": 4,
        "recovery": 22,
        "cancel": ["SU"],
        "description": "Ground bounce follow-up",
        "hitReaction": "Ground Bounce"
    },
    "jS1": {  # Rocket Grab (Air)
        "damage": 176,
        "startup": 14,
        "active": 14,
        "recovery": 12,  # after landing
        "on_block": 0,  # 0 to +10
        "guardType": ["A"],
        "cancel": ["SU"],
        "description": "7-hit multi hit drill",
        "hits": 7
    },
    "jS1_steam": {  # Rocket Grab Air Empowered
        "damage": 109,
        "startup": 14,
        "active": 14,
        "recovery": 12,
        "on_block": 0,
        "guardType": ["L", "H", "A"],
        "cancel": ["SU"],
        "description": "Steam version",
        "properties": ["destroys_projectiles"]
    },
    
    # Specials - Rocket Punch
    "5S2": {  # Rocket Punch
        "damage": 120,
        "startup": 21,
        "active": 13,
        "recovery": 25,
        "on_block": -15,
        "guardType": ["L", "H", "A"],
        "cancel": ["SP", "SU"],
        "description": "Long range punching strike",
        "properties": ["destroys_projectiles", "can_wallbounce_on_air"]
    },
    
    # Specials - Spinning Turbine line
    "6S2": {  # Spinning Turbine
        "damage": 140,
        "startup": 24,
        "active": 14,
        "recovery": 19,
        "on_block": -12,
        "guardType": ["L", "H", "A"],
        "cancel": ["F", "SU"],
        "description": "Forward translating spinning strike",
        "properties": ["hits_both_sides", "charges_steam"]
    },
    "6S2_2S2": {  # Prompt Disposal (follow-up)
        "damage": 250,
        "startup": 6,  # After Spinning Turbine
        "active": 8,
        "recovery": 58,
        "guardType": ["U"],
        "cancel": ["N"],
        "description": "Command grab retaining forward momentum",
        "properties": ["kara_cancel_window_8f"]
    },
    "6S2_2S2_steam": {  # Prompt Disposal Empowered
        "damage": 300,
        "startup": 6,
        "active": 8,
        "recovery": 58,
        "guardType": ["U"],
        "cancel": ["N"],
        "description": "Empowered version with armor",
        "armor": "1 hit",
        "armor_startup": 4
    },
    
    # Specials - Garbage Collection
    "2S2": {  # Garbage Collection
        "damage": 250,
        "startup": 6,
        "active": 8,
        "recovery": 57,
        "guardType": ["U"],
        "cancel": ["SU"],
        "description": "Close range command grab",
        "properties": ["charges_steam_on_grab_outside_combo"]
    },
    "2S2_hold": {  # Garbage Collection Running
        "damage": 250,
        "startup": 6,
        "active": 66,
        "recovery": 58,
        "guardType": ["U"],
        "cancel": ["SU"],
        "description": "Running bear grab"
    },
    "2S2_steam": {  # Garbage Collection Empowered
        "damage": 300,
        "startup": 6,
        "active": 8,
        "recovery": 57,
        "guardType": ["U"],
        "armor": "1 hit",
        "armor_startup": 4,
        "description": "Empowered with super armor"
    },
    "jS2": {  # Wrecking Ball
        "damage": 157,
        "startup": 20,
        "active": 0,  # Variable
        "recovery": 10,  # After landing
        "on_block": -11,  # -11 to +6
        "guardType": ["L", "H", "A"],
        "cancel": ["SU"],
        "description": "Can swing up to 3 times when held",
        "properties": ["charges_steam", "can_crossup"]
    },
    "j2S2": {  # Garbage Collection (Air)
        "damage": 250,
        "startup": 6,
        "active": 2,
        "recovery": 22,  # After landing
        "guardType": ["U"],
        "cancel": ["SU"],
        "description": "Air version"
    },
    
    # Supers
    "Super1": {  # Helping Hand
        "damage": 260,
        "startup": 15,
        "active": 3,
        "recovery": 45,
        "on_block": -27,
        "guardType": ["L", "H", "A"],
        "description": "Charges steam on activation and on hit",
        "hitReaction": "Ground Bounce"
    },
    "Super2": {  # Static Field
        "damage": 255,
        "startup": 20,
        "active": 0,  # Variable
        "recovery": 84,
        "on_block": -54,
        "guardType": ["L", "H", "A"],
        "description": "Giant electrical field"
    },
    "Super2_empowered": {
        "damage": 351,
        "startup": 20,
        "active": 0,
        "recovery": 94,
        "on_block": -59,
        "guardType": ["L", "H", "A"],
        "description": "Empowered with extra hits"
    },
    
    # Ultimate
    "Ultimate": {  # Trash Compactor
        "damage": 520,
        "startup": 6,
        "active": 7,
        "recovery": 47,
        "guardType": ["U"],
        "invulnerable": "All 1",
        "description": "Command grab with invincible startup"
    },
    
    # Assists
    "5T": {  # Rocket Grab Assist
        "damage": 1,
        "startup": 29,
        "active": 23,
        "recovery": 76,
        "on_block": 44,
        "guardType": ["L", "H", "A"],
        "description": "Pulls point opponent on hit or block"
    },
    "4T": {  # Air Purifier Assist
        "damage": 1,
        "startup": 23,
        "active": 11,
        "recovery": 119,
        "on_block": 44,
        "guardType": ["L", "H", "A"],
        "description": "Diagonal grab for airborne opponent"
    },
    "2T": {  # Static Field Assist
        "damage": 205,
        "startup": 96,
        "active": 0,  # Variable
        "recovery": 76,
        "on_block": 47,
        "guardType": ["L", "H", "A"],
        "description": "Can only activate when KO'd"
    },
}

# General frame data constants
FRAME_DATA_CONSTANTS = {
    "JUMPSQUAT": 4,  # Frames to jump
    "DASHFORWARD_STARTUP": 4,
    "DASHBACK_STARTUP": 4,
    "BLOCKSTUN_MULTIPLIER": 1.0,  # Can vary
    "HITSTUN_MULTIPLIER": 1.0,  # Can vary
}

# Game mechanics
MECHANICS = {
    "steam_system": {
        "description": "Blitzcrank's unique mechanic",
        "charges": ["5S1", "6S2", "jS2", "Super1"],
        "full_bar_benefits": "10% movement speed buff, enhanced specials",
        "drain_rate": "Gradual over time"
    },
    "juggernaut_mode": {
        "description": "Juggernaut fuse replaces Tag Launcher",
        "replaces": "2T (Tag Launcher)",
        "with": "Eject - forces opponent to switch character"
    }
}


def get_frame_data(move_name):
    """Get frame data for a specific move"""
    return BLITZCRANK_FRAME_DATA.get(move_name, None)


def is_safe_on_block(move_name):
    """Check if a move is safe on block"""
    data = get_frame_data(move_name)
    if data and "on_block" in data:
        return data["on_block"] >= 0
    return False


def get_block_advantage(move_name):
    """Get frame advantage/disadvantage on block"""
    data = get_frame_data(move_name)
    if data and "on_block" in data:
        advantage = data["on_block"]
        if advantage >= 0:
            return f"+{advantage}f (advantage)"
        return f"{advantage}f (disadvantage)"
    return "Unknown"


def is_combo_starter(move_name):
    """Check if move can start combos"""
    data = get_frame_data(move_name)
    if not data:
        return False
    
    combo_starters = ["2M", "2H", "5H", "5H_charged", "66H", "4H", "jS1", "jS1_steam"]
    return move_name in combo_starters or data.get("hitReaction") in ["Ground Bounce", "Air Tailspin"]


def get_move_category(move_name):
    """Categorize move type"""
    if "S1" in move_name or "5S1" in move_name or "2S1" in move_name:
        return "grab"
    elif "S2" in move_name:
        return "special"
    elif "Super" in move_name:
        return "super"
    elif "Ultimate" in move_name:
        return "ultimate"
    elif move_name[0].isdigit() or move_name.startswith("j"):
        return "normal"
    return "unknown"
