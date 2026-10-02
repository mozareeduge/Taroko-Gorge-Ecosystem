> **Superseded in part** (2026-10-02): the row count given for `elc_paratext_sections` (53) is from the offline run; the later live run produced 1124 section entries (see `archive_mvp_v2_live_paratext_run_log.md`).

# Query Index v2 — Usage Guide

## Database

`data/private/taroko_query_index_v2.sqlite` (244 KB, 16 content tables + FTS5 index)

## CLI Tool

```
python3 scripts/20_query_archive_v2.py <command> [options]
```

## Commands

### overview
Show row counts for all tables.
```
python3 scripts/20_query_archive_v2.py overview
```

### entities
List all work entities with status columns.
```
python3 scripts/20_query_archive_v2.py entities
```

### entity --id ID
Full details for one work entity including evidence matrix and links.
```
python3 scripts/20_query_archive_v2.py entity --id we_0001
```

### statements
Query the statement layer.
```
python3 scripts/20_query_archive_v2.py statements
python3 scripts/20_query_archive_v2.py statements --work we_0008
python3 scripts/20_query_archive_v2.py statements --type editorial_statement
```

### paratext --work CANDIDATE_ID
Show paratext sections for a context page.
```
python3 scripts/20_query_archive_v2.py paratext --work ctx_0001
```

### evidence --work ENTITY_ID
Show the evidence matrix for a work entity.
```
python3 scripts/20_query_archive_v2.py evidence --work we_0001
```

### lexical
Query lexical mechanism audit.
```
python3 scripts/20_query_archive_v2.py lexical
python3 scripts/20_query_archive_v2.py lexical --work dl_0033
python3 scripts/20_query_archive_v2.py lexical-status confirmed_poem_arrays
```

### mirrors
Show known mirror pairs (same work, multiple URLs or same sha256).
```
python3 scripts/20_query_archive_v2.py mirrors
```

### failures
Show failed downloads from download_log.
```
python3 scripts/20_query_archive_v2.py failures
```

### search --text TEXT
Full-text search across inventory (uses FTS5 index on titles and URLs).
```
python3 scripts/20_query_archive_v2.py search --text "Montfort"
python3 scripts/20_query_archive_v2.py search --text "gorge"
```

### sql --query "SELECT ..."
Run a read-only SELECT query directly (SQL experts only).
```
python3 scripts/20_query_archive_v2.py sql --query "SELECT work_entity_id, canonical_title FROM work_entities WHERE lexical_status='confirmed_poem_arrays'"
```

### export --query QUERY_NAME
Export a named safe query to `data/private/query_exports/export_<name>.csv`.

Available queries:
- `work_entities` — all work entities with status columns
- `evidence_matrix` — full evidence matrix
- `statement_inventory` — statement sources without full excerpts
- `paratext_sections` — ELC paratext sections (if captured)
- `lexical_status` — lexical mechanism audit per dl_id
- `failures_by_work` — failed downloads
- `mirror_relations` — mirror pairs
- `public_safe_metadata` — inventory metadata (title, score, author)

```
python3 scripts/20_query_archive_v2.py export --query work_entities
python3 scripts/20_query_archive_v2.py export --query lexical_status
```

## Tables Available

| Table | Source | Rows |
|-------|--------|------|
| candidates | data/public/taroko_links.csv | 61 |
| downloads | data/public/download_log.csv | 61 |
| inventory | data/public/inventory.csv | 55 |
| lexical_summary | data/public/lexical_array_summary.csv | 31 |
| runtime_samples | data/public/runtime_sample_log.csv | 50 |
| work_entities | data/private/work_entities.csv | 48 |
| work_entity_links | data/private/work_entity_links.csv | 55 |
| work_entity_evidence_matrix | data/private/work_entity_evidence_matrix.csv | 240 |
| context_page_candidates | data/private/context/context_page_candidates.csv | 53 |
| context_page_capture_log | data/private/context/context_page_capture_log.csv | 53 |
| elc_paratext_sections | data/private/context/elc_paratext_sections.csv | 53 |
| statement_sources | data/private/statement_sources_v2.csv | 49 |
| statement_excerpts | data/private/statement_excerpts_safe.csv | 3 |
| lexical_mechanisms | data/private/lexical_mechanisms_v2.csv | 55 |
| audit_scores | data/private/query_exports/audit_scores.csv | 55 |
| mirror_pairs | data/private/query_exports/mirror_pair_hash_comparison.csv | 8 |
