> **Superseded** (2026-10-02): 'all 53 fetches failed' describes the offline run only. In the later live run (2026-06-28; see `archive_mvp_v2_live_paratext_run_log.md`) 51 of 53 pages were captured and 3 section entries were marked present.

# ELC Paratext Capture Report

Generated: 2026-06-28

## Summary

Script 13 (`13_collect_context_pages.py`) identified **53 context-page candidates** from:
- 6 known high-priority URLs (ELC3 collection page, ELC3 work page, ELMCIP, nickm.com index, etc.)
- 47 additional URLs from `data/public/taroko_links.csv` and `data/public/inventory.csv`

Script 14 (`14_capture_paratext_pages.py`) attempted to fetch all 53 URLs. All **53 fetches failed** — the archive environment does not have outbound network access. This is an expected failure in the isolated runtime. The capture log (`data/private/context/context_page_capture_log.csv`) records all attempts with `capture_method=failed` and `notes=network_unavailable_in_archive_environment`.

Script 15 (`15_extract_paratext_sections.py`) processed the capture log and wrote output CSVs:
- `elc_paratext_sections.csv`: 53 rows, all with `present=no` (no pages captured to parse)
- `elc_work_metadata.csv`: 0 rows (empty, no pages parsed)
- `elc_download_links.csv`: 0 rows (empty)

## High-Priority URLs Not Captured

| URL | Source Type | Priority |
|-----|-------------|----------|
| https://collection.eliterature.org/3/collection-taroko.html | elc_collection | high |
| https://collection.eliterature.org/3/work.html?work=taroko-gorge | elc_work | high |
| https://elmcip.net/creative-work/taroko-gorge | elmcip | high |
| https://nickm.com/taroko_gorge/ | post_position | high |

Note: dl_0002 in the main archive (`archive/raw_html/0002_*.html`) is the ELC3 collection page successfully fetched in the v1 pipeline. The v2 ELC3 work page (`work.html?work=taroko-gorge`) was not in the v1 download set and could not be fetched in v2.

## What Would Be Extracted (When Network Is Available)

The ELC3 work page for Taroko Gorge typically contains:
- Statement section (explicit author/artist text)
- Author(s) listing
- Bio section
- Year, Language, Keywords metadata
- Tech Details section
- Downloads section (links to executable, source)
- Editorial Statement section

The v2 paratext extraction script (script 15) is ready to process these when the pages are captured in a network-accessible environment.

## Recommendations

To complete paratext capture:
1. Run `python3 scripts/14_capture_paratext_pages.py` in a network-accessible environment
2. Then re-run `python3 scripts/15_extract_paratext_sections.py` to parse the captured HTML
3. Re-run `python3 scripts/19_build_query_index_v2.py` to import results into SQLite
