"""Extract JS array summaries from probable Taroko files."""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

IN_INVENTORY = "data/public/inventory.csv"
OUT_SUMMARY = "data/public/lexical_array_summary.csv"
OUT_FULL = "archive/extracted_full/lexical_arrays_full.json"
MIN_SCORE = 3

ARRAY_PATTERN = re.compile(
    r'(?:var\s+|let\s+|const\s+)?(\w+)\s*=\s*\[([\s\S]*?)\](?:\s*;)?',
    re.MULTILINE,
)
STRING_ITEM = re.compile(r'"([^"\\]|\\.)*?"|\'([^\'\\]|\\.)*?\'')


def extract_arrays(content):
    results = []
    for m in ARRAY_PATTERN.finditer(content):
        name = m.group(1)
        body = m.group(2)
        items = STRING_ITEM.findall(body)
        flat = [i[0] or i[1] for i in items]
        if flat:
            results.append({"name": name, "items": flat})
    return results


def extract_lexical():
    utils.ensure_dirs("data/public", "archive/extracted_full")
    inventory = utils.read_csv(IN_INVENTORY)

    summary_rows = []
    full_data = {}

    for entry in inventory:
        try:
            score = int(entry.get("probable_taroko_score", 0))
        except ValueError:
            continue
        if score < MIN_SCORE:
            continue

        local_path = entry.get("local_path", "")
        if not local_path or not os.path.exists(local_path):
            continue

        with open(local_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        arrays = extract_arrays(content)
        full_data[entry["id"]] = {
            "url": entry["url"],
            "local_path": local_path,
            "arrays": arrays,
        }

        for arr in arrays:
            item_text = "|".join(arr["items"])
            sample_hash = hashlib.sha256(item_text.encode("utf-8")).hexdigest()[:16]
            summary_rows.append({
                "id": entry["id"],
                "url": entry["url"],
                "array_name": arr["name"],
                "item_count": len(arr["items"]),
                "sample_hash": sample_hash,
                "notes": "",
            })

    utils.write_csv(OUT_SUMMARY, summary_rows)
    print(f"Lexical array summary: {OUT_SUMMARY} ({len(summary_rows)} entries)")

    with open(OUT_FULL, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    print(f"Full arrays (local-only): {OUT_FULL}")


if __name__ == "__main__":
    extract_lexical()
