---
name: master-list-create
description: "DEPRECATED — the master list moved to rockstarr-orchestrator. This skill still triggers on \"create the master list\", \"build the content master list\", \"generate the master list of content\", \"refresh the master list\", or \"make the master sheet\", but it no longer builds a workbook here. The master list is now a comprehensive, orchestrator-owned artifact (long-form AND social) at 06_reports/master-list.xlsx, built by rockstarr-orchestrator:baseline-audit. This skill redirects there: it points the user at baseline-audit (full inventory) or its refresh mode (rebuild the workbook from the publish log, no re-crawl). It builds nothing and changes nothing itself."
---

# master-list-create (deprecated → see rockstarr-orchestrator)

> **This skill is deprecated.** The master list is no longer a
> content-plugin, long-form-only export. It is now a **comprehensive,
> cross-channel master list** (long-form **and** social) **owned by the
> team lead**, because the inventory spans functions. It lives at
> `06_reports/master-list.xlsx` and is built by
> **`rockstarr-orchestrator:baseline-audit`**.

## What to do instead

When the user asks to create / build / refresh the master list:

1. **If `rockstarr-orchestrator` is installed** (it's the foundational
   team lead — most clients have it), point them at it:
   - **Full inventory / first time:** run
     `rockstarr-orchestrator:baseline-audit` — it discovers what already
     exists across channels (blogs, LinkedIn newsletter, recent social),
     backfills the canonical publish log, and builds the comprehensive
     `06_reports/master-list.xlsx`.
   - **Just refresh the workbook** from the current publish log (no
     re-crawl): run `baseline-audit` in its **refresh mode** (rebuild
     from the log only).
   Briefly say why (the master list is now cross-channel and lives with
   the orchestrator), then hand off. Do not build a competing workbook.

2. **If `rockstarr-orchestrator` is NOT installed:** tell the user the
   master list now lives in the orchestrator plugin and recommend their
   Rockstarr lead add it. Don't silently rebuild the old long-form-only
   sheet — that's the duplication this consolidation removes.

The canonical store is unchanged: `05_published/_publish.log` (owned by
`rockstarr-infra`) is still the source of truth; the master list is its
export — just a comprehensive, orchestrator-owned one now.

## What NOT to do

- Do NOT build `06_reports/master-list-of-content.xlsx` (the old
  long-form-only workbook) — it's superseded by the comprehensive
  `master-list.xlsx`.
- Do NOT edit any workbook by hand. Gaps are still fixed at the source
  (`rockstarr-infra:publish-log`), then the master list regenerates.

## Related

- `rockstarr-orchestrator:baseline-audit` — builds the comprehensive
  master list (long-form + social); the new home.
- `rockstarr-content:master-list-blog-audit` — still the blog-side
  discovery that backfills the publish log (dispatched by baseline-audit).
- `rockstarr-infra:publish-log` — the canonical store.
