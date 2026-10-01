# Inquiry 04 — Poem Statements, Author Notes, and Contextual Frames

Generated: 2026-06-28

## Research Question

Does the Taroko Gorge archive contain explicit author/artist statements, about-texts, project descriptions, or introductory frames? What statement-like material is available in the local corpus, and what remains absent or requires external verification?

## Method

All evidence was drawn from:
- FTS5 raw-search over `archive_search` (terms: statement, about, author, description, remix, inspired, adapted, Montfort, generated, note, project, poem, after, source, context, explanation)
- `archive/output_samples/` text traces (50 files, 500-char captures of runtime-visible text)
- `archive/raw_html/` filenames and paths (not full text inspected)
- SQLite inventory, downloads, and FTS tables via `scripts/11_query_archive.py`

**Scope limit**: Output samples capture ~500 characters of visible text from a 3-second Playwright render. Statement-like text that appears below the fold, in hidden HTML elements, or in source-code comments is not captured. The raw HTML is present but was not bulk-inspected.

---

## Category 1: Works with Explicit Statement-Like Text

These works contain prose statements, author notes, or project descriptions that are fully captured in the local archive.

### dl_0002 — Collection: Taroko Gorge Remixes (ELO Collection)
**URL**: https://collection.eliterature.org/3/collection-taroko.html  
**Evidence path**: `archive/output_samples/dl_0002_sample.txt`  
**Type**: Explicit editorial statement  
**Confidence**: High

The output sample contains a full editorial statement (captured verbatim in the runtime sample):

> *Inspired by a visit to Taroko Gorge in Taiwan, Nick Montfort's modest, procedurally-generated poem has produced an entire subgenre of remixes, remakes, constrained writing experiments, and parodies. The original Taroko Gorge brings together the enormous scale and diversity of geological space with the recombinatorial potential of computation.*

This is the most substantive statement in the archive. It describes Taroko Gorge as a platform for "poetic play," frames the ELC3 collection's preservation rationale, and explicitly discusses the poem's code economics ("less than a thousand words"). This is an editorial statement, not an author statement from Montfort — it is attributed to the ELC3 editorial apparatus. External verification not needed: full text is in the sample.

---

### dl_0013 — YOKO ENGORGED | exinfoam
**URL**: http://exinfoam.wordpress.com/2011/07/18/yoko-engorged/  
**Evidence path**: `archive/output_samples/dl_0013_sample.txt`  
**Type**: Explicit author/artist statement (blog post)  
**Confidence**: High

The WordPress blog post format means the full author statement appears as page body text and was captured in the runtime sample:

> *Ever wondered what would happen if you took the playful and free spirited method to be found in Yoko Ono's Fluxus writings and forced upon it the perhaps also liberating but rather more sordid and mechanical approach of a digital de Sade writing Beatles fan fiction? Well wonder no more…*

> *The poem uses Nick Montfort's streamlined and nimble Taroko Gorge code (a JavaScript port of a poetry generator originally written as a 1k Python program). All I have done is command, cup, exercise, explore, finger, flog, fondle, graze, grope, imagine, lick, manipulate, massage, plow, poke, pucker, range, reveal, ride, roam, rub, smear, soften, squeeze, stroke, suck, stimulate, tease, tickle, tongue, and trail the variables.*

This is the only explicit first-person author statement in the archive. It names the Fluxus/Ono conceptual ground, describes the transformation method ("all I have done is... the variables"), and contextualizes it within a creative lineage. External verification not needed.

**Note on contamination**: This is also the work (dl_0013) whose extracted JS arrays are WordPress/analytics arrays (`linkElements`, `ccpa_applies`, `s`), not poem vocabulary. The author statement is reliable; the extraction is not.

---

### dl_0018 — Designer Gulch (Brendan Howell)
**URL**: https://nickm.com/taroko_gorge/designer_gulch/  
**Evidence path**: `archive/output_samples/dl_0018_sample.txt`  
**Type**: About/project description  
**Confidence**: High

