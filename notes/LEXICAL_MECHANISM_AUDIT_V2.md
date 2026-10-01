# Lexical Mechanism Audit v2

Generated: 2026-06-28  
Source: `scripts/18_audit_lexical_mechanisms_v2.py`

## Summary

Audited 55 inventory entries against 31 lexical_array_summary rows.

| Status | Count |
|--------|-------|
| confirmed_poem_arrays | 4 |
| contaminated_extraction | 1 |
| no_array_evidence | 50 |

## Confirmed Poem Arrays (4)

These dl_ids have arrays matching known Taroko vocabulary variable names:

| dl_id | Title | Array Names |
|-------|-------|-------------|
| dl_0033 | Wąwóz Taroko | above, below, trans, imper, intrans |
| dl_0040 | Wąwóz Kraków | above, below, trans, imper, intrans |
| dl_0041 | Garaż w Tokio | above1, above2, above3, below1, below2, below3, trans, imper, intrans |
| dl_0042 | Oko na Donbas | above1, above2, above3, below1, below2, below3, trans, imper, intrans |

All are Polish-language remixes. Item count per array: 4. These share the Taroko Gorge positional/verb structure (above, below, transitive, imperative, intransitive).

## Contaminated Extraction (1): dl_0013

**URL**: http://exinfoam.wordpress.com/2011/07/18/yoko-engorged/  
**Arrays**: linkElements (1), ccpa_applies (13), s (2)  
**Classification**: `contaminated_extraction`  
**Confidence**: 0.95

All three arrays are WordPress platform/analytics infrastructure. Not poem vocabulary. The Yoko Engorged poem mechanism exists in this page's JS but was not extracted by the array detector (variable names differ from the detector's regex).

## No Array Evidence (50)

Most of the 55 inventory entries (50) have `no_array_evidence`:
- 47 have `probable_taroko_score=3` — these are probable poems but the extractor (script 04) did not find arrays matching the known name regex (`above|below|trans|intrans|imper|stanza|line|words`)
- 3 have `score=0` — no Taroko signals detected
- The original Taroko Gorge (dl_0001, dl_0005) falls in this category because its arrays use different variable names not in the detector regex

## Coverage Gap

The original Taroko Gorge JavaScript uses variable names not detected by the KNOWN_ARRAYS regex. This is a known limitation of the v1 extractor. The 4 confirmed-array works all use the Polish-language remix's explicit `above/below/trans/imper/intrans` naming convention.

## Output Files

| File | Rows |
|------|------|
| data/private/lexical_mechanisms_v2.csv | 55 |
| data/private/lexical_candidates_v2.json | 55 keys |
