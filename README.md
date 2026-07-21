# NAAS Assam Agromet Advisory Extractor

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**Rule-based extraction of structured agricultural advisory data from NAAS (National Academy of Agricultural Sciences) agromet bulletin PDFs — the Assam-state pipeline.**

---
## 📌 Project Context & Scope

This repository implements **my individual contribution** to a 4-person B.Tech thesis project:

> **"Extraction of Agricultural Advisory Data from NAAS Bulletins using Regex, Machine Learning, and Hybrid Validation"**
> Bachelor Thesis, Department of Computer Science and Engineering
> **Indian Institute of Information Technology, Kalyani** — Spring Semester 2026
> Authors: Subhadeep Mondal · Subham Das · **Sk Jishan** · Tanveer Ahmed
> Supervisor: **Dr. Sanjay Chatterji**

The full thesis covers four states — **West Bengal, Assam, Bihar, and Odisha** — split one-per-team-member, plus a shared machine-learning validation and hybrid regex–ML layer evaluated across all four states combined. **This repository contains only the Assam extraction pipeline**, which I designed, implemented, and tested. The other three states' extractors and the ML/hybrid validation layer were built by my teammates / developed collaboratively and are not included here.

If you're reviewing this as a standalone project: everything in this repo — the regex design, the crop/field schema, and the results below — reflects the Assam component specifically.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Folder Structure](#-folder-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Output Format](#-output-format)
- [Regex Coverage](#-regex-coverage)
- [Example](#-example)
- [Methodology](#-methodology)
- [Evaluation Metrics & Results](#-evaluation-metrics--results)
- [Sample Data](#-sample-data)
- [Challenges Addressed](#-challenges-addressed)
- [Tech Stack](#-tech-stack)
- [Limitations](#-limitations)
- [Future Work](#-future-work)
- [Citation](#-citation)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🌾 Project Overview

### Background & Motivation

Agricultural advisories give farmers timely, actionable guidance on sowing, transplanting, irrigation, drainage, fertilizer application, pest/disease control, harvesting, and protection from adverse weather. NAAS bulletins publish this information state-wise, several times a month, for use by farmers, researchers, and policymakers.

The catch: these bulletins are distributed as **semi-structured PDFs** — free-flowing paragraphs and bullet points, not machine-readable tables — which makes them hard to analyze, search, or feed into any downstream decision-support system at scale.

### Problem Statement

Given a NAAS bulletin PDF containing an Assam advisory section, automatically extract:

- **Weather/advisory-level fields**: advisory date, rainfall forecast date, rainfall amount, excess/deficit category, Week 1 / Week 2 forecast qualifiers, flood alerts.
- **Crop-wise fields** (up to 4 crops per bulletin): crop name, land type, growth stage, field condition, field preparation, seed requirement, pests/disease, fertilizer, pesticides, precaution source, precaution tool, cause of damage, recommendation, varieties, and extra information.

The same information routinely appears in different sentence structures across bulletins — e.g. *"18.2 mm (-20% deficit) rainfall was received over Assam"* vs. *"Rainfall received over Assam was 18.2 mm (-20% deficit)"* — so a single regex pattern per field is not enough; each field needs primary + fallback patterns.

### Objectives

1. Isolate the Assam-specific advisory block from a multi-state bulletin PDF.
2. Extract weather/rainfall/forecast fields for Assam specifically (single-series rainfall — unlike West Bengal, Assam does not need a Gangetic/Sub-Himalayan split).
3. Detect crop names (including Assam-specific rice types: Sali, Boro, Ahu, Kharif) and extract 15 structured fields per crop.
4. Output a clean, wide-format CSV/XLSX matching the project's shared schema.
5. Maintain a **precision-oriented** extraction policy — a blank field is safer than a wrong one.

---

## 🗂️ Folder Structure
```
naas-advisory-extraction/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── main.py # entry point — processes bulletin PDFs end to end
├── src/
│ ├── init.py
│ └── extraction/
│ ├── init.py
│ ├── constants.py # state-boundary list (to know where Assam's section ends)
│ ├── pdf_reader.py # PyMuPDF text extraction + advisory date parsing
│ ├── text_normalizer.py # PDF text clean-up (line breaks, bullets, whitespace)
│ ├── block_extractor.py # isolates the Assam block + splits it into bullets
│ ├── weather_extractor.py # rainfall, forecast window, week qualifiers, flood alert
│ ├── crop_detector.py # crop-name dictionary + detection
│ ├── crop_fields.py # the 15 crop-wise field extractors + merge logic
│ ├── output_writer.py # wide-format CSV/XLSX builder (2-row header)
│ └── pipeline.py # orchestrates all of the above per PDF
└── results/
└── Assam_Advisories.csv # sample extracted output, verified against real bulletins

```
---

## ⚙️ Installation

```bash
git clone https://github.com/SkJishan04/naas-advisory-extraction.git
cd naas-advisory-extraction

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**Requirements** (`requirements.txt`):

PyMuPDF>=1.24.0
pandas>=2.0.0
openpyxl>=3.1.0


---

## ▶️ Usage

1. Place your NAAS bulletin PDF(s) in the project root (or wherever `main.py`'s `PDF_PATHS` list points).
2. Run:

```bash
python3 main.py
```

3. The script will:
   - Extract raw text from each PDF page-by-page (PyMuPDF)
   - Normalize the text (join broken words, fold bullet glyphs)
   - Isolate the **Assam** advisory block (stopping at the next state heading — West Bengal, Bihar, Odisha, or Disclaimer)
   - Extract weather + crop-wise fields
   - Merge repeated mentions of the same crop
   - Write everything to `Assam_Advisories.csv`

Sample console output:

📄 NAAS_Bulletin-16-July-2024.pdf
📅 16 July 2024 | Flood: YES | 🌾 ['Sali Rice', 'Banana, Citrus, Papaya', 'Coconut']

============================================================
✅ Done — 3 rows × 69 columns

16 July 2024: Sali Rice, Banana, Citrus, Papaya, Coconut

💾 Saved → Assam_Advisories.csv


---
## 📊 Output Format

The output is a **wide-format table with a 2-row header**, matching the schema shared across all four states in the project:

**Row 1** — group labels (blank, blank, ..., `Crop 1`, blank..., `Crop 2`, ...)
**Row 2** — actual column names

**Weather/advisory columns (9):**

| Column | Description |
|---|---|
| `Advisory Date` | Bulletin issue date |
| `Rainfall Forecast Date` | Validity window of the forecast |
| `Rainfall(Assam) mm` | Rainfall received over Assam |
| `Excess(+)/Deficit(-)` | Departure from normal rainfall |
| `Week 1` / `Week 2` | Forecast date ranges |
| `W1_Assam` / `W2_Assam` | Forecast qualifier (above normal / below normal / normal / no rainfall) |
| `Flood_Alert` | `YES` if flood/Brahmaputra/danger-level language is detected |

**Crop-wise columns (15 × up to 4 crop slots = 60 columns):**

`Crop Name`, `Land`, `Stage`, `Field Condition`, `Field Preparation`, `Seeds Requirement`, `Pests/Disease`, `Fertilizer`, `Pesticides`, `Precaution from`, `Precaution tool`, `Cause of Damage`, `Recommendation`, `Varieties`, `Extra Information`

→ **69 columns total** (9 weather + 4 × 15 crop fields). If a bulletin has more than 4 crops, additional rows are created for the same advisory date, with the weather columns left blank on the overflow row(s).

---


## 🔎 Regex Coverage

This extractor implements **~180 regex-based rules**, organized as follows (counting each dictionary/alternation entry as one rule, consistent with the thesis's regex inventory methodology, Ch. 5):

| Group | Approx. Count | Purpose |
|---|---|---|
| Text normalization | 5 | Clean line breaks, whitespace, bullet glyphs |
| Assam block extraction | 6 | Isolate the Assam section from the full bulletin |
| Assam rainfall extraction | 6 | Rainfall amount + excess/deficit departure |
| Assam week forecast | 4 | Week 1 / Week 2 date ranges + qualifiers |
| Crop dictionary | 51 | Crop name detection (incl. Assam-specific rice types) |
| Action-based crop detection | 1 | Detects crop names near "sowing of", "harvest of", etc. |
| Land | 6 | Upland / lowland / irrigated / rainfed / flood-prone |
| Stage | 8 | Sowing, transplanting, flowering, harvesting, etc. |
| Field Condition | 7 | Water-logging, moisture, standing water, etc. |
| Field Preparation | 8 | Land prep, drainage, bunding, mulching |
| Seeds Requirement | 8 | Seed rate per bigha, seed treatment |
| Pests/Disease | 9 | Stem borer, blast, Ganoderma, aphid, etc. |
| Fertilizer | 10 | Urea/SSP/MOP/DAP/FYM quantities |
| Pesticides | 10 | Emamectin Benzoate, Lambda Cyhalothrin, generic dosages |
| Precaution from / tool | 12 | Risk source + protective measure |
| Cause of Damage | 6 | Flood, Brahmaputra, danger-level triggers |
| Recommendation | 10 | Advisory action sentences |
| Varieties | 8 | Named varieties (Ranjit, Luit, Mahsuri, TS-/PM- codes, etc.) |
| Extra Information | 6 | Flood safety notes, livestock advisories, trench dimensions |
| Bullet splitting | 1 | Splits the block into per-crop advisory units |

*(This is the Assam-relevant subset of the project's full ~267-rule inventory documented in the thesis, Ch. 5.7 — the state-block/rainfall/week-forecast rows above are specific to Assam; the crop-detection and crop-field rows reflect the shared schema design used across all four states, as implemented in this Assam extractor.)*

---

## 💡 Example

**Input** (an advisory bullet from an Assam section):

> *"Farmers are advised for sowing of Sali rice in medium and upland fields. Apply 40 kg Urea per bigha for the mustard crop at the flowering stage."*

**Extracted structured output:**

| Field | Value |
|---|---|
| Crop Name | Sali Rice/Paddy |
| Land | medium and upland |
| Stage | sowing |
| Fertilizer | 40 kg Urea per bigha |

**Weather example:**

> *"18.2 mm (-20% deficit) rainfall was received over Assam during the past week."*

| Field | Value |
|---|---|
| Rainfall(Assam) mm | 18.2 mm |
| Excess(+)/Deficit(-) | -20% deficit |

---

## 🧠 Methodology

The extractor follows a **precision-oriented, rule-based approach**:

1. **PDF → text**: PyMuPDF extracts raw text page-by-page.
2. **Normalization**: hyphen-broken words are rejoined, whitespace is collapsed, and bullet glyphs (`·`, `▪`, `●`, etc.) are folded to a single canonical `•` so bullet-splitting is reliable regardless of the source PDF's formatting.
3. **State-block isolation**: a boundary regex (built from every other Indian state name that could appear as a heading) marks where the Assam section ends.
4. **Field extraction**: each field has a primary pattern plus fallback patterns to catch differently-worded sentences expressing the same information.
5. **Precision-first philosophy**: when no pattern matches confidently, the field is left **blank** rather than guessed — an incorrect pesticide/fertilizer/rainfall value can mislead someone relying on it, while a blank value is easy to spot and manually fill in later.

---

## 📈 Evaluation Metrics & Results

Fields are evaluated against manually prepared ground truth using:

- **Precision** = TP / (TP + FP) — of everything extracted, how much was correct
- **Recall** = TP / (TP + FN) — of everything that should have been extracted, how much was found
- **F1-score** = harmonic mean of precision and recall
- **False Discovery Rate (FDR)** = 1 − Precision
- **False Negative Rate (FNR)** = 1 − Recall

**Assam-specific results (rule-based extraction), as reported in the thesis:**

| Metric | Value |
|---|---|
| True Positives (TP) | 684 |
| False Positives (FP) | 172 |
| False Negatives (FN) | 431 |
| **Precision** | **0.7991** |
| **Recall** | **0.6135** |
| **F1-score** | **0.6940** |

Assam recorded the highest true-positive count and F1-score among the project's four state components, while maintaining precision above recall — consistent with the project-wide design goal.

*For context (team-wide, all 4 states combined, including the ML/hybrid layers not part of this repo): the full project achieved 0.7912 precision / 0.6065 recall (rule-based), improving to 0.8439 precision / 0.5808 recall with hybrid regex–ML validation.*

---

## 🧾 Sample Data

`results/Assam_Advisories.csv` contains extraction results manually verified against real NAAS bulletins (June, July, and November 2024), including real advisory content such as flood conditions along the Brahmaputra, Ganoderma disease in coconut, aphid infestation in rapeseed-mustard, and named Assam rice/mustard varieties (Sali Paddy, TS-36, PM-26, etc.). This file demonstrates the extractor's output on genuine advisory text, not synthetic data.

---

## 🧩 Challenges Addressed

- Multiple state sections within a single bulletin PDF
- Inconsistent state headings and section boundaries
- PDF text extraction noise: broken lines, irregular spacing, hyphenation
- Crop synonyms (paddy vs. rice vs. Sali rice vs. Boro rice vs. Kharif rice)
- Pest/disease names appearing in varied sentence forms
- Fields missing entirely in some bulletins
- Overly broad regex capturing unwanted trailing text

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **PyMuPDF (fitz)** — PDF text extraction
- **pandas** — tabular data handling
- **openpyxl** — Excel (.xlsx) export
- **re** (standard library) — the extraction engine itself

---

## ⚠️ Limitations

- Regex rules can miss values when a bulletin uses unseen sentence structures.
- Broad fallback patterns occasionally capture extra trailing text.
- PDF text-extraction noise (line breaks, inconsistent bullet glyphs) can still affect matching in edge cases — this is mitigated but not eliminated by `text_normalizer.py`.
- No automated comparison against ground truth is wired into this repo yet (see Future Work).
- Crop-order in the output may not always match a manually prepared reference file, since bullets are processed in the order they appear in the PDF.

---

## 🚀 Future Work

- [ ] Add an `evaluation/` module that compares extractor output against `assam_ground_truth.xlsx` and reports Precision/Recall/F1/FDR/FNR automatically
- [ ] Add a `tests/` suite (pytest) covering each extraction function against known worked examples
- [ ] Replace hardcoded `PDF_PATHS` in `main.py` with CLI arguments (`argparse`) and a `data/pdfs/` folder convention
- [ ] Expand fallback regex coverage for `Recommendation` and `Extra Information` (currently the lowest-precision fields project-wide)
- [ ] OCR fallback for scanned/image-based bulletin PDFs
- [ ] Explore ML-based candidate validation (as done project-wide with Logistic Regression / Linear SVM / Random Forest) scoped specifically to Assam's extracted candidates

---

## 📖 Citation

If referencing this work:

Mondal, S., Das, S., Jishan, S., & Ahmed, T. (2026).
Extraction of Agricultural Advisory Data from NAAS Bulletins using Regex,
Machine Learning, and Hybrid Validation.
Bachelor's Thesis, Department of Computer Science and Engineering,
Indian Institute of Information Technology, Kalyani.
Supervisor: Dr. Sanjay Chatterji.


This repository implements the Assam-state component of that thesis.

---

## 📄 License

Released under the [MIT License](LICENSE).

---
