> **Superseded in part** (2026-10-02): the 'Paratext Sections' and 'ELC3 vs ELMCIP' items assume no context page was captured. In the later live run (2026-06-28; see `archive_mvp_v2_live_paratext_run_log.md`) 51 of 53 pages were captured; the ELMCIP pages (dl_0003, dl_0004) still returned HTTP 403. Other uncertainties (authorship, original array structure, rights) are unchanged.

# What Remains Uncertain (v2)

## Author Attribution

Most remix authors are listed as "Unknown" in work_entities.csv. The local archive has title tags, URL slug patterns, and the nickm.com index page's link text (which often names the author), but does not have structured author metadata extracted from all pages. The ELC3 work pages (not captured) would resolve this for the ~30 works in the ELC3 collection.

**Evidence needed**: ELC3 work page capture (`scripts/14_capture_paratext_pages.py` in network-accessible environment).

## Paratext Sections

The ELC3 work page for Taroko Gorge and each individual remix almost certainly contains structured paratext (Statement, Bio, Keywords, Tech Details, etc.). None of this was captured because all 53 context-page fetches failed (no network in archive environment).

**Evidence needed**: Live fetch via `python3 scripts/14_capture_paratext_pages.py`.

## Original Taroko Gorge Lexical Structure

The original Taroko Gorge (dl_0001, dl_0005) has score 3 but `no_array_evidence` because the array variable names don't match the detector regex. The actual vocabulary is in the HTML but was not extracted. The poem's variable names are documented in secondary literature but were not programmatically confirmed from the local file.

**Evidence needed**: Read the actual JS from `archive/raw_html/0001_*.html` programmatically and identify the array names.

## Most Remix Authors

For ~40 of 48 work entities, authorship is inferred only from URL slugs, title tags, and the nickm.com index link text. None have been confirmed against the ELC3 work pages or ELMCIP records.

## dl_0013 Poem Mechanism

Yoko Engorged (dl_0013, exinfoam blog post) has a confirmed author statement but the poem's actual JavaScript arrays were not extracted. The vocabulary replacement method is described in the statement but not programmatically verified.

## Works with Score 0

Four works have `probable_taroko_score=0` (dl_0010, dl_0023, dl_0051, dl_0057, dl_0058). These may still be Taroko remixes with different vocabulary than the detector regex expects, or they may be context pages or unrelated files.

## Rights Status

Copyright status of all remixes is unresolved. The archive treats all third-party content as private. Fair use analysis for short excerpts has not been conducted.

## ELC3 vs ELMCIP Discrepancies

The ELMCIP record for Taroko Gorge (dl_0003, dl_0004) returned 403 in the v1 download. It may contain different metadata than ELC3. No comparison is possible without successful capture.

## Mirror Pair sha256 Matching

The sha256-based mirror detection in `mirror_pair_hash_comparison.csv` found no exact matches. The 6 identified mirror pairs were found by title/URL pattern matching. It is possible that some page pairs serve identical content but were not matched (e.g., due to different whitespace or encoding).
