import re

from .crop_detector import detect_crop


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

def _first(text, patterns, flags=re.IGNORECASE):
    """
    Return first capturing group or full match.
    """

    for p in patterns:
        m = re.search(p, text, flags)
        if m:
            return (m.group(1) if m.lastindex else m.group(0)).strip()

    return ""


def _all_unique(text, pattern, flags=re.IGNORECASE):
    """
    Return unique regex matches.
    """

    return ", ".join(
        sorted(
            set(
                m.strip().lower()
                for m in re.findall(pattern, text, flags)
            )
        )
    )


# ─────────────────────────────────────────────────────────────────────────────
# Stage
# ─────────────────────────────────────────────────────────────────────────────

def col_stage(t):

    return _all_unique(
        t,
        r'\b(sowing|nursery|transplanting|vegetative|flowering|'
        r'early\s+flowering|fruiting|harvesting|seedling|tillering|'
        r'germinating|planting|milk\s+stage|grain\s+filling|'
        r'panicle\s+initiation|PI\s+stage|grand\s+growth|'
        r'fruiting\s+and\s+harvesting|'
        r'post\s+harvest(?:ing)?|relay\s+cropping|maturity|retting)\b'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Field Condition
# ─────────────────────────────────────────────────────────────────────────────

def col_field_condition(t):

    return _all_unique(
        t,
        r'\b(water[\s-]*logg?ing|water\s+stagnation|wapsa|'
        r'excess\s+(?:rain)?water|flood(?:ed)?|submerged|'
        r'moist(?:ure)?|cracking\s+appears?\s+in\s+soil|'
        r'upland|low\s*land|dry\s+weather|standing\s+water)\b'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Field Preparation
# ─────────────────────────────────────────────────────────────────────────────

def col_field_prep(t):

    return _first(
        t,
        [

            r'((?:land\s+preparation|ploughing|bunding|mulching|'
            r'earthing\s+up|gap\s+filling|raised\s+bed|'
            r'ridge\s*[&]?\s*furrow|'
            r'drain(?:age)?\s+channel)[^\.\n]{0,120})',

            r'(drain\s+out\s+(?:excess\s+)?(?:rain)?water[^\.\n]{0,80})',

            r'(cover\s+the\s+seeded\s+area\s+with[^\.\n]{0,80})',

            r'(field\s+ditch(?:es)?[^\.\n]{0,80})',
        ]
    )


# ─────────────────────────────────────────────────────────────────────────────
# Seed Requirement
# ─────────────────────────────────────────────────────────────────────────────

def col_seeds(t):

    return _first(
        t,
        [

            r'([\d.]+(?:\s*[-–]\s*[\d.]+)?\s*(?:g(?:ram)?|kg)\s*/\s*bigha[^\.\n]{0,60})',

            r'(seed\s+rate[^\.\n]{0,100})',

            r'(\d+[-–]?\d*\s*kg/ha\s+seed[^\.\n]{0,60})',

            r'(@\s*\d+[-–]?\d*\s*(?:g|kg)\s*(?:for|per)[^\.\n]{0,60})',

            r'([\d.]+\s*(?:g|kg)\s+(?:of\s+)?seeds?\s+(?:are\s+)?required[^\.\n]{0,60})',

        ]
    )

# ─────────────────────────────────────────────────────────────────────────────
# Pests / Disease
# ─────────────────────────────────────────────────────────────────────────────

def col_pests(t):

    return _all_unique(
        t,
        r'\b(aphid|borer|stem\s+borer|rice\s+borer|leaf\s+folder|caseworm|'
        r'rice\s+hispa|gall\s+midge|thrips|whitefly|white\s*fly|'
        r'Epilachna\s+beetle|red\s+pumpkin\s+beetle|black\s+pumpkin\s+beetle|'
        r'fruit\s*fly|mealy\s*bug|termite|hopper|nematode|'
        r'late\s+blight|blight|blast|Ganoderma|fungal\s+wilt|'
        r'rhizome\s+rot|anthracnose|anthacnose|fruit\s+rot|'
        r'sigatoka|downy\s+mildew|mosaic|wilt|rot|rust)\b'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Fertilizer
# ─────────────────────────────────────────────────────────────────────────────

def col_fertilizer(t):

    return _first(
        t,
        [

            r'((?:\d+\s+to\s+\d+|\d+)\s*quintals?\s+of\s+(?:compost|FYM)[^\.\n]{0,150})',

            r'((?:apply|application\s+of)\s+\d+\s*quintals?\s+of\s+(?:FYM|compost)[^\.\n]{0,100})',

            r'(\d+(?:\.\d+)?\s*kg\s+(?:Urea|SSP|MOP|DAP|NPK|Borax|FYM|compost)\b[^\.\n]{0,100})',

            r'(?:apply|application\s+of)\s+([^\.\n]{0,80}'
            r'(?:FYM|compost|urea|Urea|NPK|DAP|MOP|SSP|Borax|vermicompost)[^\.\n]{0,60})',

            r'(\d+:\d+:\d+\s*kg/ha\s*(?:\([^)]*\))?[^\.\n]{0,80})',

        ]
    )


# ─────────────────────────────────────────────────────────────────────────────
# Pesticides
# ─────────────────────────────────────────────────────────────────────────────

def col_pesticides(t):

    return _first(
        t,
        [

            r'(Emamectin\s+Benzoate\s+[\d.]+\s*%?\s*(?:SG|EC|WG)?[^\.\n]{0,80})',

            r'(Lambda\s+Cyhalothrin\s+[\d.]+\s*EC[^\.\n]{0,80})',

            r'(treat(?:ment|ing)?\s+(?:the\s+)?(?:dry\s+)?\w+\s+seeds?\s+with\s+'
            r'[A-Za-z][A-Za-z\s]+?\s*@\s*[\d.]+\s*(?:g|ml)/kg[^\.\n]{0,60})',

            r'(?:spray|apply|use)\s+('
            r'(?:Dimethoate|Buprofezin|Imidacloprid|Acetamiprid|Mancozeb|'
            r'Carbendazim|Chlorpyri(?:fos|phos)|Metalaxyl|Fipronil|'
            r'Chlorantraniliprole|Emamectin|Spinosad|Thiamethoxam|'
            r'Novaluron|Propiconazole|Hexaconazole|Bordeaux|'
            r'Quinalphos|Flubendiamide|Trichoderma|Pseudomonas|'
            r'Ferbam|Nabam|Cymoxanil|Cymozanil|Captan|Saaf|'
            r'Carbendazim|Fenitrothion|Malathion|Acephate|'
            r'Carboxyn|Streptocycline|Chlorpyriphos)'
            r'[^\.\n]{0,120})',

            r'(?:spray|apply)\s+([A-Za-z][^\.\n]{5,100}?'
            r'(?:ml|g|kg|litre|EC|WP|SC|SG|WG))',

        ]
    )


# ─────────────────────────────────────────────────────────────────────────────
# Precaution From
# ─────────────────────────────────────────────────────────────────────────────

def col_precaution_from(t):

    return _all_unique(
        t,
        r'\b(flood|heavy\s+rain(?:fall)?|excess\s+rainfall|rain(?:fall)?|'
        r'gusty\s+wind|strong\s+wind|thunderstorm|lightning|hail|'
        r'water[\s-]*logging|water\s+stagnation|high\s+temperature|heat|'
        r'disease|pest\s+infestation|wilting|lodging|cold|'
        r'landslide|cyclone|extreme\s+event)\b'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Precaution Tool
# ─────────────────────────────────────────────────────────────────────────────

def col_precaution_tool(t):

    return _all_unique(
        t,
        r'\b(drainage\s+channels?|tarpaulin|polythene|'
        r'mulch(?:ing)?|propping|staking|mechanical\s+support|'
        r'raised\s+bed|bunding|shade|net|trap|irrigation|'
        r'shed|insur(?:e|ance)|temporary\s+shed)\b'
    )