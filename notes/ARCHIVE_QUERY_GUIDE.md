# Archive Query Guide

A non-technical researcher's guide to using the Taroko Gorge archive inquiry workbench.

## What the Workbench Provides

The archive contains 61 candidate URLs collected from seed sources related to Nick Montfort's
*Taroko Gorge* (2009) and its remixes. The workbench gives you structured access to:

- Which URLs were found and where they came from
- Which ones downloaded successfully, which failed and why
- Which works match the Taroko Gorge source pattern (score 0–5)
- What JavaScript word arrays each work contains
- Screenshots and text traces from live rendering
- SHA256 checksums for every archived file

## Getting Started

You need Python 3.9+ and the archive files present locally. First build the index:

```bash
python scripts/10_build_query_index.py
```

This reads all CSV files and builds `data/private/taroko_query_index.sqlite`.

Then query it:

```bash
python scripts/11_query_archive.py overview
```

## Common Tasks

### See overall archive statistics
```bash
python scripts/11_query_archive.py overview
```

### Search for a term across all metadata
```bash
python scripts/11_query_archive.py find "nature"
python scripts/11_query_archive.py find "rockfall"
python scripts/11_query_archive.py find "elmcip"
```

### Look up a specific work by ID
```bash
python scripts/11_query_archive.py work inv_0001
```

### See the word arrays for a work
```bash
python scripts/11_query_archive.py arrays inv_0001
```

### See all items in one specific array
```bash
python scripts/11_query_archive.py array inv_0001 N
```

### See all failed downloads
```bash
python scripts/11_query_archive.py failures
```

### See runtime sampling status
```bash
python scripts/11_query_archive.py runtime
```

### See all files archived for a work
```bash
python scripts/11_query_archive.py paths inv_0001
```

### Run a custom SQL query (read-only)
```bash
python scripts/11_query_archive.py sql "SELECT id, url, probable_taroko_score FROM inventory WHERE probable_taroko_score >= 4"
```

### Export results to CSV
```bash
python scripts/11_query_archive.py export failures failures.csv
python scripts/11_query_archive.py export overview overview.csv
```

Exports go to `data/private/query_exports/`.

## Score Guide

The `probable_taroko_score` column (0–5) indicates how closely a work matches the
Taroko Gorge source pattern:

| Score | Meaning |
|-------|---------|
| 5 | Full Taroko pattern: known arrays (N, V, A, etc.) + generative JS structure |
| 4 | Strong match: most key arrays present |
| 3 | Moderate match: some key arrays, likely a remix |
| 2 | Weak match: a few array names present |
| 1 | Minimal signal |
| 0 | No Taroko pattern detected |

## What Is NOT in the Index

The index stores metadata, paths, checksums, and short previews. It does NOT store:

- Full raw HTML content (too large; use the file paths to read directly)
- Full runtime text captures (>500 char preview stored; use `text_sample_path`)
- Full lexical arrays inline (use `array` command or read `archive/extracted_full/lexical_arrays_full.json`)

## File Locations

| What | Where |
|------|-------|
| Raw HTML source files | `archive/raw_html/` |
| Screenshots | `archive/screenshots/` |
| Runtime text traces | `archive/output_samples/` |
| Full JS arrays (JSON) | `archive/extracted_full/lexical_arrays_full.json` |
| SQLite index | `data/private/taroko_query_index.sqlite` |
| Query exports | `data/private/query_exports/` |
| Zip package | `private_archive/taroko_full_archive.zip` |
