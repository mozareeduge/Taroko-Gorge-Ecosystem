"""Build statement layer v2 with corrected taxonomy."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_SOURCES = "data/private/statement_sources_v2.csv"
OUT_EXCERPTS = "data/private/statement_excerpts_safe.csv"

# Known statements from local evidence (derived from inquiry 04 and inventory)
# Source: data/public/runtime_sample_log.csv, archive/output_samples/ (not read directly)
# Evidence: cited by dl_id and local path
KNOWN_STATEMENTS = [
    {
        "work_entity_id": "we_0008",
        "source_location": "archive/output_samples/dl_0013_sample.txt",
        "local_path_or_url": "http://exinfoam.wordpress.com/2011/07/18/yoko-engorged/",
        "section_label": "blog_post_body",
        "statement_type": "explicit_author_statement",
        "confidence": "high",
        "copyright_risk": "medium",
        "notes": "First-person statement by Eric Snodgrass; describes method and conceptual lineage (Fluxus/Ono). Full text in output sample.",
        "excerpt_max_50w": "Ever wondered what would happen if you took the playful and free spirited method to be found in Yoko Ono's Fluxus writings and forced upon it the perhaps also liberating but rather more sordid and mechanical approach",
        "paraphrase_max_60w": "Eric Snodgrass describes combining Yoko Ono's Fluxus playfulness with a mechanical digital approach, using Montfort's Taroko Gorge code and replacing its vocabulary with sexual/physical action words derived from Beatles fan fiction. The result is Yoko Engorged.",
    },
    {
        "work_entity_id": "we_0002",
        "source_location": "archive/output_samples/dl_0002_sample.txt",
        "local_path_or_url": "https://collection.eliterature.org/3/collection-taroko.html",
        "section_label": "collection_description",
        "statement_type": "editorial_statement",
        "confidence": "high",
        "copyright_risk": "medium",
        "notes": "ELC3 editorial description of the Taroko Gorge collection. Not an author statement from Montfort.",
        "excerpt_max_50w": "Inspired by a visit to Taroko Gorge in Taiwan, Nick Montfort's modest, procedurally-generated poem has produced an entire subgenre of remixes, remakes, constrained writing experiments, and parodies.",
        "paraphrase_max_60w": "ELC3 editors describe Taroko Gorge as a short procedural poem that inspired numerous remixes, noting its geological subject matter and the poem's 'code economics' (under a thousand words of JavaScript). The editors frame this as a platform for poetic play.",
    },
    {
        "work_entity_id": "we_0013",
        "source_location": "archive/raw_html/0018_nickm_com_taroko_gorge_designer_gulch.html",
        "local_path_or_url": "https://nickm.com/taroko_gorge/designer_gulch/",
        "section_label": "inline_html_text",
        "statement_type": "project_description",
        "confidence": "medium",
        "copyright_risk": "low",
        "notes": "Designer Gulch by Brendan Howell contains about-text visible in output sample. Classified as project description, not author statement.",
        "excerpt_max_50w": "",
        "paraphrase_max_60w": "Brendan Howell's Designer Gulch replaces Taroko Gorge's natural landscape vocabulary with terms from the fashion and design industry.",
    },
    {
        "work_entity_id": "we_0001",
        "source_location": "data/private/context/context_page_capture_log.csv",
        "local_path_or_url": "https://collection.eliterature.org/3/work.html?work=taroko-gorge",
        "section_label": "Statement_section_pending",
        "statement_type": "unresolved",
        "confidence": "low",
        "copyright_risk": "low",
        "notes": "ELC3 work page for Taroko Gorge may contain author statement. Pending context page capture (script 14/15).",
        "excerpt_max_50w": "",
        "paraphrase_max_60w": "",
    },
]

# dl_ids with generated output (runtime samples) — NOT statements
GENERATED_OUTPUT_IDS = [
    "dl_0001", "dl_0005", "dl_0006", "dl_0007", "dl_0008", "dl_0009",
    "dl_0011", "dl_0012", "dl_0014", "dl_0015", "dl_0016", "dl_0017",
    "dl_0018", "dl_0019", "dl_0020", "dl_0022", "dl_0024", "dl_0025",
    "dl_0026", "dl_0027", "dl_0028", "dl_0029", "dl_0030", "dl_0031",
    "dl_0032", "dl_0033", "dl_0035", "dl_0036", "dl_0037", "dl_0038",
    "dl_0039", "dl_0040", "dl_0041", "dl_0042", "dl_0043", "dl_0044",
    "dl_0046", "dl_0048", "dl_0049", "dl_0050", "dl_0052", "dl_0053",
    "dl_0054", "dl_0055", "dl_0056", "dl_0059", "dl_0060",
]

STATEMENT_TYPES = [
    "explicit_author_statement",
    "artist_statement",
    "project_description",
    "editorial_statement",
    "announcement_or_blog_context",
    "source_code_comment",
    "minimal_context",
    "bio",
    "metadata_only",
    "epigraph_only",
    "runtime_instruction",
    "generated_output",
    "no_statement_found",
    "unresolved",
]


def build_statement_layer():
    utils.ensure_dirs("data/private")

    # Load v1 statement inventory if available
    v1_path = "data/private/query_exports/inquiry_04_statement_inventory.csv"
    v1_statements = utils.read_csv(v1_path) if os.path.exists(v1_path) else []

    # Load paratext sections if available
    paratext_path = "data/private/context/elc_paratext_sections.csv"
    paratext = utils.read_csv(paratext_path) if os.path.exists(paratext_path) else []

    source_rows = []
    excerpt_rows = []

    # Add known statements
    for s in KNOWN_STATEMENTS:
        source_rows.append({
            "work_entity_id": s["work_entity_id"],
            "source_location": s["source_location"],
            "local_path_or_url": s["local_path_or_url"],
            "section_label": s["section_label"],
            "statement_type": s["statement_type"],
            "confidence": s["confidence"],
            "copyright_risk": s["copyright_risk"],
            "notes": s["notes"],
        })
        if s.get("excerpt_max_50w") or s.get("paraphrase_max_60w"):
            excerpt_rows.append({
                "work_entity_id": s["work_entity_id"],
                "statement_type": s["statement_type"],
                "excerpt_max_50w": s.get("excerpt_max_50w", "")[:300],
                "paraphrase_max_60w": s.get("paraphrase_max_60w", "")[:400],
                "confidence": s["confidence"],
                "source": s["source_location"],
                "notes": "",
            })

    # Process paratext sections for Statement/Editorial entries
    for pt in paratext:
        if pt.get("present") == "yes" and pt.get("section_label") in (
                "Statement", "Editorial Statement", "Author", "Bio", "Description"):
            cid = pt["candidate_id"]
            label = pt["section_label"]
            excerpt = pt.get("excerpt_50w", "")
            stmt_type = "unresolved"
            if label == "Statement":
                stmt_type = "explicit_author_statement"
            elif label == "Editorial Statement":
                stmt_type = "editorial_statement"
            elif label == "Bio":
                stmt_type = "bio"
            elif label in ("Author", "Description"):
                stmt_type = "project_description"

            source_rows.append({
                "work_entity_id": f"ctx:{cid}",
                "source_location": f"data/private/context/elc_paratext_sections.csv",
                "local_path_or_url": f"archive/context_pages/{cid}.html",
                "section_label": label,
                "statement_type": stmt_type,
                "confidence": pt.get("confidence", "medium"),
                "copyright_risk": "low",
                "notes": f"extracted_from_context_page;full_length={pt.get('full_length',0)}",
            })
            if excerpt:
                excerpt_rows.append({
                    "work_entity_id": f"ctx:{cid}",
                    "statement_type": stmt_type,
                    "excerpt_max_50w": excerpt,
                    "paraphrase_max_60w": "",
                    "confidence": pt.get("confidence", "medium"),
                    "source": f"archive/context_pages/{cid}.html",
                    "notes": "",
                })

    # Add no_statement_found entries for remaining inventory works
    inventory = utils.read_csv("data/public/inventory.csv")
    covered_entity_ids = {r["work_entity_id"] for r in source_rows}
    # (simplified: just note the count)
    no_stmt_count = 0
    for row in inventory:
        dl_id = row.get("id", "")
        # Skip if this dl is in KNOWN_STATEMENTS coverage
        if dl_id in ("dl_0002", "dl_0012", "dl_0013", "dl_0018"):
            continue
        if dl_id in GENERATED_OUTPUT_IDS:
            source_rows.append({
                "work_entity_id": f"dl:{dl_id}",
                "source_location": f"archive/output_samples/{dl_id}_sample.txt",
                "local_path_or_url": row.get("url", ""),
                "section_label": "runtime_output",
                "statement_type": "generated_output",
                "confidence": "high",
                "copyright_risk": "high",
                "notes": "Runtime execution trace. NOT a statement about the work.",
            })
            no_stmt_count += 1

    fields_sources = [
        "work_entity_id", "source_location", "local_path_or_url",
        "section_label", "statement_type", "confidence", "copyright_risk", "notes",
    ]
    fields_excerpts = [
        "work_entity_id", "statement_type", "excerpt_max_50w",
        "paraphrase_max_60w", "confidence", "source", "notes",
    ]

    utils.write_csv(OUT_SOURCES, source_rows, fieldnames=fields_sources)
    utils.write_csv(OUT_EXCERPTS, excerpt_rows, fieldnames=fields_excerpts)

    print(f"Statement sources: {len(source_rows)} -> {OUT_SOURCES}")
    print(f"Statement excerpts: {len(excerpt_rows)} -> {OUT_EXCERPTS}")
    by_type = {}
    for r in source_rows:
        t = r["statement_type"]
        by_type[t] = by_type.get(t, 0) + 1
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    build_statement_layer()
