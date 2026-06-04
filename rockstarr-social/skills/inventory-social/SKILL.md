---
name: inventory-social
description: "This skill should be used when the user wants to inventory the social posts a client has already published recently — e.g. \"inventory our social posts\", \"what have we posted on LinkedIn lately\", \"catalog the last 3 months of social\", or as the social step of the orchestrator's baseline audit. It opens each enabled social channel via Chrome MCP, lists posts published in a lookback window (default last 3 months) with date, permalink, and a short topic summary, diffs them against 05_published/_publish.log, reports the untracked ones, and — only after the operator confirms — backfills them through rockstarr-infra:publish-log. Read-only against the platforms; it never posts, comments, edits, or schedules anything."
---

# inventory-social

Catalog the social posts a client has **already published** in a recent
window (default: last 3 months), so they land in the canonical publish
log (and the master list) — the social half of knowing "what already
exists" before the team produces anything new. It protects against
re-posting topics the client just covered.

> **Read-only + canonical-store.** This skill reads each platform and
> records already-public posts; it **never** posts, comments, edits,
> schedules, or deletes. Gaps are fixed at the source
> (`rockstarr-infra:publish-log`), never by hand-editing a workbook.

## When to run

- On demand: "inventory our social posts", "catalog the last 3 months".
- As the social step of `rockstarr-orchestrator:baseline-audit`.

## Preconditions

- `/rockstarr-ai/05_published/` exists.
- The enabled channels from `stack.md` (`social_channels`) and a session
  for each reachable via Chrome MCP. Inventory only enabled channels;
  default to LinkedIn when that's the only one on.
- Follow `rockstarr-infra` `_shared/references/chrome-mcp-clicking.md`
  (read-only here — navigation + reading the activity/posts feed).

## Procedure

1. **Anchor**, then for each enabled channel open the account's
   posts/activity view via Chrome MCP (navigate + read).
2. **Lookback window** — default the **last 3 months** (the
   orchestrator's baseline passes the window; honor it if given). Scroll
   until posts predate the window.
3. **List each post**: publish date, permalink, post type
   (post / poll / article / repost), and a one-line topic summary (for
   duplicate-awareness — the point is to see what's been said).
4. **Diff against the log**: an item is "tracked" if a record for that
   channel carries its permalink (`external_url`). Report tracked vs
   untracked counts + the untracked list, grouped by channel.
5. **Confirm, then backfill.** Ask the operator before logging. For each
   confirmed untracked post, call `rockstarr-infra:publish-log` with the
   channel (e.g. `linkedin`), the permalink as `external_url`, the
   publish date, the post type in a `format` marker (e.g.
   `format: linkedin-post` / `linkedin-poll`), and the one-line topic in
   the title/summary. Note the master list will pick them up next build.

## What NOT to do

- Do NOT post, comment, react, edit, schedule, or delete — read-only.
- Do NOT inventory channels that aren't enabled in `social_channels`.
- Do NOT write rows into any workbook; backfill through `publish-log`.
- Do NOT log anything before the operator confirms.
- Do NOT exceed a reasonable scroll — if the feed is enormous, cap at
  the window and say how many you covered + that older posts were not
  inventoried.

## Related

- `rockstarr-orchestrator:baseline-audit` — the cross-channel starting
  snapshot that dispatches this skill (and passes the lookback window).
- `rockstarr-content:master-list-blog-audit` /
  `inventory-linkedin-newsletter` — the long-form siblings; same
  discover → confirm → publish-log pattern.
- `rockstarr-infra:publish-log` — the canonical store gaps are logged to.
