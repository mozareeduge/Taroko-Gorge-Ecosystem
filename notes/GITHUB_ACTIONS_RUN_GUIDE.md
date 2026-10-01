# How to Run the Pipeline on GitHub Actions

This guide is for someone who has never used GitHub Actions before.

---

## What This Does

Running this workflow fetches the Taroko Gorge seed pages, extracts metadata, and packages the safe public outputs as a downloadable file. Raw HTML and source code are kept on the runner only and are never uploaded.

---

## Step-by-Step

### 1. Go to the GitHub Repository

Open the repository page in your browser.

### 2. Open the Actions Tab

Click the **Actions** tab near the top of the page (next to Code, Issues, Pull requests).

### 3. Select the Workflow

On the left side you will see a list of workflows. Click **Taroko Public Metadata Pipeline**.

### 4. Click "Run workflow"

You will see a button on the right side that says **Run workflow**. Click it.

### 5. Choose the Branch

A small dropdown will appear. Select the branch you want to run (for example `claude/taroko-gorge-archive-yl062k` or `main`). Then click the green **Run workflow** button.

### 6. Wait for Completion

The workflow will appear in the list with a yellow spinning circle. Wait until it turns green (success) or red (failure). This usually takes 2–5 minutes.

### 7. Download the Artifact

Once the workflow is green:

1. Click on the workflow run (the row in the list).
2. Scroll to the bottom of the page to the **Artifacts** section.
3. Click **taroko-public-metadata** to download a zip file.
4. Unzip it. You will find:
   - `data/public/*.csv` — links, download log, inventory, lexical summaries
   - `notes/RUN_REPORT.md` — validation results
   - `notes/HANDOFF.md` — current pipeline state
   - `notes/METHOD.md` — methodology
   - `README.md`

---

## Public Repo Safety Reminder

The artifact contains **only metadata and logs** — no raw HTML, no screenshots, no full word arrays, no source code content. Do not manually add those files to the artifact or commit them to the repository.

---

## If the Workflow Fails

1. Click on the red failed run.
2. Click on the failed step (shown in red).
3. Scroll to the bottom of the log output.
4. Copy the last 40 lines of that output.
5. Paste them into a message to the person helping you debug.

Common causes of failure:
- A seed URL is unreachable (expected; pipeline logs the error and continues).
- A Python import error (check `scripts/` for typos).
- Missing `requirements.txt` package.
