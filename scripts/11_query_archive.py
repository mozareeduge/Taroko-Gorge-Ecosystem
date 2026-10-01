"""CLI inquiry tool for the Taroko Gorge archive query index.

Usage: python scripts/11_query_archive.py <command> [args]

Commands:
  overview              Archive-wide statistics
  find <term>           FTS search across all metadata
  work <id>             Full record for one work
  arrays <id>           Lexical arrays for one work
  array <id> <name>     Items in a specific array
  failures              All failed downloads
  runtime               Runtime sample status table
  manifest [category]   Manifest rows (optionally filtered by category)
  paths <id>            File paths for one work
  sql <query>           Read-only SQL query
  export <cmd> <file>   Export command output to CSV
  raw-search <term>     Search FTS and show raw snippet
"""
import argparse
import csv
import io
import json
import os
import sqlite3
import sys

DB_PATH = "data/private/taroko_query_index.sqlite"
EXPORT_DIR = "data/private/query_exports"


def connect():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: index not found at {DB_PATH}")
        print("Run: python scripts/10_build_query_index.py")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only=ON")
    return conn


def print_table(rows, cols=None):
    if not rows:
        print("(no rows)")
        return
    if cols is None:
        cols = list(rows[0].keys())
    widths = {c: max(len(c), max((len(str(r[c] or "")) for r in rows), default=0)) for c in cols}
    widths = {c: min(w, 60) for c, w in widths.items()}
    header = "  ".join(c.ljust(widths[c]) for c in cols)
    sep = "  ".join("-" * widths[c] for c in cols)
    print(header)
    print(sep)
    for row in rows:
        line = "  ".join(str(row[c] or "")[:widths[c]].ljust(widths[c]) for c in cols)
        print(line)


def cmd_overview(conn, _args):
    rows = conn.execute("SELECT key, value FROM archive_summary ORDER BY key").fetchall()
    print("=== Archive Overview ===")
    for r in rows:
        print(f"  {r['key']:30s} {r['value']}")


def cmd_find(conn, args):
    if not args:
        print("Usage: find <term>")
        return
    term = " ".join(args)
    rows = conn.execute(
        "SELECT work_id, url, title, snippet(archive_search,3,'>>','<<','...',12) AS match "
        "FROM archive_search WHERE archive_search MATCH ? ORDER BY rank LIMIT 30",
        (term,),
    ).fetchall()
    print(f"=== Find: '{term}' ({len(rows)} results) ===")
    print_table(rows, ["work_id", "url", "title", "match"])


def cmd_work(conn, args):
    if not args:
        print("Usage: work <id>")
        return
    wid = args[0]
    row = conn.execute("SELECT * FROM inventory WHERE id=?", (wid,)).fetchone()
    if not row:
        print(f"No inventory record for: {wid}")
        return
    print(f"=== Work: {wid} ===")
    for k in row.keys():
        print(f"  {k:25s} {row[k]}")

    dl = conn.execute("SELECT * FROM downloads WHERE archive_id=?", (wid,)).fetchone()
    if dl:
        print("\n--- Download ---")
        for k in dl.keys():
            print(f"  {k:25s} {dl[k]}")

    rs = conn.execute("SELECT status, seconds, error, captured_at FROM runtime_samples WHERE id=?", (wid,)).fetchone()
    if rs:
        print("\n--- Runtime Sample ---")
        for k in rs.keys():
            print(f"  {k:25s} {rs[k]}")


def cmd_arrays(conn, args):
    if not args:
        print("Usage: arrays <id>")
        return
    wid = args[0]
    rows = conn.execute(
        "SELECT array_name, item_count, sample_hash FROM lexical_array_summary WHERE id=? ORDER BY array_name",
        (wid,),
    ).fetchall()
    if not rows:
        rows = conn.execute(
            "SELECT array_name, item_count, items_preview AS sample_hash FROM full_arrays WHERE work_id=? ORDER BY array_name",
            (wid,),
        ).fetchall()
    print(f"=== Arrays for {wid} ({len(rows)} arrays) ===")
    print_table(rows, ["array_name", "item_count", "sample_hash"])


def cmd_array(conn, args):
    if len(args) < 2:
        print("Usage: array <id> <name>")
        return
    wid, name = args[0], args[1]
    row = conn.execute(
        "SELECT items_preview FROM full_arrays WHERE work_id=? AND array_name=?",
        (wid, name),
    ).fetchone()
    if not row:
        row = conn.execute(
            "SELECT sample_hash AS items_preview FROM lexical_array_summary WHERE id=? AND array_name=?",
            (wid, name),
        ).fetchone()
    if not row:
        print(f"No array '{name}' for work '{wid}'")
        return
    print(f"=== Array '{name}' for {wid} ===")
    items = row["items_preview"] or ""
    for item in items.split(" | "):
        print(f"  {item}")


