# Inquiry 03 — Procedural Rhetoric-Poetics of the Archive Pipeline

Generated: 2026-06-27

## Research Question

What is the Taroko archive pipeline as a rhetorical and poetic apparatus — not as neutral infrastructure but as a sequence of acts that construct the archive's epistemic claims and preserve its literary encounter?

## Two Pressures in One Apparatus

The pipeline operates under two simultaneous pressures that are in structural tension:

**Procedural rhetoric** (Ian Bogost's term): The pipeline makes claims through its rules. Each script enacts an argument about what counts as evidence, what is authentic, what is a Taroko Gorge work. The `probable_taroko_score` is not a neutral measurement — it is a rhetorical act that defines the corpus.

**Procedural poetics**: The pipeline is also a literary apparatus. It preserves generative works not as static documents but as executable objects. The runtime sample is a trace of a poem being performed. The screenshot is a temporal witness.

These two pressures cannot be resolved — they are both operating simultaneously in every script. The pipeline is methodologically credible *and* literarily sensitive by design.

## Stage-by-Stage Analysis

### Stage 01 — collect_links (Rhetorical Foundation)
**Operation:** Crawl four seed URLs, extract anchor hrefs, filter for probable Taroko candidates.  
**Rhetorical act:** Defines the corpus boundary. The seed selection (nickm.com, ELO, ELMCIP) is an argument about authoritative lineage — these sources are treated as legitimate archival authorities.  
**Poetic dimension:** The link list is a bibliography-before-reading. It names works before encountering them.  
**Residue:** `data/public/taroko_links.csv` — 61 candidate URLs, each with `candidate_id`, `source_page`, `link_text`.

### Stage 02 — download_pages (Material Capture)
**Operation:** HTTP GET each candidate URL, write raw HTML to `archive/raw_html/`, log status.  
**Rhetorical act:** Six failures (403, 404, DNS, connection) are not erasures — they are documented absences. The download log makes inaccessibility a data point, not a silence.  
**Poetic dimension:** The raw HTML is the poem's material substrate. Downloading it is an act of custody, not reading.  
**Residue:** `data/public/download_log.csv` — 55 successful, 6 failed. Raw HTML in `archive/raw_html/`.

### Stage 03 — extract_metadata (Scoring as Argument)
**Operation:** Parse HTML, extract title, detect JavaScript, score 0–5 by KNOWN_ARRAYS regex and generator signals.  
**Rhetorical act:** The `probable_taroko_score` is the pipeline's central epistemic claim. Score 5 means: this work has the gorge vocabulary, JavaScript, a generator pattern, and named arrays in the standard Taroko set. This is a falsifiable claim — one that can be checked against the source.  
**Poetic dimension:** The score is a reading without interpretation. It counts signals without understanding them. This is deliberate: the pipeline avoids subjective literary judgment.  
**Residue:** `data/public/inventory.csv` — 55 rows with scores, titles, array name detection flags.

### Stage 04 — extract_lexical_arrays (The Lexical Turn)
**Operation:** For works scoring ≥3, extract JS arrays by regex (`ARRAY_PATTERN`), serialize items to JSON.  
**Rhetorical act:** Array extraction makes the vocabulary of each work legible as data. The items become countable, comparable, hashable. This is the pipeline's strongest methodological claim: that a generative poem's identity is substantially carried by its lexical arrays.  
**Poetic dimension:** The array items are not the poem — they are the poem's material. A word in an array is a potential, not an utterance. Extraction freezes the potential without realizing it.  
**Residue:** `archive/extracted_full/lexical_arrays_full.json` — 31 array records across 5 works. `data/public/lexical_array_summary.csv`.  
**Limitation noted:** Only 5 of 55 works yield extracted arrays. Works using non-standard array names are invisible to this stage. This is a documented methodological boundary, not a failure.

### Stage 05 — runtime_sample (The Poetic Witness)
**Operation:** Launch Playwright headless Chromium, navigate to each score-3+ URL, capture screenshot and visible text after 3 seconds.  
**Rhetorical act:** The runtime sample proves the work was alive — executable, not merely present. A screenshot at a specific timestamp is evidence of a generative event.  
**Poetic dimension:** The 3-second wait is an editorial judgment — long enough to let the generator run, short enough to capture a moment, not a scroll. Each runtime sample is one reading of an infinite poem.  
**Residue:** `archive/screenshots/` — 50 PNG files. `archive/output_samples/` — 50 text traces. `data/public/runtime_sample_log.csv`.  
**Anomaly:** dl_0037 runtime output is hex ASCII — the poem produces machine-readable encoding as surface text. The runtime sample captures this encoding faithfully without interpreting it.

### Stage 06 — validate_private (Integrity Claim)
**Operation:** 21 automated checks: directory existence, file counts, CSV row counts, JSON existence, catalog and manifest presence, zip, runtime, screenshots.  
**Rhetorical act:** Validation is the pipeline's self-audit. It makes the archive's completeness a checkable claim. Failures produce a FAIL exit code and stop the pipeline — integrity is non-negotiable.  
**Poetic dimension:** The validation report is a certificate of witness. It says: at this timestamp, the archive was complete.  
**Residue:** `notes/RUN_REPORT.md` — validation output with PASS/FAIL per check.

### Stage 07 — build_corpus_catalog (Integration)
**Operation:** Join all pipeline outputs (links, downloads, inventory, arrays, runtime) into a single per-URL catalog.  
**Rhetorical act:** The catalog is the pipeline's unified claim about each work — all evidence assembled in one row. It is the archive's primary research interface.  
**Poetic dimension:** Joining tables is an act of synthesis. The catalog does not read the poems; it describes the archive's knowledge of them.  
**Residue:** `data/private/taroko_corpus_catalog.csv`.

### Stage 08 — build_manifest (SHA256 Chain)
**Operation:** Walk all archive files, compute SHA256 checksums, record path, size, category, source URL.  
**Rhetorical act:** The manifest is a cryptographic proof of integrity. Any modification to any archived file will break the SHA256 chain. This is the archive's strongest evidentiary claim.  
**Poetic dimension:** Each file's SHA256 is a fingerprint of a moment — the moment the poem was captured. The manifest is a chain of fingerprints.  
**Residue:** `data/private/archive_manifest.csv` — 174 rows.

### Stage 09 — build_zip (Packaging)
**Operation:** Bundle all archive contents into `private_archive/taroko_full_archive.zip`.  
**Rhetorical act:** The zip is the archive as object — portable, transferable, depositable. It makes the archive a discrete research artifact.  
**Poetic dimension:** Compression is the last act of the pipeline. The poems are sealed.  
**Residue:** `private_archive/taroko_full_archive.zip`.

### Stage 10 — build_query_index (Inquiry Surface)
**Operation:** Load all CSVs and JSON into SQLite, build FTS5 full-text search index, compute archive summary statistics.  
**Rhetorical act:** The query index makes the archive interrogable without opening files. It separates inquiry from custody.  
**Poetic dimension:** FTS5 search over poem titles, array names, and runtime text previews is a new kind of reading — pattern-matching across the corpus without encountering any single poem directly.  
**Residue:** `data/private/taroko_query_index.sqlite` — 10 tables + FTS5 virtual table.

### Stage 11 — query_archive (Research Interface)
**Operation:** CLI tool with 12 commands: overview, find, work, arrays, array, failures, runtime, manifest, paths, sql, export, raw-search.  
**Rhetorical act:** The CLI makes the archive's claims portable — any researcher with the SQLite file can reproduce every query in this inquiry series.  
**Poetic dimension:** `find <term>` over FTS5 is reading without reading. `array <id> <name>` surfaces the poem's vocabulary without generating the poem.  
**Residue:** `data/private/query_exports/inquiry_*.csv` — exported inquiry results.

### Stage 12 — verify_archive_package (Final Audit)
**Operation:** Check DB existence, all 11 tables, row counts >0 for 5 core tables, FTS population, CSV sources, zip, preservation metadata (datapackage.json, ro-crate-metadata.json), query exports directory.  
**Rhetorical act:** The final verification is the pipeline's closure argument. It confirms the archive is complete, consistent, and inquirable.  
**Poetic dimension:** The verification report is the last word the pipeline speaks about itself.  
**Residue:** `notes/ARCHIVE_QUERY_VERIFICATION.md`.

## Cross-Cutting Observations

### Determinism as Rhetorical Commitment
The pipeline's refusal of randomness and LLMs is a rhetorical act. Every output is reproducible given the same inputs. This is a claim about scholarly credibility — the archive can be challenged, rerun, and falsified.

### The Score as Literary Judgment Without Interpretation
The `probable_taroko_score` is the pipeline's most compressed literary act. It encodes a hypothesis (this work is a Taroko Gorge remix) as a number without making any claims about the work's quality, intent, or meaning. It is a presence detector, not a reading.

### Absence as Data
Six failed downloads, five unscored works, and the extraction scope limit (5 of 55 works with confirmed arrays) are all documented absences. The pipeline treats failure as evidence — the download log's error column, the validation FAIL exit, the manifest's completeness check all make absence visible.

### The Runtime Sample as Temporal Witness
Stage 05 is the pipeline's only encounter with the poems as performance. The 3-second capture window is a curatorial decision that is both arbitrary and repeatable. The screenshot and text trace are not readings — they are timestamps.

### Preservation Metadata as Scholarly Frame
`datapackage.json` (Frictionless Data) and `ro-crate-metadata.json` (RO-Crate/schema.org) are not part of the technical pipeline — they are scholarly framing devices. They locate the archive in standards-based preservation practice and make its contents citable as research objects.

## Findings

1. **The pipeline is a compound apparatus**: it enacts methodological credibility (determinism, checksums, validation, falsifiable scoring) and literary sensitivity (runtime sampling, source-as-archival-object, documented absence) simultaneously.

2. **The score function is the pipeline's argumentative core**: it defines what counts as a Taroko Gorge work by operationalizing a hypothesis. This definition can be challenged by modifying the regex — the pipeline makes its argument explicit and modifiable.

3. **Extraction scope is a known limitation, not a failure**: the array extraction script captures 5 of 55 works. This boundary is documented and reproducible. The remaining 50 works are present in the archive; they simply require different extraction methods.

4. **The inquiry workbench (stages 10–12) separates custody from inquiry**: the SQLite index and CLI tool allow research queries without touching the archived files. This separation is both a technical and a rhetorical achievement.

5. **The pipeline speaks about itself**: stage 12 verifies stage 10's output; stage 06 verifies stages 02–05. The pipeline has a self-auditing structure that makes its claims checkable at every layer.

Full pipeline operations in: `data/private/query_exports/inquiry_03_pipeline_operations.csv`
