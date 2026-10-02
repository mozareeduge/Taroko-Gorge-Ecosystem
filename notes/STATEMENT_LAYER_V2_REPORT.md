> **Superseded** (2026-10-02): the counts in this report (1 explicit author statement; ELC3 work page 'unresolved/not captured') are from the offline run. A later live-capture run (2026-06-28; see `archive_mvp_v2_live_paratext_run_log.md`) captured 51 of 53 context pages and recorded 2 `explicit_author_statement` rows, 1 `editorial_statement` and 1 `project_description` in the local statement layer. The origin of the second author-statement row (a captured context page) has not been re-audited in this public repository, because the private tables are not committed. The corrected taxonomy it describes still stands.

# Statement Layer v2 Report

Generated: 2026-06-28  
Source: `scripts/17_build_statement_layer_v2.py`

## Summary

The v2 statement layer applies a corrected taxonomy to all statement-type evidence in the archive.

## Statement Types Found

| Type | Count | Notes |
|------|-------|-------|
| explicit_author_statement | 1 | dl_0013 (Yoko Engorged, Eric Snodgrass) |
| editorial_statement | 1 | dl_0002 (ELC3 collection page, ELO editors) |
| project_description | 1 | dl_0018 (Designer Gulch, Brendan Howell) |
| unresolved | 1 | ELC3 work page for Taroko Gorge (not captured) |
| generated_output | 45 | Runtime traces from runtime_sample_log.csv |

## Key Statement Details

### Explicit Author Statement: Yoko Engorged (we_0008)
- **Source**: `archive/output_samples/dl_0013_sample.txt`
- **Author**: Eric Snodgrass (exinfoam)
- **Confidence**: High
- **Copyright risk**: Medium (reproduced text)
- **Excerpt (≤50w)**: "Ever wondered what would happen if you took the playful and free spirited method to be found in Yoko Ono's Fluxus writings and forced upon it the perhaps also liberating but rather more sordid and mechanical approach"

### Editorial Statement: ELC3 Collection Page (we_0002)
- **Source**: `archive/output_samples/dl_0002_sample.txt`
- **Author**: ELO Editorial (not Nick Montfort)
- **Confidence**: High
- **Excerpt (≤50w)**: "Inspired by a visit to Taroko Gorge in Taiwan, Nick Montfort's modest, procedurally-generated poem has produced an entire subgenre of remixes, remakes, constrained writing experiments, and parodies."

## Taxonomy Corrections from v1

v1 inquiry 04 conflated:
- Bio text → now `bio` (not `explicit_author_statement`)
- Editorial text → now `editorial_statement` (not generic "statement")
- Runtime output → now `generated_output` (not any form of statement)
- Tech details → now `metadata_only` or `project_description`

## Output Files

| File | Rows |
|------|------|
| data/private/statement_sources_v2.csv | 49 |
| data/private/statement_excerpts_safe.csv | 3 (explicit_author, editorial, project_desc) |
