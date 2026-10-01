# Archive MVP v2 — Verification Report
Generated: 2026-06-28T13:25:31Z

**Summary**: 22/22 PASS, 0 FAIL, 0 WARNING

## Check Results

| Status | Check | Detail |
|--------|-------|--------|
| PASS | v1 query index exists | data/private/taroko_query_index.sqlite |
| PASS | v2 query index exists | data/private/taroko_query_index_v2.sqlite |
| PASS | v2 required tables present | all required tables present |
| PASS | inventory non-zero | inventory: 55 rows |
| PASS | downloads non-zero | downloads: 61 rows |
| PASS | work_entities non-zero | work_entities: 48 rows |
| PASS | statement_sources non-zero | statement_sources: 50 rows |
| PASS | lexical_mechanisms non-zero | lexical_mechanisms: 55 rows |
| PASS | context_page_candidates non-zero | data/private/context/context_page_candidates.csv: 53 rows |
| PASS | context_page_capture_log exists | data/private/context/context_page_capture_log.csv: 53 rows (may be 0 if fetch failed) |
| PASS | statement_sources_v2.csv non-zero | data/private/statement_sources_v2.csv: 50 rows |
| PASS | work_entities.csv non-zero | data/private/work_entities.csv: 48 rows |
| PASS | lexical_mechanisms_v2.csv non-zero | data/private/lexical_mechanisms_v2.csv: 55 rows |
| PASS | archive dir: archive/raw_html | archive/raw_html |
| PASS | archive dir: archive/screenshots | archive/screenshots |
| PASS | archive dir: archive/context_pages | archive/context_pages |
| PASS | public CSV non-zero: data/public/taroko_links.csv | data/public/taroko_links.csv: 61 rows |
| PASS | public CSV non-zero: data/public/download_log.csv | data/public/download_log.csv: 61 rows |
| PASS | public CSV non-zero: data/public/inventory.csv | data/public/inventory.csv: 55 rows |
| PASS | public CSV non-zero: data/public/lexical_array_summary.csv | data/public/lexical_array_summary.csv: 31 rows |
| PASS | public CSV non-zero: data/public/runtime_sample_log.csv | data/public/runtime_sample_log.csv: 50 rows |
| PASS | dl_0013 contamination flagged | dl_0013 lexical_status=contaminated_extraction |