Full project description captured in runtime sample:

> *Designer Gulch is an interactive, generative poem about working in the design world. It is installed in the lobby of the Berliner Technische Kunsthochschule. A simple context-free grammar and lists of industry jargon are combined to generate random permutations of verse. Each time a person walks by, the machine spits out one or two more lines in a never-ending epic of graphic labor. The work is a remix of Nick Montfort's poem Taroko Gorge.*

This explicitly names the source ("remix of Nick Montfort's poem Taroko Gorge"), describes the physical installation context, and frames the domain substitution (design world vocabulary). External verification not needed.

---

### dl_0019 — Inside the House (Adam Sylvain)
**URL**: https://nickm.com/taroko_gorge/inside_the_house/  
**Evidence path**: `archive/output_samples/dl_0019_sample.txt`  
**Type**: Page introduction  
**Confidence**: High

Brief but explicit framing captured in runtime:

> *a remix of Nick Montfort's "Taroko Gorge" — original poem inspired by House of Leaves*

Two lineage claims in one line: names Taroko Gorge as source and names House of Leaves as the domain inspiration. Concise author statement. External verification not needed.

---

### dl_0026 — Scholars contemplate the Irish beer (Judy Malloy)
**URL**: https://nickm.com/taroko_gorge/scholars_contemplate_the_irish_beer/  
**Evidence path**: `archive/output_samples/dl_0026_sample.txt`  
**Type**: Metadata description with attribution framing  
**Confidence**: High

Structural attribution captured:

> *Intervention: Judy Malloy / Authoring System: Nick Montfort: Taroko Gorge*

The "Intervention" / "Authoring System" vocabulary is a specific framing vocabulary that names Malloy's role as interventionist and Montfort's Taroko Gorge as the procedural base. This is a structured attribution frame, not prose — but it is explicit and meaningful. External verification not needed.

---

### dl_0032 — Wandering through Taroko Gorge
**URL**: https://nickm.com/taroko_gorge/wandering_through_taroko_gorge/  
**Evidence path**: `archive/output_samples/dl_0032_sample.txt`  
**Type**: Page introduction (interactive framing)  
**Confidence**: High

Interactive framing text captured:

> *Touch the buttons to add to the poem... What is above you? What is below you? What is inside you? What does it feel like? How does it end? Answers are cumulative.*

This is a user-facing interactive description — not an author statement but explicit procedural framing. It positions the reader as participant in poem construction. External verification not needed for this framing.

---

## Category 2: Works with Only Metadata, Title, or Structural Context Clues

These works have title-embedded or structural attribution that implies context but no prose statement in the local archive.

### dl_0017 — Argot Ogre, OK! (Andrew Plotkin)
**Evidence path**: `archive/output_samples/dl_0017_sample.txt`  
**Type**: Page introduction + deferred source-code comment  
**Confidence**: High for intro, deferred for note

Runtime captures:

> *Following Nick Montfort's Taroko Gorge, and including its remixes by Scott Rettberg, J.R. Carpenter, Talan Memmott, Eric Snodgrass, Mark Sample, Maria Engberg, and Flourish Klink. (View source for author's notes.)*

The intro is explicit. However, the author's note is embedded in the JavaScript source code — a `var source = YokoEngorged;` comment is visible in the sample (the page embeds multiple remixes and their source). **External verification needed**: the in-source author's note is not captured in the output sample.

### dl_0024 — Tournedo Gorge
**Evidence path**: `archive/output_samples/dl_0024_sample.txt`  
**Type**: Epigraph as contextual frame  
**Confidence**: Medium

Epigraph captured: *"Let things taste of what they are." — Alice Waters*

This is an epigraph, not an author statement. It establishes the culinary domain but does not describe the remix process. Prose author note may exist in full HTML.

### dl_0029 — Pigeon Forge
FTS title includes "(after Nick Montfort's Taroko Gorge)" — title-embedded attribution. No prose statement in sample. May exist in HTML.

