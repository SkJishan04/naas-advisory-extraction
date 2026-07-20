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