# rockstarr-content (developer notes)

This file is for Claude Code working on this plugin's source. For the
full skill catalog, version history, drafting rules, lane definitions,
and folder contract, read `README.md` in this folder. This CLAUDE.md
is its developer-perspective complement.

## Why this plugin is different from the rest

It is a **content factory**. Most skills read files from
`/rockstarr-ai/00_intake/` + `/01_knowledge_base/` + `/02_inputs/`,
produce files into `02_inputs/` (planning artifacts) or `03_drafts/`
(approvable prose), and stop.

**Two lanes deliberately reach outside that file-in/file-out box:**

- **The SEO lane.** `seo-strategy` and (as of v0.8) `seo-site-audit`
  reach the open web — `WebFetch`/`WebSearch` for strategy, and
  Googlebot-UA fetches + schema extraction + (optional) the
  PageSpeed API for the audit. An SEO audit is worthless without
  touching the live site.
- **The LinkedIn-newsletter publish lane (as of v0.9).**
  `publish-linkedin-newsletter` and `verify-linkedin-newsletter`
  drive the LinkedIn UI via **Chrome MCP**. This is the first
  realized member of the deferred-`publish-*` class the plugin
  always anticipated (publish-wp / publish-ga were the placeholders
  for it). Publishing is otherwise still somebody else's job, but
  the LinkedIn newsletter has no API path that reproduces the
  editor's newsletter target + scheduling, so the connector lives
  here. Its top risk is posting to the wrong account — every run
  confirms the signed-in session, mirroring the outreach plugins'
  `confirm-session` pattern.

These are scoped exceptions, not a license to loosen the posture.
**Don't let network access or browser automation leak into the
drafting skills** — those never fetch or click; they read the KB
and write drafts. The publish lane never rewrites approved prose;
it transcribes an already-approved, already-stop-slopped piece.

Three properties follow:

1. **Failure modes are quality-of-output, not infrastructure.** A
   broken Chrome selector in interceptly is operationally visible —
   the bot stops sending. A subtle voice drift in this plugin is
   not — the bot keeps producing drafts; the client publishes them;
   six weeks later they wonder why their blog stopped sounding
   like them. The mandatory passes (stop-slop, TL rubric, blog
   SEO/GEO checklist) are the structural defense against this.
2. **The mandatory passes are the most important code in this
   plugin.** Skipping them ships broken content. The pass order
   is non-negotiable: domain-quality pass (TL rubric / SEO
   checklist) FIRST, stop-slop LAST. Style guide shapes voice
   during drafting; quality passes catch substance; stop-slop
   strips AI tells right before write.
3. **Cadence gates are binding.** Every lane is gated by a field
   in `stack.md` (`blogs_per_month`, `thought_leadership_per_month`,
   etc.). Cadence 0 means the lane is suppressed — no topics
   proposed, no slots scheduled, no drafts written. Drafting
   skills refuse to emit when their cadence is 0. Don't bypass.

## Skill groupings (mental map)

17 active skills sort into eight groups (plus two deferred and one
moved-out — see README):

1. **Strategy + audit (run on demand, typically quarterly)** —
   `seo-site-audit` then `seo-strategy`. `seo-site-audit` (new
   in v0.8) diagnoses the *existing* site (indexability, schema,
   on-page, content/topical authority, GEO, Core Web Vitals) and
   writes `02_inputs/seo/audit_[date].md` + a canonical
   `audit_state.md` punch-list. `seo-strategy` produces
   `02_inputs/seo/backlog.md` — the canonical 25-32 prioritized
   blog topics in 4-5 clusters — and, when a recent audit exists,
   folds its `refresh`/`consolidate`/`expand` content findings
   into the backlog alongside net-new (`new`) topics. The
   strategy/audit docs are dated and audit-preserved; the backlog
   and audit_state are canonical (regenerated/overwritten).
2. **Monthly planning** — `ideate-topics`, `content-calendar`.
   Reads the backlog (if present) and the publish log, proposes
   topic angles, slots them across the month.
3. **Long-form (outline-first; both lanes refuse to draft without
   an approved outline)** — `outline-blog` → `draft-blog`,
   `outline-thought-leadership` → `draft-thought-leadership`.
4. **Single-shot lanes** — `draft-newsletter`, `draft-case-study`.
   No outline-first gate.
5. **Derivatives** — `repurpose`. Takes one approved long-form
   piece, fans into LinkedIn post / X-or-Threads thread /
   newsletter highlight / (gated) video script.
6. **Publishing (Chrome MCP; as of v0.9)** —
   `publish-linkedin-newsletter` republishes an approved TL piece
   as a LinkedIn newsletter edition on the author's personal
   account (gated on `linkedin_newsletters_per_month`);
   `verify-linkedin-newsletter` confirms the edition went live.
   These are the realized members of the deferred-`publish-*`
   class. They drive a browser and keep humans in the loop for the
   cover image, the intro post, and the final Schedule click.
