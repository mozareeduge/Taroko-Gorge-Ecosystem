"""CLI query tool for taroko_query_index_v2.sqlite."""
import sys
import os
import sqlite3
import argparse
import csv
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

DB_PATH = "data/private/taroko_query_index_v2.sqlite"

SAFE_EXPORTS = {
    "work_entities": "SELECT work_entity_id, canonical_title, known_author_or_creator_trace, representation_status, statement_status, lexical_status FROM work_entities",
    "evidence_matrix": "SELECT * FROM work_entity_evidence_matrix",
    "statement_inventory": "SELECT work_entity_id, statement_type, confidence, copyright_risk, notes FROM statement_sources",
    "paratext_sections": "SELECT candidate_id, section_label, present, excerpt_50w, confidence FROM elc_paratext_sections",
    "lexical_status": "SELECT dl_id, url, arrays_found, lexical_status, contamination_notes FROM lexical_mechanisms",
    "failures_by_work": "SELECT id, url, status_code, error FROM downloads WHERE status_code != '200' OR error != ''",
    "mirror_relations": "SELECT * FROM mirror_pairs",
    "public_safe_metadata": "SELECT i.id, i.url, i.title_tag, i.probable_taroko_score, i.author_guess FROM inventory i",
}


def get_conn():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}. Run script 19 first.")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)


def table_exists(conn, name):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


def print_rows(rows, headers=None):
    if not rows:
        print("(no results)")
        return
    if headers is None and rows:
        headers = [d[0] for d in rows[0].keys()] if hasattr(rows[0], 'keys') else None
    for row in rows:
        print("  " + " | ".join(str(v) for v in row))


def cmd_overview(conn):
    print("=== Archive v2 Overview ===")
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    for (tname,) in tables:
        try:
            count = conn.execute(f'SELECT COUNT(*) FROM "{tname}"').fetchone()[0]
            print(f"  {tname}: {count} rows")
        except Exception:
            print(f"  {tname}: (error)")


def cmd_entities(conn):
    if not table_exists(conn, "work_entities"):
        print("work_entities table not found.")
        return
    rows = conn.execute(
        "SELECT work_entity_id, canonical_title, known_author_or_creator_trace, "
        "representation_status, statement_status, lexical_status FROM work_entities"
    ).fetchall()
    print(f"=== Work Entities ({len(rows)}) ===")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | {row[2]} | rep={row[3]} | stmt={row[4]} | lex={row[5]}")


def cmd_entity(conn, entity_id):
    if not table_exists(conn, "work_entities"):
        print("work_entities table not found.")
        return
    row = conn.execute(
        "SELECT * FROM work_entities WHERE work_entity_id=?", (entity_id,)
    ).fetchone()
    if not row:
        print(f"Entity '{entity_id}' not found.")
        return
    cols = [d[0] for d in conn.execute("SELECT * FROM work_entities LIMIT 0").description]
    print(f"=== Entity: {entity_id} ===")
    for col, val in zip(cols, row):
        print(f"  {col}: {val}")

    # Evidence matrix
    if table_exists(conn, "work_entity_evidence_matrix"):
        matrix = conn.execute(
            "SELECT evidence_type, evidence_present, count FROM work_entity_evidence_matrix WHERE work_entity_id=?",
            (entity_id,)
        ).fetchall()
        print("  Evidence:")
        for ev_type, present, count in matrix:
            print(f"    {ev_type}: {present} (count={count})")

    # Links
    if table_exists(conn, "work_entity_links"):
        links = conn.execute(
            "SELECT link_type, url_or_path, status FROM work_entity_links WHERE work_entity_id=?",
            (entity_id,)
        ).fetchall()
        print("  Links:")
        for lt, url, status in links:
            print(f"    {lt}: {url} [{status}]")