def cmd_failures(conn, _args):
    rows = conn.execute(
        "SELECT archive_id, url, status_code, error "
        "FROM downloads WHERE error!='' AND error IS NOT NULL AND status_code!=200 ORDER BY archive_id"
    ).fetchall()
    print(f"=== Failed Downloads ({len(rows)}) ===")
    print_table(rows, ["archive_id", "url", "status_code", "error"])


def cmd_runtime(conn, _args):
    rows = conn.execute(
        "SELECT id, url, status, seconds, error FROM runtime_samples ORDER BY id"
    ).fetchall()
    print(f"=== Runtime Samples ({len(rows)}) ===")
    print_table(rows, ["id", "url", "status", "seconds", "error"])


def cmd_manifest(conn, args):
    cat = args[0] if args else None
    if cat:
        rows = conn.execute(
            "SELECT path, category, bytes, sha256, public_or_private FROM manifest WHERE category=? ORDER BY path",
            (cat,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT path, category, bytes, sha256, public_or_private FROM manifest ORDER BY category, path"
        ).fetchall()
    label = f"category={cat}" if cat else "all"
    print(f"=== Manifest ({label}, {len(rows)} rows) ===")
    print_table(rows, ["path", "category", "bytes", "sha256", "public_or_private"])


def cmd_paths(conn, args):
    if not args:
        print("Usage: paths <id>")
        return
    wid = args[0]
    rows = conn.execute(
        "SELECT file_type, path, bytes, sha256 FROM files_by_work WHERE work_id=? ORDER BY file_type",
        (wid,),
    ).fetchall()
    if not rows:
        # fallback: query manifest by work_id prefix
        rows = conn.execute(
            "SELECT category AS file_type, path, bytes, sha256 FROM manifest WHERE path LIKE ? ORDER BY category",
            (f"%{wid}%",),
        ).fetchall()
    print(f"=== Files for {wid} ({len(rows)}) ===")
    print_table(rows, ["file_type", "path", "bytes", "sha256"])


def cmd_sql(conn, args):
    if not args:
        print("Usage: sql <query>")
        return
    query = " ".join(args)
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        print("ERROR: only SELECT queries permitted")
        return
    try:
        rows = conn.execute(query).fetchall()
        print(f"=== SQL result ({len(rows)} rows) ===")
        if rows:
            print_table(rows)
    except sqlite3.Error as e:
        print(f"SQL error: {e}")


def cmd_export(conn, args):
    if len(args) < 2:
        print("Usage: export <command+args> <output.csv>")
        print("Example: export find taroko output.csv")
        return
    out_file = args[-1]
    cmd_args = args[:-1]
    if not out_file.endswith(".csv"):
        out_file += ".csv"
    if not os.path.isabs(out_file):
        os.makedirs(EXPORT_DIR, exist_ok=True)
        out_file = os.path.join(EXPORT_DIR, out_file)

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        dispatch(conn, cmd_args)
    finally:
        sys.stdout = old_stdout

    lines = [l for l in buf.getvalue().splitlines() if l and not l.startswith("===") and not l.startswith("---")]
    if not lines:
        print("No output to export.")
        return
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Exported to: {out_file}")


def cmd_raw_search(conn, args):
    if not args:
        print("Usage: raw-search <term>")
        return
    term = " ".join(args)
    rows = conn.execute(
        "SELECT work_id, url, title FROM archive_search WHERE archive_search MATCH ? ORDER BY rank LIMIT 50",
        (term,),
    ).fetchall()
    print(f"=== Raw FTS: '{term}' ({len(rows)} hits) ===")
    for r in rows:
        print(f"  {r['work_id']:15s}  {r['title'] or '(no title)':30s}  {r['url']}")


COMMANDS = {
    "overview": cmd_overview,
    "find": cmd_find,
    "work": cmd_work,
    "arrays": cmd_arrays,
    "array": cmd_array,
    "failures": cmd_failures,
    "runtime": cmd_runtime,
    "manifest": cmd_manifest,
    "paths": cmd_paths,
    "sql": cmd_sql,
    "export": cmd_export,
    "raw-search": cmd_raw_search,
}


def dispatch(conn, args):
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    rest = args[1:]
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(sorted(COMMANDS))}")
        return
    fn(conn, rest)


def main():
    conn = connect()
    dispatch(conn, sys.argv[1:])
    conn.close()


if __name__ == "__main__":
    main()
