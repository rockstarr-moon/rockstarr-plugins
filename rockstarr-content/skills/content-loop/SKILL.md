---
name: content-loop
description: "This skill should be used when the scheduled daily content task fires, or when the user says \"run the content loop\", \"advance the content schedule\", or \"run content autopilot\". The scheduled driver for content production: it reads the APPROVED monthly content-calendar, infers each piece's state from the workspace files, and advances each item that is due today (and not blocked) by ONE production step — running the right drafting skill in background mode and then stopping at the human approval gate. It NEVER approves and NEVER publishes (publishing is a later phase). Honors lane cadence, the outline-first gate, and the mandatory quality passes. Silent on days with nothing due. Gated on stack.md content_autopilot."
---

# content-loop

The scheduled heartbeat of content production. Where the monthly
flow used to require a human to kick off each outline and draft on
its calendar date, this skill does the **production** automatically
and parks each piece at the next **human gate**. It is the content
analog of the outreach `daily-loop`, and it follows the same
background-mode discipline.

> **Template convention.** Fenced code blocks below show `# ---`
> where YAML front-matter delimiters belong. **Emit real `---` in any
> output file.**

## The one rule: produce on schedule, never approve or publish

This skill advances pieces through the production steps (write the
outline, write the draft) on their calendar dates. It **stops at
every human gate**:

- It never moves a file to `04_approved/` — approval is a human
  action through `rockstarr-infra:approve`.
- It never publishes — publishing connectors are a later phase, and
  even then publishing keeps a human in the loop.
- If a piece is due to be drafted but its outline isn't approved yet,
  it does NOT draft (and does NOT approve the outline to unblock
  itself). It records the slippage and leaves the nudge to the
  approvals notifications.

Drafts it produces land in `03_drafts/content/` with
`approval_status: pending` (the drafting skills already do this), so
the daily `rockstarr-infra:approvals-digest` surfaces them to the
human the same way an operator-run draft would.

## When it runs

- **Scheduled:** a daily cron (`stack.md.content_loop_cron`, wired by
  `rockstarr-infra:scaffold-client` when `content_autopilot` is on).
  Schedule it shortly BEFORE the 6am `approvals-digest` so anything
  produced this morning is included in today's digest.
- **On demand:** "run the content loop" / "advance the content
  schedule".

Most days nothing is due (the calendar spaces pieces out) — on those
days the loop exits silently, like the digest does on empty days.

## Preconditions

Tier 1 cheap checks; exit quietly (not an error) if any fail:

- `stack.md` exists and `content_autopilot` is not `false` (default
  on). If autopilot is off, exit — the client opted out of scheduled
  production.
- An **approved** `02_inputs/content-calendar_[YYYY-MM].md` exists for
  the current month (front-matter `approval_status: approved`). No
  approved calendar = nothing committed to produce; exit quietly.
- `style-guide.md` is present and approved (drafting needs it).

## What it advances (and what it does NOT)

**Eligible production actions** (the only things this skill runs
unattended):

- `outline-blog`, `outline-thought-leadership` — produce the outline,
  stage it pending. (The outline is itself a human gate; the loop
  stops here.)
- `draft-blog`, `draft-thought-leadership` — only when the matching
  outline is **approved**.
- `draft-newsletter` — single-shot (no outline gate); produce + stage.

**Never run unattended by this skill:**

- `draft-case-study` — interview-driven (`AskUserQuestion` per
  question); it would hang in a scheduled run. Case studies stay
  human-initiated, and they live outside the monthly calendar anyway.
- `ideate-topics` / `content-calendar` — they need human picks and a
  human calendar approval. Monthly planning stays foreground (a later
  phase may auto-produce the topic list, still human-approved).
- `publish-linkedin-newsletter` and any publish step — publishing is
  out of scope for the loop (human-in-the-loop / a later phase).
- `repurpose` — runs off an approved long-form piece on demand, not
  on the calendar.

## Workflow

### Step 1 — Anchor + load the calendar

Read the approved `content-calendar_[YYYY-MM].md`. Use its
chronological table (Date / Lane / Action / Slug) as the schedule of
record.

