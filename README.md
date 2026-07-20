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

