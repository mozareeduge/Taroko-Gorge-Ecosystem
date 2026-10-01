"""Collect candidate Taroko/remix URLs from seed pages."""
import os
import re
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils
from bs4 import BeautifulSoup

SEEDS_CSV = "seeds/taroko_seed_urls.csv"
OUT_LINKS = "data/public/taroko_links.csv"
OUT_LOG = "data/public/collect_links_log.csv"

SKIP_EXTENSIONS = re.compile(
    r"\.(css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|pdf|zip|mp3|mp4|avi|mov|xml)$",
    re.I,
)
SKIP_SCHEMES = re.compile(r"^(mailto:|javascript:|#)", re.I)
SOCIAL_PATTERNS = re.compile(
    r"(twitter\.com|facebook\.com|share|tweet|linkedin|instagram)", re.I
)


def should_keep_nickm(url, link_text):
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return False, None
    if SKIP_EXTENSIONS.search(parsed.path):
        return False, None
    if SOCIAL_PATTERNS.search(url):
        return False, None
    if re.search(r"(taroko|gorge|remix|poem|generate)", url + " " + link_text, re.I):
        return True, "nickm-taroko-related"
    if "nickm.com" in parsed.netloc and "/taroko" in parsed.path:
        return True, "nickm-taroko-path"
    return False, None


def should_keep_elc(url, link_text):
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return False, None
    if SKIP_EXTENSIONS.search(parsed.path):
        return False, None
    if "eliterature.org" in parsed.netloc:
        if re.search(r"(taroko|gorge|collection)", url + " " + link_text, re.I):
            return True, "elc-taroko"
        if "/collection" in parsed.path and "/works" in parsed.path:
            return True, "elc-work-link"
    if re.search(r"(taroko|gorge)", url + " " + link_text, re.I):
        return True, "elc-taroko-related"
    return False, None


def should_keep_elmcip(url, link_text):
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return False, None
    if SKIP_EXTENSIONS.search(parsed.path):
        return False, None
    if "elmcip.net" in parsed.netloc:
        if re.search(r"(taroko|gorge|attachment|files/media)", url + " " + link_text, re.I):
            return True, "elmcip-taroko"
        if "/sites/default/files/" in parsed.path:
            return True, "elmcip-attachment"
    if re.search(r"(taroko|gorge)", url + " " + link_text, re.I):
        return True, "elmcip-taroko-related"
    return False, None


def collect_links():
    utils.ensure_dirs("data/public")
    seeds = utils.read_csv(SEEDS_CSV)

    all_links = []
    log_rows = []
    candidate_id = 0

    for s in seeds:
        candidate_id += 1
        all_links.append({
            "candidate_id": f"cand_{candidate_id:04d}",
            "source_page": s["seed_url"],
            "url": s["seed_url"],
            "link_text": s["note"],
            "reason_kept": "seed-url",
            "captured_at": utils.now_iso(),
        })

    for s in seeds:
        seed_url = s["seed_url"]
        print(f"Fetching seed: {seed_url}")
        resp = utils.fetch_url(seed_url)

        if resp is None or isinstance(resp, tuple):
            error = resp[1] if isinstance(resp, tuple) else "no response"
            log_rows.append({
                "source_page": seed_url, "status_code": "",
                "links_found": 0, "links_kept": 0,
                "error": error, "captured_at": utils.now_iso(),
            })
            continue

        status = resp.status_code
        if status != 200:
            log_rows.append({
                "source_page": seed_url, "status_code": status,
                "links_found": 0, "links_kept": 0,
                "error": f"HTTP {status}", "captured_at": utils.now_iso(),
            })
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        anchors = soup.find_all("a", href=True)
        found = 0
        kept = 0

        for a in anchors:
            href = a["href"].strip()
            if SKIP_SCHEMES.match(href):
                continue
            norm = utils.normalize_url(seed_url, href)
            link_text = a.get_text(strip=True)[:200]
            found += 1

            parsed_seed = urlparse(seed_url)
            keep, reason = False, None

            if "nickm.com" in parsed_seed.netloc:
                keep, reason = should_keep_nickm(norm, link_text)
            elif "eliterature.org" in parsed_seed.netloc:
                keep, reason = should_keep_elc(norm, link_text)
            elif "elmcip.net" in parsed_seed.netloc:
                keep, reason = should_keep_elmcip(norm, link_text)

            if keep:
                if not any(r["url"] == norm and r["source_page"] == seed_url for r in all_links):
                    candidate_id += 1
                    all_links.append({
                        "candidate_id": f"cand_{candidate_id:04d}",
                        "source_page": seed_url,
                        "url": norm,
                        "link_text": link_text,
                        "reason_kept": reason,
                        "captured_at": utils.now_iso(),
                    })
                    kept += 1

        log_rows.append({
            "source_page": seed_url, "status_code": status,
            "links_found": found, "links_kept": kept,
            "error": "", "captured_at": utils.now_iso(),
        })

    utils.write_csv(OUT_LINKS, all_links)
    utils.write_csv(OUT_LOG, log_rows)
    print(f"Saved {len(all_links)} candidate links to {OUT_LINKS}")
    print(f"Log saved to {OUT_LOG}")


if __name__ == "__main__":
    collect_links()
