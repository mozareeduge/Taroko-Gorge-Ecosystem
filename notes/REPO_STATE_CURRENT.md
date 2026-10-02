> **Historical snapshot (2026-06-28)** (2026-10-02): the `archive-mvp-v2` branch and the commit hashes below no longer exist; all work is on `main`. Kept for the record of what was built in v2.

# Repository State — Current

**Branch (historical)**: archive-mvp-v2 (deleted)  
**As of**: 2026-06-28

## Recent Git Log (--oneline -5)

```
f04e1df chore: update ARCHIVE_QUERY_VERIFICATION.md from inquiry 04 verification run
b7a1f6b docs: add Taroko statement inventory inquiry
3672a62 docs: add Taroko inquiry 02 and 03 reports
4cf4255 feat: add Taroko archive inquiry workbench
d0ae199 feat: merge full archive into inquiry workbench branch
```

## Scripts (scripts/)

Pipeline scripts (01-12) + utils + run helpers:
- 01_collect_links.py
- 02_download_pages.py
- 03_extract_metadata.py
- 04_extract_lexical_arrays.py
- 05_runtime_sample.py
- 06_validate_corpus.py
- 06_validate_private.py
- 07_build_corpus_catalog.py
- 08_build_manifest.py
- 09_build_zip.py
- 10_build_query_index.py
- 11_query_archive.py
- 12_verify_archive_package.py
- utils_module.py
- __init__.py
- run_pipeline.py
- run_pipeline_full.py

v2 scripts added:
- 13_collect_context_pages.py
- 14_capture_paratext_pages.py
- 15_extract_paratext_sections.py
- 16_reconcile_work_entities.py
- 17_build_statement_layer_v2.py
- 18_audit_lexical_mechanisms_v2.py
- 19_build_query_index_v2.py
- 20_query_archive_v2.py
- 21_verify_archive_mvp_v2.py

## Notes Files (notes/)

| File | Lines |
|------|-------|
| AUTOMATED_GITHUB_RUN.md | 38 |
| RUN_REPORT.md | 42 |
| ARCHIVE_QUERY_VERIFICATION.md | 44 |
| METHOD.md | 54 |
| HANDOFF.md | 56 |
| GITHUB_ACTIONS_RUN_GUIDE.md | 72 |
| FULL_ARCHIVE_README.md | 81 |
| INQUIRY_02_GROUND_TO_PROXY_TRANSFORMATION.md | 96 |
| CLAUDE_ARCHIVE_INQUIRY_PROTOCOL.md | 97 |
| ARCHIVE_QUERY_GUIDE.md | 122 |
| INQUIRY_03_PROCEDURAL_RHETORIC_POETICS.md | 124 |
| INQUIRY_04_POEM_STATEMENTS_AND_CONTEXTS.md | 265 |

v2 notes added:
- ARCHIVE_MVP_V2_PLAN.md
- ARCHIVE_MVP_V2_RUNNING_LOG.md
- REPO_STATE_CURRENT.md (this file)
- SCORE_FORMULA.md
- LEXICAL_FALSE_POSITIVE_REPORT.md
- ERRATA_INQUIRIES_01_TO_04.md
- ARCHIVE_CLAIMS_CORRECTIONS.md
- ELC_PARATEXT_CAPTURE_REPORT.md
- WORK_ENTITY_RECONCILIATION_REPORT.md
- STATEMENT_LAYER_V2_REPORT.md
- LEXICAL_MECHANISM_AUDIT_V2.md
- QUERY_INDEX_V2_GUIDE.md
- ARCHIVE_MVP_V2_VERIFICATION.md
- ARCHIVE_MVP_V2_FINAL_REPORT.md
- PUBLIC_PRIVATE_BOUNDARY_V2.md
- WHAT_CAN_NOW_BE_ASKED.md
- WHAT_REMAINS_UNCERTAIN.md

## data/public/ CSVs (row counts include header)

| File | Lines (incl. header) | Data rows |
|------|---------------------|-----------|
| collect_links_log.csv | 5 | 4 |
| download_log.csv | 62 | 61 |
| inventory.csv | 56 | 55 |
| lexical_array_summary.csv | 32 | 31 |
| runtime_sample_log.csv | 51 | 50 |
| taroko_links.csv | 62 | 61 |
| validation_summary.csv | 22 | 21 |

## data/private/ Files

- taroko_query_index.sqlite (v1 query index)
- taroko_corpus_catalog.csv
- archive_manifest.csv
- taroko_query_index_v2.sqlite (v2, added in this phase)
- work_entities.csv
- work_entity_links.csv
- work_entity_evidence_matrix.csv
- statement_sources_v2.csv
- statement_excerpts_safe.csv
- lexical_mechanisms_v2.csv
- lexical_candidates_v2.json
- context/ (directory)
- query_exports/ (directory)

## archive/ Item Counts

- raw_html/: 55 files (HTML downloads)
- screenshots/: varies (Playwright captures)
- output_samples/: varies (text traces)
- extracted_full/: lexical arrays JSON
- context_pages/: added in v2
- context_screenshots/: added in v2
