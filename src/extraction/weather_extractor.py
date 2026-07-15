import re


def get_weather(assam):
    """
    Extract Assam weather information.
    """

    w = {}

    # ------------------------------------------------------------------
    # Realized rainfall
    # ------------------------------------------------------------------

    m = re.search(
        r'([\d.]+)\s*mm\s*\(([^)]+)\)\s*rainfall\s*(?:was\s*)?received\s*over\s*Assam',
        assam,
        re.IGNORECASE
    )

    if m:
        w["Rainfall(Assam) mm"] = m.group(1) + " mm"
        w["Excess(+)/Deficit(-)"] = m.group(2).strip()

    else:

        m2 = re.search(
            r'[Rr]ainfall\s+received\s+over\s+Assam\s+was\s+([\d.]+)\s*mm\s*\(([^)]+)\)',
            assam
        )

        if m2:
            w["Rainfall(Assam) mm"] = m2.group(1) + " mm"
            w["Excess(+)/Deficit(-)"] = m2.group(2).strip()

    # ------------------------------------------------------------------
    # Cumulative rainfall period
    # ------------------------------------------------------------------

    m = re.search(
        r'(?:during|from)\s+([\d]+\s+\w+[\s\-–to]+[\d]+\s+\w+\s+\d{4})',
        assam
    )

    if m:
        w["Rainfall Forecast Date"] = m.group(1).strip()

    # ------------------------------------------------------------------
    # Week 1 / Week 2 date ranges
    # ------------------------------------------------------------------

    m = re.search(
        r'next\s+two\s+weeks\s*\(([^)]+)\)',
        assam
    )

    if m:

        parts = re.split(
            r'\s+and\s+',
            m.group(1),
            maxsplit=1
        )

        w["Week 1"] = parts[0].strip()

        if len(parts) > 1:
            w["Week 2"] = parts[1].strip()

    # ------------------------------------------------------------------
    # Forecast text
    # ------------------------------------------------------------------

    hdr = assam.split("•")[0] if "•" in assam else assam[:900]

    m = re.search(
        r'(?:next\s+two\s+weeks[^)]*\)\s*is\s*|forecast.*?is\s+)(.*?)(?:\.\s*$|\.\s*•)',
        hdr,
        re.DOTALL
    )

    if m:

        forecast_txt = re.sub(
            r'\s+',
            ' ',
            m.group(1)
        ).strip()

        mw1 = re.search(
            r'(above\s+normal|below\s+normal|normal|no\s+rain(?:fall)?|large\s+(?:excess|deficit))'
            r'(?:\s+rainfall)?\s+for\s+week\s*1',
            forecast_txt,
            re.IGNORECASE
        )

        if mw1:
            w["W1_Assam"] = mw1.group(1).strip()

        mw2 = re.search(
            r'(?:and\s+)'
            r'(above\s+normal|below\s+normal|normal|no\s+rain(?:fall)?|large\s+(?:excess|deficit))'
            r'(?:\s+rainfall)?\s+for\s+week\s*2',
            forecast_txt,
            re.IGNORECASE
        )

        if mw2:
            w["W2_Assam"] = mw2.group(1).strip()

        if "W1_Assam" not in w:

            mw12 = re.search(
                r'(above\s+normal|below\s+normal|normal|no\s+rain(?:fall)?|large\s+(?:excess|deficit))'
                r'(?:\s+rainfall)?\s+for\s+week\s*1\s+and\s+week\s*2',
                forecast_txt,
                re.IGNORECASE
            )

            if mw12:
                w["W1_Assam"] = mw12.group(1).strip()
                w["W2_Assam"] = mw12.group(1).strip()

    # ------------------------------------------------------------------
    # Flood Alert
    # ------------------------------------------------------------------

    if re.search(
        r'(?:flood(?:ing)?\s+condition|Brahmaputra\s+river|'
        r'above\s+(?:the\s+)?danger\s+level|flood[\s-]prone\s+area)',
        assam,
        re.IGNORECASE
    ):
        w["Flood_Alert"] = "YES"

    return w