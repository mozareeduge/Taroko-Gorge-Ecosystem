"""Build complete corpus catalog joining all pipeline outputs."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

CATALOG_COLS = [
    "candidate_id", "archive_id", "url", "source_page", "link_text",
    "download_status", "http_status", "content_type", "local_raw_html_path",
    "sha256", "bytes", "title_tag", "h1_text", "author_guess",
    "probable_taroko_score", "has_javascript", "generator_signals",
    "array_names", "array_count", "runtime_sample_path", "screenshot_path",
    "failure_or_gap_note", "captured_at", "rights_note", "research_note",
]


def build_catalog():
    utils.ensure_dirs("data/private")

    links = utils.read_csv("data/public/taroko_links.csv")
    dl_log = utils.read_csv("data/public/download_log.csv")
    inventory = utils.read_csv("data/public/inventory.csv")
    lex_summary = utils.read_csv("data/public/lexical_array_summary.csv")
    runtime_log = utils.read_csv("data/public/runtime_sample_log.csv")

    dl_by_url = {row["url"]: row for row in dl_log}
    inv_by_url = {row["url"]: row for row in inventory}

    lex_by_id = {}
    for row in lex_summary:
        rid = row["id"]
        if rid not in lex_by_id:
            lex_by_id[rid] = {"names": [], "count": 0}
        lex_by_id[rid]["names"].append(row["array_name"])
        try:
            lex_by_id[rid]["count"] += int(row.get("item_count", 0))
        except ValueError:
            pass

    runtime_by_id = {row["id"]: row for row in runtime_log}

    rows = []
    for link in links:
        url = link["url"]
        dl = dl_by_url.get(url, {})
        inv = inv_by_url.get(url, {})
        archive_id = dl.get("id", "")
        lex = lex_by_id.get(archive_id, {})
        rt = runtime_by_id.get(archive_id, {})

        if not dl:
            dl_status = "not_attempted"
        elif dl.get("skipped") == "true" and not dl.get("error"):
            dl_status = "skipped_cached"
        elif dl.get("error"):
            dl_status = "failed"
        elif str(dl.get("status_code", "")) == "200":
            dl_status = "success"
        else:
            dl_status = f"http_{dl.get('status_code', 'unknown')}"

        gap = ""
        if dl.get("error"):
            gap = dl["error"]
        elif not dl:
            gap = "URL not in download log"
        elif not inv and dl_status == "success":
            gap = "downloaded but not in inventory"
        if rt.get("status") == "error":
            rt_err = rt.get("error", "runtime error")
            gap = (gap + "; " if gap else "") + f"runtime failed: {rt_err[:100]}"

        rows.append({
            "candidate_id": link.get("candidate_id", ""),
            "archive_id": archive_id,
            "url": url,
            "source_page": link.get("source_page", ""),
            "link_text": link.get("link_text", ""),
            "download_status": dl_status,
            "http_status": dl.get("status_code", ""),
            "content_type": dl.get("content_type", ""),
            "local_raw_html_path": dl.get("local_path", ""),
            "sha256": dl.get("sha256", ""),
            "bytes": dl.get("bytes", ""),
            "title_tag": inv.get("title_tag", ""),
            "h1_text": inv.get("h1_text", ""),
            "author_guess": inv.get("author_guess", ""),
            "probable_taroko_score": inv.get("probable_taroko_score", ""),
            "has_javascript": inv.get("has_javascript", ""),
            "generator_signals": inv.get("contains_generator_signals", ""),
            "array_names": "|".join(lex.get("names", [])),
            "array_count": str(lex.get("count", "")) if lex.get("count") else "",
            "runtime_sample_path": rt.get("text_sample_path", ""),
            "screenshot_path": rt.get("screenshot_path", ""),
            "failure_or_gap_note": gap,
            "captured_at": dl.get("captured_at", link.get("captured_at", "")),
            "rights_note": "",
            "research_note": "",
        })

    utils.write_csv("data/private/taroko_corpus_catalog.csv", rows, fieldnames=CATALOG_COLS)
    print(f"Corpus catalog: data/private/taroko_corpus_catalog.csv ({len(rows)} rows)")
    successes = sum(1 for r in rows if r["download_status"] == "success")
    failures = sum(1 for r in rows if r["download_status"] == "failed")
    print(f"  success: {successes}, failed: {failures}, total: {len(rows)}")


if __name__ == "__main__":
    build_catalog()
