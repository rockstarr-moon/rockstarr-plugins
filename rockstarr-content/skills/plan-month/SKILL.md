---
name: plan-month
description: "This skill should be used when the scheduled monthly planning task fires, or when the user says \"plan the month\", \"run monthly planning\", or \"propose this month's content plan\". The scheduled driver for monthly content PLANNING (autopilot Phase 2): runs ideate-topics in background to produce the month's ranked topic list, auto-selects a provisional pick set (fill each enabled lane to its stack.md cadence), then runs content-calendar in background to produce a PROVISIONAL monthly calendar staged for approval. It NEVER approves, drafts, or publishes — it stops at the human approval gate so the operator edits the picks and approves. Gated on stack.md content_autopilot."
---

# plan-month

The monthly counterpart to `content-loop`. Where `content-loop`
advances per-piece *production* daily, this advances the *monthly
plan* once a month: it ideates, makes a **provisional** editorial
selection, and lays out a proposed calendar — then **stops at the
human approval gate**. The operator edits the picks and approves;
from there `content-loop` takes over the daily drafting.

> **Template convention.** Fenced code blocks below show `# ---`
> where YAML front-matter delimiters belong. **Emit real `---` in any
> output file.**

## The one rule: propose, never commit

This skill produces a **proposed** month and stops. It:

- **never approves** the calendar (approval is a human action via
  `rockstarr-infra:approve`),
- **never drafts** content (that's `content-loop`, after approval),
- **never publishes.**

The picks it makes are a **provisional default** the operator is
expected to edit — fill-to-cadence starting points, not final
editorial decisions. The human re-picks freely and approves.

## When it runs

- **Scheduled:** a monthly cron (`stack.md.content_plan_cron`, wired
  by `rockstarr-infra:scaffold-client` when `content_autopilot` is on),
  early on the 1st so the proposed plan is waiting at the start of the
  month.
- **On demand:** "plan the month" / "propose this month's content
  plan".

## Preconditions

Tier 1 cheap checks; exit quietly if any fail:

- `stack.md` exists, `content_autopilot` is not `false`, and at least
  one content cadence is >= 1. If autopilot is off or all cadences are
  0, exit — nothing to plan.
- `client-profile.md` and an approved `style-guide.md` exist (ideation
  needs them).

**Idempotency / don't clobber.** If this month already has a
`content-calendar_[YYYY-MM].md` that is **approved**, do nothing — the
month is committed. If a provisional plan from a prior run of THIS
skill exists but is still pending and untouched, regenerate it. If the
operator has already started editing (picks changed, partial
approvals), do NOT overwrite — surface that a plan already exists and
stop.

## Workflow

### Step 1 — Anchor, then ideate (background)

Fire the anchor ("Proposing this month's content plan…"), then run
`ideate-topics` in **background mode**: it produces the ranked
`02_inputs/content-topics_[YYYY-MM].md` for the enabled lanes (reading
the SEO backlog when present), and — because no operator is in chat —
it **flags** any rhyming-enemy TL pairs in the file rather than asking
about them. It does not pick.

### Step 2 — Auto-select a provisional pick set

Mark `Pick: yes` on a default selection, lane by lane, up to each
lane's `stack.md` cadence. This is a starting proposal, not a verdict:

- **Researched blog** (`blogs_per_month`): prefer SEO-backlog items —
  quick-wins (⭐) first, then a pillar before its supporting posts
  within a cluster, then spread across clusters. Fill to cadence.
- **Thought leadership** (`thought_leadership_per_month`): pick up to
  cadence, keeping the month's enemies diverse — if two angles' enemies
  rhyme (per the flag from Step 1), pick the stronger and leave the
  other unpicked. Never auto-pick a rhyming pair.
- **Email newsletter** (`email_newsletters_per_month`): select to
  cadence; these anchor to the month's selected long-form.
- **LinkedIn newsletter** (`linkedin_newsletters_per_month`): only when
  a selected TL piece is `linkedin_newsletter_eligible`.
- Lanes at cadence 0 are skipped. Case studies are NOT planned here
  (quarterly, interview-driven).

Record in the topics file that the picks were **auto-proposed by
plan-month** so the operator knows they're a default to review, not a
human decision.

### Step 3 — Build the provisional calendar (background)

Run `content-calendar` in **background mode** against the auto-picked
topics. It produces `02_inputs/content-calendar_[YYYY-MM].md` with
`approval_status: pending`, marked **provisional / auto-proposed**,
applying its normal scheduling rules (outline-before-draft, pillar
ships before its supports, newsletters on the preferred weekday,
spacing). No drafting happens.

### Step 4 — Stage + hand off to the human

The proposed plan now sits as two pending files (topics + calendar).
Surface it for review — do NOT approve. Notify the operator (the
existing `approvals-digest` will also list the pending calendar):

> Your [Month] content plan is proposed and ready to review:
> [N] picks across [lanes]. Edit the picks if you want, then approve
> the calendar. Once approved, the daily content-loop drafts each
> piece on its date.

If a rhyming-enemy TL pair was flagged in Step 1, call it out here so
the operator resolves it before approving.

## Output

- `02_inputs/content-topics_[YYYY-MM].md` — ranked list with the
  auto-proposed `Pick: yes` set + any enemy-rhyme flags.
- `02_inputs/content-calendar_[YYYY-MM].md` — provisional, pending
  approval.
- A run summary: `month`, `picks_per_lane`, `flagged` (rhyming TL
  pairs), `state: proposed-pending-approval`.

## What NOT to do

- Do NOT approve the calendar or any piece. The gate is human.
- Do NOT draft or publish — `content-loop` drafts only AFTER the
  human approves the calendar.
- Do NOT overwrite a month the operator has already approved or
  started editing. Surface and stop.
- Do NOT auto-pick a rhyming-enemy TL pair, or pick a lane whose
  cadence is 0.
- Do NOT plan case studies (quarterly, interview-driven) here.
- Do NOT run when `content_autopilot` is `false`.

## Related

- `rockstarr-content:ideate-topics` — produces the ranked list
  (background mode).
- `rockstarr-content:content-calendar` — lays out the provisional
  calendar (background mode), pending human approval.
- `rockstarr-content:content-loop` — the daily Phase 1 driver that
  drafts the approved calendar to the gates.
- `rockstarr-infra:scaffold-client` — wires the monthly cron and reads
  `content_autopilot` / `content_plan_cron`.
- `rockstarr-infra:approve` — the human gate this skill stops at.
