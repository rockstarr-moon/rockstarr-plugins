---
name: master-list-create
description: "This skill should be used when the user asks to \"create the master list\", \"build the content master list\", \"generate the master list of content\", \"refresh the master list\", or \"make the master sheet\". Generates a local Excel workbook at 06_reports/master-list-of-content.xlsx from the canonical 05_published/_publish.log, one row per long-form piece (Blog or Case study) with the four canonical columns (Content type, Posted on LinkedIn newsletter, Posted in email newsletter, URL of final blog) plus Title, Published date, and Slug. The publish log stays the source of truth; this workbook is a regenerable export, not a hand-maintained sheet. Re-run any time to refresh. Pairs with master-list-blog-audit, which reconciles it against the client's live site."
---

# master-list-create

Generate (or refresh) the client's **Master List of Content** as a
local Excel workbook. This is the workspace-native, file-based version
of the old Google-Sheets master list: a single tracker of long-form
content (blogs and case studies) and where each piece was reposted.

> **The publish log is canonical; the workbook is an export.** This
> skill does NOT replace `05_published/_publish.log` — it reads it.
> The workbook is a human-friendly Excel snapshot generated from the
> log. You never hand-maintain it; if something is wrong or missing,
> fix it at the source (log the publish via `rockstarr-infra:publish-log`)
> and re-run this skill.

## When to run

- After a batch of content publishes, to refresh the tracker.
- On request: "create / build / refresh the master list of content".
- After `master-list-blog-audit` surfaces untracked live blogs and
  they've been logged — re-run here to fold them in.

## Preconditions

Tier 1 cheap checks first; refuse fast if any fail:

- `/rockstarr-ai/05_published/` exists (the publish log lives here).
  If there's no publish log yet, there's nothing to tabulate — say so
  and stop (the workbook would be empty).
- `python3` with `openpyxl` is available in the environment. The
  bundled writer script fails with a clear `pip install openpyxl`
  hint if it's missing.

This is workspace-local and per-client. There is no Google Drive, no
sharing step, and no ClickUp — the workbook is a file in the client's
own `/rockstarr-ai/` folder.

## Inputs

1. **`05_published/_publish.log`** — the append-only log. Each line is
   `[ISO]  [channel]  [published_by]  [published filename]  [external_url]`.
2. **`05_published/[channel]/[date]_[slug].md`** — the per-publish
   records. Front-matter carries `channel`, `published_at`,
   `external_url`, `source_approved_file`. The filename carries the
   date and slug.
3. **`04_approved/content/[slug].md`** — the approved piece's
   front-matter gives the precise lane (`channel: researched-blog` vs
   `channel: case-study`) for the Content type column, plus `title`.
4. **`00_intake/client.toml`** — client name (informational only; the
   workbook filename is fixed, see Output).
5. The newsletter publish records' `monthly_pieces_linked` (when
   present) — used to fill the email-newsletter column (see below).

## Workflow

### Step 1 — Anchor, then read the log

Fire the anchor message ("Building your master list of content…"),
then read `_publish.log` and the per-publish records.

### Step 2 — Build one row per long-form piece (join by slug)

Group the publish records by `slug` (from the filename / front-matter).
Each long-form piece (Blog or Case study) becomes one row. Fill each
column:

- **Content type** — `Blog` or `Case study`. Read the matching
  `04_approved/content/[slug].md` front-matter: `channel: case-study`
  maps to `Case study`; researched-blog (or a `blog` publish with no
  case-study lane) maps to `Blog`. Thought-leadership pieces are not
  long-form blog content for this tracker; include them only if they
  were published to the client's blog (channel `blog`).
- **URL of final blog** — the `external_url` from the piece's `blog`
  publish record.
- **Posted on LinkedIn newsletter** — the `published_at` date of the
  piece's `linkedin-newsletter` publish record, if one exists. (That
  channel string is what `publish-linkedin-newsletter` logs.) Blank
  if the piece was never republished there.
- **Posted in email newsletter** — the `published_at` date of the
  `email` / `newsletter` publish whose `monthly_pieces_linked`
  includes this piece's slug. Blank if no newsletter featured it.
- **Title** — from the approved piece's `title`.
- **Published date** — the piece's blog `published_at` (date only).
- **Slug** — the join key.

Sort rows by Published date (oldest first) for stable output.

### Step 3 — Write the workbook

Emit the rows as a JSON array to a temp file (one object per row with
keys `content_type`, `linkedin_newsletter`, `email_newsletter`,
`url`, `title`, `published_date`, `slug`), then run the bundled
writer:

```bash
python3 scripts/write_master_list_xlsx.py \
  --rows /tmp/master-list-rows.json \
  --out /rockstarr-ai/06_reports/master-list-of-content.xlsx
```

The script writes the `Content` tab with the canonical-four-first
column order, a bold + frozen header row, and a Blog/Case study
dropdown on the Content type column. Re-running overwrites the file
with the current state of the log — that's intended; the workbook is
a snapshot, not a separate source of truth.

### Step 4 — Confirm

Reply with: the row count, the path
(`06_reports/master-list-of-content.xlsx`), and a one-line note that
it reflects the publish log as of now. Do NOT share, move, or change
permissions on the file.

## Output

- `/rockstarr-ai/06_reports/master-list-of-content.xlsx` — `Content`
  tab, the four canonical columns plus Title / Published date / Slug,
  one row per long-form piece, header bold + frozen, Blog/Case study
  dropdown on column A.

## What NOT to do

- Do NOT hand-edit rows into the workbook. It's generated; edits get
  overwritten on the next run. Fix the source (`publish-log`) instead.
- Do NOT invent rows for content not in the publish log. If a live
  blog isn't tracked, that's `master-list-blog-audit`'s job to surface.
- Do NOT create the workbook in Google Drive or share it — this is a
  local, per-client file.
- Do NOT add the leading-underscore / client-name filename convention
  from the old Drive sheet; the workspace is already per-client.

## Related

- `rockstarr-infra:publish-log` — the canonical source this reads from.
- `rockstarr-content:master-list-blog-audit` — reconciles this against
  the client's live site and routes gaps back through publish-log.
- `scripts/write_master_list_xlsx.py` — the bundled openpyxl writer.
