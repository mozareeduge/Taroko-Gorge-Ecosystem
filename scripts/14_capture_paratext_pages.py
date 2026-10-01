"""Fetch context pages and save HTML to archive/context_pages/."""
import sys
import os
import hashlib
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

IN_CANDIDATES = "data/private/context/context_page_candidates.csv"
OUT_LOG = "data/private/context/context_page_capture_log.csv"
CONTEXT_DIR = "archive/context_pages"


def sha256_str(text):
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def try_playwright(url, out_path):
    """Try to fetch with playwright; return (html, method) or (None, 'failed')."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000, wait_until="networkidle")
            html = page.content()
            browser.close()
            with open(out_path, "w", encoding="utf-8", errors="replace") as f:
                f.write(html)
            return html, "playwright"
    except Exception as e:
        return None, f"playwright_failed:{e}"


def capture_pages():
    utils.ensure_dirs(CONTEXT_DIR, "archive/context_screenshots", "data/private/context")

    candidates = utils.read_csv(IN_CANDIDATES)
    if not candidates:
        print(f"No candidates found at {IN_CANDIDATES}. Run script 13 first.")
        return

    import requests as req
    log_rows = []

    for cand in candidates:
        cid = cand["candidate_id"]
        url = cand["url"]
        out_path = os.path.join(CONTEXT_DIR, f"{cid}.html")
        row = {
            "candidate_id": cid,
            "url": url,
            "http_status": "",
            "capture_method": "failed",
            "local_path": "",
            "sha256": "",
            "capture_timestamp": utils.now_iso(),
            "notes": "",
        }

        # Try requests first
        try:
            time.sleep(1.0)
            resp = req.get(url, headers={"User-Agent": utils.USER_AGENT},
                           timeout=utils.REQUEST_TIMEOUT, allow_redirects=True)
            row["http_status"] = str(resp.status_code)
            if resp.status_code == 200:
                html = resp.text
                with open(out_path, "w", encoding="utf-8", errors="replace") as f:
                    f.write(html)
                row["capture_method"] = "requests"
                row["local_path"] = out_path
                row["sha256"] = sha256_str(html)
                row["notes"] = f"content_type={resp.headers.get('content-type','')[:80]}"
            else:
                # Try playwright for non-200 (JS-rendered pages)
                html, method = try_playwright(url, out_path)
                if html:
                    row["capture_method"] = method
                    row["local_path"] = out_path
                    row["sha256"] = sha256_str(html)
                    row["notes"] = f"requests_failed_{resp.status_code}_playwright_ok"
                else:
                    row["notes"] = f"http_{resp.status_code}_{method}"
        except Exception as e:
            row["http_status"] = "error"
            row["notes"] = str(e)[:200]
            # Try playwright as fallback
            html, method = try_playwright(url, out_path)
            if html:
                row["capture_method"] = method
                row["local_path"] = out_path
                row["sha256"] = sha256_str(html)
                row["notes"] = f"requests_exception_playwright_ok"

        log_rows.append(row)
        status = row["capture_method"]
        print(f"  {cid} {url[:60]} -> {status}")

    fields = ["candidate_id", "url", "http_status", "capture_method",
              "local_path", "sha256", "capture_timestamp", "notes"]
    utils.write_csv(OUT_LOG, log_rows, fieldnames=fields)
    ok = sum(1 for r in log_rows if r["capture_method"] not in ("failed",) and "failed" not in r["capture_method"])
    print(f"Captured: {ok}/{len(log_rows)} pages -> {OUT_LOG}")


if __name__ == "__main__":
    capture_pages()
