> **Historical (June 2026)** (2026-10-02): this handoff predates the public release. The branch `claude/taroko-gorge-archive-yl062k`, the workflow `.github/workflows/taroko-public-metadata.yml` and the push instructions below no longer apply; the workflows were removed before release.

# HANDOFF

## Current State

Pipeline structure complete. GitHub Actions workflow added. Ready to run outside
the Claude Code environment.

## Completed

- [x] All directories, .gitkeep files, .gitignore
- [x] requirements.txt (requests, beautifulsoup4)
- [x] seeds/taroko_seed_urls.csv (4 seeds)
- [x] scripts/utils_module.py
- [x] scripts/01_collect_links.py through 06_validate_corpus.py
- [x] scripts/run_pipeline.py
- [x] README.md (public-repo safety warning included)
- [x] CLAUDE.md
- [x] notes/METHOD.md
- [x] notes/RUN_REPORT.md
- [x] notes/GITHUB_ACTIONS_RUN_GUIDE.md
- [x] .github/workflows/taroko-public-metadata.yml
- [x] Pushed to branch: claude/taroko-gorge-archive-yl062k (historical)

## Hard Blocker (local execution only)

Network egress blocked for all seed domains in Claude Code remote environment.
The GitHub Actions workflow runs on ubuntu-latest with standard internet access
and will not have this limitation.

## Do Not Touch

- .gitignore
- .gitkeep files
- archive/ contents (local-only, not tracked)
- data/private/ contents (local-only, not tracked)

## Next Exact Action (for user)

1. Commit and push the new workflow file and guide:
   ```
   git add .github/workflows/taroko-public-metadata.yml notes/GITHUB_ACTIONS_RUN_GUIDE.md notes/RUN_REPORT.md notes/HANDOFF.md
   git commit -m "Add GitHub Actions workflow for public metadata pipeline"
   git push origin claude/taroko-gorge-archive-yl062k
   ```
2. Go to GitHub → Actions → "Taroko Public Metadata Pipeline" → Run workflow.
3. Download artifact taroko-public-metadata after completion.
4. See notes/GITHUB_ACTIONS_RUN_GUIDE.md for step-by-step UI instructions.

## Verification

After running the workflow, the artifact should contain:
- data/public/taroko_links.csv with >4 rows (seed + extracted links)
- data/public/download_log.csv with status_code 200 rows
- data/public/inventory.csv with probable_taroko_score populated
- notes/RUN_REPORT.md showing PASS or WARN (not FAIL)
- NO archive/ files, NO raw HTML, NO screenshots
