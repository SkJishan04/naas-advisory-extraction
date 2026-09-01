import re


# ─────────────────────────────────────────────────────────────────────────────
# Bullet normalization
# ─────────────────────────────────────────────────────────────────────────────

BULLET_CHARS = "•·▪●◦‣⁃"


def normalize_bullets(text):
    """
    Convert common PDF bullet characters into a single canonical bullet.

    The extractor expects '•' as the canonical bullet separator.
    """

    for bullet in BULLET_CHARS:
        text = text.replace(bullet, "•")

    return text


# ─────────────────────────────────────────────────────────────────────────────
# PDF text normalization
# ─────────────────────────────────────────────────────────────────────────────

def normalize_text(text):
    """
    Normalize PDF-extracted text while preserving meaningful line breaks.

    Operations:
    - remove carriage returns
    - remove soft hyphens
    - join words broken across PDF line endings
    - normalize bullet characters
    - collapse repeated spaces/tabs
    - remove excessive blank lines

    Line breaks are intentionally preserved because state headings and
    section boundaries depend on them.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u00ad", "")

    # Join words split at the end of a PDF line:
    # "rain-\nfall" -> "rainfall"
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # Normalize bullet characters.
    text = normalize_bullets(text)

    # Normalize horizontal whitespace without destroying line structure.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces surrounding newlines.
    text = re.sub(r" *\n *", "\n", text)

    # Collapse excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()