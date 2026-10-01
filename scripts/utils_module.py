import csv
import hashlib
import os
import re
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests

USER_AGENT = "TarokoArchiveBot/1.0 (research; non-commercial)"
REQUEST_TIMEOUT = 20
POLITE_DELAY = 1.5


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)


def safe_filename(url, index=None, ext=".html"):
    parsed = urlparse(url)
    slug = parsed.netloc + parsed.path
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")[:80]
    prefix = f"{index:04d}_" if index is not None else ""
    return f"{prefix}{slug}{ext}"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_url(base, href):
    href = href.strip()
    if href.startswith("//"):
        parsed = urlparse(base)
        return f"{parsed.scheme}:{href}"
    return urljoin(base, href)


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames=None):
    if not rows:
        if fieldnames:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fetch_url(url, delay=True):
    if delay:
        time.sleep(POLITE_DELAY)
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        return resp
    except requests.RequestException as e:
        return None, str(e)


def is_probably_html_content_type(ct):
    if not ct:
        return False
    ct = ct.lower()
    return "html" in ct or "javascript" in ct or "text/plain" in ct


def short_text(text, maxlen=200):
    if not text:
        return ""
    text = " ".join(text.split())
    return text[:maxlen]
