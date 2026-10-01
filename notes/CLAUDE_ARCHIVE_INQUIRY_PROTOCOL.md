# Claude Archive Inquiry Protocol

Instructions for a Claude session working with this archive.

## What This Archive Contains

This is a research archive of Nick Montfort's *Taroko Gorge* (2009) and its remixes.
It contains 61 candidate URLs. Pipeline run date: see `notes/RUN_REPORT.md`.

Key counts (see `data/private/taroko_query_index.sqlite` / `archive_summary` table):
- 55 successful downloads, 6 failed
- 55 inventory records with Taroko scores
- 31 lexical array records
- 50 runtime samples, 50 screenshots
- 174 manifest rows

## Mandatory Rules for This Session

1. **Do not re-run the archive pipeline.** The data is already collected.
2. **Do not crawl the web.** All source material is in `archive/raw_html/`.
3. **Do not modify archive contents.** Read only.
4. **Do not read raw HTML files one by one manually.** Use the query index.
5. **Do not print long raw outputs.** Use preview columns and short summaries.
6. **Do not store or echo full HTML content.** Reference by path only.
7. **Keep responses under 250 words** unless the researcher asks for detail.

## How to Answer Researcher Questions

### "What works are in the archive?"
```bash
python scripts/11_query_archive.py overview
python scripts/11_query_archive.py sql "SELECT id, url, probable_taroko_score FROM inventory ORDER BY probable_taroko_score DESC"
```

### "Which works have the strongest Taroko pattern?"
```bash
python scripts/11_query_archive.py sql "SELECT id, url, array_names FROM inventory WHERE probable_taroko_score >= 4"
```

### "What word arrays does [work] use?"
```bash
python scripts/11_query_archive.py arrays <id>
```

### "What words are in the [array] array of [work]?"
```bash
python scripts/11_query_archive.py array <id> <array_name>
```

### "Why did [URL] fail?"
```bash
python scripts/11_query_archive.py failures
python scripts/11_query_archive.py work <id>
```

### "What does the live rendering look like?"
- Screenshot path: `python scripts/11_query_archive.py paths <id>`
- Text trace: `python scripts/11_query_archive.py work <id>` (see text_sample_path)
- Do NOT render pages live. Reference the archived screenshot and text trace.

### "Search for a term across the archive"
```bash
python scripts/11_query_archive.py find "<term>"
```

### "What files exist for work X?"
```bash
python scripts/11_query_archive.py paths <id>
```

## Building or Rebuilding the Index

If the SQLite index is missing or stale:
```bash
python scripts/10_build_query_index.py
```

## Verifying Integrity

```bash
python scripts/12_verify_archive_package.py
```

Output: `notes/ARCHIVE_QUERY_VERIFICATION.md`

## What the Index Does NOT Contain

The index stores metadata, paths, previews (500 chars), and checksums only.
- Full raw HTML → read from `archive/raw_html/<path>`
- Full runtime text → read from `archive/output_samples/<path>`
- Full lexical arrays → `archive/extracted_full/lexical_arrays_full.json`

## Archive Is the Authoritative Source

For generative works, the JavaScript source code in `archive/raw_html/` is the
primary archival object. Runtime samples are supplementary execution traces.
The source code encodes all possible outputs; a screenshot captures one moment.
