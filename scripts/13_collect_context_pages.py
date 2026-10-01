"""Identify context-page candidates for ELC/ELMCIP/author pages."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_CANDIDATES = "data/private/context/context_page_candidates.csv"

# Known high-priority context pages to always include
KNOWN_CONTEXT_PAGES = [
    {
        "url": "https://collection.eliterature.org/3/collection-taroko.html",
        "source_type": "elc_collection",
        "priority": "high",
        "notes": "ELC3 collection index for Taroko Gorge remixes cluster",
    },
    {
        "url": "https://collection.eliterature.org/3/work.html?work=taroko-gorge",
        "source_type": "elc_work",
        "priority": "high",
        "notes": "ELC3 individual work page for Taroko Gorge",
    },
    {
        "url": "https://elmcip.net/creative-work/taroko-gorge",
        "source_type": "elmcip",
        "priority": "high",
        "notes": "ELMCIP record for Taroko Gorge",
    },
    {
        "url": "https://nickm.com/taroko_gorge/",
        "source_type": "post_position",
        "priority": "high",
        "notes": "Nick Montfort post position index page (author site)",
    },
    {
        "url": "https://nickm.com/",
        "source_type": "author_page",
        "priority": "medium",
        "notes": "Nick Montfort author homepage",
    },
    {
        "url": "https://collection.eliterature.org/3/index.html",
        "source_type": "elc_collection",
        "priority": "medium",
        "notes": "ELC3 main index page",
    },
]


def classify_url(url):
    """Classify a URL into a source_type and priority."""
    url_lower = url.lower()
    if "collection.eliterature.org" in url_lower:
        if "work.html" in url_lower:
            return "elc_work", "high"
        return "elc_collection", "high"
    if "elmcip.net" in url_lower:
        return "elmcip", "high"
    if "nickm.com" in url_lower:
        return "post_position", "medium"
    if "eliterature.org" in url_lower:
        return "elc_collection", "medium"
    return "other", "low"


def collect_context_pages():
    utils.ensure_dirs("data/private/context")

    links = utils.read_csv("data/public/taroko_links.csv")
    inventory = utils.read_csv("data/public/inventory.csv")

    # Build set of already-known URLs
    known_urls = {r["url"] for r in KNOWN_CONTEXT_PAGES}

    candidates = []
    cand_id = 1

    # Add all known context pages first
    for kp in KNOWN_CONTEXT_PAGES:
        candidates.append({
            "candidate_id": f"ctx_{cand_id:04d}",
            "url": kp["url"],
            "source_type": kp["source_type"],
            "discovered_from": "known_list",
            "priority": kp["priority"],
            "notes": kp["notes"],
        })
        cand_id += 1

    # Scan taroko_links.csv for ELC/ELMCIP/author pages
    for row in links:
        url = row.get("url", "").strip()
        if not url or url in known_urls:
            continue
        source_type, priority = classify_url(url)
        if source_type in ("elc_work", "elc_collection", "elmcip", "post_position"):
            candidates.append({
                "candidate_id": f"ctx_{cand_id:04d}",
                "url": url,
                "source_type": source_type,
                "discovered_from": "taroko_links.csv",
                "priority": priority,
                "notes": row.get("link_text", "")[:100],
            })
            known_urls.add(url)
            cand_id += 1

    # Scan inventory for ELC/ELMCIP pages
    for row in inventory:
        url = row.get("url", "").strip()
        if not url or url in known_urls:
            continue
        source_type, priority = classify_url(url)
        if source_type in ("elc_work", "elc_collection", "elmcip"):
            candidates.append({
                "candidate_id": f"ctx_{cand_id:04d}",
                "url": url,
                "source_type": source_type,
                "discovered_from": "inventory.csv",
                "priority": priority,
                "notes": row.get("title_tag", "")[:100],
            })
            known_urls.add(url)
            cand_id += 1

    utils.write_csv(OUT_CANDIDATES, candidates,
                    fieldnames=["candidate_id", "url", "source_type",
                                "discovered_from", "priority", "notes"])
    print(f"Context page candidates: {len(candidates)} -> {OUT_CANDIDATES}")


if __name__ == "__main__":
    collect_context_pages()