def cmd_statements(conn, work_id=None, stmt_type=None):
    if not table_exists(conn, "statement_sources"):
        print("statement_sources table not found.")
        return
    if work_id:
        rows = conn.execute(
            "SELECT work_entity_id, statement_type, confidence, notes FROM statement_sources WHERE work_entity_id=?",
            (work_id,)
        ).fetchall()
        print(f"=== Statements for {work_id} ===")
    elif stmt_type:
        rows = conn.execute(
            "SELECT work_entity_id, statement_type, confidence, notes FROM statement_sources WHERE statement_type=?",
            (stmt_type,)
        ).fetchall()
        print(f"=== Statements of type '{stmt_type}' ===")
    else:
        rows = conn.execute(
            "SELECT work_entity_id, statement_type, confidence, notes FROM statement_sources"
        ).fetchall()
        print("=== All Statements ===")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | conf={row[2]} | {row[3][:80]}")


def cmd_paratext(conn, work_id):
    if not table_exists(conn, "elc_paratext_sections"):
        print("elc_paratext_sections not found.")
        return
    rows = conn.execute(
        "SELECT section_label, present, excerpt_50w FROM elc_paratext_sections WHERE candidate_id LIKE ?",
        (f"%{work_id}%",)
    ).fetchall()
    print(f"=== Paratext for {work_id} ===")
    for section_label, present, excerpt in rows:
        print(f"  {section_label}: {present} | {excerpt[:60]}")


def cmd_evidence(conn, work_id):
    if not table_exists(conn, "work_entity_evidence_matrix"):
        print("work_entity_evidence_matrix not found.")
        return
    rows = conn.execute(
        "SELECT evidence_type, evidence_present, count, notes FROM work_entity_evidence_matrix WHERE work_entity_id=?",
        (work_id,)
    ).fetchall()
    print(f"=== Evidence Matrix for {work_id} ===")
    for ev_type, present, count, notes in rows:
        print(f"  {ev_type}: {present} (count={count}) | {notes}")


def cmd_lexical(conn, work_id=None, status=None):
    if not table_exists(conn, "lexical_mechanisms"):
        print("lexical_mechanisms not found.")
        return
    if work_id:
        rows = conn.execute(
            "SELECT dl_id, url, arrays_found, lexical_status, contamination_notes FROM lexical_mechanisms WHERE dl_id LIKE ?",
            (f"%{work_id}%",)
        ).fetchall()
        print(f"=== Lexical for {work_id} ===")
    elif status:
        rows = conn.execute(
            "SELECT dl_id, url, arrays_found, lexical_status FROM lexical_mechanisms WHERE lexical_status=?",
            (status,)
        ).fetchall()
        print(f"=== Lexical status '{status}' ===")
    else:
        rows = conn.execute(
            "SELECT dl_id, url, arrays_found, lexical_status FROM lexical_mechanisms"
        ).fetchall()
        print("=== All Lexical ===")
    for row in rows:
        print("  " + " | ".join(str(v) for v in row))


def cmd_mirrors(conn):
    if not table_exists(conn, "mirror_pairs"):
        print("mirror_pairs not found.")
        return
    rows = conn.execute("SELECT * FROM mirror_pairs").fetchall()
    print(f"=== Mirror Pairs ({len(rows)}) ===")
    for row in rows:
        print("  " + " | ".join(str(v) for v in row))


def cmd_failures(conn):
    rows = conn.execute(
        "SELECT id, url, status_code, error FROM downloads WHERE status_code != '200' OR (error IS NOT NULL AND error != '')"
    ).fetchall()
    print(f"=== Failed Downloads ({len(rows)}) ===")
    for row in rows:
        print(f"  {row[0]} | {row[1][:60]} | status={row[2]} | {row[3]}")


def cmd_search(conn, text):
    # Try FTS5 first
    if table_exists(conn, "archive_search"):
        try:
            rows = conn.execute(
                'SELECT dl_id, url, title FROM archive_search WHERE archive_search MATCH ?',
                (text,)
            ).fetchall()
            print(f"=== Search: '{text}' (FTS5, {len(rows)} results) ===")
            for row in rows:
                print(f"  {row[0]} | {row[1][:60]} | {row[2]}")
            return
        except Exception:
            pass
    # Fallback: LIKE search in inventory
    rows = conn.execute(
        "SELECT id, url, title_tag FROM inventory WHERE url LIKE ? OR title_tag LIKE ? OR h1_text LIKE ?",
        (f"%{text}%", f"%{text}%", f"%{text}%")
    ).fetchall()
    print(f"=== Search: '{text}' (LIKE, {len(rows)} results) ===")
    for row in rows:
        print(f"  {row[0]} | {row[1][:60]} | {row[2]}")


