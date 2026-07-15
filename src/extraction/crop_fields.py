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

# ─────────────────────────────────────────────────────────────────────────────
# Cause of Damage
# ─────────────────────────────────────────────────────────────────────────────

def col_cause(t):

    hits = re.findall(
        r'(?:[Dd]ue\s+to|[Bb]ecause\s+of)\s+([^\.\n]{5,120}?)(?:\.|,\s*(?:it|farmers|drain|light))',
        t
    )

    flood = re.search(
        r'(flood(?:ing)?\s+condition[^\.\n]{0,80}|'
        r'Brahmaputra\s+river[^\.\n]{0,80}|'
        r'above\s+(?:the\s+)?danger\s+level[^\.\n]{0,60})',
        t,
        re.IGNORECASE
    )

    if flood:
        hits.insert(0, flood.group(1).strip())

    return "; ".join(h.strip() for h in hits[:2])


# ─────────────────────────────────────────────────────────────────────────────
# Recommendation
# ─────────────────────────────────────────────────────────────────────────────

def col_recommendation(t):

    hits = re.findall(
        r'(?:[Ff]armers\s+(?:are|may)\s+(?:advised?|adopt)\s+(?:to\s+)?|'
        r'[Ii]t\s+is\s+(?:advised|recommended)\s+to\s+|'
        r'[Ii]mmediately\s+|'
        r'[Ii]t\s+is\s+advised\s+to\s+)'
        r'[^\.\n]{5,200}',
        t
    )

    if not hits:

        hits = re.findall(
            r'(?:[Hh]arvest(?:ing)?|'
            r'[Ss]ow(?:ing)?|'
            r'[Tt]ransplant|'
            r'[Mm]aintain|'
            r'[Ss]pray|'
            r'[Aa]pply|'
            r'[Dd]rain|'
            r'[Cc]arry\s+out|'
            r'[Uu]se\s+of|'
            r'[Pp]rovide\s+mechanical\s+support|'
            r'[Dd]igging\s+a\s+\d+\s*cm\s+deep|'
            r'[Mm]ulch(?:ing)?|'
            r'[Pp]lant\s+the)'
            r'\s+[^\.\n]{5,180}',
            t
        )

    return "; ".join(
        h.strip()[:200]
        for h in hits[:2]
    )


# ─────────────────────────────────────────────────────────────────────────────
# Varieties
# ─────────────────────────────────────────────────────────────────────────────

def col_varieties(t):

    m = re.search(
        r'(?:variet(?:y|ies)\s*(?:like|such\s+as|are|viz\.?|recommended|:)?\s*'
        r'(?:[\w\s]*?(?:may\s+adopt|is|include|for\s+the\s+state\s+of\s+Assam))?\s*[.:]?\s*)'
        r'([\w\s,\-–()&/]+?)(?:\.\s|The\s|$)',
        t,
        re.IGNORECASE
    )

    if m and len(m.group(1).strip()) > 3:
        return m.group(1).strip().rstrip(",;. ")[:250]

    named = []

    named += re.findall(
        r'\b(TS-\d{2,}|PM-\d{2}|NRCHB-\d{3}|T-\d{3}|Bonneville)\b',
        t
    )

    named += re.findall(
        r'\b(Ranjit(?:\s+Sub\s*1)?|Bahadur|Satyaranjan|'
        r'Basundhara|Mahsuri|Ketekijoha|Luit|'
        r'Kop(?:i|ee)lee|Dishang|Chilarai|'
        r'Lachit|JyotiPrasad|Bishnuprasad|'
        r'[Kk]anaklata|'
        r'[Dd]inanath(?:\s+[Jj]oymoti)?|'
        r'Swarnabh|Boro-[12]|'
        r'Cauvery|Joymati|IR-50)\b',
        t
    )

    named += re.findall(
        r'(Pratap|Sonai|SGC\s*\d+|K\s*851|K\s*815|'
        r'Pusa\s+\w+(?:\s+\d+)?|'
        r'SG-\d|'
        r'Ganga\s*\d+|'
        r'Bio\s*\d{4}|'
        r'Vivek\s+Maize\s+Hybrid\s+\d+|'
        r'Dhawal|Navjot|Rio-de-Geneiro|'
        r'Nadia|Karkai|Bardwan|Moran|Jorhat|China)\b',
        t
    )

    return ", ".join(dict.fromkeys(named))[:250] if named else ""


# ─────────────────────────────────────────────────────────────────────────────
# Extra Information
# ─────────────────────────────────────────────────────────────────────────────

def col_extra(t):

    if re.search(
        r'\b(?:Avoid\s+staying|'
        r'Seek\s+shelter|'
        r'Refrain\s+from|'
        r'landslide|'
        r'danger\s+level|'
        r'Brahmaputra)\b',
        t,
        re.IGNORECASE
    ):
        return t.strip()[:200]

    if re.search(
        r'\b(?:cattle|livestock|animal|shed|apiar)\b',
        t,
        re.IGNORECASE
    ):
        return t.strip()[:200]

    m = re.search(
        r'(?:dig(?:ging)?|trench)\s+(?:a\s+)?'
        r'(\d+)\s*cm\s+deep,?\s*'
        r'(\d+)\s*cm\s+wide\s+trench,?\s*'
        r'(\d+)\s*m\s+(?:away\s+from|from)\s+trunk',
        t,
        re.IGNORECASE
    )

    if m:
        return (
            f"Trench: {m.group(1)} cm deep × "
            f"{m.group(2)} cm wide, "
            f"{m.group(3)} m from trunk"
        )

    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Extract Crop
# ─────────────────────────────────────────────────────────────────────────────

def extract_crop(bullet):

    return {
        "Crop Name": detect_crop(bullet),
        "Land": _first(
            bullet,
            [
                r'\b(medium\s+and\s+upland|'
                r'low\s*land|'
                r'upland|'
                r'lowland|'
                r'irrigated|'
                r'rainfed|'
                r'flood[- ]prone)\b'
            ]
        ),
        "Stage": col_stage(bullet),
        "Field Condition": col_field_condition(bullet),
        "Field Preparation": col_field_prep(bullet),
        "Seeds Requirement": col_seeds(bullet),
        "Pests/Disease": col_pests(bullet),
        "Fertilizer": col_fertilizer(bullet),
        "Pesticides": col_pesticides(bullet),
        "Precaution from": col_precaution_from(bullet),
        "Precaution tool": col_precaution_tool(bullet),
        "Cause of Damage": col_cause(bullet),
        "Recommendation": col_recommendation(bullet),
        "Varieties": col_varieties(bullet),
        "Extra Information": col_extra(bullet),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Merge Duplicate Crop Advisories
# ─────────────────────────────────────────────────────────────────────────────

def merge_crops(records):

    merged = {}
    order = []

    for r in records:

        name = r["Crop Name"]

        if name not in merged:
            merged[name] = dict(r)
            order.append(name)

        else:

            for k, v in r.items():

                if k == "Crop Name" or not v:
                    continue

                if v not in merged[name].get(k, ""):
                    merged[name][k] = (
                        merged[name][k] + "; " + v
                    ).lstrip("; ")

    useful_keys = [
        "Pests/Disease",
        "Pesticides",
        "Fertilizer",
        "Recommendation",
        "Varieties",
        "Seeds Requirement",
    ]

    return [
        merged[n]
        for n in order
        if n != "General Advisory"
        or any(merged[n].get(k) for k in useful_keys)
    ]