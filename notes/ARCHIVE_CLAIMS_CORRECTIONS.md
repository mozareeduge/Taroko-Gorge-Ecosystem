> **Superseded in part** (2026-10-02): Claim 1 counts 'one confirmed' explicit author statement from the offline run. A later live-capture run (2026-06-28; see `archive_mvp_v2_live_paratext_run_log.md`) captured 51 of 53 context pages and recorded 2 `explicit_author_statement` rows, 1 `editorial_statement` and 1 `project_description` in the local statement layer. The origin of the second author-statement row (a captured context page) has not been re-audited in this public repository, because the private tables are not committed. Claims 2 to 4 still stand.

# Archive Claims Corrections

## Old Claims vs. Corrected Claims (v2)

### Claim 1 — Statements

**Old claim (INQUIRY_04)**: "The archive contains explicit author/artist statements in [N] works."  
**Correction**: The archive contains one confirmed explicit first-person author statement (dl_0013, Eric Snodgrass / exinfoam blog post). Other "statement-like" text found is either editorial (dl_0002 ELC3 editors), project descriptions (dl_0018 Designer Gulch), bio text, or minimal about-text. The count of "statements" depends critically on the taxonomy applied. With the v2 taxonomy:
- `explicit_author_statement`: 1 (dl_0013)
- `editorial_statement`: 1 (dl_0002)
- `project_description`: a small number with about-text
- `bio`: present on ELC context pages but not in raw HTML downloads
- `generated_output`: runtime samples are NOT statements

### Claim 2 — Scores

**Old claim**: "probable_taroko_score >= 3 indicates a likely Taroko Gorge work."  
**Correction**: Score 3 indicates the page has JavaScript plus taroko/gorge keywords plus function definitions or setInterval. This fires on nearly all nickm.com/taroko_gorge/* pages regardless of whether they actually contain Taroko poem arrays. Score 3 is a necessary but not sufficient indicator. Score 5 is the strongest indicator (full pattern match). Score 0 does not rule out a remix (could use different variable names).

### Claim 3 — Lexical Arrays

**Old claim**: dl_0013 has extracted lexical arrays.  
**Correction**: The arrays extracted from dl_0013 (`linkElements`, `ccpa_applies`, `s`) are WordPress platform/analytics arrays, not poem vocabulary arrays. dl_0013's lexical extraction is contaminated and should not be used in analyses of the poem ecosystem's vocabulary.

### Claim 4 — Mirror Pairs

**Old claim** (implicit): Each URL is a distinct work.  
**Correction**: Some URLs are mirrors of the same work. For example:
- dl_0007 (nickm.com/taroko_gorge/gorge/) and dl_0008 (luckysoap.com/generations/gorge.html) are both GORGE by J.R. Carpenter
- dl_0012 (nickm.com/taroko_gorge/yoko_engorged/) and dl_0013 (exinfoam.wordpress.com/...) are both Yoko Engorged (executable vs. blog post)
- dl_0035 (nickm.com/taroko_gorge/hey_gorgeous/) and dl_0036 (tinysubversions.com/stuff/gorge/) are both Hey Gorgeous
- dl_0049 (nickm.com/taroko_gorge/kanjono_taroko/) and dl_0050 (inthescales.com) are both Kanjono Taroko
- dl_0053 (nickm.com/taroko_gorge/gorge_of_anathema/) and dl_0054 (multimodalmel.com) are both Gorge of Anathema
- dl_0059 (nickm.com/taroko_gorge/taroko_gary_revisited/) and dl_0060 (iloveepoetry.org) are both Taroko Gary Revisited

The v2 work entity layer reconciles URLs into distinct work entities.

### Claim 5 — ELC3 Context

**Old claim**: The ELC3 context page was downloaded and its statement is in the archive.  
**Clarification**: dl_0002 (`collection.eliterature.org/3/collection-taroko.html`) is the ELC3 *collection index* page for the Taroko Gorge remixes cluster, not the individual work page. The individual ELC3 work page (`collection.eliterature.org/3/work.html?work=taroko-gorge`) was not in the original download set. The v2 context-page capture phase (script 13-15) adds both URLs for attempted capture.
