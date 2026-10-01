# Lexical False Positive Report

Source files examined:
- `data/public/lexical_array_summary.csv` (31 data rows)
- `data/public/inventory.csv` (55 data rows)

## Summary

Only 4 distinct dl_ids have entries in lexical_array_summary.csv:
- dl_0013 (exinfoam WordPress blog)
- dl_0033 (wawoz_taroko — Wąwóz Taroko)
- dl_0040 (wawoz_krakow — Wąwóz Kraków)
- dl_0041 (garaz_w_tokio — Garaż w Tokio)
- dl_0042 (oko_na_donbas — Oko na Donbas)

## dl_0013 — Confirmed Contamination

**URL**: http://exinfoam.wordpress.com/2011/07/18/yoko-engorged/  
**Arrays extracted**: `linkElements` (1 item), `ccpa_applies` (13 items), `s` (2 items)  
**Classification**: VENDOR/ANALYTICS — confirmed false positives

These are WordPress platform arrays:
- `linkElements`: DOM navigation array
- `ccpa_applies`: California Consumer Privacy Act consent management (WordPress plugin)
- `s`: likely WordPress/analytics tracking object

**None of these are poem vocabulary arrays.** The extractor (script 04) fired because the page contains JavaScript arrays, but they are platform infrastructure, not the Yoko Engorged poem mechanism.

The Yoko Engorged poem vocabulary is present in the HTML but was not extracted as named arrays — likely because it uses different variable name patterns than the detector regex (`above|below|trans|intrans|imper|stanza|line|words`).

**Action**: dl_0013 arrays should be excluded from any analysis of Taroko-ecosystem lexical mechanisms. The `probable_taroko_score` of 3 for dl_0013 is technically correct (it has JS, taroko/gorge words) but should not be interpreted as confirming extraction of poem arrays.

## dl_0033, dl_0040, dl_0041, dl_0042 — Confirmed Poem Arrays

These four dl_ids have arrays named: `above`, `below`, `trans`, `imper`, `intrans` (and variants `above1/2/3`, `below1/2/3` for dl_0041, dl_0042).

These are the core Taroko Gorge vocabulary array names. Each has item_count=4, consistent with small vocabulary sets used in the Polish-language remixes (Wąwóz Taroko, Wąwóz Kraków, Garaż w Tokio, Oko na Donbas). These are confirmed poem arrays.

## Entries with Score ≥ 3 but No Array Extraction

From inventory.csv, 47 of 55 entries have probable_taroko_score=3 but `contains_known_array_names=false`. This means:
- The original dl_0001 (taroko_gorge/) has score 3, not 5 — its arrays use different names
- Most remixes on nickm.com use the same structure as the original but with renamed or differently structured arrays

This is an extractor coverage gap, not evidence of absence.

## Recommendations

1. Mark dl_0013 as contaminated in all lexical analyses
2. Note that score=3 majority reflects detection of setInterval/function patterns, not confirmed array extraction
3. The 4 confirmed-array works (dl_0033, dl_0040, dl_0041, dl_0042) are all Polish-language remixes by the same author cluster
