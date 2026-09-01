import argparse
from pathlib import Path

from src.extraction.pipeline import run_pipeline


def parse_args():

    parser = argparse.ArgumentParser(
        description="Extract structured Assam agricultural advisories from NAAS PDFs."
    )

    parser.add_argument(
        "pdfs",
        nargs="+",
        help="Path(s) to NAAS bulletin PDF files."
    )

    parser.add_argument(
        "-o",
        "--output",
        default="results/Assam_Advisories.csv",
        help="Output CSV path."
    )

    return parser.parse_args()


def main():

    args = parse_args()

    output_path = Path(args.output)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    run_pipeline(
        args.pdfs,
        str(output_path)
    )


if __name__ == "__main__":
    main()