### Step 2 — Find what's due

Collect calendar rows whose **Action is an eligible production
action** (above) AND whose **Date is today or earlier** AND that are
**not already done** (see Step 3 state inference). Sort oldest-date
first. Skip `publish` rows and ineligible actions.

### Step 3 — Infer each candidate's state from the files

For each candidate slug, determine state by checking the workspace
(no separate state file — same file-inference the monthly skills
use):

- Outline present? `03_drafts/content/outline-blog_[slug].md` or
  `outline-tl_[slug].md`. Approved? a matching entry in
  `04_approved/content/` or `approval_status: approved` in the
  outline front-matter.
- Draft present? `03_drafts/content/[slug].md`. Approved / published?
  `04_approved/content/[slug].md` / a `[slug]` line in
  `05_published/_publish.log`.

Decide the next step per candidate:

- Action `outline-*` and no outline yet → **produce the outline.**
- Action `draft-*` and outline approved and no draft yet → **produce
  the draft.**
- Action `draft-*` but outline NOT approved → **blocked.** Do not
  draft, do not approve the outline. Record slippage (Step 5).
- Already produced (file exists for this step) → no-op; move on.

### Step 4 — Advance ONE step (turn-budget bound)

Run the next step for the **single oldest-due unblocked candidate**,
invoking the drafting skill in **background mode** (produce + stage
with `approval_status: pending`; do NOT present in chat; do NOT
approve). One production step per run by default
(`stack.md.content_loop_max_per_run`, default 1) — a full researched
draft is turn-heavy and a scheduled task has a hard turn ceiling, so
the loop deliberately does a little each day rather than risk a
half-finished run. The calendar's spacing means more than one step is
rarely due on the same day; when it is, the rest wait for the next
tick and are surfaced as slippage.

The drafting skill runs its normal pipeline unchanged — the
domain-quality pass (SEO/GEO checklist or TL rubric) then stop-slop,
in that fixed order. The loop does not bypass any pass.

### Step 5 — Record + hand off to the human

- If a draft/outline was produced: it sits pending in
  `03_drafts/content/`. The next `approvals-digest` lists it. Append a
  one-line note to `05_published/content/[today].md` (or an autopilot
  log): `content-loop — produced [outline|draft] for [slug]`.
- If candidates were **blocked** (draft due, outline unapproved) or
  **slipped** (more due than the per-run bound): record them so the
  human sees the queue isn't moving — the existing
  `approvals-backlog-alert` already nudges on stale pending items;
  note blocked/slipped slugs in the run summary too.
- If nothing was due: exit silently.

## Output

A short run summary (also fine to leave silent on empty days):

- `produced` — `{slug, step}` if a step ran this tick.
- `blocked` — slugs whose draft is due but outline isn't approved.
- `slipped` — due candidates beyond the per-run bound, deferred to
  the next tick.
- `nothing_due` — true on quiet days.

## What NOT to do

- Do NOT approve anything. Ever. The gate is human.
- Do NOT publish, and do NOT run `publish-linkedin-newsletter`.
- Do NOT run `draft-case-study` (interview) or `ideate-topics` /
  `content-calendar` (human-gated) unattended.
- Do NOT draft a blog/TL whose outline isn't approved — record the
  block; don't self-unblock.
- Do NOT bypass the mandatory passes or the outline-first gate.
- Do NOT exceed `content_loop_max_per_run` production steps in one
  tick — protect the scheduled-task turn budget.
- Do NOT run for a lane whose `stack.md` cadence is 0, or when
  `content_autopilot` is `false`.

## Related

- `rockstarr-content:content-calendar` — produces the approved
  calendar this loop reads.
- `rockstarr-content:outline-blog` / `draft-blog` /
  `outline-thought-leadership` / `draft-thought-leadership` /
  `draft-newsletter` — the production skills it invokes (background
  mode).
- `rockstarr-infra:approvals-digest` / `approvals-backlog-alert` — the
  human-facing nudges for what the loop stages.
- `rockstarr-infra:scaffold-client` — wires the daily cron and the
  `content_autopilot` / `content_loop_cron` config.