def cmd_sql(conn, query):
    query_stripped = query.strip().upper()
    if not query_stripped.startswith("SELECT"):
        print("ERROR: Only SELECT queries are allowed.")
        return
    try:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        print("  " + " | ".join(cols))
        print("  " + "-" * 60)
        for row in rows:
            print("  " + " | ".join(str(v) for v in row))
        print(f"  ({len(rows)} rows)")
    except Exception as e:
        print(f"SQL error: {e}")


def cmd_export(conn, query_name):
    if query_name not in SAFE_EXPORTS:
        print(f"Unknown export: {query_name}. Available: {', '.join(SAFE_EXPORTS)}")
        return
    sql = SAFE_EXPORTS[query_name]
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        out_path = f"data/private/query_exports/export_{query_name}.csv"
        utils.ensure_dirs("data/private/query_exports")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        print(f"Exported {len(rows)} rows -> {out_path}")
    except Exception as e:
        print(f"Export error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Query the Taroko Gorge v2 archive.")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("overview", help="Show row counts for all tables")
    sub.add_parser("entities", help="List all work entities")
    p_ent = sub.add_parser("entity", help="Show details for one work entity")
    p_ent.add_argument("--id", required=True, help="work_entity_id")

    p_stmt = sub.add_parser("statements", help="Query statements")
    p_stmt.add_argument("--work", help="Filter by work_entity_id")
    p_stmt.add_argument("--type", dest="stmt_type", help="Filter by statement_type")

    p_pt = sub.add_parser("paratext", help="Show paratext sections")
    p_pt.add_argument("--work", required=True)

    p_ev = sub.add_parser("evidence", help="Show evidence matrix")
    p_ev.add_argument("--work", required=True)

    p_lex = sub.add_parser("lexical", help="Query lexical mechanisms")
    p_lex.add_argument("--work", help="Filter by dl_id fragment")

    p_ls = sub.add_parser("lexical-status", help="Filter by lexical_status")
    p_ls.add_argument("status")

    sub.add_parser("mirrors", help="Show mirror pairs")
    sub.add_parser("failures", help="Show failed downloads")

    p_search = sub.add_parser("search", help="Text search")
    p_search.add_argument("--text", required=True)

    p_sql = sub.add_parser("sql", help="Run a read-only SQL query")
    p_sql.add_argument("--query", required=True)

    p_exp = sub.add_parser("export", help="Export a named query to CSV")
    p_exp.add_argument("--query", required=True, dest="query_name")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    conn = get_conn()
    conn.row_factory = sqlite3.Row

    if args.command == "overview":
        cmd_overview(conn)
    elif args.command == "entities":
        cmd_entities(conn)
    elif args.command == "entity":
        cmd_entity(conn, args.id)
    elif args.command == "statements":
        cmd_statements(conn, work_id=getattr(args, "work", None),
                       stmt_type=getattr(args, "stmt_type", None))
    elif args.command == "paratext":
        cmd_paratext(conn, args.work)
    elif args.command == "evidence":
        cmd_evidence(conn, args.work)
    elif args.command == "lexical":
        cmd_lexical(conn, work_id=getattr(args, "work", None))
    elif args.command == "lexical-status":
        cmd_lexical(conn, status=args.status)
    elif args.command == "mirrors":
        cmd_mirrors(conn)
    elif args.command == "failures":
        cmd_failures(conn)
    elif args.command == "search":
        cmd_search(conn, args.text)
    elif args.command == "sql":
        cmd_sql(conn, args.query)
    elif args.command == "export":
        cmd_export(conn, args.query_name)

    conn.close()


if __name__ == "__main__":
    main()