7. **Content tracking (v0.10; master list moved out in v0.13)** —
   `master-list-create` is **deprecated**: the master list is now a
   comprehensive, cross-channel artifact (long-form + social) owned by
   `rockstarr-orchestrator` (`baseline-audit` → `06_reports/master-list.xlsx`),
   and this skill is a thin redirect there (builds nothing).
   `master-list-blog-audit` crawls
   the client's live sitemap and reconciles it against the log,
   routing untracked live blogs back through `publish-log`. First
   skills in this plugin to emit an `.xlsx` (bundled openpyxl
   writer); the publish log stays the source of truth.
   `inventory-linkedin-newsletter` (as of v0.13) is the LinkedIn-side
   sibling: it opens the client's LinkedIn newsletter via Chrome MCP,
   lists already-published editions, and backfills untracked ones
   through `publish-log` (`format: linkedin-newsletter`). Read-only
   against LinkedIn — it never posts or publishes. Both blog-audit and
   this feed the orchestrator's `baseline-audit` (the cross-channel
   "where things stand" snapshot); the comprehensive master list now
   lives in `rockstarr-orchestrator`, this plugin just supplies
   long-form discovery.
8. **Scheduled production / autopilot** — `plan-month` (monthly,
   v0.12) + `content-loop` (daily, v0.11). `plan-month` is the
   monthly planning tick: it ideates in background, auto-selects a
   provisional pick set (fill-to-cadence, quick-wins/pillars first
   from the backlog, TL kept enemy-diverse), and produces a
   **provisional** `content-calendar` staged for the human to edit
   and approve — it never approves/drafts/publishes. Once the human
   approves the calendar, `content-loop` (below) takes over the
   daily drafting. Both are stop-at-gate, gated on `content_autopilot`,
   wired as crons by `scaffold-client`.

   `content-loop` is the daily background driver (content analog of
   the outreach `daily-loop`). Reads the approved
   `content-calendar`, infers each piece's state from the workspace
   files, and advances each due+unblocked item by ONE production
   step (outline on its date; draft on its date once the outline is
   approved), invoking the drafting skills in **background mode**.
   It is **stop-at-gate**: it stages drafts pending and never
   approves, never publishes. Bounded to ~1 production step per run
   (the scheduled-task turn ceiling). `scaffold-client` wires its
   daily cron when `content_autopilot` is on (default) and a content
   cadence is set; the existing `approvals-digest` surfaces what it
   produces. Publishing autopilot is a later phase (the publish
   connectors are still deferred). NOT autopilot-eligible:
   `draft-case-study` (interview), `ideate-topics`/`content-calendar`
   (human-gated planning), and the publish lanes.

   **Background mode.** The drafting skills (`outline-blog`,
   `draft-blog`, the TL pair, `draft-newsletter`) each carry a
   "Run modes" note: foreground (operator in chat) vs background
   (invoked by `content-loop` — produce + stage pending + don't
   present inline + never approve). The pipeline (domain pass →
   stop-slop) is identical in both; only the chat presentation
   differs. This is the same foreground/background split the outreach
   plugins use.

`draft-polls` moved out to `rockstarr-social` in v0.7 — short-form
social lives there now. The workspace conventions (`polls_cadence`
in stack.md, the LinkedIn polls subsection of style-guide.md) are
unchanged; only the implementing skill moved.

## The two-step pattern (outline-first)

Both long-form lanes use a strict two-step pattern:

1. **Outline skill** — produces the structural artifact (FAQ
   sections, keyword plan, internal linking plan, meta drafts for
   blog; thesis / counter-argument / opening scene / quotable line
   / buried proprietary term for TL).
2. **Approval gate** — the operator must explicitly approve the
   outline. Drafting skill **refuses to run** without an approved
   outline.
3. **Draft skill** — consumes the approved outline + runs the
   domain-quality pass (SEO/GEO checklist for blog, TL rubric for
   TL) + runs stop-slop + writes.

The gate exists because outline-quality is much cheaper to fix
than draft-quality. If you find yourself wanting to merge the two
steps "for speed," don't — the gate is the quality multiplier in
this plugin.

## Mandatory passes — order matters

Every prose-producing skill runs through this pipeline:

| Pass | Read | Run during | Notes |
|------|------|------------|-------|
| Style guide | `/00_intake/style-guide.md` | Throughout drafting | Shapes voice. Not a separate pass — it's the foundation. |
| TL rubric (TL only) | `_shared/references/tl-rubric.md` | Pass 1 (TL drafts) | Argument quality. Slogans don't get polished. |
| SEO/GEO checklist (blog only) | `_shared/references/blog-seo-geo.md` | Pass 1 (blog drafts) | 13-item checklist. FAQ required. |
| stop-slop | `_shared/stop-slop/` | Pass 2 (always last) | Strips AI tells. Writes `stop_slop_score` to front-matter. |

If you're modifying a drafting skill, verify the pass order. The
common bug is "stop-slop first, rubric second" — which means the
rubric judges already-stripped prose and misses argument-level
issues.

Structural artifacts (topic lists, calendars, outlines, interview
transcripts) are exempt from stop-slop by design — they're meant
to be machine-readable, not human-readable prose.

## First-party vs third-party content

