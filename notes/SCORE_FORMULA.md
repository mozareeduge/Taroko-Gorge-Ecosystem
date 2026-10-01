# Score Formula — probable_taroko_score

Extracted from `scripts/03_extract_metadata.py`, function `score_file()`.

## Formula (0–5 scale)

The score is computed deterministically from six boolean signals extracted from raw HTML content:

| Signal | Variable | Detection Method |
|--------|----------|-----------------|
| has_taroko | `\btaroko\b` regex (case-insensitive) in full HTML text |
| has_gorge | `\bgorge\b` regex (case-insensitive) in full HTML text |
| has_js | `<script>` tag present (BeautifulSoup) |
| has_setinterval | `setInterval` literal in content |
| has_function | `function\s*[\w(]` regex in content |
| has_known_arrays | `\b(above\|below\|trans\|intrans\|imper\|stanza\|line\|words)\s*=\s*\[` regex |

## Score Assignment Logic

```
score = 0
if has_taroko OR has_gorge:
    score = 1
if (has_taroko OR has_gorge) AND has_js:
    score = 2
if score >= 2 AND (has_setinterval OR has_function):
    score = 3
if has_known_arrays:
    score = 4
if has_known_arrays AND has_setinterval AND has_function AND (has_taroko OR has_gorge):
    score = 5
```

## Score Meanings

| Score | Meaning |
|-------|---------|
| 0 | No Taroko signals detected |
| 1 | Taroko/gorge word present, no JS |
| 2 | Taroko/gorge word + JS present |
| 3 | Taroko/gorge + JS + setInterval or function |
| 4 | Known Taroko array variable names detected |
| 5 | Full pattern: known arrays + setInterval + function + taroko/gorge word |

## Known Array Names Detected

The regex matches these array variable names (left-hand side of `= [`):
- `above`, `below`, `trans`, `intrans`, `imper`, `stanza`, `line`, `words`

## Caveats

- Score 3 is the most common (applies to nearly all nickm.com/taroko_gorge/* pages that have any JS)
- Score 5 is the most reliable indicator of the actual Taroko Gorge generative mechanism
- Score 0 does NOT mean not a remix — it means the detection heuristics did not fire (could be a legitimate remix with different variable names)
- `has_known_arrays` is `false` for dl_0001 (the original) because the original uses different array names not in the regex
- dl_0013 (exinfoam WordPress): score=3, but arrays extracted are WordPress/analytics, not poem arrays — score is unreliable for this page type
