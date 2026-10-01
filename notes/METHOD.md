# Methodology — Taroko Gorge Ecosystem Archive

## Seed Selection

Four seeds chosen to cover: original work (nickm.com), institutional collection (ELC3), research database (ELMCIP), and direct source attachment (ELMCIP HTML copy).

## Link Collection (01_collect_links.py)

- Fetch each seed page once (no recursion).
- Parse `<a href>` with BeautifulSoup.
- Normalize relative URLs.
- Filter by domain-specific heuristics: Taroko/gorge keywords, known remix patterns, attachment paths.
- Skip binary assets, social share links, CSS/JS/image files.
- All four seed URLs are always included regardless of link extraction.

## Download Provenance (02_download_pages.py)

- Deduplicate URLs before downloading.
- Store each file in `archive/raw_html/` with a deterministic slug filename.
- Record URL, status code, content-type, sha256, byte size, and timestamp.
- Skip binary content-types.
- No overwrite without `--force`.

## Metadata Extraction (03_extract_metadata.py)

- Read only local files referenced in download_log.csv.
- Extract: title tag, h1, meta author, JavaScript presence, script count.
- Score 0–5 using deterministic keyword/pattern matching.
- No LLM extraction.

## Lexical Array Extraction (04_extract_lexical_arrays.py)

- Process only files with score >= 3.
- Regex-detect JavaScript array declarations.
- Public output: array name, item count, sha256 hash of content only (no full items).
- Full arrays saved to `archive/extracted_full/` (Git-ignored).

## Optional Runtime Sampling (05_runtime_sample.py)

- Requires Playwright; gracefully exits if not installed.
- Opens original URL in headless Chromium, waits N seconds, captures screenshot and body text.
- Saved to Git-ignored directories.
- Runtime text is a trace of one execution — not the complete poem.

## Limitations

- Link collection is keyword-heuristic, not comprehensive.
- Some remixes may be hosted without Taroko/Gorge in URL or link text.
- JavaScript array detection misses obfuscated or dynamically loaded code.
- Runtime sampling requires network access to original URLs.

## Future Casebook Use

`data/public/inventory.csv` with probable_taroko_score can be used to select candidates for detailed casebook entries. `archive/extracted_full/lexical_arrays_full.json` provides the raw vocabulary for computational analysis (local-only).
