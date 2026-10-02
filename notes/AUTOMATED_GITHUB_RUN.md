> **Historical** (2026-10-02): the workflow described here was removed from the public repository; kept only as a record of how the first data run was made.

# Automated GitHub Actions Run

## What This Workflow Does

The workflow `taroko-public-metadata.yml` runs the full Taroko metadata pipeline
on GitHub's infrastructure, where the seed URLs are reachable.

It:
1. Installs Python dependencies
2. Runs `scripts/run_pipeline.py` (fetches seeds, collects links, downloads pages, extracts metadata)
3. Runs `scripts/06_validate_corpus.py`
4. Uploads a public-safe artifact named `taroko-public-metadata`

## What Gets Uploaded

Only safe public metadata:
- `data/public/*.csv` — links, download log, inventory, lexical array summaries
- `notes/RUN_REPORT.md`, `notes/HANDOFF.md`, `notes/METHOD.md`
- `README.md`

## What Does NOT Get Uploaded

The following are created on the runner during execution but disappear when the
runner terminates. They are never uploaded:

- `archive/raw_html/` — downloaded HTML source files
- `archive/screenshots/` — Playwright screenshots (not used unless --runtime flag)
- `archive/output_samples/` — runtime text samples
- `archive/extracted_full/` — full word arrays from source code
- `data/private/` — any private data

## How to Trigger

Go to: GitHub → Actions → Taroko Public Metadata Pipeline → Run workflow → select branch → Run workflow

## How to Get the Outputs

After the run completes (green), click the run → scroll to Artifacts → download `taroko-public-metadata`.
