# Taroko Gorge Ecosystem Archive

by Mohammad Zare ([ORCID 0009-0002-9032-3614](https://orcid.org/0009-0002-9032-3614))

## What this is

This is a research archive of Nick Montfort's generative poem *Taroko Gorge* (2009) and the remixes, rewritings and responses that grew around it. A small Python pipeline collects candidate pages from four seed addresses, records what was fetched, and reconciles the collected pages into distinct works (several addresses can host one poem). The archive treats the surrounding text, such as editors' framing, authors' statements and biographies, as paratext, and records each kind separately.

## What this public repository holds

Counts below are data rows (header excluded) of the files committed here, computed by reading each CSV:

- `seeds/taroko_seed_urls.csv`: 4 seed addresses.
- `data/public/collect_links_log.csv`: 4 rows, one per seed page crawled.
- `data/public/taroko_links.csv`: 61 candidate addresses.
- `data/public/download_log.csv`: 61 fetch attempts (55 succeeded, 4 returned an HTTP error, 2 failed to connect), with content hashes but no content.
- `data/public/inventory.csv`: 55 downloaded pages, each with page title, author guess and a 0-5 heuristic score for how likely it is to be a Taroko-type generator.
- `data/public/lexical_array_summary.csv`: 31 rows giving the name, size and a short hash of each word list found in page source, but not the words.
- `data/public/runtime_sample_log.csv`: 50 rows logging browser runs of the poems (status and timing only).
- `data/public/validation_summary.csv`: 21 pipeline checks.
- the pipeline scripts (`scripts/`) and the working notes (`notes/`; start with [`notes/README.md`](notes/README.md)).

## What is deliberately not public

Raw captured pages, screenshots, runtime text samples, full word arrays and the private research tables stay on the author's machine, because they reproduce other people's works. The public tables describe the corpus; they cannot be used to rebuild it. The v2 layer (48 reconciled work entities, typed paratext records, the v2 query index) is built from those private files and therefore runs only on the local copy. Its design and results are documented in `notes/`, but it cannot be re-run from this repository alone.

What the archive does not claim: it is not a complete census of Taroko remixes; most remix authorship is inferred from page titles and links, not confirmed; the 0-5 score is a keyword heuristic, not a judgement about literary merit; and copyright clearance of third-party works has not been done.

## How to read it

**Source code is the archival object.** For a generative poem, the program is the work. Text that the program prints, or a screenshot of it, is one trace of one run, and the archive keeps it only as supplementary evidence.

**Paratext comes in different kinds.** The archive distinguishes editorial statements (a curator's framing, such as the editors of the Electronic Literature Collection), author statements (the maker writing about the work), biographies (about the person, not the work), project descriptions, and generated output (a trace, not a statement). An early version of the archive counted biographies as author statements. That was corrected, and the correction is documented in [`notes/ERRATA_INQUIRIES_01_TO_04.md`](notes/ERRATA_INQUIRIES_01_TO_04.md) and [`notes/STATEMENT_LAYER_V2_REPORT.md`](notes/STATEMENT_LAYER_V2_REPORT.md). It showed that any pattern drawn from the corpus is only as reliable as the distinctions the corpus makes.

## How to cite

Zare, M. (2026). *Taroko Gorge Ecosystem Archive* (Version 2.0.0) [Computer software and dataset]. https://github.com/mozareeduge/Taroko-Gorge-Ecosystem

## Rights

Code: MIT License (see `LICENSE`). Public metadata tables in `data/public/`: CC0 1.0 Universal. *Taroko Gorge* and all remixes remain the works of their authors; this archive reproduces none of them.

---

## Technical notes

### Install

```bash
pip install -r requirements.txt
```

Playwright is optional and only needed for runtime sampling.

### Pipeline commands

Run the full non-runtime pipeline (needs network access):

```bash
python scripts/run_pipeline.py
```

Other options: `--limit 5` (test run), `--runtime --seconds 10` (runtime sampling, requires Playwright), `--force` (re-download existing files).

Run validation only:

```bash
python scripts/06_validate_corpus.py
```

The v2 scripts (`scripts/13_*.py` to `scripts/21_*.py`) and the query tool `python scripts/20_query_archive_v2.py overview` read the local private layer and will not work on a fresh clone. See [`notes/QUERY_INDEX_V2_GUIDE.md`](notes/QUERY_INDEX_V2_GUIDE.md).

### Public / private boundary

Raw captures and private tables are listed in `.gitignore` and are not committed:

- `archive/raw_html/`, `archive/screenshots/`, `archive/output_samples/`, `archive/extracted_full/`
- `archive/context_pages/`, `archive/context_screenshots/`
- `data/private/`

Only `data/public/*.csv`, scripts, seeds and notes are intended for the public repository. Full detail: [`notes/PUBLIC_PRIVATE_BOUNDARY_V2.md`](notes/PUBLIC_PRIVATE_BOUNDARY_V2.md).

### Local-only paths

| Path | Description |
|------|-------------|
| `archive/raw_html/` | Downloaded HTML/JS source files |
| `archive/screenshots/` | Playwright runtime screenshots |
| `archive/output_samples/` | Visible text samples from runtime |
| `archive/extracted_full/lexical_arrays_full.json` | Full word arrays from source code |
| `data/private/` | Work-entity, statement, lexical-mechanism and query-index tables |

### Scoring (`probable_taroko_score`)

- **0** No evidence
- **1** Mentions Taroko/Gorge only
- **2** JavaScript + Taroko/Gorge
- **3** JavaScript + generator-like function/timer signals
- **4** Known Taroko array/function patterns detected
- **5** Likely direct Taroko source or remix

Score 3 is necessary but not sufficient, and score 0 does not rule out a remix; see [`notes/SCORE_FORMULA.md`](notes/SCORE_FORMULA.md) and [`notes/ARCHIVE_CLAIMS_CORRECTIONS.md`](notes/ARCHIVE_CLAIMS_CORRECTIONS.md).
