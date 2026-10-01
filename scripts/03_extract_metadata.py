"""Extract deterministic metadata from downloaded HTML files."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils
from bs4 import BeautifulSoup

IN_LOG = "data/public/download_log.csv"
OUT_INVENTORY = "data/public/inventory.csv"

TAROKO_SIGNALS = re.compile(
    r"\b(taroko|gorge|setInterval|stanza|line\b|above|below|trans|intrans|imper|"
    r"choose|words|poem|generate|generator)\b",
    re.I,
)
KNOWN_ARRAYS = re.compile(
    r"\b(above|below|trans|intrans|imper|stanza|line|words)\s*=\s*\[",
    re.I,
)
GENERATOR_SIGNALS = re.compile(
    r"(setInterval|function\s+\w+|function\s*\()", re.I
)


def score_file(content, soup):
    has_taroko = bool(re.search(r"\btaroko\b", content, re.I))
    has_gorge = bool(re.search(r"\bgorge\b", content, re.I))
    has_js = bool(soup.find("script"))
    script_count = len(soup.find_all("script"))
    has_setinterval = bool(re.search(r"setInterval", content))
    has_function = bool(re.search(r"function\s*[\w(]", content))
    has_known_arrays = bool(KNOWN_ARRAYS.search(content))

    score = 0
    if has_taroko or has_gorge:
        score = 1
    if (has_taroko or has_gorge) and has_js:
        score = 2
    if score >= 2 and (has_setinterval or has_function):
        score = 3
    if has_known_arrays:
        score = 4
    # Check for full Taroko pattern: arrays + setInterval + function
    if has_known_arrays and has_setinterval and has_function and (has_taroko or has_gorge):
        score = 5

    return {
        "has_javascript": str(has_js).lower(),
        "script_count": script_count,
        "contains_taroko_word": str(has_taroko).lower(),
        "contains_gorge_word": str(has_gorge).lower(),
        "contains_generator_signals": str(bool(GENERATOR_SIGNALS.search(content))).lower(),
        "contains_setInterval": str(has_setinterval).lower(),
        "contains_function_definition": str(has_function).lower(),
        "contains_known_array_names": str(has_known_arrays).lower(),
        "probable_taroko_score": score,
    }


def extract_metadata():
    utils.ensure_dirs("data/public")
    log = utils.read_csv(IN_LOG)
    rows = []

    for entry in log:
        local_path = entry.get("local_path", "")
        skipped = entry.get("skipped", "false")
        error = entry.get("error", "")

        if not local_path or skipped == "true" or error:
            continue
        if not os.path.exists(local_path):
            continue

        with open(local_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        title_tag = soup.title.string.strip() if soup.title and soup.title.string else ""
        h1 = soup.find("h1")
        h1_text = h1.get_text(strip=True)[:200] if h1 else ""

        author_guess = ""
        meta_author = soup.find("meta", attrs={"name": re.compile("author", re.I)})
        if meta_author:
            author_guess = meta_author.get("content", "")[:200]
        if not author_guess:
            if re.search(r"nick\s+montfort", content, re.I):
                author_guess = "Nick Montfort (detected)"

        signals = score_file(content, soup)
        notes = ""
        if signals["probable_taroko_score"] == 0:
            notes = "no Taroko signals detected"

        rows.append({
            "id": entry["id"],
            "url": entry["url"],
            "local_path": local_path,
            "title_tag": title_tag[:300],
            "h1_text": h1_text,
            "author_guess": author_guess,
            **signals,
            "notes": notes,
        })

    utils.write_csv(OUT_INVENTORY, rows)
    print(f"Inventory saved: {OUT_INVENTORY} ({len(rows)} entries)")
    high = [r for r in rows if int(r["probable_taroko_score"]) >= 3]
    print(f"Probable Taroko score >= 3: {len(high)}")


if __name__ == "__main__":
    extract_metadata()
