"""Build zip package of the full private archive."""
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

OUT_ZIP = "private_archive/taroko_full_archive.zip"

INCLUDE_DIRS = [
    "data/public",
    "data/private",
    "archive/raw_html",
    "archive/extracted_full",
    "archive/output_samples",
    "archive/screenshots",
]

INCLUDE_FILES = [
    "notes/FULL_ARCHIVE_README.md",
    "notes/METHOD.md",
    "notes/RUN_REPORT.md",
    "README.md",
]


def build_zip():
    utils.ensure_dirs("private_archive")

    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        count = 0
        for directory in INCLUDE_DIRS:
            if not os.path.isdir(directory):
                continue
            for fname in sorted(os.listdir(directory)):
                if fname == ".gitkeep":
                    continue
                fpath = os.path.join(directory, fname)
                if os.path.isfile(fpath):
                    zf.write(fpath)
                    count += 1

        for fpath in INCLUDE_FILES:
            if os.path.isfile(fpath):
                zf.write(fpath)
                count += 1

    size = os.path.getsize(OUT_ZIP)
    print(f"Archive zip: {OUT_ZIP} ({count} files, {size} bytes)")


if __name__ == "__main__":
    build_zip()
