> **Superseded in part** (2026-10-02): the `context_page_pending` status for we_0001 reflects the offline run; a later live capture was run on 2026-06-28 (see `archive_mvp_v2_live_paratext_run_log.md`).

# Work Entity Reconciliation Report

Generated: 2026-06-28  
Source: `scripts/16_reconcile_work_entities.py`

## Summary

The v1 archive treated each URL as a separate entry. The v2 reconciliation groups URLs into **48 distinct work entities** from 55 inventory entries and 61 download log entries.

## Key Findings

### Mirror Pairs (same work, multiple URLs)

| Work Entity | dl_ids | Notes |
|-------------|--------|-------|
| we_0004 GORGE (J.R. Carpenter) | dl_0007, dl_0008 | nickm.com and luckysoap.com — same poem |
| we_0008 Yoko Engorged | dl_0012, dl_0013 | dl_0012 = executable, dl_0013 = blog post |
| we_0028 Hey Gorgeous | dl_0035, dl_0036 | nickm.com and tinysubversions.com |
| we_0039 Kanjono Taroko | dl_0049, dl_0050 | nickm.com and inthescales.com |
| we_0042 Gorge of Anathema | dl_0053, dl_0054 | nickm.com and multimodalmel.com |
| we_0047 Taroko Gary Revisited | dl_0059, dl_0060 | nickm.com and iloveepoetry.org |
| we_0001 Taroko Gorge (original) | dl_0001, dl_0005 | index + original.html (same poem, two entry points) |

### Representation Status

- **archived**: 47 of 48 entities have at least one successful download (status_code=200)
- **failed_or_absent**: 1 entity (ELMCIP entries, status 403)

### Statement Status

- `author_statement_present`: 1 (we_0008 Yoko Engorged)
- `editorial_statement_present`: 1 (we_0002 ELC3 collection page)
- `context_page_pending`: 1 (we_0001 Taroko Gorge, pending ELC3 work page capture)
- `not_found`: 45 entities — no statement evidence in local archive

### Lexical Status

- `confirmed_poem_arrays`: 4 entities (Polish remixes: Wąwóz Taroko, Wąwóz Kraków, Garaż w Tokio, Oko na Donbas)
- `contaminated_vendor_arrays`: 1 (we_0008 Yoko Engorged — WordPress arrays extracted, not poem)
- `not_extracted`: 43 entities — probable poem mechanism but arrays not extracted

### Output Files

| File | Rows |
|------|------|
| data/private/work_entities.csv | 48 |
| data/private/work_entity_links.csv | 55 |
| data/private/work_entity_evidence_matrix.csv | 240 (5 evidence types × 48 entities) |

## Notes

- Author attribution is partial. Most remix authors are listed as "Unknown" because the local archive has title tags and URL patterns but not structured author metadata.
- The ELC3 collection page (we_0002) is an editorial context page, not a poem itself.
- The ELC3 main index (we_0048, dl_0061) is similarly not a poem.
