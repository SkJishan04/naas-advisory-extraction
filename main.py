import os

from extraction.pdf_reader import (
    pdf_to_text,
    get_date,
)

from extraction.block_extractor import (
    get_assam_block,
    get_bullets,
)

from extraction.weather_extractor import (
    get_weather,
)

from extraction.crop_fields import (
    extract_crop,
    merge_crops,
)

from extraction.output_writer import (
    make_rows,
    build_dataframe,
    save_csv,
)

# ------------------------------------------------------------------
# PDF Paths
# ------------------------------------------------------------------

PDF_PATHS = [
    "NAAS_Bulletin-18-June-2024.pdf",
    "NAAS_Bulletin-16-July-2024.pdf",
    "NAAS_Bulletin-19-November-2024.pdf",
    "NAAS_Bulletin-16-April-2024.pdf",
]

PDF_PATHS = [
    p
    for p in PDF_PATHS
    if os.path.exists(p)
]

OUTPUT = "Assam_Advisories.csv"

# ------------------------------------------------------------------
# Process PDFs
# ------------------------------------------------------------------

all_rows = []

for path in sorted(PDF_PATHS):

    print(f"\n📄 {path}")

    txt = pdf_to_text(path)

    date = get_date(txt)

    assam = get_assam_block(txt)

    if not assam:

        print("⚠️ No Assam section found — skipping")

        continue

    weather = get_weather(assam)

    bullets = get_bullets(assam)

    crops = merge_crops(
        [
            extract_crop(b)
            for b in bullets
        ]
    )

    names = [
        c["Crop Name"]
        for c in crops
    ]

    print(
        f"📅 {date} | "
        f"Flood: {weather.get('Flood_Alert','')} | "
        f"🌾 {names}"
    )

    all_rows.extend(
        make_rows(
            date,
            weather,
            crops,
        )
    )

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------

df = build_dataframe(all_rows)

save_csv(df, OUTPUT)

print("\n" + "=" * 60)
print(
    f"Done — {df.shape[0]} rows × {df.shape[1]} columns"
)
print("=" * 60)

for _, r in df.iterrows():

    d = r.get("Advisory Date", "")

    if not d:
        continue

    names = [
        r.get(f"C{i}_Crop Name", "")
        for i in range(1, 5)
    ]

    names = [
        n
        for n in names
        if n
    ]

    print(f"{d}: {', '.join(names)}")

print(f"\nSaved → {OUTPUT}")