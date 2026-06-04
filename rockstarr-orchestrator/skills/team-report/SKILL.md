---
name: team-report
description: "This skill should be used when the user wants a single cross-team status — e.g. \"how's the team doing\", \"team report\", \"what has the marketing team done\", \"what's waiting on me\", \"where are we against our goals\", or \"give me the marketing status\". The team lead's single pane: it reads the goals spine (00_intake/marketing-plan.md) and each function's outputs across the workspace, then writes ONE unified report — activity per function, the consolidated approval queue, progress vs goals, and flags. It is strictly READ-ONLY: it scans and summarizes; it never drafts, sends, publishes, approves, or runs any other skill."
---

# team-report

The founder's single pane. Instead of checking five plugins, the team
lead reads across the whole workspace and gives you one status: what
the team did, what needs you, and how it ladders up to your goals.

> **Strictly read-only (Phase A).** This skill **only reads and
> summarizes.** It does not draft, send, publish, approve, run other
> skills, or change any file except the report it writes. It is a
> mirror, not a hand. (Proactive planning and acting on the "safe"
> internal work come in a later phase.)

## When to run

- On demand: "how's the team doing?", "team report", "what's waiting on
  me?", "where are we against our goals?".
- Useful weekly as a Monday status, or before a strategy call.

## Preconditions

- `/rockstarr-ai/` exists (a scaffolded client workspace).
- Read `references/role-registry.md` (this plugin) for the function →
  output-path map. Read `00_intake/marketing-plan.md` if present (the
  goals); if absent, still produce the activity report and note that no
  goals are set yet (suggest `set-marketing-goals`).

## What it reads (per the role registry)

Scan, do not modify. For each function, gather recent activity + current
state from the paths the registry lists:

- **Content & SEO** — recent `05_published/_publish.log` blog/TL/
  newsletter entries; pending items in `03_drafts/content/`; SEO backlog
  remaining vs cadence (`02_inputs/seo/backlog.md`); latest audit /
  strategy date; whether a provisional `content-calendar_*` is awaiting
  approval.
- **Brand & Social** — pending batches/posts in `03_drafts/social/`;
  recent `05_published/social*`; any engagement artifacts.
- **Demand Gen** — outreach metrics from the workbook/mirror (connects
  sent vs the weekly cap, accepts, replies, booked); pending replies in
  `03_drafts/replies/` + `02_inputs/replies/_flags.md`; upcoming
  call-prep.
- **RevOps & Foundation** — total pending-approval count across all
  `03_drafts/` channels (the single approval queue); recent publishes;
  any `_errors.md` (incidents).

Use what's present; note what's missing rather than guessing. If a
plugin/function isn't installed or has no data, say so briefly — don't
fabricate activity.

## What it writes

One report to `/rockstarr-ai/06_reports/team/team-report_[YYYY-MM-DD].md`
(create the `team/` dir if missing; if today's report exists, append
`-2`). Sections:

1. **Headline** — one or two sentences: the team's state this period.
2. **By function** — a short block each (Content & SEO, Brand & Social,
   Demand Gen, RevOps & Foundation): what shipped/was produced, what's
   in flight.
3. **Awaiting your approval** — the consolidated queue across every
   channel (content drafts, reply drafts, social batches, a provisional
   calendar). This is the single approvals view — counts + the oldest
   items first.
4. **Progress vs goals** — for each objective in `marketing-plan.md`,
   map the period's activity to it and give a plain-language read
   (on track / needs attention / no movement). Be honest that Phase A
   measures *activity*, not analytics — we don't yet pull GA4 / Ahrefs /
   CRM metrics, so this is "is the team doing the work that should move
   this goal," not a metrics dashboard. Flag that distinction.
5. **Flags** — anything stuck or risky: `_errors.md` entries, stale
   pending approvals, a thinning SEO backlog, an outreach cap nearly
   hit, autopilot blocked on an unapproved gate. **Also flag if no
   baseline exists** — if there's no `06_reports/master-list.xlsx`, the
   team hasn't inventoried what already exists; recommend running
   `baseline-audit` first (it's one of the first things a new client
   should do).
6. **Suggested next moves** — a short, advisory list ("approve the 3
   blog drafts," "refresh the backlog — 2 items left," "the calendar is
   waiting"). **Advisory only** — this skill does not act on them.

Then print a tight chat summary (headline + the approval count + the
top 1–2 flags) and the report path.

## What NOT to do

- Do NOT modify any file except the report it writes. No drafting,
  approving, sending, publishing, or running other skills.
- Do NOT approve or clear the pending queue — only report it.
- Do NOT fabricate metrics or activity. Report what the files show;
  name the gaps.
- Do NOT present analytics as if they were measured — Phase A reports
  activity-vs-goals, not outcome metrics.

## Related

- `rockstarr-orchestrator/set-marketing-goals` — the goals this report
  measures against.
- `references/role-registry.md` — the function → output-path map this
  report scans.
- `rockstarr-infra:approvals-digest` — the per-day approvals nudge; this
  report is the broader cross-function single pane.
