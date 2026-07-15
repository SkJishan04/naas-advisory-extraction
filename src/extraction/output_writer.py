import re
import io
import csv
import pandas as pd

from .constants import (
    MAX_CROPS,
    CROP_COLS,
    WEATHER_COLS,
    ALL_COLS,
)


# ─────────────────────────────────────────────────────────────────────────────
# Build Wide Rows
# ─────────────────────────────────────────────────────────────────────────────

def make_rows(date, weather, crops):

    rows = []

    for chunk_start in range(0, max(len(crops), 1), MAX_CROPS):

        row = {c: "" for c in ALL_COLS}

        if chunk_start == 0:

            row["Advisory Date"] = date
            row["Rainfall Forecast Date"] = weather.get(
                "Rainfall Forecast Date", ""
            )

            row["Rainfall(Assam) mm"] = weather.get(
                "Rainfall(Assam) mm", ""
            )

            row["Excess(+)/Deficit(-)"] = weather.get(
                "Excess(+)/Deficit(-)", ""
            )

            row["Week 1"] = weather.get("Week 1", "")
            row["W1_Assam_Forecast"] = weather.get("W1_Assam", "")

            row["Week 2"] = weather.get("Week 2", "")
            row["W2_Assam_Forecast"] = weather.get("W2_Assam", "")

            row["Flood_Alert"] = weather.get("Flood_Alert", "")

        for slot in range(MAX_CROPS):

            ci = chunk_start + slot

            if ci >= len(crops):
                break

            for col in CROP_COLS:
                row[f"C{slot+1}_{col}"] = crops[ci].get(col, "")

        rows.append(row)

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# DataFrame
# ─────────────────────────────────────────────────────────────────────────────

def build_dataframe(rows):

    df = pd.DataFrame(rows, columns=ALL_COLS)
    df.fillna("", inplace=True)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# CSV Text
# ─────────────────────────────────────────────────────────────────────────────

def dataframe_to_csv_text(df):

    buf = io.StringIO()
    writer = csv.writer(buf)

    group_header = []

    for c in ALL_COLS:

        m = re.match(r"C(\d+)_Crop Name", c)

        if m:
            group_header.append(f"Crop {m.group(1)}")
        else:
            group_header.append("")

    writer.writerow(group_header)

    writer.writerow(
        [
            re.sub(r"^C\d+_", "", c)
            for c in ALL_COLS
        ]
    )

    for _, row in df.iterrows():

        writer.writerow(
            [
                str(row[c])
                if pd.notna(row[c]) and row[c] != ""
                else ""
                for c in ALL_COLS
            ]
        )

    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# Save CSV
# ─────────────────────────────────────────────────────────────────────────────

def save_csv(df, output_path):

    csv_text = dataframe_to_csv_text(df)

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        f.write(csv_text)