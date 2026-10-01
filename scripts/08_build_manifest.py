"""Build SHA256 manifest for all archived files."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

MANIFEST_COLS = [
    "path", "category", "source_url", "sha256", "bytes",
    "created_at", "public_or_private", "note",
]

ARCHIVE_DIRS = [
    ("archive/raw_html", "raw_html", "private"),
    ("archive/screenshots", "screenshot", "private"),
    ("archive/output_samples", "output_sample", "private"),
    ("archive/extracted_full", "extracted_full", "private"),
    ("data/public", "public_metadata", "public"),
    ("data/private", "private_metadata", "private"),
    ("notes", "notes", "public"),
]


def build_manifest():
    utils.ensure_dirs("data/private")
    dl_log = utils.read_csv("data/public/download_log.csv")
    path_to_url = {row.get("local_path", ""): row.get("url", "") for row in dl_log}

    rows = []

    for directory, category, visibility in ARCHIVE_DIRS:
        if not os.path.isdir(directory):
            continue
        for fname in sorted(os.listdir(directory)):
            if fname == ".gitkeep":
                continue
            fpath = os.path.join(directory, fname)
            if not os.path.isfile(fpath):
                continue
            sha = utils.sha256_file(fpath)
            size = os.path.getsize(fpath)
            rows.append({
                "path": fpath,
                "category": category,
                "source_url": path_to_url.get(fpath, ""),
                "sha256": sha,
                "bytes": size,
                "created_at": utils.now_iso(),
                "public_or_private": visibility,
                "note": "",
            })

    for fname in ["README.md", "CLAUDE.md", "requirements.txt"]:
        if os.path.isfile(fname):
            sha = utils.sha256_file(fname)
            size = os.path.getsize(fname)
            rows.append({
                "path": fname, "category": "source",
                "source_url": "", "sha256": sha, "bytes": size,
                "created_at": utils.now_iso(), "public_or_private": "public", "note": "",
            })

    utils.write_csv("data/private/archive_manifest.csv", rows, fieldnames=MANIFEST_COLS)
    print(f"Archive manifest: data/private/archive_manifest.csv ({len(rows)} files)")


if __name__ == "__main__":
    build_manifest()
