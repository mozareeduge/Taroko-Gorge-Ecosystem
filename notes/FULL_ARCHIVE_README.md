> **Historical** (2026-10-02): this was written for the private working repository ('This repository is private'). The public repository holds only the metadata tables, scripts and notes; see the root `README.md` and `PUBLIC_PRIVATE_BOUNDARY_V2.md`.

# Taroko Gorge Ecosystem — Full Private Archive

## What Is Captured

This repository is **private**. It stores the complete archive outputs alongside the pipeline source.

### Archive Contents

| Path | Description |
|------|-------------|
| `archive/raw_html/` | Downloaded HTML/JS source files for all candidate URLs |
| `archive/screenshots/` | Playwright screenshots of probable Taroko/remix pages |
| `archive/output_samples/` | Visible text captured from runtime execution (one trace per page) |
| `archive/extracted_full/lexical_arrays_full.json` | Full JS array content extracted from probable Taroko source files |
| `data/public/` | Public-safe metadata CSVs (links, download log, inventory, lexical summary) |
| `data/private/taroko_corpus_catalog.csv` | One-row-per-URL complete catalog (see below) |
| `data/private/archive_manifest.csv` | SHA256 manifest for every archived file |
| `private_archive/taroko_full_archive.zip` | Zip package of the complete archive |
| `notes/RUN_REPORT.md` | Pipeline validation report |
| `notes/METHOD.md` | Methodology documentation |

## What Failed

See `data/private/taroko_corpus_catalog.csv`, column `failure_or_gap_note`, for per-URL failure details.
See `data/public/download_log.csv` for HTTP status codes and errors on every attempted download.

Known failure categories:
- HTTP 403 (Forbidden): server denied access
- HTTP 404 (Not Found): page no longer exists
- DNS resolution failure: domain unreachable at time of archiving
- Runtime sample failed: Playwright could not render the page within the timeout

## How to Read the Corpus Catalog

File: `data/private/taroko_corpus_catalog.csv`

One row per candidate URL. Key columns:

| Column | Meaning |
|--------|--------|
| `candidate_id` | Identifier assigned during link collection |
| `archive_id` | Download log identifier (dl_NNNN) |
| `url` | Candidate URL |
| `download_status` | success / failed / skipped_cached / not_attempted |
| `probable_taroko_score` | 0–5 match score (5 = full Taroko pattern) |
| `array_names` | Detected JS array names (pipe-separated) |
| `runtime_sample_path` | Path to text trace (if captured) |
| `screenshot_path` | Path to PNG screenshot (if captured) |
| `failure_or_gap_note` | Reason for failure or gap, if any |
| `rights_note` | Rights/license note (manually populated) |
| `research_note` | Researcher annotation (manually populated) |

## Runtime Samples: Traces, Not Complete Poems

For Taroko Gorge-style generative works, **source code is the primary archival object**.

The JavaScript source code (in `archive/raw_html/`) contains the complete vocabulary,
structure, and generation algorithm. It is the work.

Runtime output samples (`archive/output_samples/`) capture **one execution trace** —
a single set of generated stanzas at a particular moment. The generated text is
infinite in potential, probabilistic, and non-repeating. No finite sample captures
the complete poem. Archive the source; treat runtime samples as supplementary evidence.

## Why Raw HTML Is a Primary Archive Object

For JavaScript generative works:
- The HTML/JS file contains the algorithm, word arrays, and generation rules.
- The browser renders one execution. Source code encodes all possible executions.
- Archiving source code preserves the work. Archiving screenshots preserves one moment.

## Reproduction

To re-run the full archive pipeline:

```bash
pip install -r requirements.txt
pip install playwright
playwright install chromium
python scripts/run_pipeline_full.py --seconds 20
```
