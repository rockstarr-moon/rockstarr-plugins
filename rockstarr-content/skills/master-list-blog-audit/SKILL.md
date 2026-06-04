---
name: master-list-blog-audit
description: "This skill should be used when the user asks to \"audit the master list\", \"check the master list\", \"make sure all live blogs are tracked\", \"audit blogs against the site\", or \"reconcile the master list with the website\". Crawls the client's live blog sitemap (Googlebot user agent), diffs the live blog URLs against what's tracked in 05_published/_publish.log and the master-list workbook, and reports any live blogs that are NOT tracked. It does not edit the workbook directly: confirmed gaps are logged through rockstarr-infra:publish-log (the canonical store), after which master-list-create regenerates the workbook. Read-only against the live site; reuses the seo-site-audit Googlebot fetch approach. Reports counts plus the untracked-URL list and waits for the operator before logging anything."
---

# master-list-blog-audit

Make sure every blog post live on the client's website is tracked in
the workspace. This is the blog-side discovery for the master list: it
checks that the canonical publish log reflects what's actually live on
the site, and backfills any gaps. It runs standalone or as the blog step
of `rockstarr-orchestrator:baseline-audit` (which builds the master list
from the log afterward).

> **The publish log is canonical — gaps are fixed there, not in the
> workbook.** This skill never writes rows into any `.xlsx`. It surfaces
> live blogs that aren't tracked; once the operator confirms, each gets
> logged via `rockstarr-infra:publish-log`, then the master list
> regenerates from the now-complete log (via
> `rockstarr-orchestrator:baseline-audit`).

## When to run

- Periodically (e.g. monthly), or on request: "audit the master list",
  "make sure all live blogs are tracked", "reconcile the master list
  with the site".
- After a stretch where the client may have published blogs outside the
  Rockstarr drafting workflow (those wouldn't be in the publish log).

## Preconditions

Tier 1 cheap checks first:

- `/rockstarr-ai/00_intake/stack.md` exists and `website_base_url` is
  set — that's the site to crawl. If missing, point the user at
  `rockstarr-infra:capture-stack`.
- `/rockstarr-ai/05_published/` exists (the publish log to diff against).
- Network access for the sitemap fetch.

## Inputs

1. **`stack.md`** — `website_base_url`, the crawl target.
2. **`05_published/_publish.log`** + the per-publish `blog` records —
   the tracked blog URLs (their `external_url` values).
3. **`06_reports/master-list.xlsx`** if present (the orchestrator's
   comprehensive master list) — the URL column, as a secondary
   cross-check. The publish log is authoritative; the workbook is just
   the human view of it.

## Workflow

### Step 1 — Anchor, then crawl the sitemap

Fire the anchor message ("Checking your live blogs against what's
tracked…"), then enumerate live blog URLs with the bundled fetch
(same Googlebot-UA approach as `seo-site-audit`):

```bash
python3 scripts/fetch_sitemap.py https://CLIENT-DOMAIN/ --json
```

It walks `/sitemap.xml` (or `/sitemap_index.xml`), follows nested
`post-sitemap*.xml` children, and returns the blog-post URLs —
skipping page / project / testimonial / category sitemaps (those are
pages, case studies, and landing pages, not blog posts).

### Step 2 — Gather the tracked blog URLs

From `_publish.log` and the `blog` publish records, collect every
`external_url` that points at the client domain. Optionally also read
the URL of final blog column from the workbook as a cross-check.

### Step 3 — Diff, normalized

Normalize both lists before comparing — lowercase, strip protocol,
strip leading `www.`, strip trailing slash (the bundled script's
`normalize` does exactly this) — so
`https://www.example.com/post/` and `https://example.com/post` match.

The set of interest is **live-but-not-tracked**: blog URLs on the live
site that have no matching tracked URL. Per the original process,
ignore the reverse case (tracked rows with no live match) — stale rows
are out of scope here.

### Step 4 — Report and wait

Report in chat:

- Live blog count.
- Tracked blog count.
- The untracked list (full URLs) — the blogs live on the site but
  missing from the publish log.

If zero untracked, report "reconciled — every live blog is tracked"
and stop.

If there are untracked blogs, ask the operator whether to log them.
**Do not log or edit anything without explicit confirmation.**

### Step 5 — Resolve through the canonical store

On confirmation, for each untracked blog, call
`rockstarr-infra:publish-log` (channel `blog`, the live URL as
`external_url`, the publish date if determinable from the page). Then
run `rockstarr-orchestrator:baseline-audit` (refresh mode) to regenerate
the master list from the updated log. The workbook is never edited
directly.

## What NOT to do

- Do NOT write rows into the `.xlsx`. Gaps are resolved through
  `publish-log`, then the workbook is regenerated.
- Do NOT auto-log untracked blogs. Surface them and wait for the
  operator — a URL on the sitemap may be intentionally untracked
  (a landing page mis-typed as a post, a draft preview, etc.).
- Do NOT remove or flag tracked rows that aren't on the live sitemap.
  Stale-row cleanup is out of scope.
- Do NOT use `curl` for the crawl if the environment blocks external
  shell HTTP — the bundled script uses Python urllib with a Googlebot
  UA; if it returns nothing, fall back to a Chrome-MCP sitemap read
  rather than assuming the site has no blogs.

## Related

- `rockstarr-orchestrator:baseline-audit` — builds/refreshes the
  comprehensive master list from the publish log; run it (refresh mode)
  after gaps are logged. (`rockstarr-content:master-list-create` is
  deprecated — it now redirects here.)
- `rockstarr-infra:publish-log` — the canonical store gaps are
  resolved through.
- `rockstarr-content:seo-site-audit` — also crawls the client sitemap
  (for SEO health rather than tracking completeness); shares the
  Googlebot-UA fetch approach.
- `scripts/fetch_sitemap.py` — the bundled blog-URL enumerator.
