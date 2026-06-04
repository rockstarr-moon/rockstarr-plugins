---
name: baseline-audit
description: "This skill should be used at the start of a client engagement, or whenever the user wants a snapshot of what content already exists — e.g. \"where do we stand today\", \"run the baseline audit\", \"what content do we already have\", \"inventory everything we've published\", or \"build our master list\". The team lead's starting-point snapshot: it dispatches specialist discovery across channels (blogs, LinkedIn newsletter editions, recent social posts), backfills the canonical publish log with what's already public, then builds the comprehensive master list (06_reports/master-list.xlsx, long-form + social) and a duplicate-awareness summary. Read-only discovery that records existing public content; it never drafts, posts, sends, or publishes anything new."
---

# baseline-audit

The first thing the team should do for a new client: take an honest
snapshot of **what already exists**. What blogs are on the site, what
editions are on the LinkedIn newsletter, what's been posted socially in
the last few months. This becomes the **master list** — the starting
point that informs the content calendar, topic ideation, and the
schedules, and keeps the team from re-creating content the client
already has.

> **Read-only discovery, canonical-store backfill.** This skill
> dispatches specialists to *read* the client's public channels and
> *record* what's already public into the canonical publish log. It
> **never drafts, posts, sends, schedules, or publishes** anything new.
> Recording already-public history is internal/reversible (AUTO on the
> autonomy line). The lead coordinates; the specialists do the crawling.

## When to run

- **Early** — one of the first things after a client is scaffolded and
  the stack is captured. `team-report` flags when no baseline exists;
  `route-request` maps "what do we already have?" here.
- On demand later: "refresh the baseline", "rebuild the master list".

## Modes

- **Full (default):** run discovery (steps 1-3) then build the workbook
  (steps 4-5). Use for a first baseline, or when you want to re-discover
  what's live.
- **Refresh-only:** when the user just wants to **rebuild the master
  list from the current publish log** without re-crawling the channels
  (e.g. right after `master-list-blog-audit` logged some gaps), **skip
  steps 1-3 and run steps 4-5 only**. This is the lightweight path the
  deprecated `rockstarr-content:master-list-create` now redirects to.

## Preconditions

- A scaffolded workspace (`/rockstarr-ai/`) with `00_intake/stack.md`
  (for the website URL, the LinkedIn newsletter URL, and
  `social_channels`).
- The specialist plugins for the channels in scope installed
  (`rockstarr-content` for blogs + LinkedIn newsletter,
  `rockstarr-social` for social). Skip a channel cleanly, noting it, if
  its plugin or its config isn't present.
- Read `references/role-registry.md` (Content & SEO + Brand & Social
  output paths) and `00_intake/marketing-plan.md` if present.

## Procedure

Dispatch each discovery specialist in turn (each is read-only and
backfills the **canonical publish log** via `rockstarr-infra:publish-log`
after the operator confirms its untracked list — do not bypass that
confirmation):

1. **Blogs** — `rockstarr-content:master-list-blog-audit`. Crawls the
   live sitemap, finds live blogs not in the log, backfills them.
2. **LinkedIn newsletter** — `rockstarr-content:inventory-linkedin-newsletter`.
   Lists already-published editions, backfills the untracked ones
   (`format: linkedin-newsletter`).
3. **Social (last 3 months)** — `rockstarr-social:inventory-social`.
   Pass the **3-month lookback window**. Lists recent posts per enabled
   channel, backfills the untracked ones with a one-line topic each.

Then assemble the comprehensive master list:

4. **Read the now-backfilled publish log** (`05_published/_publish.log`
   + per-publish records). Group into two row sets:
   - **long_form** — Blogs, Case studies, LinkedIn-newsletter editions,
     email newsletters (one row per piece; reuse the canonical column
     shape: Content type / Posted on LinkedIn newsletter / Posted in
     email newsletter / URL / Title / Published date / Slug).
   - **social** — recent social posts (Channel / Type / Published date /
     Permalink / Topic).
5. **Write the workbook** to `06_reports/master-list.xlsx` via
   `scripts/write_master_list_xlsx.py --rows rows.json --out
   06_reports/master-list.xlsx`. This is the **comprehensive,
   orchestrator-owned master list** (long-form + social). It is a
   regenerable export of the publish log — re-run any time.

## Output

- `06_reports/master-list.xlsx` — the comprehensive master list.
- A short **starting-point summary** in chat (and optionally appended to
  the latest `06_reports/team/` report): counts per channel, the date
  range covered, and a **duplicate-awareness list** — the themes/topics
  already covered, so ideation and the calendar avoid re-creating them.
- Note what was skipped (a channel with no plugin/config, or social
  beyond the 3-month window) — never imply full coverage you didn't do.

## What NOT to do

- Do NOT draft, post, send, schedule, or publish anything new — this is
  inventory only.
- Do NOT bypass each specialist's operator-confirmation before backfill.
- Do NOT hand-write workbook rows or treat the `.xlsx` as canonical —
  the publish log is the source of truth; the workbook is its export.
- Do NOT fabricate dates/topics — record what the pages show; flag gaps.

## Related

- `rockstarr-content:master-list-blog-audit` /
  `inventory-linkedin-newsletter`, `rockstarr-social:inventory-social` —
  the discovery specialists this dispatches.
- `rockstarr-infra:publish-log` — the canonical store everything
  backfills into.
- `rockstarr-orchestrator:team-report` — flags when no baseline exists;
  `set-marketing-goals` — the goals this inventory informs.
- Note: `rockstarr-content:master-list-create` is **deprecated** — it
  redirects here. This baseline's comprehensive `master-list.xlsx`
  (long-form + social) is the one master list.
