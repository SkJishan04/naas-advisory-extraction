import re

from .constants import _CROPS


def detect_crop(text):
    """
    Detect crop from advisory text.

    Priority order is preserved exactly as defined
    in _CROPS inside constants.py.
    """

    for name, pattern in _CROPS:
        if re.search(pattern, text, re.IGNORECASE):
            return name

    return "General Advisory"