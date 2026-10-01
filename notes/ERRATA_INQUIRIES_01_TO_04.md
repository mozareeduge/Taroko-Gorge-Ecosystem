# Errata — Inquiries 01 to 04

## Overview

This document records corrections to the inquiry reports produced during the v1 archive phase. The primary errors involve conflation of statement types in INQUIRY_04.

---

## INQUIRY_04 — Poem Statements and Contexts

**File**: `notes/INQUIRY_04_POEM_STATEMENTS_AND_CONTEXTS.md`  
**Date of original**: 2026-06-28 (v1)

### Error 1: Bio ≠ Author Statement

INQUIRY_04 treats biographical text about the author as equivalent to a statement about the work. These are distinct:

- **Author statement**: first-person or attributed text explaining the work's concept, method, or intent
- **Bio**: background information about the author's career, affiliations, or other works

Bio sections (e.g., from ELC work pages) describe who made the work; they do not constitute the author's statement *about* the work. Bio should be classified as `bio`, not `explicit_author_statement`.

### Error 2: Editorial Statement ≠ Author Statement

The ELC3 collection page (dl_0002) contains an editorial statement written by ELC3 editors, not by Nick Montfort. INQUIRY_04 correctly identifies it as editorial, but the summary section ambiguously groups it with "works with explicit statement-like text" without consistently distinguishing editorial voice from author voice.

Correction: dl_0002's statement is `editorial_statement` (ELC3 editorial apparatus), not an `explicit_author_statement` from Montfort.

### Error 3: Runtime Output ≠ Statement

Some inquiry findings describe generated poem output (text captured from runtime sampling) as if it were a contextual statement about the work. Generated output is a runtime trace — one execution of the generative process. It tells us nothing about the author's intent or the work's concept. It is classified as `generated_output`, not any form of statement.

### Error 4: Tech Details ≠ Statement

Descriptions of JavaScript mechanisms, file sizes, or technical implementation notes (e.g., "less than a thousand words" code) are technical metadata, not author statements. They should be classified as `metadata_only` or `project_description` (if authored) rather than counted as statements.

### Error 5: dl_0013 Array Extraction Conflation

INQUIRY_04 correctly identifies dl_0013's author statement (from the blog post body) as reliable. However, it does not explicitly flag that the *lexical arrays* extracted from dl_0013 are WordPress/analytics arrays, not poem vocabulary. A future reader could conflate the reliable statement with the unreliable extraction. The lexical arrays for dl_0013 are `linkElements`, `ccpa_applies`, and `s` — all vendor arrays.

---

## INQUIRY_02 and INQUIRY_03

No critical factual errors identified. INQUIRY_02 (ground-to-proxy transformations) and INQUIRY_03 (procedural rhetoric) are analytical frameworks applied to existing data and do not make falsifiable claims about statement types or extraction results.

---

## Corrections Applied in v2

The v2 statement layer (script 17, `data/private/statement_sources_v2.csv`) applies the corrected taxonomy. Each statement is labeled with one of: `explicit_author_statement`, `editorial_statement`, `bio`, `generated_output`, `metadata_only`, `project_description`, etc.
