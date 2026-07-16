import os

from .pdf_reader import (
    pdf_to_text,
    get_date,
)

from .block_extractor import (
    get_assam_block,
    get_bullets,
)

from .weather_extractor import (
    get_weather,
)

from .crop_fields import (
    extract_crop,
    merge_crops,
)

from .output_writer import (
    make_rows,
    build_dataframe,
    save_csv,
)


def run_pipeline(pdf_paths, output_path):

    pdf_paths = [
        p
        for p in pdf_paths
        if os.path.exists(p)
    ]

    all_rows = []

    for path in sorted(pdf_paths):

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

    df = build_dataframe(all_rows)

    save_csv(df, output_path)

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

    print(f"\nSaved → {output_path}")