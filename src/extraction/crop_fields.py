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