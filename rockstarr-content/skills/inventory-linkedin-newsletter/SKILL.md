---
name: inventory-linkedin-newsletter
description: "This skill should be used when the user wants to inventory the LinkedIn newsletter editions that already exist on a client's account — e.g. \"inventory our LinkedIn newsletter\", \"what newsletter editions have we published\", \"catalog past LinkedIn newsletter articles\", or as the LinkedIn-newsletter step of the orchestrator's baseline audit. It opens the client's LinkedIn newsletter via Chrome MCP, lists the already-published editions (title, URL, publish date), diffs them against what's tracked in 05_published/_publish.log, reports the untracked ones, and — only after the operator confirms — backfills them through rockstarr-infra:publish-log (channel linkedin). Read-only against LinkedIn; it never posts, edits, or publishes anything."
---

# inventory-linkedin-newsletter

Catalog the LinkedIn newsletter editions a client has **already
published**, so they land in the canonical publish log (and from there,
the master list) — part of knowing "what already exists" before the
team produces anything new.

> **Read-only + canonical-store.** This skill reads LinkedIn and records
> already-public editions; it **never** posts, edits, schedules, or
> publishes. Like `master-list-blog-audit`, gaps are fixed at the source
> (`rockstarr-infra:publish-log`), not by hand-editing any workbook.

## When to run

- On demand: "inventory our LinkedIn newsletter", "what editions have we
  published".
- As the LinkedIn-newsletter step of `rockstarr-orchestrator:baseline-audit`.

## Preconditions

- `/rockstarr-ai/05_published/` exists (the publish log lives here).
- A LinkedIn session reachable via Chrome MCP, and the client's personal
  LinkedIn newsletter URL (from `stack.md` if captured, else ask).
- Follow `rockstarr-infra` `_shared/references/chrome-mcp-clicking.md`
  for real-CDP interaction (read-only here — navigation + reading).

## Procedure

1. **Anchor**, then open the newsletter's "all editions" / archive view
   on LinkedIn via Chrome MCP (navigate + read; no clicks that mutate).
2. **List each published edition**: title, public URL, and publish date
   (as shown on the page). Scroll/paginate until the list is exhausted
   or you reach editions older than the client's history needs.
3. **Diff against the log**: read `05_published/_publish.log` +
   per-publish records; an edition is "tracked" if a `linkedin` record
   carries its URL (`external_url`) or a matching newsletter title.
   Report tracked vs untracked counts + the untracked list.
4. **Confirm, then backfill.** Ask the operator before logging anything.
   For each confirmed untracked edition, call `rockstarr-infra:publish-log`
   with channel `linkedin`, the edition's public URL as `external_url`,
   its publish date, and a `format: linkedin-newsletter` marker in the
   record so downstream (the master list) can tell newsletter editions
   from ordinary LinkedIn posts. Then note that the master list will pick
   them up on its next build.

## What NOT to do

- Do NOT post, edit, schedule, or publish on LinkedIn — read-only.
- Do NOT write rows into any workbook; backfill through `publish-log`.
- Do NOT log anything before the operator confirms the untracked list.
- Do NOT invent dates — if a publish date isn't legible on the page,
  record the edition with an empty date and flag it for the operator.

## Related

- `rockstarr-orchestrator:baseline-audit` — the cross-channel starting
  snapshot that dispatches this skill.
- `rockstarr-content:master-list-blog-audit` — the sibling blog-side
  discovery; same discover → confirm → publish-log → regenerate pattern.
- `rockstarr-content:publish-linkedin-newsletter` — the go-live skill
  that creates new editions (this one only catalogs existing ones).
- `rockstarr-infra:publish-log` — the canonical store gaps are logged to.