This is the content-specific application of the repo-wide rule.
Only `01_knowledge_base/processed/` files with
`kb_scope: owned` AND `style_guide_eligible: true` may inform
*voice*. Third-party material (competitor posts, industry
research, saved articles) lives under `processed/third-party/`
and is **reference-only** — cited or linked, never paraphrased
as if the client said it.

The front-matter flags are the integrity check. `generate-style-guide`
(in rockstarr-infra) is required to ignore third-party files when
building the style guide; drafting skills here must respect the
same boundary. If a skill produces a draft that paraphrases
third-party copy in the client's voice, it's a bug — not a
stylistic choice.

## Shared references this plugin reads

This plugin is the heaviest consumer of `rockstarr-infra`'s shared
references:

- `_shared/references/tl-rubric.md` — read by
  `outline-thought-leadership`, `draft-thought-leadership`, and
  `ideate-topics` (the enemy-diversity check).
- `_shared/references/blog-seo-geo.md` — read by `outline-blog`
  (research phase, FAQ outline, keyword + linking plans, meta
  drafts) and `draft-blog` (FAQ in body, inline sources, keyword
  density, direct-answer pattern, structured definitions, the
  13-item gate).
- `_shared/references/case-study-prompt.md` — the case-study
  interview script for `draft-case-study`.
- `_shared/stop-slop/SKILL.md` — the mandatory final pass.

None of these may be forked into this plugin. If you find
yourself wanting to alter a rubric's behavior just for content,
the change goes upstream in `rockstarr-infra` and every consumer
takes the new behavior.

## Front-matter contract for drafts

Every draft this plugin writes carries a documented front-matter
shape (see "Drafting rules" in the README — rule 5). The
operationally-load-bearing fields:

- `channel`, `title`, `slug`, `produced_by`, `produced_at`
- `style_guide_version` — `approve` audits this for drift
- `kb_sources_used` — which KB files informed the draft
- `cta_text`, `cta_destination`
- `approval_status` (set to `pending` on first write),
  `awaiting_approval_since` — read by
  `rockstarr-infra:approvals-digest` and
  `rockstarr-infra:approvals-backlog-alert`
- Lane-specific: `outline_source` (blog/TL), `stance` (TL),
  `linkedin_newsletter_eligible` (TL — flags the approved piece as
  a LinkedIn-newsletter republish source for
  `publish-linkedin-newsletter`), `monthly_pieces_linked`
  (newsletter), `interview_source` (case study), `source_path`
  (derivatives)
- `stop_slop_score` — the numeric output of the final pass

The cross-bot fields (`approval_status`, `awaiting_approval_since`)
are the same contract `rockstarr-reply` uses for reply drafts.
Changes there are cross-plugin coordination work.

## What's high-risk to change in this plugin

- **The mandatory pass order.** TL rubric / SEO checklist before
  stop-slop. Inversion ships broken content quietly.
- **The two-step outline-first gate.** Removing it ships shallow
  drafts at scale.
- **The cadence-gate logic.** Bypassing it means clients get
  drafts in lanes they don't publish, which surfaces as noise in
  their queue.
- **The first-party vs third-party content boundary.**
  Paraphrasing third-party as the client's voice is a real-bug,
  not a stylistic call.
- **The draft front-matter contract.** Other plugins read these
  fields.
- **`stack.md` content-cadence block schema.** Six fields, all
  read by multiple skills. Adding optional fields is safe;
  renaming or removing is not.

## What's safe to change without much ceremony

- Internal logic of any single drafting skill (tone heuristics,
  topic-angle generation, paragraph structure) as long as the
  pass order and the front-matter shape are preserved.
- The `seo-strategy` six-phase workflow — the output shapes
  (`strategy_<date>.md` + `backlog.md`) are what downstream
  skills depend on; the journey to those outputs can evolve.
- New optional lane-specific front-matter fields.
- Wording of operator-facing prompts and confirmations.
- The DEFER publish skills (when they're built; they're not
  yet).

## Versioning

Major version axis: the front-matter contract, the lane set, the
cadence-gate schema. Minor: new skills, new optional config,
significant new passes (the SEO/GEO checklist at v0.4 was a
minor; the TL rubric at v0.3 was a minor).

Bump via `/bump rockstarr-content <new-version>` at the repo
root.

## Testing your changes

Drafting skills are LLM-prompted; no automated test harness can
judge "is this draft on-voice." The manual approach for this
plugin:

1. **Build the `.zip`** via `scripts/package-plugin.sh
   rockstarr-content`.
2. **Sideload** into your own Cowork against a real test client
   workspace (one with `client-profile.md`, an approved
   `style-guide.md`, and some first-party KB files).
3. **Run the skill** end-to-end. Read the output as a human.
4. **Verify the front-matter** matches the contract.
5. **Verify the pass order** by inspecting the skill body — the
   right order is style-guide → domain rubric (TL or SEO) →
   stop-slop → write.

For `seo-strategy`, you can validate the backlog shape without
sideloading — it's a deterministic format check on
`02_inputs/seo/backlog.md`.

CI in this monorepo only checks skill-name uniqueness.

## When you're stuck

Ask Jon in the PR. Voice-rule and pass-order questions especially —
those are the most consequential decisions in this plugin and the
most likely to be silently wrong.
