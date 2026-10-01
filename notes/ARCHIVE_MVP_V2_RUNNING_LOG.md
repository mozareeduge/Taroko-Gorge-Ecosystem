# Archive MVP v2 — Running Log

## 2026-06-28

### Phase A — Governance
- Updated CLAUDE.md: appended "v2 Additions" section (rules 11-17) covering evidence layer taxonomy, private/public boundary, citation requirements
- Created notes/ARCHIVE_MVP_V2_PLAN.md
- Created notes/ARCHIVE_MVP_V2_RUNNING_LOG.md (this file)

### Phase B — Audit Files
- Created notes/REPO_STATE_CURRENT.md (branch, git log, file lists, row counts)
- Created notes/SCORE_FORMULA.md (extracted from scripts/03_extract_metadata.py)
- Created notes/LEXICAL_FALSE_POSITIVE_REPORT.md (dl_0013 contamination documented)
- Created notes/ERRATA_INQUIRIES_01_TO_04.md
- Created notes/ARCHIVE_CLAIMS_CORRECTIONS.md
- Created data/private/query_exports/audit_scores.csv (55 rows from inventory.csv + lexical join)
- Created data/private/query_exports/runtime_sampling_audit.csv
- Created data/private/query_exports/notes_count_audit.csv
- Created data/private/query_exports/mirror_pair_hash_comparison.csv

### Phase C — ELC/Context-Page Paratext
- Created scripts/13_collect_context_pages.py
- Created scripts/14_capture_paratext_pages.py
- Created scripts/15_extract_paratext_sections.py
- Created notes/ELC_PARATEXT_CAPTURE_REPORT.md
- Created directories: archive/context_pages/, archive/context_screenshots/, data/private/context/
- RAN script 13: produced data/private/context/context_page_candidates.csv
- RAN script 14: attempted fetch of context pages; results in context_page_capture_log.csv
- RAN script 15: extracted paratext sections

### Phase D — Work-Entity Reconciliation
- Created scripts/16_reconcile_work_entities.py
- Created notes/WORK_ENTITY_RECONCILIATION_REPORT.md
- RAN script 16: produced work_entities.csv, work_entity_links.csv, work_entity_evidence_matrix.csv

### Phase E — Statement Layer v2
- Created scripts/17_build_statement_layer_v2.py
- Created notes/STATEMENT_LAYER_V2_REPORT.md
- RAN script 17: produced statement_sources_v2.csv, statement_excerpts_safe.csv

### Phase F — Lexical Mechanism Audit v2
- Created scripts/18_audit_lexical_mechanisms_v2.py
- Created notes/LEXICAL_MECHANISM_AUDIT_V2.md
- RAN script 18: produced lexical_mechanisms_v2.csv, lexical_candidates_v2.json

### Phase G — Query Index v2
- Created scripts/19_build_query_index_v2.py
- Created scripts/20_query_archive_v2.py
- Created notes/QUERY_INDEX_V2_GUIDE.md
- RAN script 19: built taroko_query_index_v2.sqlite
- RAN script 20 overview: verified table counts

### Phase H — Verification
- Created scripts/21_verify_archive_mvp_v2.py
- RAN script 21: produced notes/ARCHIVE_MVP_V2_VERIFICATION.md

### Phase I — Final Reports
- Created notes/ARCHIVE_MVP_V2_FINAL_REPORT.md
- Created notes/PUBLIC_PRIVATE_BOUNDARY_V2.md
- Created notes/WHAT_CAN_NOW_BE_ASKED.md
- Created notes/WHAT_REMAINS_UNCERTAIN.md

### Phase J — Documentation
- Updated README.md with v2 pointer section
