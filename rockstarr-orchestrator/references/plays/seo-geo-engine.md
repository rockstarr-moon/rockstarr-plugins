---
play: "seo-geo-engine"
title: "SEO/GEO Engine"
intent_match:
  - "get us ranking"
  - "improve our SEO"
  - "rank for our category"
  - "show up in AI answers"
  - "get cited by AI / ChatGPT / Perplexity"
  - "build our SEO engine"
  - "organic visibility"
  - "content that ranks"
functions:
  - "Content & SEO"
---

# Play: SEO/GEO Engine

Stand up the organic-visibility + AI-citation engine for a client:
audit where they stand, turn that into a concrete SEO/GEO strategy and
a prioritized backlog, then begin filling the highest-priority cluster
with drafts — stopping cleanly at the publish gate.

All steps below run inside **`rockstarr-content`** (the Content & SEO
function). The team lead dispatches them in order; it does not do the
work itself.

## Preconditions

- A scaffolded client workspace (`/rockstarr-ai/`) with an approved
  `00_intake/style-guide.md` and `stack.md`.
- The client runs content (`blogs_per_month` >= 1 in `stack.md`). If
  cadence is 0, run the audit + strategy (AUTO) but **do not** auto-draft
  — present the strategy and ask whether to turn content on.
- Read `../role-registry.md` (Content & SEO output paths) and, if
  present, `00_intake/marketing-plan.md` (the SEO/GEO objective this
  play serves).

## Steps

| # | Step | Specialist skill | Tag | Produces |
|---|------|------------------|-----|----------|
| 1 | Audit current organic + GEO posture | `rockstarr-content:seo-site-audit` | **AUTO** | `02_inputs/seo/audit_*.md` (+ `audit_state.md`) |
| 2 | Turn the audit into strategy + a prioritized backlog | `rockstarr-content:seo-strategy` | **AUTO** | `02_inputs/seo/strategy_*.md`, `02_inputs/seo/backlog.md` |
| 3 | Shape topics for the top cluster (if the backlog needs them) | `rockstarr-content:ideate-topics` | **AUTO** | `02_inputs/content-topics_*.md` |
| 4 | Outline the next backlog item(s) | `rockstarr-content:outline-blog` | **AUTO** | outline in `03_drafts/content/` |
| 5 | Draft the next backlog item(s), bounded by cadence | `rockstarr-content:draft-blog` | **AUTO** | blog draft in `03_drafts/content/` (drafts + stops) |
| — | **Approve drafts** | (human via `rockstarr-infra:approve`) | **GATED** | — |
| — | **Publish** to the site | (human / publish flow) | **GATED** | — |

## Stop point

After step 5, **STOP.** Steps 4–5 are bounded to **one batch** — the
client's `blogs_per_month` cadence, or **1** if unset — so the play
seeds the cluster without flooding the queue. Approval and publishing
are GATED: the lead never approves and never publishes.

Present to the founder:
- the refreshed strategy + backlog (what the engine will work toward),
- the drafts now sitting in `03_drafts/content/` awaiting approval (the
  pending queue), and
- the remaining backlog count + the note that the **content autopilot**
  (`plan-month` / `content-loop`, if enabled in `stack.md`) will keep
  drafting the cluster on cadence from here — this play is the on-demand
  kickstart, the autopilot is the steady state.

## Notes / bounds

- **AUTO only through drafting.** Everything up to and including drafting
  to `03_drafts/` is reversible and audience-never-sees-it, so it runs
  automatically. The first audience-facing gate is publish — the play
  halts there.
- **Don't re-audit needlessly.** If a recent `audit_*.md` exists (check
  `audit_state.md`), summarize it and skip step 1 unless the founder
  asks for a fresh audit.
- **Respect the cadence cap** in step 5; log how many drafts were
  produced and how many backlog items remain.
- **GEO is part of the goal**, not a separate step — `seo-site-audit`
  and `seo-strategy` already cover AI-citation posture (see infra's
  `blog-seo-geo.md`). Surface the GEO findings in the summary.
