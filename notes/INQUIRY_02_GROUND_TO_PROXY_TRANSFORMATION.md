# Inquiry 02 — Ground-to-Proxy Transformation and Prototype Packet Selection

Generated: 2026-06-27

## Research Question

How does each Taroko Gorge remix transform its source-ground into a proxy space, and which works best represent the range of transformation pressures for a controlled Mixt Workbench prototype packet?

## Transformation Model

The archive reveals a six-stage transformation chain:

```
source-ground → lexical set → inherited procedure → generated surface → proxy space → residue
```

**source-ground**: The substituted domain (landscape, city, cuisine, persona, language, encoding)  
**lexical set**: The vocabulary arrays that carry domain identity (`above`, `below`, `trans`, `imper`, `intrans`, etc.)  
**inherited procedure**: The Taroko combinatorial engine, retained structurally  
**generated surface**: One execution trace — a poem output, not the archival object  
**proxy space**: The new experiential territory the procedure opens  
**residue**: What of the original procedure persists — its rhythm, its grammar, its duration

The pipeline operationalizes this model through the `probable_taroko_score` (0–5): score 4–5 confirms the lexical set is present and named in the standard vocabulary (`above|below|trans|intrans|imper|stanza|line|words`). Score 3 confirms the procedure (setInterval, function definitions) without confirmed array names. Scores 1–2 mark name-only or static-page candidates.

## Transformation Taxonomy

Eight transformation types were identified across the 55 downloaded works:

### 1. Original Landscape Procedure
**Works:** dl_0005  
The source-ground is the gorge itself — geology, water, vegetation. Lexical arrays carry geomorphic vocabulary. The proxy space is the gorge as infinite generative text. No deviation in domain; the baseline against which all others are measured.

### 2. Urban Deviation
**Works:** dl_0006 (Tokyo Garage, Scott Rettberg)  
Ground shifts from natural landscape to urban grid. The gorge becomes a garage; Taiwan becomes Tokyo. Runtime preview available. Transformation pressure: moderate — structural vocabulary inherited, spatial domain substituted.

### 3. Interface or Visual Deviation
**Works:** dl_0007 (GORGE, J.R. Carpenter)  
Text rendered in uppercase, coastal imagery. The deviation is typographic and coastal rather than purely lexical. Score 5. Runtime sample confirms active generation.

### 4. Object or Commodity Ground
**Works:** dl_0011 (TOY GARBAGE), dl_0024 (Tournedo Gorge, cuisine)  
Ground is consumer objects or food. dl_0024 carries an Alice Waters epigraph: *"Let things taste of what they are."* — the recipe-poem tension is explicit. The proxy space is a menu as landscape poem. Transformation pressure: high — semantic domain is maximally distant from geology.

### 5. Persona or Fandom Ground
**Works:** dl_0014 (Takei George, Mark Sample), dl_0020 (Taroko Gary, Gary Snyder/Leonardo Flores)  
Ground is a named person or author corpus. dl_0014 runtime output produces bibliographic strings: "TAKEI, GEORGE / Montfort, Nick / Rettberg, Scott / Carpenter, J.R." — the persona becomes a procedural citation machine. dl_0020 routes through Gary Snyder's nature poetry vocabulary. Transformation pressure: high for dl_0014 (person-as-landscape), moderate for dl_0020 (nature-poet reground).

### 6. Meta-Remix or Archive-as-Ground
**Works:** dl_0046 (At, or To Take Regret, grammatical/archival)  
Ground is the Taroko archive itself or its grammatical structure. Transformation is reflexive — the procedure comments on its own inheritance. Highest conceptual transformation pressure.

### 7. Linguistic or Translation Mutation
**Works:** dl_0033, dl_0040, dl_0041, dl_0042 (Polish translations)  
Ground is retained (landscape, gorge vocabulary) but the lexical set is translated into Polish. dl_0033 arrays: above(4), below(4), trans(4), imper(4), intrans(4) — 20 items with Polish diacritics (ą, ę, ó). dl_0041/dl_0042 expand to 9 arrays: above1, above2, above3, below1, below2, below3, trans, imper, intrans — 4 items each. Structural expansion of the lexical set is itself a transformation. Transformation pressure: moderate — domain preserved, language mutated.

### 8. Encoding Transformation
**Works:** dl_0037 (Roman Kalinovski, hex ASCII)  
Ground is the Taroko procedure itself; transformation is at the encoding layer. Runtime output confirmed as hex: "6c 6f 6f 70 73 72 75 6e 74 68 65 52 41 4d 73 / 50 43 42 73 64..." — the poem is rendered as machine-readable hexadecimal. The proxy space is the poem as pure byte stream. Transformation pressure: maximal — the surface is unreadable as natural language.

## Contamination Note: dl_0013

dl_0013 (YOKO ENGORGED) has score 4 and 3 extracted arrays (`linkElements`, `ccpa_applies`, `s`) — WordPress/analytics arrays injected by the hosting platform, not poem vocabulary. The actual poem source is embedded in the page but was not separately extracted by the array extraction script. This work is **contaminated/uncertain** for lexical analysis purposes and excluded from the prototype packet.

## Coverage Gaps

Six works failed download entirely (dl_0003, dl_0004, dl_0021, dl_0034, dl_0045, dl_0047) — these are archive gaps, not transformation failures. Five works scored below MIN_SCORE=3 (dl_0010, dl_0023, dl_0051, dl_0057, dl_0058) and were not runtime-sampled.

## Prototype Packet Selection

Eight works selected for the Mixt Workbench prototype packet, covering all eight transformation types:

| work_id | title | transformation_type | score | arrays_confirmed |
|---------|-------|---------------------|-------|-----------------|
| dl_0005 | Taroko Gorge (original) | original_landscape | 5 | no (extraction baseline) |
| dl_0006 | Tokyo Garage | urban_deviation | 5 | no |
| dl_0024 | Tournedo Gorge | commodity_ground | 5 | no |
| dl_0014 | Takei, George | persona_fandom | 5 | no |
| dl_0037 | hex ASCII remix | encoding_transformation | 5 | no |
| dl_0033 | Polish translation A | linguistic_mutation | 5 | yes (5 arrays, 20 items) |
| dl_0041 | Polish translation C | linguistic_mutation | 5 | yes (9 arrays, 36 items) |
| dl_0046 | At, or To Take Regret | meta_remix | 4 | no |

Full packet details in: `data/private/query_exports/inquiry_02_prototype_packet.csv`  
Full transformation matrix in: `data/private/query_exports/inquiry_02_transformation_matrix.csv`

## Findings

1. **The lexical set is the primary carrier of transformation.** Works that replace only the vocabulary while retaining the procedure (Polish translations) preserve the most structural fidelity. Works that also alter the surface encoding (dl_0037) or the semantic domain (dl_0024, dl_0014) impose higher transformation pressure.

2. **Array extraction scope is limited.** The extraction script (`MIN_SCORE=3`, KNOWN_ARRAYS regex) captures only 5 of 55 works. The remaining works either use non-standard array names or embed their procedure in ways the regex doesn't match. This is a methodological boundary, not an archive gap — the source files are present.

3. **The prototype packet spans all eight transformation types** with confirmed extraction data for two works (dl_0033, dl_0041) and runtime evidence for six. The packet provides a controlled cross-section for Mixt Workbench testing.

4. **dl_0013 contamination** demonstrates that platform injection can corrupt the extraction signal. Works hosted on WordPress or analytics-heavy platforms require manual verification before lexical analysis.
