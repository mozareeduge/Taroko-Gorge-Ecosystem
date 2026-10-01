# What Can Now Be Asked (v2)

Questions the v2 archive can answer reliably, with the evidence source for each.

## Work Entities

- How many distinct poems are in the Taroko Gorge ecosystem? **48 work entities** (work_entities table)
- Which URLs are mirrors of the same poem? (mirror_pairs table, work_entity_links)
- What is the representation status of each work entity? (work_entities.representation_status)
- Which works have multiple hosting locations? (mirror_pairs table)

## Statements

- Is there an explicit author statement for any work in the archive? Yes — Yoko Engorged (we_0008) in statement_sources_v2.csv
- What type is the ELC3 collection page statement? Editorial (not author) — statement_sources_v2.csv
- Which statements are from ELC3 editors vs. individual authors? (statement_type column in statement_sources)
- Is generated output (runtime traces) a statement? No — classified as `generated_output`

## Lexical Mechanisms

- Which works have confirmed Taroko vocabulary arrays extracted? 4 works (dl_0033, dl_0040, dl_0041, dl_0042) — all Polish remixes
- Is dl_0013's extracted lexical data reliable? No — contaminated with WordPress/analytics arrays
- How many works have probable poem mechanisms but unextracted arrays? ~50

## Downloads and Failures

- How many URLs failed to download? 6 (failures command in script 20)
- Which sites returned 403? ELMCIP (dl_0003, dl_0004)
- Which pages are 404 (dead links)? dl_0021, dl_0047

## Paratext (Conditional on Live Capture)

- What sections does the ELC3 work page for Taroko Gorge contain? (Available after network capture via scripts 14-15)
- Is there a Statement section on the ELC3 work page? (Pending capture)
- What metadata fields are present? (Pending capture)

## Scores

- What is the probable_taroko_score formula? See notes/SCORE_FORMULA.md
- How many works have score 5 (full pattern)? 4 (dl_0033, dl_0040, dl_0041, dl_0042)
- How many have score 3? The majority (~47) of archived works
- What does score 0 mean? No Taroko signals detected (not necessarily non-Taroko)

## Evidence Layer Questions

- What evidence types are present for a given work entity? (evidence_matrix command in script 20)
- Is there a screenshot for a given work? (runtime_samples table, screenshot_path column)
- Is there a source code file for a given work? (extractable if score ≥ 3; the JS is embedded in the HTML)

## Counts and Aggregates (from public CSVs)

- Total URLs in seed list: 61 (taroko_links.csv)
- Total successful downloads: 55 (inventory.csv)
- Total runtime samples: 50 (runtime_sample_log.csv)
- Total lexical array entries: 31 (lexical_array_summary.csv)
