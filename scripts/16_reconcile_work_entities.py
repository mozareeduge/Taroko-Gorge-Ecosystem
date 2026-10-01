"""Group URLs into distinct work entities."""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_ENTITIES = "data/private/work_entities.csv"
OUT_LINKS = "data/private/work_entity_links.csv"
OUT_MATRIX = "data/private/work_entity_evidence_matrix.csv"

# Known work entity definitions: (entity_id, canonical_title, url_patterns_or_dl_ids, author)
# Mirror pairs and title-based groupings
KNOWN_ENTITIES = [
    ("we_0001", "Taroko Gorge", "taroko_gorge_original", "Nick Montfort",
     ["dl_0001", "dl_0005"], "nickm.com/taroko_gorge/"),
    ("we_0002", "ELC3 Taroko Gorge Collection Page", "elc3_collection", "ELO Editorial",
     ["dl_0002"], "collection.eliterature.org"),
    ("we_0003", "Tokyo Garage", "tokyo_garage", "Scott Rettberg",
     ["dl_0006"], "nickm.com"),
    ("we_0004", "GORGE", "gorge_jrc", "J.R. Carpenter",
     ["dl_0007", "dl_0008"], "nickm.com / luckysoap.com"),
    ("we_0005", "WHISPER WIRE", "whisper_wire", "J.R. Carpenter",
     ["dl_0009"], "nickm.com"),
    ("we_0006", "Along the Briny Beach", "along_the_briny_beach", "J.R. Carpenter",
     ["dl_0010"], "nickm.com"),
    ("we_0007", "TOY GARBAGE", "toy_garbage", "Talan Memmott",
     ["dl_0011"], "nickm.com"),
    ("we_0008", "Yoko Engorged", "yoko_engorged", "Eric Snodgrass",
     ["dl_0012", "dl_0013"], "nickm.com / exinfoam.wordpress.com"),
    ("we_0009", "Takei, George", "takei_george", "Mark Sample",
     ["dl_0014"], "nickm.com"),
    ("we_0010", "Alone Engaged", "alone_engaged", "Unknown",
     ["dl_0015"], "nickm.com"),
    ("we_0011", "FRED & GEORGE", "fred_and_george", "Unknown",
     ["dl_0016"], "nickm.com"),
    ("we_0012", "Argot Ogre, OK!", "argot_ogre_ok", "Unknown",
     ["dl_0017"], "nickm.com"),
    ("we_0013", "Designer Gulch", "designer_gulch", "Brendan Howell",
     ["dl_0018"], "nickm.com"),
    ("we_0014", "Inside the House", "inside_the_house", "Unknown",
     ["dl_0019"], "nickm.com"),
    ("we_0015", "Taroko Gary", "taroko_gary", "Unknown",
     ["dl_0020"], "nickm.com"),
    ("we_0016", "Snowball", "snowball", "Unknown",
     ["dl_0022"], "nickm.com"),
    ("we_0017", "Camel Tail", "camel_tail", "Unknown",
     ["dl_0023"], "nickm.com"),
    ("we_0018", "Tournedo Gorge", "tournedo_gorge", "Unknown",
     ["dl_0024"], "nickm.com"),
    ("we_0019", "Tasty Gougere", "tasty_gougere", "Unknown",
     ["dl_0025"], "nickm.com"),
    ("we_0020", "Scholars contemplate the Irish beer", "scholars_contemplate", "Unknown",
     ["dl_0026"], "nickm.com"),
    ("we_0021", "The Dark Side of the Wall", "dark_side_of_the_wall", "Unknown",
     ["dl_0027"], "nickm.com"),
    ("we_0022", "Tacoma Grunge", "tacoma_grunge", "Unknown",
     ["dl_0028"], "nickm.com"),
    ("we_0023", "Pigeon Forge", "pigeon_forge", "Unknown",
     ["dl_0029"], "nickm.com"),
    ("we_0024", "TransmoGrify", "transmogrify", "Unknown",
     ["dl_0030"], "nickm.com"),
    ("we_0025", "Take Ogre", "take_ogre", "Unknown",
     ["dl_0031"], "nickm.com"),
    ("we_0026", "Wandering through Taroko Gorge", "wandering_through_taroko_gorge", "Unknown",
     ["dl_0032"], "nickm.com"),
    ("we_0027", "Wąwóz Taroko", "wawoz_taroko", "Unknown",
     ["dl_0033"], "nickm.com"),
    ("we_0028", "Hey Gorgeous", "hey_gorgeous", "Unknown",
     ["dl_0035", "dl_0036"], "nickm.com / tinysubversions.com"),
    ("we_0029", "54 61 72 6F 6B 6F", "hex_taroko", "Roman Kalinovski",
     ["dl_0037"], "nickm.com"),
    ("we_0030", "Tolle Garbage", "tolle_garbage", "Unknown",
     ["dl_0038"], "nickm.com"),
    ("we_0031", "Take Gonzo", "take_gonzo", "Unknown",
     ["dl_0039"], "nickm.com"),
    ("we_0032", "Wąwóz Kraków", "wawoz_krakow", "Unknown",
     ["dl_0040"], "nickm.com"),
    ("we_0033", "Garaż w Tokio", "garaz_w_tokio", "Unknown",
     ["dl_0041"], "nickm.com"),
    ("we_0034", "Oko na Donbas", "oko_na_donbas", "Unknown",
     ["dl_0042"], "nickm.com"),
    ("we_0035", "Karaoke Mirage", "karaoke_mirage", "Unknown",
     ["dl_0043"], "nickm.com"),
    ("we_0036", "OK, Artgoer, Go!", "ok_artgoer_go", "Unknown",
     ["dl_0044"], "nickm.com"),
    ("we_0037", "At, or To Take Regret", "at_or_to_take_regret", "Unknown",
     ["dl_0046"], "nickm.com"),
    ("we_0038", "Dress for Overcast", "dress_for_overcast", "Unknown",
     ["dl_0048"], "nickm.com"),
    ("we_0039", "Kanjono Taroko", "kanjono_taroko", "Unknown",
     ["dl_0049", "dl_0050"], "nickm.com / inthescales.com"),
    ("we_0040", "Infinite Monkey Theorem", "infinite_monkey_theorem", "Unknown",
     ["dl_0051"], "nickm.com"),
    ("we_0041", "Li Po", "li_po", "Unknown",
     ["dl_0052"], "nickm.com"),
    ("we_0042", "Gorge of Anathema", "gorge_of_anathema", "Unknown",
     ["dl_0053", "dl_0054"], "nickm.com / multimodalmel.com"),
    ("we_0043", "Tranced Gaze", "tranced_gaze", "Unknown",
     ["dl_0055"], "nickm.com"),
    ("we_0044", "Melroko Porridge", "melroko_porridge", "Unknown",
     ["dl_0056"], "nickm.com"),
    ("we_0045", "Tough Guise", "tough_guise", "Unknown",
     ["dl_0057"], "nickm.com"),
    ("we_0046", "Within and Against / Against and Within", "within_and_against", "Unknown",
     ["dl_0058"], "nickm.com"),
    ("we_0047", "Taroko Gary Revisited", "taroko_gary_revisited", "Unknown",
     ["dl_0059", "dl_0060"], "nickm.com / iloveepoetry.org"),
    ("we_0048", "ELC3 Main Index", "elc3_index", "ELO Editorial",
     ["dl_0061"], "collection.eliterature.org"),
]


