"""Verify archive package integrity and query index consistency.

Outputs: notes/ARCHIVE_QUERY_VERIFICATION.md
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

DB_PATH = "data/private/taroko_query_index.sqlite"
REPORT_PATH = "notes/ARCHIVE_QUERY_VERIFICATION.md"
ZIP_PATH = "private_archive/taroko_full_archive.zip"
DATAPACKAGE = "datapackage.json"
RO_CRATE = "ro-crate-metadata.json"


def check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {label}" + (f": {detail}" if detail else ""))
    return passed


def main():
    utils.ensure_dirs("notes", "data/private")
    lines = ["# Archive Query Verification\n"]
    lines.append(f"Generated: {utils.now_iso()}\n")

    all_pass = True

    # --- SQLite index checks ---
    lines.append("## SQLite Query Index\n")
    db_exists = os.path.exists(DB_PATH)
    ok = check("DB file exists", db_exists, DB_PATH)
    all_pass = all_pass and ok
    lines.append(f"- [{'PASS' if ok else 'FAIL'}] DB file exists: `{DB_PATH}`\n")

    if db_exists:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        expected_tables = [
            "candidates", "downloads", "inventory", "lexical_array_summary",
            "manifest", "runtime_samples", "screenshots", "full_arrays",
            "files_by_work", "archive_summary", "archive_search",
        ]
        existing = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','shadow')").fetchall()}
        for t in expected_tables:
            ok = check(f"Table '{t}' exists", t in existing)
            all_pass = all_pass and ok
            lines.append(f"- [{'PASS' if ok else 'FAIL'}] Table `{t}`\n")

        counts = {}
        for t in ["candidates", "downloads", "inventory", "manifest", "runtime_samples"]:
            try:
                n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                counts[t] = n
                ok = check(f"{t} count > 0", n > 0, str(n))
                all_pass = all_pass and ok
                lines.append(f"- [{'PASS' if ok else 'FAIL'}] `{t}` rows: {n}\n")
            except sqlite3.Error as e:
                check(f"{t} query", False, str(e))
                all_pass = False
                lines.append(f"- [FAIL] `{t}` query error: {e}\n")

        # FTS test
        try:
            n = conn.execute("SELECT COUNT(*) FROM archive_search").fetchone()[0]
            ok = check("FTS index populated", n > 0, str(n))
            all_pass = all_pass and ok
            lines.append(f"- [{'PASS' if ok else 'FAIL'}] FTS rows: {n}\n")
        except sqlite3.Error as e:
            check("FTS index", False, str(e))
            all_pass = False
            lines.append(f"- [FAIL] FTS error: {e}\n")

        # summary table
        try:
            summary_rows = conn.execute("SELECT key, value FROM archive_summary").fetchall()
            ok = check("archive_summary populated", len(summary_rows) > 0, f"{len(summary_rows)} keys")
            all_pass = all_pass and ok
            lines.append(f"- [{'PASS' if ok else 'FAIL'}] archive_summary: {len(summary_rows)} keys\n")
        except sqlite3.Error as e:
            check("archive_summary", False, str(e))
            all_pass = False

        conn.close()

    # --- CSV sources ---
    lines.append("\n## Source CSVs\n")
    csvs = [
        "data/public/taroko_links.csv",
        "data/public/download_log.csv",
        "data/public/inventory.csv",
        "data/public/lexical_array_summary.csv",
        "data/public/runtime_sample_log.csv",
        "data/private/taroko_corpus_catalog.csv",
        "data/private/archive_manifest.csv",
    ]
    for p in csvs:
        exists = os.path.exists(p)
        ok = check(p, exists)
        all_pass = all_pass and ok
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] `{p}`\n")

    # --- Zip ---
    lines.append("\n## Archive Zip\n")
    ok = check("Zip exists", os.path.exists(ZIP_PATH), ZIP_PATH)
    all_pass = all_pass and ok
    lines.append(f"- [{'PASS' if ok else 'FAIL'}] `{ZIP_PATH}`\n")
    if os.path.exists(ZIP_PATH):
        size = os.path.getsize(ZIP_PATH)
        lines.append(f"- Size: {size:,} bytes\n")

    # --- Preservation metadata ---
    lines.append("\n## Preservation Metadata\n")
    for p in [DATAPACKAGE, RO_CRATE]:
        ok = check(p, os.path.exists(p))
        all_pass = all_pass and ok
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] `{p}`\n")

    # --- Query exports dir ---
    lines.append("\n## Query Exports Directory\n")
    ok = check("data/private/query_exports/ exists", os.path.isdir("data/private/query_exports"))
    all_pass = all_pass and ok
    lines.append(f"- [{'PASS' if ok else 'FAIL'}] `data/private/query_exports/`\n")

    # --- Final status ---
    status = "PASS" if all_pass else "FAIL"
    lines.append(f"\n## Verification Status: {status}\n")
    print(f"\nVerification Status: {status}")

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Report: {REPORT_PATH}")

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
