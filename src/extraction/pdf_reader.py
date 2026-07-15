import fitz
import re


# ─────────────────────────────────────────────────────────────────────────────
# PDF → Text
# ─────────────────────────────────────────────────────────────────────────────

def pdf_to_text(path):
    doc = fitz.open(path)
    txt = "\n".join(p.get_text("text") for p in doc)
    doc.close()
    return txt


# ─────────────────────────────────────────────────────────────────────────────
# Advisory Date
# RE_01
# ─────────────────────────────────────────────────────────────────────────────

def get_date(txt):
    """
    Extract advisory date.

    Primary format:
    Date of issue: 16 July 2024
    """

    m = re.search(
        r"Date\s+of\s+issue\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        txt,
    )

    return m.group(1).strip() if m else "Unknown"