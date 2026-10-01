"""Full private archive pipeline runner."""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.utils_module as utils

DIRS = [
    "seeds", "scripts", "data/public", "data/private",
    "archive/raw_html", "archive/screenshots",
    "archive/output_samples", "archive/extracted_full",
    "notes", "private_archive",
]


def run_step(label, args_list, log_file="notes/last_run.log"):
    print(f"\n=== {label} ===")
    with open(log_file, "a") as log:
        log.write(f"\n=== {label} ===\n")
        result = subprocess.run(
            args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        log.write(result.stdout)
        last = result.stdout.strip().splitlines()[-5:] if result.stdout.strip() else []
        for line in last:
            print(line)
        if result.returncode != 0:
            print(f"[ERROR] Step failed with code {result.returncode}")
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--seconds", type=int, default=20)
    args = parser.parse_args()

    for d in DIRS:
        os.makedirs(d, exist_ok=True)

    open("notes/last_run.log", "w").close()

    py = sys.executable

    dl_args = [py, "scripts/02_download_pages.py"]
    if args.limit:
        dl_args += ["--limit", str(args.limit)]
    if args.force:
        dl_args += ["--force"]

    rt_args = [py, "scripts/05_runtime_sample.py", "--seconds", str(args.seconds)]
    if args.limit:
        rt_args += ["--limit", str(args.limit)]

    steps = [
        ("01 collect_links", [py, "scripts/01_collect_links.py"]),
        ("02 download_pages", dl_args),
        ("03 extract_metadata", [py, "scripts/03_extract_metadata.py"]),
        ("04 extract_lexical_arrays", [py, "scripts/04_extract_lexical_arrays.py"]),
        ("05 runtime_sample", rt_args),
        ("07 build_corpus_catalog", [py, "scripts/07_build_corpus_catalog.py"]),
        ("08 build_manifest", [py, "scripts/08_build_manifest.py"]),
        ("09 build_zip", [py, "scripts/09_build_zip.py"]),
        ("validate", [py, "scripts/06_validate_private.py"]),
    ]

    for label, cmd in steps:
        ok = run_step(label, cmd)
        if not ok:
            print(f"\nPipeline stopped at: {label}")
            print("See notes/last_run.log for details")
            sys.exit(1)

    print("\n=== Full archive pipeline complete ===")


if __name__ == "__main__":
    main()
