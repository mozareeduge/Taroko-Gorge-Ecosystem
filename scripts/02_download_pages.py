"""Download candidate pages locally into archive/raw_html/."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

IN_LINKS = "data/public/taroko_links.csv"
OUT_LOG = "data/public/download_log.csv"
RAW_HTML_DIR = "archive/raw_html"


def is_binary_ct(ct):
    if not ct:
        return False
    ct = ct.lower()
    return any(x in ct for x in ["image/", "audio/", "video/", "application/octet", "font/"])


def download_pages(limit=None, force=False):
    utils.ensure_dirs("data/public", RAW_HTML_DIR)
    links = utils.read_csv(IN_LINKS)

    seen = {}
    for row in links:
        url = row["url"]
        if url not in seen:
            seen[url] = row

    urls = list(seen.values())
    if limit:
        urls = urls[:limit]

    log_rows = []
    idx = 0

    for row in urls:
        url = row["url"]
        idx += 1
        ext = ".html"
        filename = utils.safe_filename(url, index=idx, ext=ext)
        local_path = os.path.join(RAW_HTML_DIR, filename)

        if os.path.exists(local_path) and not force:
            sha = utils.sha256_file(local_path)
            size = os.path.getsize(local_path)
            log_rows.append({
                "id": f"dl_{idx:04d}", "url": url, "status_code": "",
                "content_type": "", "local_path": local_path,
                "sha256": sha, "bytes": size, "skipped": "true",
                "error": "", "captured_at": utils.now_iso(),
            })
            print(f"[skip] {url}")
            continue

        print(f"[{idx}] Fetching {url}")
        resp = utils.fetch_url(url)

        if resp is None or isinstance(resp, tuple):
            error = resp[1] if isinstance(resp, tuple) else "no response"
            log_rows.append({
                "id": f"dl_{idx:04d}", "url": url, "status_code": "",
                "content_type": "", "local_path": "",
                "sha256": "", "bytes": 0, "skipped": "false",
                "error": error, "captured_at": utils.now_iso(),
            })
            continue

        ct = resp.headers.get("Content-Type", "")
        status = resp.status_code

        if status != 200:
            log_rows.append({
                "id": f"dl_{idx:04d}", "url": url, "status_code": status,
                "content_type": ct, "local_path": "",
                "sha256": "", "bytes": 0, "skipped": "false",
                "error": f"HTTP {status}", "captured_at": utils.now_iso(),
            })
            continue

        if is_binary_ct(ct):
            log_rows.append({
                "id": f"dl_{idx:04d}", "url": url, "status_code": status,
                "content_type": ct, "local_path": "",
                "sha256": "", "bytes": 0, "skipped": "true",
                "error": "binary content-type skipped", "captured_at": utils.now_iso(),
            })
            continue

        if "javascript" in ct.lower():
            filename = utils.safe_filename(url, index=idx, ext=".js")
            local_path = os.path.join(RAW_HTML_DIR, filename)

        with open(local_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(resp.text)

        sha = utils.sha256_file(local_path)
        size = os.path.getsize(local_path)

        log_rows.append({
            "id": f"dl_{idx:04d}", "url": url, "status_code": status,
            "content_type": ct, "local_path": local_path,
            "sha256": sha, "bytes": size, "skipped": "false",
            "error": "", "captured_at": utils.now_iso(),
        })
        print(f"  -> {local_path} ({size} bytes)")

    utils.write_csv(OUT_LOG, log_rows)
    print(f"Download log saved to {OUT_LOG} ({len(log_rows)} entries)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_pages(limit=args.limit, force=args.force)
