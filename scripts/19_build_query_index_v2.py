"""Build taroko_query_index_v2.sqlite from all v2 CSVs."""
import sys
import os
import csv
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_DB = "data/private/taroko_query_index_v2.sqlite"

# Table definitions: (table_name, csv_path)
TABLE_SOURCES = [
    ("candidates", "data/public/taroko_links.csv"),
    ("downloads", "data/public/download_log.csv"),
    ("inventory", "data/public/inventory.csv"),
    ("lexical_summary", "data/public/lexical_array_summary.csv"),
    ("runtime_samples", "data/public/runtime_sample_log.csv"),
    ("work_entities", "data/private/work_entities.csv"),
    ("work_entity_links", "data/private/work_entity_links.csv"),
    ("work_entity_evidence_matrix", "data/private/work_entity_evidence_matrix.csv"),
    ("context_page_candidates", "data/private/context/context_page_candidates.csv"),
    ("context_page_capture_log", "data/private/context/context_page_capture_log.csv"),
    ("elc_paratext_sections", "data/private/context/elc_paratext_sections.csv"),
    ("elc_work_metadata", "data/private/context/elc_work_metadata.csv"),
    ("elc_download_links", "data/private/context/elc_download_links.csv"),
    ("statement_sources", "data/private/statement_sources_v2.csv"),
    ("statement_excerpts", "data/private/statement_excerpts_safe.csv"),
    ("lexical_mechanisms", "data/private/lexical_mechanisms_v2.csv"),
    ("audit_scores", "data/private/query_exports/audit_scores.csv"),
    ("mirror_pairs", "data/private/query_exports/mirror_pair_hash_comparison.csv"),
]


def sanitize_col(name):
    """Make column name SQL-safe."""
    import re
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


def load_csv_to_table(conn, table_name, csv_path):
    if not os.path.exists(csv_path):
        print(f"  SKIP (not found): {csv_path} -> {table_name}")
        return 0

    rows = utils.read_csv(csv_path)
    if not rows:
        print(f"  SKIP (empty): {csv_path} -> {table_name}")
        return 0

    cols = [sanitize_col(k) for k in rows[0].keys()]
    orig_cols = list(rows[0].keys())

    col_defs = ", ".join(f'"{c}" TEXT' for c in cols)
    conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    conn.execute(f'CREATE TABLE "{table_name}" ({col_defs})')

    placeholders = ", ".join("?" for _ in cols)
    insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'

    data = []
    for row in rows:
        data.append(tuple(row.get(orig_k, "") for orig_k in orig_cols))

    conn.executemany(insert_sql, data)
    conn.commit()
    print(f"  OK: {csv_path} -> {table_name} ({len(rows)} rows)")
    return len(rows)


def build_fts(conn):
    """Build FTS5 index over key text columns."""
    try:
        conn.execute("DROP TABLE IF EXISTS archive_search")
        conn.execute("""
            CREATE VIRTUAL TABLE archive_search USING fts5(
                dl_id, url, title, text_content,
                content='',
                tokenize='unicode61'
            )
        """)
        # Index inventory
        for row in conn.execute("SELECT id, url, title_tag, h1_text FROM inventory").fetchall():
            conn.execute(
                "INSERT INTO archive_search(dl_id, url, title, text_content) VALUES (?,?,?,?)",
                (row[0], row[1], row[2], row[3])
            )
        conn.commit()
        print("  FTS5 index built: archive_search")
    except Exception as e:
        print(f"  FTS5 index failed (optional): {e}")


def build_index():
    utils.ensure_dirs("data/private")

    if os.path.exists(OUT_DB):
        os.remove(OUT_DB)

    conn = sqlite3.connect(OUT_DB)
    conn.execute("PRAGMA journal_mode=WAL")

    total_tables = 0
    total_rows = 0

    for table_name, csv_path in TABLE_SOURCES:
        n = load_csv_to_table(conn, table_name, csv_path)
        if n > 0:
            total_tables += 1
            total_rows += n

    build_fts(conn)
    conn.close()

    size_kb = os.path.getsize(OUT_DB) // 1024
    print(f"\nBuilt {OUT_DB}: {total_tables} tables, {total_rows} total rows, {size_kb} KB")


if __name__ == "__main__":
    build_index()
