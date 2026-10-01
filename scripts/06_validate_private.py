"""Validate private archive pipeline outputs and write RUN_REPORT.md."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

REQUIRED_DIRS = [
    "seeds", "scripts", "data/public", "data/private",
    "archive/raw_html", "archive/screenshots",
    "archive/output_samples", "archive/extracted_full",
    "notes", "private_archive",
]


def validate_private():
    utils.ensure_dirs("data/public", "data/private", "notes")
    issues = []
    checks = []

    for d in REQUIRED_DIRS:
        exists = os.path.isdir(d)
        checks.append({"check": f"dir:{d}", "status": "ok" if exists else "FAIL", "detail": ""})
        if not exists:
            issues.append(f"Missing directory: {d}")

    raw_html_files = []
    if os.path.isdir("archive/raw_html"):
        raw_html_files = [
            f for f in os.listdir("archive/raw_html")
            if f != ".gitkeep" and os.path.isfile(os.path.join("archive/raw_html", f))
        ]
    s = "ok" if raw_html_files else "FAIL"
    checks.append({"check": "raw_html files", "status": s, "detail": f"{len(raw_html_files)} files"})
    if not raw_html_files:
        issues.append("No raw HTML files found in archive/raw_html")

    for path, label in [
        ("data/public/taroko_links.csv", "taroko_links.csv"),
        ("data/public/download_log.csv", "download_log.csv"),
        ("data/public/inventory.csv", "inventory.csv"),
        ("data/public/lexical_array_summary.csv", "lexical_array_summary.csv"),
    ]:
        rows = utils.read_csv(path) if os.path.isfile(path) else []
        s = "ok" if rows else "WARN"
        checks.append({"check": label, "status": s, "detail": f"{len(rows)} rows"})
        if not rows:
            issues.append(f"Missing or empty: {path}")

    full_path = "archive/extracted_full/lexical_arrays_full.json"
    exists = os.path.isfile(full_path)
    checks.append({"check": "lexical_arrays_full.json", "status": "ok" if exists else "WARN", "detail": full_path})
    if not exists:
        issues.append(f"Missing: {full_path}")

    catalog_path = "data/private/taroko_corpus_catalog.csv"
    catalog = utils.read_csv(catalog_path) if os.path.isfile(catalog_path) else []
    s = "ok" if catalog else "FAIL"
    checks.append({"check": "corpus catalog", "status": s, "detail": f"{len(catalog)} rows"})
    if not catalog:
        issues.append("Corpus catalog missing or empty")

    manifest_path = "data/private/archive_manifest.csv"
    manifest = utils.read_csv(manifest_path) if os.path.isfile(manifest_path) else []
    s = "ok" if manifest else "FAIL"
    checks.append({"check": "archive manifest", "status": s, "detail": f"{len(manifest)} rows"})
    if not manifest:
        issues.append("Archive manifest missing or empty")

    zip_path = "private_archive/taroko_full_archive.zip"
    zip_exists = os.path.isfile(zip_path)
    zip_size = os.path.getsize(zip_path) if zip_exists else 0
    s = "ok" if zip_exists and zip_size > 0 else "FAIL"
    checks.append({"check": "archive zip", "status": s, "detail": f"{zip_size} bytes" if zip_exists else "missing"})
    if not zip_exists:
        issues.append("Archive zip missing")

    samples = []
    if os.path.isdir("archive/output_samples"):
        samples = [
            f for f in os.listdir("archive/output_samples")
            if f != ".gitkeep" and os.path.isfile(os.path.join("archive/output_samples", f))
        ]
    checks.append({"check": "runtime samples", "status": "ok" if samples else "WARN", "detail": f"{len(samples)} files"})

    shots = []
    if os.path.isdir("archive/screenshots"):
        shots = [
            f for f in os.listdir("archive/screenshots")
            if f != ".gitkeep" and os.path.isfile(os.path.join("archive/screenshots", f))
        ]
    checks.append({"check": "screenshots", "status": "ok" if shots else "WARN", "detail": f"{len(shots)} files"})

    utils.write_csv("data/public/validation_summary.csv", checks)

    fails = [c for c in checks if c["status"] == "FAIL"]
    warns = [c for c in checks if c["status"] == "WARN"]
    if fails:
        overall = "FAIL"
    elif warns:
        overall = "WARN"
    else:
        overall = "PASS"

    non_ok = [c for c in checks if c["status"] != "ok"]
    report = f"""# RUN_REPORT (Private Archive)

Generated: {utils.now_iso()}

## Validation Status: {overall}

### Checks ({len(checks)} total, {len(non_ok)} non-ok)

| Check | Status | Detail |
|-------|--------|--------|
"""
    for c in checks:
        report += f"| {c['check']} | {c['status']} | {c['detail']} |\n"

    if issues:
        report += "\n## Issues\n\n"
        for i in issues:
            report += f"- {i}\n"
    else:
        report += "\nNo issues found.\n"

    report += f"""
## Archive Summary

- Raw HTML files: {len(raw_html_files)}
- Corpus catalog rows: {len(catalog)}
- Archive manifest rows: {len(manifest)}
- Runtime samples: {len(samples)}
- Screenshots: {len(shots)}
- Zip: {zip_path} ({zip_size} bytes)
"""

    with open("notes/RUN_REPORT.md", "w") as f:
        f.write(report)

    print(f"Validation: {overall}")
    print(f"Report: notes/RUN_REPORT.md")
    for i in issues:
        print(f"  ISSUE: {i}")


if __name__ == "__main__":
    validate_private()
