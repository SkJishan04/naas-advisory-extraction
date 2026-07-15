import re

from .constants import _BOUNDARY_RE


# ─────────────────────────────────────────────────────────────────────────────
# Extract Assam Block
# ─────────────────────────────────────────────────────────────────────────────

def get_assam_block(txt):
    """
    Extract only Assam advisory block.
    """

    # Pattern:
    # Assam
    # <digits>
    # ...
    # until next state heading

    pat = rf'(Assam\s*\n[\d].*?)(?=\n\s*(?:{_BOUNDARY_RE})\s*\n)'

    m = re.search(
        pat,
        txt,
        re.DOTALL
    )

    if m:
        return m.group(1).strip()

    # ------------------------------------------------------------------
    # Fallback
    # ------------------------------------------------------------------

    m2 = re.search(
        r'(Assam\b.*?)(?=\n\s*(?:{_BOUNDARY_RE})\b)'.format(
            _BOUNDARY_RE=_BOUNDARY_RE
        ),
        txt,
        re.DOTALL,
    )

    return m2.group(1).strip() if m2 else None


# ─────────────────────────────────────────────────────────────────────────────
# Split into Bullet Points
# ─────────────────────────────────────────────────────────────────────────────

def get_bullets(assam):

    parts = re.split(r'\s*•\s*', assam)

    return [
        re.sub(r'\s+', ' ', p).strip()
        for p in parts[1:]
        if p.strip() and len(p.strip()) > 15
    ]