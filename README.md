# Taroko Gorge Ecosystem Archive

A deterministic, low-token research archive pipeline for Nick Montfort's *Taroko Gorge* and its remix ecosystem.

> **v2 Archive (branch: archive-mvp-v2)**: Added work-entity reconciliation, ELC/context-page paratext capture infrastructure, statement taxonomy v2, lexical mechanism audit v2, and v2 query index. See [`notes/ARCHIVE_MVP_V2_FINAL_REPORT.md`](notes/ARCHIVE_MVP_V2_FINAL_REPORT.md) for what changed. Query tool: `python3 scripts/20_query_archive_v2.py overview`. Guide: [`notes/QUERY_INDEX_V2_GUIDE.md`](notes/QUERY_INDEX_V2_GUIDE.md).

---

## ⚠️ Public Repo Safety Warning

This repository is **public**. Raw downloaded HTML, screenshots, full extracted word arrays, and runtime output samples are **local-only** and **Git-ignored**. Do NOT commit files from:

- `archive/raw_html/`
- `archive/screenshots/`
- `archive/output_samples/`
- `archive/extracted_full/`
- `data/private/`

Only `data/public/*.csv`, `data/public/*.md`, scripts, seeds, and notes are commit-safe.

---

## Interpretation Principle

For Taroko-style generative works, **source code is the primary archival object**. Runtime output (generated text, screenshots) is a trace of one execution, not the complete poem. Archive the source; treat runtime samples as supplementary evidence only.

---

## Install

```bash
pip install -r requirements.txt
```

---

## Pipeline Commands

Run the full non-runtime pipeline:

```bash
python scripts/run_pipeline.py
```

Run with download limit (test):

```bash
python scripts/run_pipeline.py --limit 5
```

Run with runtime sampling (requires Playwright):

```bash
python scripts/run_pipeline.py --runtime --seconds 10
```

Force re-download existing files:

```bash
python scripts/run_pipeline.py --force
```

Run validation only:

```bash
python scripts/06_validate_corpus.py
```

---

## Output Files

### Public (commit-safe)

| File | Description |
|------|-------------|
| `seeds/taroko_seed_urls.csv` | Four initial seed URLs |
| `data/public/taroko_links.csv` | Candidate Taroko/remix URLs |
| `data/public/collect_links_log.csv` | Link collection log per seed |
| `data/public/download_log.csv` | Download status, sha256, local paths |
| `data/public/inventory.csv` | Metadata + Taroko signal scores (0–5) |
| `data/public/lexical_array_summary.csv` | Array name, count, hash (no full content) |
| `data/public/validation_summary.csv` | Pipeline validation results |
| `notes/METHOD.md` | Compact methodology |
| `notes/HANDOFF.md` | Current state receipt |
| `notes/RUN_REPORT.md` | Validation report |

### Local-only (Git-ignored)

| Path | Description |
|------|-------------|
| `archive/raw_html/` | Downloaded HTML/JS source files |
| `archive/screenshots/` | Playwright runtime screenshots |
| `archive/output_samples/` | Visible text samples from runtime |
| `archive/extracted_full/lexical_arrays_full.json` | Full word arrays from source code |
| `data/private/` | Any private research data |

---

## Scoring (probable_taroko_score)

- **0** No evidence
- **1** Mentions Taroko/Gorge only
- **2** JavaScript + Taroko/Gorge
- **3** JavaScript + generator-like function/timer signals
- **4** Known Taroko array/function patterns detected
- **5** Likely direct Taroko source or remix
