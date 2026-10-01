"""Extract paratext sections from captured context pages."""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

IN_LOG = "data/private/context/context_page_capture_log.csv"
OUT_SECTIONS = "data/private/context/elc_paratext_sections.csv"
OUT_METADATA = "data/private/context/elc_work_metadata.csv"
OUT_LINKS = "data/private/context/elc_download_links.csv"

# Section labels to search for (case-insensitive heading text)
SECTION_LABELS = [
    "Statement", "Author", "Authors", "Bio", "Biography",
    "Metadata", "Year", "Language", "Keywords", "Tech Details",
    "Technical Details", "Editorial Statement", "Downloads",
    "Previous Publication", "Further References", "Copyright",
    "Copyright Info", "Begin", "About", "Description",
    "Project Description", "Notes",
]

HEADING_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6", "dt", "strong", "b", "th"]

LINK_TYPES = {
    "executable": re.compile(r"\b(begin|launch|play|run|start|execute|open)\b", re.I),
    "source": re.compile(r"\b(source|code|js|javascript|download source)\b", re.I),
    "download": re.compile(r"\b(download|zip|archive|pdf)\b", re.I),
}


def words_50(text):
    """Return first 50 words of text."""
    words = text.split()
    return " ".join(words[:50])


def classify_link(text, href):
    href_lower = href.lower()
    text_lower = text.lower()
    if href_lower.endswith((".js", ".html", ".htm")) or LINK_TYPES["executable"].search(text_lower):
        return "executable"
    if LINK_TYPES["source"].search(text_lower) or href_lower.endswith((".py", ".js")):
        return "source"
    if LINK_TYPES["download"].search(text_lower) or href_lower.endswith((".zip", ".pdf")):
        return "download"
    return "external"


def extract_sections(candidate_id, soup):
    """Extract sections by heading labels. Returns list of section dicts."""
    sections = []
    found_labels = set()

    # Find headings matching known section labels
    for tag in soup.find_all(HEADING_TAGS):
        heading_text = tag.get_text(strip=True)
        for label in SECTION_LABELS:
            if label.lower() in heading_text.lower() and label not in found_labels:
                # Get next sibling content
                content_parts = []
                sibling = tag.find_next_sibling()
                chars = 0
                while sibling and chars < 2000:
                    # Stop at next heading
                    if sibling.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        break
                    text = sibling.get_text(separator=" ", strip=True)
                    if text:
                        content_parts.append(text)
                        chars += len(text)
                    sibling = sibling.find_next_sibling()

                content = " ".join(content_parts).strip()
                full_len = len(content)
                excerpt = words_50(content)
                confidence = "high" if full_len > 20 else "low"
                present = "yes" if full_len > 5 else "no"

                sections.append({
                    "candidate_id": candidate_id,
                    "section_label": label,
                    "present": present,
                    "excerpt_50w": excerpt,
                    "full_length": full_len,
                    "confidence": confidence,
                    "extraction_method": "heading_sibling",
                    "notes": f"heading='{heading_text[:60]}'",
                })
                found_labels.add(label)
                break

    # Mark missing sections
    for label in SECTION_LABELS:
        if label not in found_labels:
            sections.append({
                "candidate_id": candidate_id,
                "section_label": label,
                "present": "no",
                "excerpt_50w": "",
                "full_length": 0,
                "confidence": "high",
                "extraction_method": "heading_sibling",
                "notes": "not found",
            })

    return sections


