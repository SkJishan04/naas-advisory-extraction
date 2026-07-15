import re

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

MAX_CROPS = 4

BOUNDARY_STATES = [
    "West Bengal", "Jharkhand", "Bihar", "Odisha", "Chhattisgarh",
    "Uttar Pradesh", "Disclaimer", "Maharashtra", "Kerala", "Karnataka",
    "Tamil Nadu", "Andhra Pradesh", "Gujarat", "Himachal", "Jammu",
    "Punjab", "Haryana", "Uttarakhand", "Rajasthan", "Madhya Pradesh",
    "Telangana", "Arunachal", "Nagaland", "Meghalaya", "Mizoram",
    "Tripura", "Sikkim", "Goa", "Madhya Maharashtra", "Vidarbha",
    "Konkan", "Parbhani", "Marathwada",
]

_BOUNDARY_RE = "|".join(re.escape(s) for s in BOUNDARY_STATES)

# ─────────────────────────────────────────────────────────────────────────────
# Crop Detection Patterns
# ─────────────────────────────────────────────────────────────────────────────

_CROPS = [
    ("Sali Rice/Paddy",      r"\bsali\s+(?:rice|paddy)\b"),
    ("Boro Rice",            r"\bboro\s+rice\b"),
    ("Ahu Rice",             r"\bahu\s+rice\b"),
    ("Kharif Rice",          r"\bkharif\s+rice\b"),

    ("Rapeseed-Mustard",     r"\b(?:rapeseed[- ]*mustard|rapeseed|mustard|toria)\b"),
    ("Sesame/Sesamum",       r"\b(?:sesame|sesamum)\b"),

    ("Jute",                 r"\bjute\b"),
    ("Tomato",               r"\btomato(?:es)?\b"),
    ("Broccoli",             r"\bbroccoli\b"),
    ("Chilli",               r"\bchil[li]+i?\b"),
    ("Brinjal",              r"\bbrinjal\b"),
    ("Cauliflower",          r"\bcauliflower\b"),
    ("Cabbage",              r"\bcabbage\b"),
    ("Potato",               r"\bpotato(?:es)?\b"),
    ("Okra",                 r"\bokra(?:s)?\b"),
    ("Pumpkin",              r"\bpumpkin\b"),
    ("Cucumber",             r"\bcucumber\b"),
    ("Sponge/Ridge Gourd",   r"\b(?:sponge|ridge|spine|bitter)\s+gourd\b"),
    ("Onion",                r"\bonion\b"),
    ("Radish",               r"\bradish\b"),
    ("Carrot",               r"\bcarrot\b"),
    ("Ginger",               r"\bginger\b"),
    ("Turmeric",             r"\bturmeric\b"),

    ("Maize",                r"\bmaize\b"),
    ("Sugarcane",            r"\bsugarcane\b"),
    ("Green Gram",           r"\bgreen\s*gram\b"),
    ("Black Gram",           r"\bblack\s*gram\b"),
    ("Cowpea",               r"\bcowpea\b"),
    ("Pea/Lathyrus",         r"\b(?:peas?|lathyrus)\b"),
    ("Groundnut",            r"\bgroundnut\b"),

    ("Banana",               r"\bbanana\b"),
    ("Citrus",               r"\bcitrus\b"),
    ("Papaya",               r"\bpapaya\b"),
    ("Coconut",              r"\bcoconut\b"),
    ("Arecanut",             r"\barecanut\b"),
    ("Mango",                r"\bmango(?:es)?\b"),
    ("Pineapple",            r"\bpineapple\b"),
    ("Guava",                r"\bguava\b"),

    ("Fodder Grasses",       r"\b(?:napier|seteria|guinea\s+grass|para\s+grass|fodder)\b"),
    ("Livestock/Cattle",     r"\b(?:cattle|livestock|animal|shed|apiar)\b"),

    ("Paddy/Rice",           r"\b(?:paddy|rice)\b"),
    ("Vegetables",           r"\bvegetable(?:s)?\b"),
]

# ─────────────────────────────────────────────────────────────────────────────
# Output Columns
# ─────────────────────────────────────────────────────────────────────────────

CROP_COLS = [
    "Crop Name",
    "Land",
    "Stage",
    "Field Condition",
    "Field Preparation",
    "Seeds Requirement",
    "Pests/Disease",
    "Fertilizer",
    "Pesticides",
    "Precaution from",
    "Precaution tool",
    "Cause of Damage",
    "Recommendation",
    "Varieties",
    "Extra Information",
]

WEATHER_COLS = [
    "Advisory Date",
    "Rainfall Forecast Date",
    "Rainfall(Assam) mm",
    "Excess(+)/Deficit(-)",
    "Week 1",
    "W1_Assam_Forecast",
    "Week 2",
    "W2_Assam_Forecast",
    "Flood_Alert",
]

ALL_COLS = WEATHER_COLS[:]

for i in range(1, MAX_CROPS + 1):
    ALL_COLS += [f"C{i}_{c}" for c in CROP_COLS]