from src.extraction.pipeline import run_pipeline


PDF_PATHS = [
    "NAAS_Bulletin-18-June-2024.pdf",
    "NAAS_Bulletin-16-July-2024.pdf",
    "NAAS_Bulletin-19-November-2024.pdf",
    "NAAS_Bulletin-16-April-2024.pdf",
]

OUTPUT = "Assam_Advisories.csv"


if __name__ == "__main__":

    run_pipeline(
        PDF_PATHS,
        OUTPUT,
    )