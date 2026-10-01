# Archive MVP v2 — Upgrade Plan

## Overview

The v1 archive (branch: main) established a pipeline for fetching, extracting metadata, sampling runtime output, and indexing the Taroko Gorge remix ecosystem. v2 adds structured work-entity reconciliation, ELC/context-page paratext capture, a statement taxonomy, a lexical mechanism audit, a v2 query index, and corrected inquiry errata.

## Phases

### Phase A — Governance Docs
- Update CLAUDE.md with v2 operational rules (evidence layer taxonomy, private/public boundary, inquiry citation requirements)
- Create this plan file
- Create running log

### Phase B — Audit Files
- Document repo state (branch, git log, file counts)
- Extract and document score formula from script 03
- Lexical false-positive report (dl_0013 contamination)
- Errata for INQUIRY_04 conflations
- Archive claims corrections
- Query-export CSVs: audit_scores, runtime_sampling_audit, notes_count_audit, mirror_pair_hash_comparison

### Phase C — ELC/Context-Page Paratext Capture
- Script 13: identify context-page candidates from existing CSVs + known ELC3 URLs
- Script 14: fetch context pages with requests; playwright fallback; save HTML to archive/context_pages/
- Script 15: extract paratext sections (Statement, Bio, Keywords, etc.) with BeautifulSoup; produce elc_paratext_sections.csv, elc_work_metadata.csv, elc_download_links.csv

### Phase D — Work-Entity Reconciliation
- Script 16: group URLs into distinct work entities (one poem = one entity, regardless of mirror URLs)
- Produce work_entities.csv, work_entity_links.csv, work_entity_evidence_matrix.csv

### Phase E — Statement Layer v2
- Script 17: apply statement taxonomy (explicit_author_statement, editorial_statement, bio, generated_output, etc.)
- Produce statement_sources_v2.csv and statement_excerpts_safe.csv (max 50w excerpts)

### Phase F — Lexical Mechanism Audit v2
- Script 18: classify arrays as confirmed_poem_arrays, ambient_vendor_arrays, contaminated_extraction, etc.
- Explicitly flag dl_0013 contamination
- Produce lexical_mechanisms_v2.csv and lexical_candidates_v2.json

### Phase G — Query Index v2
- Script 19: build taroko_query_index_v2.sqlite from all v2 CSVs
- Script 20: CLI query tool (overview, entities, statements, paratext, evidence, lexical, mirrors, failures, sql, export)

### Phase H — Verification
- Script 21: automated pass/fail checks for all v2 outputs
- Produce ARCHIVE_MVP_V2_VERIFICATION.md

### Phase I — Final Reports
- ARCHIVE_MVP_V2_FINAL_REPORT.md
- PUBLIC_PRIVATE_BOUNDARY_V2.md
- WHAT_CAN_NOW_BE_ASKED.md
- WHAT_REMAINS_UNCERTAIN.md

### Phase J — Documentation
- Update README.md with v2 pointer
