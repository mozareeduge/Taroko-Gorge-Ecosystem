"""Optional runtime screenshots and visible text samples via Playwright."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

IN_INVENTORY = "data/public/inventory.csv"
OUT_LOG = "data/public/runtime_sample_log.csv"
SCREENSHOTS_DIR = "archive/screenshots"
SAMPLES_DIR = "archive/output_samples"
MIN_SCORE = 3


def run_runtime_sample(limit=None, seconds=10):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed. Skipping runtime sampling.")
        print("To enable: pip install playwright && playwright install chromium")
        return

    utils.ensure_dirs(SCREENSHOTS_DIR, SAMPLES_DIR, "data/public")
    inventory = utils.read_csv(IN_INVENTORY)

    candidates = [
        r for r in inventory
        if int(r.get("probable_taroko_score", 0)) >= MIN_SCORE
    ]
    if limit:
        candidates = candidates[:limit]

    log_rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for entry in candidates:
            url = entry["url"]
            eid = entry["id"]
            print(f"Runtime sample: {url}")

            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{eid}_screenshot.png")
            text_path = os.path.join(SAMPLES_DIR, f"{eid}_sample.txt")

            try:
                page = browser.new_page()
                page.goto(url, timeout=30000)
                page.wait_for_timeout(seconds * 1000)
                page.screenshot(path=screenshot_path, full_page=False)
                text = page.inner_text("body")
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(text[:4000])
                page.close()
                log_rows.append({
                    "id": eid, "url": url, "status": "ok",
                    "screenshot_path": screenshot_path,
                    "text_sample_path": text_path,
                    "seconds": seconds, "error": "",
                    "captured_at": utils.now_iso(),
                })
            except Exception as e:
                log_rows.append({
                    "id": eid, "url": url, "status": "error",
                    "screenshot_path": "", "text_sample_path": "",
                    "seconds": seconds, "error": str(e)[:300],
                    "captured_at": utils.now_iso(),
                })
        browser.close()

    utils.write_csv(OUT_LOG, log_rows)
    print(f"Runtime sample log: {OUT_LOG} ({len(log_rows)} entries)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seconds", type=int, default=10)
    args = parser.parse_args()
    run_runtime_sample(limit=args.limit, seconds=args.seconds)