### dl_0043 — Karaoke Mirage
FTS title includes "(after Nick Montfort's Taroko Gorge)" — same pattern. No prose statement in sample.

### dl_0046 — At, or To Take Regret: Some Reflections on Grammars (Johannah Rodgers)
Subtitle "Some Reflections on Grammars" is itself a statement-like framing. Author and date visible in runtime. The word "Reflections" in the subtitle implies a prose component in the full HTML not captured in the runtime sample. **External verification needed**.

### dl_0050 — Kanjono Taroko (inthescales.com)
Detailed attribution format with contributor initials. External site — full HTML may have prose framing.

### dl_0059 — Taroko Gary Revisited
Runtime ends with "scroll → About" — an About section exists but its text was not captured in the 3-second render window. **External verification possible via raw HTML**.

### dl_0009 — WHISPER WIRE (J.R. Carpenter)
"Taroko Gorge / by Nick Montfort" — minimal but explicit attribution framing embedded in runtime.

### dl_0030 — TransmoGrify
"I ♥ E-Poetry presents: TransmoGrify" — presenter framing. No prose author statement.

### dl_0056 — Melroko Porridge
"Melroko Porridge - DHSI 2016" — workshop context (Digital Humanities Summer Institute 2016). Workshop context is a contextual frame for the work's origin but not an author statement.

**Additional attribution-only works** (title + author names only, no prose): dl_0001, dl_0005, dl_0006, dl_0007, dl_0008, dl_0011, dl_0012, dl_0014, dl_0015, dl_0016, dl_0020, dl_0022, dl_0027, dl_0028, dl_0031, dl_0033, dl_0036, dl_0038, dl_0039, dl_0040, dl_0041, dl_0042, dl_0044, dl_0048, dl_0049, dl_0052, dl_0053, dl_0054, dl_0055, dl_0061.

---

## Category 3: Works with Runtime-Visible but Unstable Contextual Text

### dl_0037 — hex ASCII remix (Roman Kalinovski)
Runtime output is pure hex ASCII — the entire generated surface is encoded. No natural-language framing visible in sample. An author note may exist in the page HTML or source comments but is not captured. The hex surface is itself a poetic argument but not a statement.

### dl_0025 — Tasty Gougère
Runtime sample captured anomalous medical/pharmaceutical text (statin drug interaction text from a medical journal). This appears to be a page rendering artifact — likely the Playwright render captured background content or a PDF embed. The sample is unreliable for this work. Raw HTML inspection recommended.

---

## Category 4: Works with No Local Statement Found

**6 failed downloads** — no content captured at all:
- dl_0003: ELMCIP Taroko Gorge page (403)
- dl_0004: ELMCIP original attachment (403)
- dl_0021: http://academic.uprm.edu/flores/TarokoGary.html (404)
- dl_0034: http://ha.art.pl/nick_montfort/wawoz_taroko.html (DNS)
- dl_0045: http://pantherfile.uwm.edu/moulthro/hypertexts/myGorge/ (connection)
- dl_0047: http://dnanovel.reddustjg1.site.aplus.net/Rodgers_Taroko_At_ (404)

**5 below-threshold works** (score < 3, not runtime-sampled):
- dl_0010: Along the Briny Beach
- dl_0023: Camel Tail
- dl_0051: Infinite Monkey Theorem
- dl_0057: Tough Guise
- dl_0058: Within and Against

Raw HTML for these works is present in `archive/raw_html/` but was not inspected.

---

## Category 5: Works Where Statement May Exist Externally

The following works likely have prose framing on their source pages that was not captured:
- **dl_0046** (At, or To Take Regret) — subtitle implies reflective essay
- **dl_0059** (Taroko Gary Revisited) — "About" section visible but not captured
- **dl_0017** (Argot Ogre) — source-code comments noted but not extracted
- **dl_0003, dl_0004** — ELMCIP editorial descriptions exist externally (ELC database)
- **dl_0021** (TarokoGary external) — may exist in Wayback Machine

