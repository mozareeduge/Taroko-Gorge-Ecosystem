# Agent rules (formerly CLAUDE.md) — Taroko Gorge Ecosystem Archive

## Operational Rules

1. **Build deterministic scripts.** No randomness, no LLMs in extraction. Results must be reproducible given the same inputs.

2. **Avoid manual corpus reading.** Do not read or summarize downloaded HTML content directly. Process files programmatically.

3. **No recursive crawling.** Fetch only explicitly listed URLs. Do not follow links from downloaded pages automatically.

4. **Public repo safety.** This repo is public. Never commit files from:
   - `archive/raw_html/`
   - `archive/screenshots/`
   - `archive/output_samples/`
   - `archive/extracted_full/`
   - `data/private/`
   Only commit scripts, seeds, `data/public/*.csv`, `data/public/*.md`, notes, and README.

5. **Generated samples are traces, not the poem.** Runtime output from a generative work is one execution trace. The source code is the archival object.

6. **Short responses.** Keep chat replies under 250 words. Use the compact FINAL RESPONSE FORMAT.

7. **No commit/push without approval.** Never run `git commit` or `git push` unless explicitly asked.

8. **Fix and retry policy.** If a script fails, fix with minimal diff and retry. Maximum 2 fix attempts per phase. After 2 failures, write the exact blocker to `notes/RUN_REPORT.md` and stop.

9. **Long output goes to log.** Redirect verbose output to `notes/last_run.log` and inspect only summary/tail.

10. **No heavy dependencies.** Use only `requests`, `beautifulsoup4`, and optionally `playwright`. No databases, Docker, paid APIs, or heavy frameworks.

## Module Import Pattern

All scripts use:
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils
```

The utility module is `scripts/utils_module.py` (not `00_utils.py`).

## v2 Additions

11. **Use workbench/query tools before raw file inspection.** Run `scripts/20_query_archive_v2.py` or `scripts/11_query_archive.py` before reading individual files. Only inspect specific raw files when a query confirms they are the relevant target.

12. **Distinguish evidence layer types.** The archive contains distinct layer types; treat them differently:
    - **URL**: a web address (may be dead or alive)
    - **work entity**: a distinct poem or source work (one entity may have multiple URLs)
    - **context page**: ELC/ELMCIP/author-page metadata page (not the executable)
    - **executable**: the running poem (JavaScript in browser)
    - **source**: the JS/HTML source code file
    - **statement**: explicit author/artist/editorial text about the work
    - **runtime**: a screenshot or text capture of one execution
    - **screenshot**: a visual capture (one trace, not the work itself)
    - **failure**: a URL that returned an error or was blocked

13. **No broad manual raw_html browsing.** Do not read or iterate through `archive/raw_html/` files directly. Use the query index or programmatic extraction scripts.

14. **Counts from commands only.** Report file counts and row counts using `wc -l`, `ls | wc -l`, or SQL COUNT queries. Never estimate or guess counts.

15. **Short excerpts only.** Maximum 50 words in any CSV field containing text excerpts from external sources. Paraphrases max 60 words.

16. **Private/public boundary:**
    - **Private** (never commit): `archive/raw_html/`, `archive/screenshots/`, `archive/output_samples/`, `archive/extracted_full/`, `archive/context_pages/`, `archive/context_screenshots/`, `data/private/`, bulk lexical arrays, full HTML captures
    - **Public-safer** (may commit): aggregate counts, titles, URLs, section presence flags, short excerpts (≤50w), `data/public/*.csv`, `notes/*.md`, scripts

17. **Every inquiry must cite evidence.** Each factual claim in inquiry reports must cite a local file path, table name, SQL query result, or specific evidence layer. No unanchored assertions.
