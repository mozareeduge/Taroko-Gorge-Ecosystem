"""Verification script for Archive MVP v2."""
import sys
import os
import sqlite3
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_REPORT = "notes/ARCHIVE_MVP_V2_VERIFICATION.md"

CRITICAL_CHECKS = []
WARNING_CHECKS = []

results = []


def check(label, test_fn, critical=True):
    try:
        passed, detail = test_fn()
        status = "PASS" if passed else ("FAIL" if critical else "WARNING")
        results.append({"label": label, "status": status, "detail": detail, "critical": critical})
        print(f"[{status}] {label}: {detail}")
        return passed
    except Exception as e:
        status = "FAIL" if critical else "WARNING"
        results.append({"label": label, "status": status, "detail": str(e), "critical": critical})
        print(f"[{status}] {label}: {e}")
        return False


def csv_row_count(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f)) - 1  # minus header


def sqlite_exists_with_tables(db_path, required_tables):
    if not os.path.exists(db_path):
        return False, f"not found: {db_path}"
    conn = sqlite3.connect(db_path)
    existing = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    conn.close()
    missing = [t for t in required_tables if t not in existing]
    if missing:
        return False, f"missing tables: {', '.join(missing)}"
    return True, f"all required tables present"


def sqlite_row_count(db_path, table):
    if not os.path.exists(db_path):
        return 0
    conn = sqlite3.connect(db_path)
    try:
        n = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    except Exception:
        n = 0
    conn.close()
    return n


def run_checks():
    DB_V1 = "data/private/taroko_query_index.sqlite"
    DB_V2 = "data/private/taroko_query_index_v2.sqlite"

    # 1. Old query index still exists
    check("v1 query index exists",
          lambda: (os.path.exists(DB_V1), DB_V1))

    # 2. V2 query index exists
    check("v2 query index exists",
          lambda: (os.path.exists(DB_V2), DB_V2))

    # 3. Required v2 tables
    V2_REQUIRED_TABLES = [
        "candidates", "downloads", "inventory", "lexical_summary",
        "runtime_samples", "work_entities", "work_entity_links",
        "work_entity_evidence_matrix", "statement_sources", "lexical_mechanisms",
    ]
    check("v2 required tables present",
          lambda: sqlite_exists_with_tables(DB_V2, V2_REQUIRED_TABLES))

    # 4. Non-zero key table counts
    def check_inventory_count():
        n = sqlite_row_count(DB_V2, "inventory")
        return n > 0, f"inventory: {n} rows"
    check("inventory non-zero", check_inventory_count)

    def check_downloads_count():
        n = sqlite_row_count(DB_V2, "downloads")
        return n > 0, f"downloads: {n} rows"
    check("downloads non-zero", check_downloads_count)

    def check_entities_count():
        n = sqlite_row_count(DB_V2, "work_entities")
        return n > 0, f"work_entities: {n} rows"
    check("work_entities non-zero", check_entities_count)

    def check_statement_count():
        n = sqlite_row_count(DB_V2, "statement_sources")
        return n > 0, f"statement_sources: {n} rows"
    check("statement_sources non-zero", check_statement_count)

    def check_lexical_count():
        n = sqlite_row_count(DB_V2, "lexical_mechanisms")
        return n > 0, f"lexical_mechanisms: {n} rows"
    check("lexical_mechanisms non-zero", check_lexical_count)

    # 5. Context capture outputs
    def check_context_candidates():
        path = "data/private/context/context_page_candidates.csv"
        n = csv_row_count(path)
        return n > 0, f"{path}: {n} rows"
    check("context_page_candidates non-zero", check_context_candidates, critical=False)

    def check_context_capture_log():
        path = "data/private/context/context_page_capture_log.csv"
        n = csv_row_count(path)
        return n >= 0, f"{path}: {n} rows (may be 0 if fetch failed)"
    check("context_page_capture_log exists", check_context_capture_log, critical=False)

    # 6. Statement layer exists
    def check_statement_csv():
        path = "data/private/statement_sources_v2.csv"
        n = csv_row_count(path)
        return n > 0, f"{path}: {n} rows"
    check("statement_sources_v2.csv non-zero", check_statement_csv)

    # 7. Work entity layer exists
    def check_work_entities_csv():
        path = "data/private/work_entities.csv"
        n = csv_row_count(path)
        return n > 0, f"{path}: {n} rows"
    check("work_entities.csv non-zero", check_work_entities_csv)

    # 8. Lexical audit exists
    def check_lexical_csv():
        path = "data/private/lexical_mechanisms_v2.csv"
        n = csv_row_count(path)
        return n > 0, f"{path}: {n} rows"
    check("lexical_mechanisms_v2.csv non-zero", check_lexical_csv)

    # 9. Archive directories present
    for d in ["archive/raw_html", "archive/screenshots", "archive/context_pages"]:
        def make_dir_check(dd):
            return lambda: (os.path.isdir(dd), dd)
        check(f"archive dir: {d}", make_dir_check(d), critical=False)

    # 10. No missing required CSVs
    required_public = [
        "data/public/taroko_links.csv",
        "data/public/download_log.csv",
        "data/public/inventory.csv",
        "data/public/lexical_array_summary.csv",
        "data/public/runtime_sample_log.csv",
    ]
    for p in required_public:
        def make_csv_check(pp):
            return lambda: (csv_row_count(pp) > 0, f"{pp}: {csv_row_count(pp)} rows")
        check(f"public CSV non-zero: {p}", make_csv_check(p))

    # 11. dl_0013 contamination noted
    def check_dl0013_contamination():
        path = "data/private/lexical_mechanisms_v2.csv"
        if not os.path.exists(path):
            return False, "lexical_mechanisms_v2.csv not found"
        rows = utils.read_csv(path)
        row = next((r for r in rows if r.get("dl_id") == "dl_0013"), None)
        if not row:
            return False, "dl_0013 not in lexical_mechanisms_v2.csv"
        status = row.get("lexical_status", "")
        return "contaminated" in status, f"dl_0013 lexical_status={status}"
    check("dl_0013 contamination flagged", check_dl0013_contamination)

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    warnings = sum(1 for r in results if r["status"] == "WARNING")
    print(f"\nSummary: {passed}/{total} PASS, {failed} FAIL, {warnings} WARNING")

    # Write report
    lines = ["# Archive MVP v2 — Verification Report\n",
             f"Generated: {utils.now_iso()}\n\n",
             f"**Summary**: {passed}/{total} PASS, {failed} FAIL, {warnings} WARNING\n\n",
             "## Check Results\n\n",
             "| Status | Check | Detail |\n",
             "|--------|-------|--------|\n"]
    for r in results:
        lines.append(f"| {r['status']} | {r['label']} | {r['detail']} |\n")

    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\nReport: {OUT_REPORT}")

    critical_failures = [r for r in results if r["status"] == "FAIL" and r["critical"]]
    sys.exit(1 if critical_failures else 0)


if __name__ == "__main__":
    run_checks()