---

## Findings

### 1. The archive does NOT contain poem statements as a systematic layer

Statement-like material is present for 6 of 55 works at high confidence (dl_0002, dl_0013, dl_0017, dl_0018, dl_0019, dl_0026, dl_0032), and partially present for ~10 more at medium confidence. The remaining ~39 works have no prose statement in the local archive. **The pipeline did not collect statement material as a design target** — runtime samples capture 500 characters of visible poem text, which typically means the generated poem output, not any framing text that might appear below it.

### 2. What statement material is actually available

| Category | Count |
|----------|-------|
| Explicit statement (high confidence, locally available) | 6 works |
| Partial/structural framing (medium confidence) | ~10 works |
| Attribution-only / inferred frame (low confidence) | ~33 works |
| No content (failed downloads) | 6 works |
| Not sampled (below threshold) | 5 works |

The only **first-person author statement** in the corpus is dl_0013 (YOKO ENGORGED, blog post). The **ELC3 editorial statement** (dl_0002) is the most substantive prose description of the entire Taroko Gorge phenomenon. Several works embed attribution framing in structured formats (dl_0026 Intervention/Authoring System; dl_0032 interactive framing) that function as contextual statements even if not prose essays.

### 3. Recommendation: Future enrichment pass

The corpus catalog (`data/private/taroko_corpus_catalog.csv`) currently has no normalized statement field. A future enrichment pass should add:

- `statement_text` — normalized prose statement (max 500 chars), NULL if absent
- `statement_source` — one of: `output_sample`, `raw_html`, `source_comment`, `external_database`, `title_metadata`, `none`
- `statement_confidence` — `high`, `medium`, `low`, `none`
- `statement_verified` — boolean, whether statement was confirmed against source

This enrichment would require:
1. Targeted raw HTML parsing for ~15 works where framing is likely in the HTML body but not in the runtime sample
2. Source-code comment extraction for dl_0017 (and any other works with documented source-comment notes)
3. External lookup for ELMCIP descriptions (dl_0003, dl_0004) and Wayback Machine for failed URLs

This is a bounded task (15–20 works) that would significantly improve the archive's usefulness for literary-historical research. It should follow the same deterministic, no-LLM pipeline principles as the existing scripts.

---

## Summary Table

| work_id | title | evidence_type | confidence | external_verification |
|---------|-------|---------------|------------|----------------------|
| dl_0002 | Collection: Taroko Gorge Remixes | explicit editorial statement | high | no |
| dl_0013 | YOKO ENGORGED (blog) | explicit author statement | high | no |
| dl_0018 | Designer Gulch | about/project description | high | no |
| dl_0019 | Inside the House | page introduction | high | no |
| dl_0026 | Scholars / Irish beer | metadata description | high | no |
| dl_0032 | Wandering through TG | page introduction (interactive) | high | no |
| dl_0017 | Argot Ogre OK! | page intro + deferred source comment | high | yes — source comment |
| dl_0024 | Tournedo Gorge | epigraph/contextual frame | medium | yes |
| dl_0046 | At, or To Take Regret | subtitle frame | medium | yes |
| dl_0059 | Taroko Gary Revisited | About section deferred | medium | yes |
| dl_0009 | WHISPER WIRE | minimal attribution frame | medium | no |
| dl_0030 | TransmoGrify | presenter frame | medium | no |
| dl_0050 | Kanjono Taroko | attribution format | medium | yes |
| dl_0029 | Pigeon Forge | title-embedded attribution | medium | yes |
| dl_0043 | Karaoke Mirage | title-embedded attribution | medium | yes |
| dl_0056 | Melroko Porridge | workshop context | low | yes |
| all others | — | inferred frame / no statement | low | yes |

Full per-work inventory: `data/private/query_exports/inquiry_04_statement_inventory.csv`