def extract_metadata_fields(candidate_id, url, soup):
    """Extract structured metadata fields."""
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""

    # Author: look for meta author or common patterns
    author = ""
    meta_author = soup.find("meta", attrs={"name": re.compile("author", re.I)})
    if meta_author:
        author = meta_author.get("content", "")[:200]

    # Year: look for 4-digit year in meta or content
    year = ""
    meta_date = soup.find("meta", attrs={"name": re.compile("date|year|created", re.I)})
    if meta_date:
        year = meta_date.get("content", "")[:10]
    if not year:
        year_match = re.search(r"\b(199\d|200\d|201\d|202\d)\b", soup.get_text())
        if year_match:
            year = year_match.group(0)

    # Language
    lang = ""
    html_tag = soup.find("html")
    if html_tag:
        lang = html_tag.get("lang", "")[:10]

    # Keywords
    keywords = ""
    meta_kw = soup.find("meta", attrs={"name": re.compile("keyword", re.I)})
    if meta_kw:
        keywords = meta_kw.get("content", "")[:300]

    # Description
    desc = ""
    meta_desc = soup.find("meta", attrs={"name": re.compile("description", re.I)})
    if meta_desc:
        desc = words_50(meta_desc.get("content", ""))

    return {
        "candidate_id": candidate_id,
        "url": url,
        "title": (title or h1_text)[:300],
        "author": author,
        "year": year,
        "language": lang,
        "keywords": keywords[:300],
        "description_excerpt": desc,
        "notes": "",
    }


def extract_links(candidate_id, url, soup):
    """Extract download/executable/source links."""
    from urllib.parse import urljoin
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#") or href.startswith("mailto"):
            continue
        abs_href = urljoin(url, href)
        if abs_href in seen:
            continue
        seen.add(abs_href)
        text = a.get_text(strip=True)[:200]
        link_type = classify_link(text, abs_href)
        if link_type in ("executable", "source", "download"):
            links.append({
                "candidate_id": candidate_id,
                "link_text": text,
                "href": abs_href,
                "link_type": link_type,
                "notes": "",
            })
    return links


def extract_paratext():
    utils.ensure_dirs("data/private/context")
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("beautifulsoup4 not available; cannot parse HTML")
        return

    capture_log = utils.read_csv(IN_LOG)
    if not capture_log:
        print(f"No capture log at {IN_LOG}. Run script 14 first.")
        # Write empty output files with headers
        utils.write_csv(OUT_SECTIONS, [], fieldnames=[
            "candidate_id", "section_label", "present", "excerpt_50w",
            "full_length", "confidence", "extraction_method", "notes"])
        utils.write_csv(OUT_METADATA, [], fieldnames=[
            "candidate_id", "url", "title", "author", "year",
            "language", "keywords", "description_excerpt", "notes"])
        utils.write_csv(OUT_LINKS, [], fieldnames=[
            "candidate_id", "link_text", "href", "link_type", "notes"])
        return

    all_sections = []
    all_metadata = []
    all_links = []

    for row in capture_log:
        cid = row["candidate_id"]
        url = row["url"]
        local_path = row.get("local_path", "")
        method = row.get("capture_method", "failed")

        if not local_path or "failed" in method or not os.path.exists(local_path):
            # Write placeholder sections
            all_sections.append({
                "candidate_id": cid,
                "section_label": "ALL",
                "present": "no",
                "excerpt_50w": "",
                "full_length": 0,
                "confidence": "n/a",
                "extraction_method": "not_captured",
                "notes": f"capture_method={method}",
            })
            continue

        with open(local_path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        sections = extract_sections(cid, soup)
        metadata = extract_metadata_fields(cid, url, soup)
        links = extract_links(cid, url, soup)

        all_sections.extend(sections)
        all_metadata.append(metadata)
        all_links.extend(links)

    fields_sections = ["candidate_id", "section_label", "present", "excerpt_50w",
                       "full_length", "confidence", "extraction_method", "notes"]
    fields_metadata = ["candidate_id", "url", "title", "author", "year",
                       "language", "keywords", "description_excerpt", "notes"]
    fields_links = ["candidate_id", "link_text", "href", "link_type", "notes"]

    utils.write_csv(OUT_SECTIONS, all_sections, fieldnames=fields_sections)
    utils.write_csv(OUT_METADATA, all_metadata, fieldnames=fields_metadata)
    utils.write_csv(OUT_LINKS, all_links, fieldnames=fields_links)

    present_count = sum(1 for s in all_sections if s.get("present") == "yes")
    print(f"Sections extracted: {len(all_sections)} entries, {present_count} present")
    print(f"Metadata rows: {len(all_metadata)} -> {OUT_METADATA}")
    print(f"Links rows: {len(all_links)} -> {OUT_LINKS}")


if __name__ == "__main__":
    extract_paratext()
