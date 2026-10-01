# Archive MVP v2 — Final Report

Generated: 2026-06-28

## What the Archive Contains After v2

### Core Holdings (unchanged from v1)
- 55 downloaded HTML files in `archive/raw_html/` (from 61 attempted downloads; 6 failed)
- 50 runtime screenshots in `archive/screenshots/` and text samples in `archive/output_samples/`
- 4 confirmed lexical array extractions in `archive/extracted_full/`
- v1 query index: `data/private/taroko_query_index.sqlite`

### Added in v2

**Work Entity Layer** (48 entities):
- `data/private/work_entities.csv` — distinct poems, not URLs
- `data/private/work_entity_links.csv` — URL-to-entity mapping
- `data/private/work_entity_evidence_matrix.csv` — per-entity evidence inventory

**Statement Layer v2** (corrected taxonomy):
- `data/private/statement_sources_v2.csv` — typed statement evidence
- `data/private/statement_excerpts_safe.csv` — short excerpts (≤50w)

**Lexical Mechanism Audit v2**:
- `data/private/lexical_mechanisms_v2.csv` — per-dl_id classification
- `data/private/lexical_candidates_v2.json` — machine-readable classification

**Context Page Infrastructure**:
- `data/private/context/context_page_candidates.csv` — 53 ELC/ELMCIP/author URLs
- `data/private/context/context_page_capture_log.csv` — capture log (all failed in offline env)
- `data/private/context/elc_paratext_sections.csv` — section presence (pending live capture)

**v2 Query Index**:
- `data/private/taroko_query_index_v2.sqlite` — 16 tables, 244 KB
- CLI: `python3 scripts/20_query_archive_v2.py overview`

**Verification**: All 22 checks pass (`python3 scripts/21_verify_archive_mvp_v2.py`)

## How Work Entities Differ from URLs

A **URL** is a web address. A **work entity** is a distinct poem or work. Multiple URLs may point to the same poem (mirrors: the same poem hosted on nickm.com and the creator's own domain). The v2 archive identifies 48 distinct work entities from 55 inventory entries — the difference is 7 mirror pairs.

## How Statements Are Represented

The v2 statement taxonomy distinguishes:
- `explicit_author_statement`: first-person text from the creator about the work
- `editorial_statement`: text from a curator/editor (e.g., ELC3 editors)
- `project_description`: about-text, not necessarily first-person
- `bio`: author biography (NOT about the specific work)
- `generated_output`: poem runtime output (NOT a statement — just a trace)

Only 1 explicit author statement is confirmed in the archive: Yoko Engorged (Eric Snodgrass, dl_0013 blog post).

## How Paratext Differs from Executable/Source

- **Executable**: the running poem in the browser (JS + HTML)
- **Source**: the JavaScript source code
- **Paratext**: contextual text on a collection/work page (statement, bio, keywords, editorial note)

ELC3 work pages contain paratext. The executables are linked from those pages. The v2 context-page capture scripts (13-15) are designed to fetch and parse paratext. Live capture requires network access.

## Evidence Layer Distinctions

| Layer | What It Is | Local Path |
|-------|-----------|------------|
| URL | Web address | candidates table |
| Download | Fetched HTML | archive/raw_html/ |
| Inventory | Metadata extracted from download | inventory table |
| Runtime | Screenshot + text trace | archive/screenshots/, output_samples/ |
| Lexical | Extracted JS arrays | archive/extracted_full/ |
| Statement | Typed statement evidence | statement_sources_v2.csv |
| Context page | ELC/ELMCIP metadata page | archive/context_pages/ |
| Work entity | Distinct poem/work | work_entities.csv |

## Corrections from Old Inquiries

See `notes/ERRATA_INQUIRIES_01_TO_04.md` and `notes/ARCHIVE_CLAIMS_CORRECTIONS.md` for full corrections. Key corrections:
1. Bio ≠ author statement
2. Editorial statement ≠ author statement
3. Runtime output ≠ statement
4. dl_0013 lexical arrays are WordPress/analytics, not poem vocabulary

## Uncertainties

See `notes/WHAT_REMAINS_UNCERTAIN.md` for full list.

## How to Ask Future Questions

Use `python3 scripts/20_query_archive_v2.py` as the primary interface. See `notes/QUERY_INDEX_V2_GUIDE.md` for command reference.

For evidence questions: always cite the evidence layer (which table, which dl_id, which local path).
