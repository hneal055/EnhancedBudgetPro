import re
from collections import Counter

# Expanded exclusion list for non-characters (locations, vehicles, generic set elements)
EXCLUSION_TERMS = {
    # Locations/Rooms
    "BATHROOM", "BEDROOM", "CORRIDOR", "KITCHEN", "LOBBY", "ROOM", "HALLWAY", "OFFICE",
    "GARAGE", "GARDEN", "BALCONY", "STAIRCASE", "DINING ROOM", "LIVING ROOM", "STREET",
    "PARK", "ROOF", "BASEMENT", "ATTIC", "YARD", "STUDIO", "LAB", "APARTMENT", "CLUB",
    "BAR", "STATION", "CAR", "BUS", "STOP", "STAIRWELL", "DOORWAY", "BOOTH", "CONVERTIBLE",
    "AREA", "TUNNEL", "WALKWAY", "BUILDING", "LOUNGE", "SUITE", "ELEVATOR", "LIGHT", "BRIDGE",
    "PLATFORM", "TRACK", "CROSSWALK", "ALLEY", "SHED", "SHACK", "CABIN", "CAMP", "CAVE",
    "CHAPEL", "CHURCH", "COTTAGE", "COURT", "DECK", "DOCK", "DORM", "DRIVEWAY", "FOYER",
    "GATE", "HUT", "INN", "JAIL", "KIOSK", "LAUNDRY", "LIBRARY", "MARKET", "MOTEL", "MUSEUM",
    "PALACE", "PATIO", "PAVILION", "PORCH", "PRISON", "RANCH", "RESTAURANT", "SALON", "SHOWER",
    "SHRINE", "STORE", "TAVERN", "TERRACE", "TOWER", "VAULT", "WAREHOUSE", "WORKSHOP", "ZOO",
    # Vehicles/Objects
    "CADILLAC", "STATION WAGON", "POLAROID", "CONVERTIBLE", "CADDY", "CAR", "BUS", "VAN",
    "TRUCK", "TAXI", "CAB", "LIMO", "JEEP", "SUV", "AMBULANCE", "FIRE TRUCK", "HELICOPTER",
    "PLANE", "AIRPLANE", "JET", "BOAT", "SHIP", "FERRY", "SUBWAY", "TRAIN", "TRAM", "TROLLEY",
    "BIKE", "BICYCLE", "MOTORCYCLE", "SCOOTER", "SKATEBOARD", "SEGWAY",
    # Generic/Other
    "END", "DAY", "NIGHT", "MORNING", "EVENING", "LATER", "TRANSITION", "VOCAL", "SUPER",
    "CUT TO", "FADE IN", "FADE OUT", "DISSOLVE TO", "V.O.", "O.S.", "CONT’D", "CONT'D"
}

# Suffixes that indicate non-characters
EXCLUSION_SUFFIXES = (
    "ROOM", "BATHROOM", "BEDROOM", "CORRIDOR", "APARTMENT", "LOBBY", "CLUB", "BAR", "STATION",
    "CAR", "BUS", "STOP", "STAIRWELL", "GARAGE", "YARD", "ROOF", "PARK", "OFFICE", "KITCHEN",
    "DINING ROOM", "HALLWAY", "DOORWAY", "BOOTH", "CONVERTIBLE", "AREA", "TUNNEL", "WALKWAY",
    "BUILDING", "BASEMENT", "ATTIC", "STUDIO", "LAB", "SUITE", "ELEVATOR", "PLATFORM", "TRACK",
    "ALLEY", "SHED", "SHACK", "CABIN", "CAMP", "CAVE", "CHAPEL", "CHURCH", "COTTAGE", "COURT",
    "DECK", "DOCK", "DORM", "DRIVEWAY", "FOYER", "GATE", "HUT", "INN", "JAIL", "KIOSK",
    "LAUNDRY", "LIBRARY", "MARKET", "MOTEL", "MUSEUM", "PALACE", "PATIO", "PAVILION", "PORCH",
    "PRISON", "RANCH", "RESTAURANT", "SALON", "SHOWER", "SHRINE", "STORE", "TAVERN", "TERRACE",
    "TOWER", "VAULT", "WAREHOUSE", "WORKSHOP", "ZOO", "END", "DAY", "NIGHT", "MORNING",
    "EVENING", "LATER", "TRANSITION", "VOCAL"
)

BASIC_EXCLUSION_TERMS = {
    "INT", "EXT", "DAY", "NIGHT", "MORNING", "EVENING", "LATER",
    "CUT TO", "FADE IN", "FADE OUT", "DISSOLVE TO", "V.O.", "O.S.",
    "CONT’D", "CONT'D", "SUPER", "TRANSITION", "END"
}
BASIC_EXCLUSION_SUFFIXES = ("ROOM", "BATHROOM", "STREET", "CORRIDOR", "APARTMENT", "LOBBY")

def is_valid_character(name):
    name_clean = name.strip(".:()").upper()
    # Exclude if in exclusion terms
    if name_clean in EXCLUSION_TERMS:
        return False
    # Exclude if ends with any exclusion suffix
    if any(name_clean.endswith(suffix) for suffix in EXCLUSION_SUFFIXES):
        return False
    # Exclude if contains "DAILY RATE" or similar
    if re.search(r"\bDAILY RATE\b", name_clean):
        return False
    # Exclude if contains common location/set words
    if any(term in name_clean for term in EXCLUSION_TERMS):
        return False
    # Must be all uppercase, not too short/long, not a scene heading
    if not name.isupper() or len(name) < 2 or len(name) > 30:
        return False
    if re.match(r"^(INT|EXT)[ .]", name):
        return False
    if re.match(r"^[A-Z]+ TO$", name):
        return False
    # Accept if all uppercase and not a number
    if re.match(r"^[A-Z '’.-]+$", name_clean) and not any(char.isdigit() for char in name_clean):
        return True
    return False

def is_likely_character(name):
    name_clean = name.strip(".:()").upper()
    if name_clean in BASIC_EXCLUSION_TERMS:
        return False
    if any(name_clean.endswith(suffix) for suffix in BASIC_EXCLUSION_SUFFIXES):
        return False
    if not name.isupper() or len(name) < 2 or len(name) > 30:
        return False
    if re.match(r"^(INT|EXT)[ .]", name):
        return False
    return True

def filter_characters(candidate_names, min_occurrences=2):
    counts = Counter(candidate_names)
    filtered = [
        name for name, count in counts.items()
        if is_valid_character(name) and count >= min_occurrences
    ]
    return filtered

def filter_characters(candidate_names):
    return [name for name in candidate_names if is_likely_character(name)]

# Example Character Intelligence Engine (simplified)
class CharacterIntelligenceEngine:
    def analyze(self, parsed_script):
        """
        parsed_script: dict with at least a 'characters' key (list of all detected character names)
        Returns: dict with filtered character stats
        """
        # Filter character names
        candidate_names = parsed_script.get("characters", [])
        filtered_names = filter_characters(candidate_names)

        # Build stats only for filtered characters
        character_stats = {}
        for name in filtered_names:
            # Example: count scenes, dialogue lines, etc.
            character_stats[name] = {
                "scenes": 0,  # Fill with your logic
                "dialogue_lines": 0,  # Fill with your logic
                "estimated_screen_time_min": 0.0  # Fill with your logic
            }
        # ... (populate stats as needed)
        return {"character_stats": character_stats}

# If you want to use is_valid_character in your UI code:
# from src.AnalysisEngine.character_intelligence import is_valid_character