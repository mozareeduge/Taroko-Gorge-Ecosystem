"""Build SQLite query index from archive CSVs and extracted data.

Stores metadata, paths, checksums, and previews — NOT raw HTML content.
"""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

DB_PATH = "data/private/taroko_query_index.sqlite"

PUBLIC = "data/public"
PRIVATE = "data/private"
FULL_ARRAYS = "archive/extracted_full/lexical_arrays_full.json"


def connect(path):
    utils.ensure_dirs(os.path.dirname(path))
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def create_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id TEXT PRIMARY KEY,
        url TEXT,
        source_page TEXT,
        collected_at TEXT,
        link_text TEXT
    );

    CREATE TABLE IF NOT EXISTS downloads (
        archive_id TEXT PRIMARY KEY,
        url TEXT,
        status_code INTEGER,
        content_type TEXT,
        local_path TEXT,
        sha256 TEXT,
        bytes INTEGER,
        skipped TEXT,
        error TEXT,
        captured_at TEXT
    );

    CREATE TABLE IF NOT EXISTS inventory (
        id TEXT PRIMARY KEY,
        url TEXT,
        local_path TEXT,
        probable_taroko_score INTEGER,
        title TEXT,
        has_js TEXT,
        contains_known_array_names TEXT,
        notes TEXT
    );

    CREATE TABLE IF NOT EXISTS lexical_array_summary (
        id TEXT,
        url TEXT,
        array_name TEXT,
        item_count INTEGER,
        sample_hash TEXT,
        notes TEXT,
        PRIMARY KEY (id, array_name)
    );

    CREATE TABLE IF NOT EXISTS manifest (
        sha256 TEXT,
        path TEXT PRIMARY KEY,
        category TEXT,
        source_url TEXT,
        bytes INTEGER,
        created_at TEXT,
        public_or_private TEXT,
        note TEXT
    );

    CREATE TABLE IF NOT EXISTS runtime_samples (
        id TEXT PRIMARY KEY,
        url TEXT,
        status TEXT,
        screenshot_path TEXT,
        text_sample_path TEXT,
        text_preview TEXT,
        seconds INTEGER,
        error TEXT,
        captured_at TEXT
    );

    CREATE TABLE IF NOT EXISTS screenshots (
        id TEXT PRIMARY KEY,
        url TEXT,
        screenshot_path TEXT,
        bytes INTEGER,
        sha256 TEXT,
        captured_at TEXT
    );

    CREATE TABLE IF NOT EXISTS full_arrays (
        work_id TEXT,
        array_name TEXT,
        item_count INTEGER,
        items_preview TEXT,
        PRIMARY KEY (work_id, array_name)
    );

    CREATE TABLE IF NOT EXISTS files_by_work (
        work_id TEXT,
        file_type TEXT,
        path TEXT,
        bytes INTEGER,
        sha256 TEXT,
        PRIMARY KEY (work_id, file_type)
    );

    CREATE TABLE IF NOT EXISTS archive_summary (
        key TEXT PRIMARY KEY,
        value TEXT
    );

    CREATE VIRTUAL TABLE IF NOT EXISTS archive_search USING fts5(
        work_id,
        url,
        title,
        array_names,
        text_preview,
        items_preview
    );
    """)

    conn.executescript("""
    CREATE INDEX IF NOT EXISTS idx_downloads_status ON downloads(status_code);
    CREATE INDEX IF NOT EXISTS idx_inventory_score ON inventory(probable_taroko_score);
    CREATE INDEX IF NOT EXISTS idx_lexical_work ON lexical_array_summary(id);
    CREATE INDEX IF NOT EXISTS idx_manifest_category ON manifest(category);
    CREATE INDEX IF NOT EXISTS idx_runtime_status ON runtime_samples(status);
    """)
    conn.commit()


def load_candidates(conn):
    rows = utils.read_csv(f"{PUBLIC}/taroko_links.csv")
    conn.executemany(
        "INSERT OR REPLACE INTO candidates VALUES (?,?,?,?,?)",
        [
            (
                r.get("candidate_id", r.get("id", "")),
                r.get("url", ""),
                r.get("source_page", r.get("source_seed", "")),
                r.get("captured_at", r.get("collected_at", "")),
                r.get("link_text", ""),
            )
            for r in rows
        ],
    )
    conn.commit()
    return len(rows)


def load_downloads(conn):
    rows = utils.read_csv(f"{PUBLIC}/download_log.csv")
    conn.executemany(
        "INSERT OR REPLACE INTO downloads VALUES (?,?,?,?,?,?,?,?,?,?)",
        [
            (
                r.get("id", ""),
                r.get("url", ""),
                _int(r.get("status_code", "")),
                r.get("content_type", ""),
                r.get("local_path", r.get("raw_html_path", "")),
                r.get("sha256", ""),
                _int(r.get("bytes", "")),
                r.get("skipped", "false"),
                r.get("error", ""),
                r.get("captured_at", r.get("downloaded_at", "")),
            )
            for r in rows
        ],
    )
    conn.commit()
    return len(rows)


def load_inventory(conn):
    rows = utils.read_csv(f"{PUBLIC}/inventory.csv")
    conn.executemany(
        "INSERT OR REPLACE INTO inventory VALUES (?,?,?,?,?,?,?,?)",
        [
            (
                r.get("id", ""),
                r.get("url", ""),
                r.get("local_path", r.get("raw_html_path", "")),
                _int(r.get("probable_taroko_score", 0)),
                r.get("title_tag", r.get("title", "")),
                r.get("has_javascript", r.get("has_js", "")),
                r.get("contains_known_array_names", ""),
                r.get("notes", ""),
            )
            for r in rows
        ],
    )
    conn.commit()
    return len(rows)


def load_lexical_summary(conn):
    rows = utils.read_csv(f"{PUBLIC}/lexical_array_summary.csv")
    conn.executemany(
        "INSERT OR REPLACE INTO lexical_array_summary VALUES (?,?,?,?,?,?)",
        [
            (
                r.get("id", ""),
                r.get("url", ""),
                r.get("array_name", ""),
                _int(r.get("item_count", 0)),
                r.get("sample_hash", r.get("array_hash", "")),
                r.get("notes", ""),
            )
            for r in rows
        ],
    )
    conn.commit()
    return len(rows)


def load_manifest(conn):
    rows = utils.read_csv(f"{PRIVATE}/archive_manifest.csv")
    if not rows:
        return 0
    conn.executemany(
        "INSERT OR REPLACE INTO manifest VALUES (?,?,?,?,?,?,?,?)",
        [
            (
                r.get("sha256", ""),
                r.get("path", ""),
                r.get("category", ""),
                r.get("source_url", ""),
                _int(r.get("bytes", 0)),
                r.get("created_at", ""),
                r.get("public_or_private", ""),
                r.get("note", ""),
            )
            for r in rows
        ],
    )
    conn.commit()
    return len(rows)


def load_runtime_samples(conn):
    rows = utils.read_csv(f"{PUBLIC}/runtime_sample_log.csv")
    result = []
    for r in rows:
        text_preview = ""
        tp = r.get("text_sample_path", "")
        if tp and os.path.exists(tp):
            try:
                with open(tp, encoding="utf-8", errors="replace") as f:
                    text_preview = f.read(500).strip()
            except OSError:
                pass
        result.append((
            r.get("id", ""),
            r.get("url", ""),
            r.get("status", ""),
            r.get("screenshot_path", ""),
            tp,
            text_preview,
            _int(r.get("seconds", 0)),
            r.get("error", ""),
            r.get("captured_at", ""),
        ))
    conn.executemany(
        "INSERT OR REPLACE INTO runtime_samples VALUES (?,?,?,?,?,?,?,?,?)",
        result,
    )
    conn.commit()
    return len(result)


def load_screenshots(conn):
    rows = utils.read_csv(f"{PUBLIC}/runtime_sample_log.csv")
    result = []
    for r in rows:
        sp = r.get("screenshot_path", "")
        if not sp or not os.path.exists(sp):
            continue
        size = os.path.getsize(sp)
        sha = utils.sha256_file(sp)
        result.append((r.get("id", ""), r.get("url", ""), sp, size, sha, r.get("captured_at", "")))
    conn.executemany(
        "INSERT OR REPLACE INTO screenshots VALUES (?,?,?,?,?,?)",
        result,
    )
    conn.commit()
    return len(result)


def load_full_arrays(conn):
    if not os.path.exists(FULL_ARRAYS):
        return 0
    with open(FULL_ARRAYS, encoding="utf-8") as f:
        data = json.load(f)
    result = []
    for work_id, work_data in data.items():
        if not isinstance(work_data, dict):
            continue
        arrays = work_data.get("arrays", [])
        if not isinstance(arrays, list):
            continue
        for arr in arrays:
            if not isinstance(arr, dict):
                continue
            array_name = arr.get("name", "")
            items = arr.get("items", [])
            if not array_name or not isinstance(items, list):
                continue
            preview = " | ".join(str(x) for x in items[:10])
            result.append((work_id, array_name, len(items), preview))
    conn.executemany(
        "INSERT OR REPLACE INTO full_arrays VALUES (?,?,?,?)",
        result,
    )
    conn.commit()
    return len(result)


def load_files_by_work(conn):
    manifest_rows = utils.read_csv(f"{PRIVATE}/archive_manifest.csv")
    result = []
    for r in manifest_rows:
        path = r.get("path", "")
        cat = r.get("category", "")
        if not path or cat not in ("raw_html", "screenshot", "output_sample", "extracted"):
            continue
        basename = os.path.basename(path)
        # derive work_id from filename prefix (e.g. dl_0001_... or inv_0001_...)
        work_id = _extract_work_id(basename)
        if work_id:
            result.append((
                work_id, cat, path,
                _int(r.get("bytes", 0)),
                r.get("sha256", ""),
            ))
    conn.executemany(
        "INSERT OR REPLACE INTO files_by_work VALUES (?,?,?,?,?)",
        result,
    )
    conn.commit()
    return len(result)


def _extract_work_id(filename):
    import re
    m = re.match(r"^([a-zA-Z0-9_]+?_\d+)", filename)
    return m.group(1) if m else None


def build_fts(conn):
    conn.execute("DELETE FROM archive_search")
    rows = conn.execute("""
        SELECT
            i.id, i.url, i.title,
            i.contains_known_array_names AS array_names,
            rs.text_preview,
            GROUP_CONCAT(fa.items_preview, ' | ') AS items_preview
        FROM inventory i
        LEFT JOIN runtime_samples rs ON i.id = rs.id
        LEFT JOIN full_arrays fa ON i.id = fa.work_id
        GROUP BY i.id
    """).fetchall()
    conn.executemany(
        "INSERT INTO archive_search VALUES (?,?,?,?,?,?)",
        [(r[0], r[1], r[2] or "", r[3] or "", r[4] or "", r[5] or "") for r in rows],
    )
    conn.commit()
    return len(rows)


def build_summary(conn):
    summary = {}
    summary["candidates_total"] = conn.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
    summary["downloads_success"] = conn.execute(
        "SELECT COUNT(*) FROM downloads WHERE status_code=200"
    ).fetchone()[0]
    summary["downloads_failed"] = conn.execute(
        "SELECT COUNT(*) FROM downloads WHERE error!='' AND error IS NOT NULL AND status_code!=200"
    ).fetchone()[0]
    summary["inventory_total"] = conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0]
    summary["score_5"] = conn.execute(
        "SELECT COUNT(*) FROM inventory WHERE probable_taroko_score=5"
    ).fetchone()[0]
    summary["score_4"] = conn.execute(
        "SELECT COUNT(*) FROM inventory WHERE probable_taroko_score=4"
    ).fetchone()[0]
    summary["score_3"] = conn.execute(
        "SELECT COUNT(*) FROM inventory WHERE probable_taroko_score=3"
    ).fetchone()[0]
    summary["runtime_ok"] = conn.execute(
        "SELECT COUNT(*) FROM runtime_samples WHERE status='ok'"
    ).fetchone()[0]
    summary["screenshots_ok"] = conn.execute("SELECT COUNT(*) FROM screenshots").fetchone()[0]
    summary["manifest_rows"] = conn.execute("SELECT COUNT(*) FROM manifest").fetchone()[0]
    summary["built_at"] = utils.now_iso()
    conn.executemany(
        "INSERT OR REPLACE INTO archive_summary VALUES (?,?)",
        list(summary.items()),
    )
    conn.commit()
    return summary


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def main():
    print(f"Building query index: {DB_PATH}")
    conn = connect(DB_PATH)
    create_schema(conn)

    n = load_candidates(conn)
    print(f"  candidates: {n}")
    n = load_downloads(conn)
    print(f"  downloads: {n}")
    n = load_inventory(conn)
    print(f"  inventory: {n}")
    n = load_lexical_summary(conn)
    print(f"  lexical_array_summary: {n}")
    n = load_manifest(conn)
    print(f"  manifest: {n}")
    n = load_runtime_samples(conn)
    print(f"  runtime_samples: {n}")
    n = load_screenshots(conn)
    print(f"  screenshots: {n}")
    n = load_full_arrays(conn)
    print(f"  full_arrays rows: {n}")
    n = load_files_by_work(conn)
    print(f"  files_by_work: {n}")
    n = build_fts(conn)
    print(f"  fts index rows: {n}")
    summary = build_summary(conn)

    conn.close()
    size = os.path.getsize(DB_PATH)
    print(f"Query index built: {DB_PATH} ({size:,} bytes)")
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()
