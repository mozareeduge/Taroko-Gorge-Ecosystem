# Public/Private Boundary v2

## Private (Never Commit)

These data types contain potentially copyrighted content, PII risks, or raw captures:

| Data Type | Path | Reason |
|-----------|------|--------|
| Raw HTML downloads | archive/raw_html/ | Copyrighted third-party content |
| Runtime screenshots | archive/screenshots/ | Copyrighted visual output |
| Text output samples | archive/output_samples/ | Copyrighted runtime content |
| Full lexical arrays | archive/extracted_full/ | Copyrighted source vocabulary |
| Context page HTML | archive/context_pages/ | Third-party copyrighted pages |
| Context screenshots | archive/context_screenshots/ | Third-party copyrighted content |
| SQLite databases | data/private/*.sqlite | Contains bulk derived content |
| Work entity files | data/private/work_*.csv | Contains derived/compiled data |
| Statement sources | data/private/statement_sources_v2.csv | Contains citation of third-party text |
| Statement excerpts | data/private/statement_excerpts_safe.csv | Contains short excerpts (borderline) |
| Lexical mechanisms | data/private/lexical_mechanisms_v2.csv | Contains URL-level derived data |
| Context captures | data/private/context/ | Contains derived/captured content |
| Query exports | data/private/query_exports/ | Derived from private data |
| Corpus catalog | data/private/taroko_corpus_catalog.csv | Bulk derived content |
| Archive manifest | data/private/archive_manifest.csv | Bulk derived content |

## Public-Safer (May Commit)

These contain only metadata, counts, URLs, and aggregate information:

| Data Type | Path | Rationale |
|-----------|------|-----------|
| Seed URLs | seeds/taroko_seed_urls.csv | Public URLs only |
| Candidate links | data/public/taroko_links.csv | Public URLs + metadata |
| Download log | data/public/download_log.csv | Status codes + hashes, no content |
| Inventory | data/public/inventory.csv | Boolean signals + scores, no content |
| Lexical array summary | data/public/lexical_array_summary.csv | Array names + counts, no content |
| Runtime sample log | data/public/runtime_sample_log.csv | Paths + status, no content |
| Validation summary | data/public/validation_summary.csv | Aggregate counts |
| All notes/*.md | notes/ | Analysis and documentation |
| All scripts | scripts/ | Pipeline code |
| Agent rules | docs/dev/AGENT_RULES.md | Operational rules (moved from CLAUDE.md) |
| README.md | README.md | Project documentation |

## Borderline Cases

- **Short excerpts (≤50w)** in CSV fields: generally public-safer under fair use for research/archival purposes, but kept private to be conservative
- **SHA256 hashes**: public-safe (no content revealed)
- **Array names** (e.g., "above", "below"): public-safe (single words, not copyrightable)
- **URLs** of failed fetches: public-safe
