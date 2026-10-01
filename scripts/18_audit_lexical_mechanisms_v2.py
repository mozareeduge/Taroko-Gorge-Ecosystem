"""Audit lexical mechanism extraction — classify array types per dl_id."""
import sys
import os
import json
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_CSV = "data/private/lexical_mechanisms_v2.csv"
OUT_JSON = "data/private/lexical_candidates_v2.json"

# Known Taroko array variable names (semantic vocabulary arrays)
POEM_ARRAY_NAMES = re.compile(
    r"^(above|below|trans|intrans|imper|stanza|line|words|"
    r"above1|above2|above3|below1|below2|below3|"
    r"nouns?|verbs?|prep|prepositions?|complement|subjects?|predicates?)$",
    re.I,
)

# Vendor/analytics/platform array indicators
VENDOR_INDICATORS = re.compile(
    r"(google|analytic|jquery|wp_|wordpress|_gaq|_ga|fb|facebook|"
    r"ccpa|linkElement|disqus|addThis|cookie|tracking|pixel)",
    re.I,
)

GENERIC_SHORT = re.compile(r"^[a-z]{1,2}$")  # e.g., "s", "q", "lb"

# Contamination override: dl_ids known to have vendor arrays only
KNOWN_CONTAMINATED = {"dl_0013"}
CONTAMINATION_NOTES = {
    "dl_0013": "WordPress/analytics arrays: linkElements, ccpa_applies, s — no poem arrays",
}


def classify_arrays(dl_id, array_names):
    """Classify a list of array names for a given dl_id."""
    if dl_id in KNOWN_CONTAMINATED:
        return "contaminated_extraction", "confirmed vendor/platform arrays", 0.95

    if not array_names:
        return "no_array_evidence", "", 1.0

    poem_count = 0
    vendor_count = 0
    for name in array_names:
        if POEM_ARRAY_NAMES.match(name):
            poem_count += 1
        elif VENDOR_INDICATORS.search(name) or GENERIC_SHORT.match(name):
            vendor_count += 1

    total = len(array_names)
    if poem_count == total:
        return "confirmed_poem_arrays", "", 0.95
    elif poem_count > 0 and vendor_count > 0:
        return "contaminated_extraction", f"{vendor_count} vendor arrays mixed with {poem_count} poem arrays", 0.7
    elif poem_count > 0:
        return "probable_poem_arrays", "", 0.8
    elif vendor_count > 0:
        return "ambient_vendor_arrays", "", 0.9
    else:
        return "needs_manual_review", "unknown array names", 0.5


def audit_lexical():
    utils.ensure_dirs("data/private")

    lexical = utils.read_csv("data/public/lexical_array_summary.csv")
    inventory = utils.read_csv("data/public/inventory.csv")

    # Group by dl_id
    arrays_by_dl = {}
    for row in lexical:
        dl_id = row["id"]
        if dl_id not in arrays_by_dl:
            arrays_by_dl[dl_id] = []
        arrays_by_dl[dl_id].append(row["array_name"])

    inv_lookup = {r["id"]: r for r in inventory}

    # For inventory entries with score >= 3 but no arrays extracted
    output_rows = []
    json_dict = {}

    # Process dl_ids that have array entries
    for dl_id, array_names in sorted(arrays_by_dl.items()):
        url = inv_lookup.get(dl_id, {}).get("url", "")
        contamination_note = CONTAMINATION_NOTES.get(dl_id, "")
        lexical_status, extra_notes, confidence = classify_arrays(dl_id, array_names)

        notes = contamination_note or extra_notes
        if dl_id in KNOWN_CONTAMINATED:
            notes = CONTAMINATION_NOTES[dl_id]

        output_rows.append({
            "dl_id": dl_id,
            "url": url,
            "arrays_found": len(array_names),
            "array_names": "|".join(array_names),
            "lexical_status": lexical_status,
            "contamination_notes": notes,
            "confidence": f"{confidence:.2f}",
            "notes": "",
        })
        json_dict[dl_id] = {
            "status": lexical_status,
            "array_names": array_names,
            "confidence": confidence,
        }

    # Process inventory entries with score >= 3 but no arrays in lexical summary
    for row in inventory:
        dl_id = row["id"]
        if dl_id in arrays_by_dl:
            continue  # already handled
        score = int(row.get("probable_taroko_score", 0))
        url = row.get("url", "")
        has_known = row.get("contains_known_array_names", "false").lower() == "true"

        if score == 5 or has_known:
            status = "extractor_missed_possible_arrays"
            notes = f"score={score} has_known_arrays={has_known} but not in lexical_array_summary"
            confidence = 0.6
        elif score >= 3:
            status = "no_array_evidence"
            notes = f"score={score}; probable poem but arrays not extracted"
            confidence = 0.8
        elif score == 0:
            status = "no_array_evidence"
            notes = "score=0; no Taroko signals"
            confidence = 0.95
        else:
            status = "no_array_evidence"
            notes = f"score={score}"
            confidence = 0.85

        output_rows.append({
            "dl_id": dl_id,
            "url": url,
            "arrays_found": 0,
            "array_names": "",
            "lexical_status": status,
            "contamination_notes": "",
            "confidence": f"{confidence:.2f}",
            "notes": notes,
        })
        json_dict[dl_id] = {
            "status": status,
            "array_names": [],
            "confidence": confidence,
        }

    fields = ["dl_id", "url", "arrays_found", "array_names",
              "lexical_status", "contamination_notes", "confidence", "notes"]
    utils.write_csv(OUT_CSV, output_rows, fieldnames=fields)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_dict, f, indent=2, ensure_ascii=False)

    print(f"Lexical mechanisms v2: {len(output_rows)} -> {OUT_CSV}")
    print(f"JSON candidates: {len(json_dict)} -> {OUT_JSON}")

    by_status = {}
    for r in output_rows:
        s = r["lexical_status"]
        by_status[s] = by_status.get(s, 0) + 1
    for s, c in sorted(by_status.items()):
        print(f"  {s}: {c}")


if __name__ == "__main__":
    audit_lexical()
