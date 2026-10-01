"""Validate pipeline outputs and write RUN_REPORT.md."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

REQUIRED_DIRS = [
    "seeds", "scripts", "data/public", "data/private",
    "archive/raw_html", "archive/screenshots",
    "archive/output_samples", "archive/extracted_full", "notes",
]
REQUIRED_FILES = {
    "seeds/taroko_seed_urls.csv": "seed file",
}
PHASE_FILES = {
    "data/public/taroko_links.csv": "collect_links output",
    "data/public/download_log.csv": "download_pages output",
    "data/public/inventory.csv": "extract_metadata output",
}

IGNORED_PATTERNS = [
    "archive/raw_html/", "archive/screenshots/",
    "archive/output_samples/", "archive/extracted_full/",
    "data/private/",
]


def check_staged_ignored():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=10
        )
        staged = result.stdout.strip().splitlines()
        violations = [
            f for f in staged
            if any(f.startswith(p) for p in IGNORED_PATTERNS)
        ]
        return violations
    except Exception as e:
        return [f"git check failed: {e}"]


def validate():
    utils.ensure_dirs("data/public", "notes")
    issues = []
    checks = []

    for d in REQUIRED_DIRS:
        exists = os.path.isdir(d)
        checks.append({"check": f"dir:{d}", "status": "ok" if exists else "FAIL", "detail": ""})
        if not exists:
            issues.append(f"Missing directory: {d}")

    for path, label in REQUIRED_FILES.items():
        exists = os.path.isfile(path)
        checks.append({"check": label, "status": "ok" if exists else "FAIL", "detail": path})
        if not exists:
            issues.append(f"Missing file: {path}")

    for path, label in PHASE_FILES.items():
        exists = os.path.isfile(path)
        rows_exist = bool(utils.read_csv(path)) if exists else False
        status = "ok" if rows_exist else ("WARN" if exists else "WARN")
        checks.append({"check": label, "status": status, "detail": path})
        if not exists:
            issues.append(f"Phase output missing (run pipeline first): {path}")

    dl_log = utils.read_csv("data/public/download_log.csv")
    for row in dl_log:
        if row.get("skipped") == "true" or row.get("error"):
            continue
        lp = row.get("local_path", "")
        if lp and not os.path.exists(lp):
            issues.append(f"download_log references missing file: {lp}")
        if not row.get("sha256"):
            issues.append(f"Missing sha256 for: {row.get('url')}")
    checks.append({"check": "download file+sha256 integrity", "status": "ok" if not [i for i in issues if "download" in i] else "FAIL", "detail": f"{len(dl_log)} rows"})

    inventory = utils.read_csv("data/public/inventory.csv")
    for row in inventory:
        if not row.get("id") or not row.get("url") or not row.get("local_path"):
            issues.append(f"Inventory row missing id/url/local_path: {row}")
        try:
            s = int(row.get("probable_taroko_score", "0"))
            if not 0 <= s <= 5:
                raise ValueError()
        except ValueError:
            issues.append(f"Invalid probable_taroko_score for {row.get('url')}")
    checks.append({"check": "inventory row validity", "status": "ok" if not [i for i in issues if "Inventory" in i or "probable" in i] else "FAIL", "detail": f"{len(inventory)} rows"})

    inv_ids = {r["id"] for r in inventory}
    lex = utils.read_csv("data/public/lexical_array_summary.csv")
    for row in lex:
        if row.get("id") not in inv_ids and inv_ids:
            issues.append(f"lexical_array_summary references unknown id: {row.get('id')}")
    checks.append({"check": "lexical summary id references", "status": "ok", "detail": f"{len(lex)} entries"})

    staged_violations = check_staged_ignored()
    if staged_violations:
        issues.append(f"Staged ignored files: {staged_violations}")
    checks.append({"check": "no ignored files staged", "status": "ok" if not staged_violations else "FAIL", "detail": str(staged_violations)})

    readme = ""
    if os.path.exists("README.md"):
        with open("README.md") as f:
            readme = f.read()
    has_warning = "public-repo" in readme.lower() or "public repo" in readme.lower() or "safety" in readme.lower()
    checks.append({"check": "README safety warning", "status": "ok" if has_warning else "WARN", "detail": ""})
    if not has_warning:
        issues.append("README.md missing public-repo safety warning")

    utils.write_csv("data/public/validation_summary.csv", checks)

    status = "PASS" if not issues else ("WARN" if all("WARN" in c["status"] for c in checks if c["status"] != "ok") else "FAIL")
    fails = [c for c in checks if c["status"] != "ok"]

    report = f"""# RUN_REPORT

Generated: {utils.now_iso()}

## Validation Status: {status}

### Checks ({len(checks)} total, {len(fails)} non-ok)

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

    with open("notes/RUN_REPORT.md", "w") as f:
        f.write(report)

    print(f"Validation: {status}")
    print(f"Report: notes/RUN_REPORT.md")
    if issues:
        for i in issues:
            print(f"  ISSUE: {i}")


if __name__ == "__main__":
    validate()