def build_dl_lookup(inventory, download_log, lexical, runtime):
    """Build lookup dicts keyed by dl_id."""
    inv = {r["id"]: r for r in inventory}
    dl_log = {r["id"]: r for r in download_log}
    lex_ids = set(r["id"] for r in lexical)
    rt_ids = set(r["id"] for r in runtime if r.get("status") == "ok")
    return inv, dl_log, lex_ids, rt_ids


def reconcile():
    utils.ensure_dirs("data/private")

    inventory = utils.read_csv("data/public/inventory.csv")
    download_log = utils.read_csv("data/public/download_log.csv")
    lexical = utils.read_csv("data/public/lexical_array_summary.csv")
    runtime = utils.read_csv("data/public/runtime_sample_log.csv")

    inv_lookup, dl_lookup, lex_ids, rt_ids = build_dl_lookup(
        inventory, download_log, lexical, runtime)

    entity_rows = []
    link_rows = []
    matrix_rows = []

    for ent in KNOWN_ENTITIES:
        eid, canonical_title, norm_key, author, dl_ids, domain_hint = ent

        # Determine statuses by checking dl_ids
        primary_dl = dl_ids[0] if dl_ids else None
        inv_row = inv_lookup.get(primary_dl, {})
        dl_row = dl_lookup.get(primary_dl, {})

        # Representation status
        any_downloaded = any(
            dl_lookup.get(d, {}).get("status_code", "") == "200" for d in dl_ids
        ) or any(
            inv_lookup.get(d) is not None for d in dl_ids
        )
        repr_status = "archived" if any_downloaded else "failed_or_absent"

        # Statement status
        statement_status = "unknown"
        if eid == "we_0008":  # Yoko Engorged
            statement_status = "author_statement_present"
        elif eid == "we_0002":  # ELC3 collection
            statement_status = "editorial_statement_present"
        elif eid == "we_0001":  # Taroko Gorge original
            statement_status = "context_page_pending"
        else:
            statement_status = "not_found"

        # Executable status
        exec_status = "present" if any_downloaded else "absent"

        # Source status (score 5 = full pattern)
        source_status = "unknown"
        scores = [int(inv_lookup.get(d, {}).get("probable_taroko_score", 0)) for d in dl_ids if inv_lookup.get(d)]
        if scores:
            max_score = max(scores)
            source_status = "extractable" if max_score >= 3 else "score_low"

        # Runtime status
        runtime_status = "present" if any(d in rt_ids for d in dl_ids) else "absent"

        # Screenshot status
        screenshot_status = "present" if any(d in rt_ids for d in dl_ids) else "absent"

        # Lexical status
        lexical_status = "arrays_extracted" if any(d in lex_ids for d in dl_ids) else "not_extracted"
        if eid == "we_0008":
            lexical_status = "contaminated_vendor_arrays"

        # Rights caution
        rights_caution = "low"
        if author not in ("Nick Montfort", "ELO Editorial", "Unknown"):
            rights_caution = "medium"

        # Primary URLs
        primary_exec_url = inv_lookup.get(primary_dl, {}).get("url", "") if primary_dl else ""
        primary_context_url = ""

        entity_rows.append({
            "work_entity_id": eid,
            "canonical_title": canonical_title,
            "normalized_title_key": norm_key,
            "known_author_or_creator_trace": author,
            "primary_context_page_url": primary_context_url,
            "primary_executable_url": primary_exec_url,
            "primary_source_url": primary_exec_url,
            "representation_status": repr_status,
            "statement_status": statement_status,
            "executable_status": exec_status,
            "source_status": source_status,
            "runtime_status": runtime_status,
            "screenshot_status": screenshot_status,
            "lexical_status": lexical_status,
            "rights_caution_status": rights_caution,
            "notes": f"dl_ids={','.join(dl_ids)}; domain={domain_hint}",
        })

        # Work entity links
        for dl_id in dl_ids:
            url = inv_lookup.get(dl_id, {}).get("url", "")
            path = inv_lookup.get(dl_id, {}).get("local_path", "")
            status_code = dl_lookup.get(dl_id, {}).get("status_code", "")
            confidence = "high" if status_code == "200" else "low"
            link_rows.append({
                "work_entity_id": eid,
                "link_type": "executable_or_mirror",
                "source_id_or_path": dl_id,
                "url_or_path": url,
                "status": status_code,
                "confidence": confidence,
                "notes": f"local={path}",
            })

        # Evidence matrix
        evidence_types = {
            "context_page": ("context_page_candidates.csv", 0),
            "executable_html": ("download_log", len([d for d in dl_ids if dl_lookup.get(d, {}).get("status_code") == "200"])),
            "runtime_screenshot": ("runtime_sample_log", len([d for d in dl_ids if d in rt_ids])),
            "lexical_arrays": ("lexical_array_summary", len([d for d in dl_ids if d in lex_ids])),
            "inventory_metadata": ("inventory", len([d for d in dl_ids if inv_lookup.get(d)])),
        }
        for ev_type, (source, count) in evidence_types.items():
            matrix_rows.append({
                "work_entity_id": eid,
                "evidence_type": ev_type,
                "evidence_present": "yes" if count > 0 else "no",
                "count": count,
                "notes": f"source={source}",
            })

    fields_ent = [
        "work_entity_id", "canonical_title", "normalized_title_key",
        "known_author_or_creator_trace", "primary_context_page_url",
        "primary_executable_url", "primary_source_url",
        "representation_status", "statement_status", "executable_status",
        "source_status", "runtime_status", "screenshot_status",
        "lexical_status", "rights_caution_status", "notes",
    ]
    fields_links = [
        "work_entity_id", "link_type", "source_id_or_path",
        "url_or_path", "status", "confidence", "notes",
    ]
    fields_matrix = [
        "work_entity_id", "evidence_type", "evidence_present", "count", "notes",
    ]

    utils.write_csv(OUT_ENTITIES, entity_rows, fieldnames=fields_ent)
    utils.write_csv(OUT_LINKS, link_rows, fieldnames=fields_links)
    utils.write_csv(OUT_MATRIX, matrix_rows, fieldnames=fields_matrix)

    print(f"Work entities: {len(entity_rows)} -> {OUT_ENTITIES}")
    print(f"Entity links: {len(link_rows)} -> {OUT_LINKS}")
    print(f"Evidence matrix: {len(matrix_rows)} -> {OUT_MATRIX}")


if __name__ == "__main__":
    reconcile()
