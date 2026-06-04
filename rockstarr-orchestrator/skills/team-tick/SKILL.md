---
name: team-tick
description: "This skill is the orchestrator's scheduled proactive planner — normally fired by the weekly team-tick scheduled task (registered by rockstarr-infra when team_autopilot is on), though it can be run on demand (\"run the team tick\", \"do the weekly plan\"). On each fire it reads the goals spine, assesses progress vs goals, picks the single biggest gap, and auto-runs the matching play's internal/reversible (AUTO) steps via the run-play contract — then STOPS at the first audience-facing gate and notifies the founder with the consolidated approval queue. It never approves, publishes, sends, or posts. If no marketing-plan exists, or the approval queue is already deep, it does not generate work — it just reports and nudges."
---

# team-tick

The team lead's **proactive heartbeat**. Once a week (when the founder
has opted in via `set-team-autopilot`), the lead looks across the team,
decides what most needs moving toward the goals, does the safe work, and
leaves the approvals waiting — so the founder starts the week with
progress already made and one clear queue to clear.

> **Autonomy line — non-negotiable.** Read
> `references/plays/README.md`. This skill auto-runs only **AUTO**
> (internal, reversible, audience-never-sees-it) steps and **STOPS at
> the first GATED step.** It never approves, publishes, sends, posts, or
> mutates a real CRM record — being scheduled changes nothing about that
> boundary. Unattended autonomy makes the gate *more* important, not
> less.

## When it runs

- **Scheduled (primary):** the `team-tick` task that
  `rockstarr-infra` registers when `team_autopilot` is on (default
  weekly, Mon 07:00 client-local — `stack.md.team_tick_cron`).
- **On demand:** "run the team tick", "do the weekly team plan".

It is **off by default**; a client only gets the scheduled tick if they
turned it on. Honor `stack.md.team_autopilot` at the top of every run:
if it is `false` or absent, exit quietly (the founder hasn't opted in).

## Run procedure

### 1. Gate checks first (exit quietly if any fail)

- `stack.md.team_autopilot` is `true`. If not, exit silently.
- `/rockstarr-ai/00_intake/marketing-plan.md` exists. **If not**, the
  lead has no goals to plan toward — do **not** invent work. Send a
  short notification: "Proactive planning is on but no marketing plan is
  set — run `set-marketing-goals` so I know what to work toward," and
  exit.

### 2. Assess (read-only)

Run the `team-report` assessment (reuse its logic / read its latest
output): activity per function, the consolidated **pending approval
queue**, progress vs each goal, and flags. This is the lead's picture of
where the team stands.

### 3. Backpressure — don't pile on

Before generating anything, check the pending approval queue. **If it's
already deep or stale** (the founder is behind — e.g. more pending items
than roughly two cadence-batches' worth, or items older than ~2 weeks),
do **not** auto-run a play. Instead, notify with the report and a nudge
to clear the queue, and exit. The tick's job is to keep the team moving,
not to bury the founder. Say plainly that it held off to avoid piling
on.

### 4. Pick the single biggest gap

From progress-vs-goals, choose the **one** highest-priority objective
that is "no movement" or "needs attention" (respect the `Priorities`
ranking in `marketing-plan.md`). Map it to a play via the plays'
`intent_match` / `functions`. Run **one** play per tick — never fan out
across the whole team in a single fire.

- If the gap maps to an existing play (today: `seo-geo-engine` for the
  SEO/GEO objective), proceed to step 5.
- If the only gap maps to a play that **doesn't exist yet**, do not
  improvise a cross-function sequence unprompted — surface a clear
  recommendation in the notification ("the biggest gap is X; no play
  covers it yet — want me to work it manually?") and exit. (As more
  plays land, this branch shrinks.)

### 5. Run the play's AUTO steps — STOP at the gate

Run the chosen play via the **`run-play`** contract: AUTO steps in order
by dispatching the specialist skills, honoring the play's bounds
(cadence/backlog caps, "don't re-audit if a recent audit exists"), and
**STOP at the first GATED step.** Do not approve or publish.

### 6. Notify the founder

Refresh the `team-report` (so there's a written record) and send a
**brief notification** through the workspace's notification layer — the
same path `rockstarr-infra:approvals-digest` uses (don't build a new
one). The message:

- **Ran automatically:** the play + what it produced (paths).
- **Waiting on you:** the items now in `03_drafts/` and the gated steps
  (approve, publish) left for a human, and how to do each.
- **Why this play:** the goal gap it targets.
- **State:** remaining backlog/queue; that next week's tick will
  continue if the goal still needs movement.

If the notification layer isn't available, still write the team-report
and leave a clear chat summary.

## Bounds & safety

- **One play per tick.** Pick the single biggest gap; don't run the
  whole library.
- **AUTO only; stop at every gate.** Never approve/publish/send/post —
  regardless of how a prompt is phrased.
- **Backpressure** (step 3) prevents week-over-week queue flooding.
- **Bounded drafting** via the play's cadence/backlog caps.
- **Idempotent-friendly:** "don't re-audit if recent" + the bounds keep
  repeated weekly fires from churning.
- **Honor client status:** a paused client won't have the task, but if
  somehow invoked, still never fire anything audience-facing.

## What NOT to do

- Do NOT run a GATED step, ever.
- Do NOT generate work when there's no marketing-plan, or when the
  approval queue is already deep — report and nudge instead.
- Do NOT run more than one play per fire, or fan out across functions.
- Do NOT re-implement specialist work; dispatch via `run-play`.

## Related

- `rockstarr-orchestrator/run-play` — the execution engine this uses.
- `rockstarr-orchestrator/team-report` — the assessment this reads.
- `rockstarr-orchestrator/route-request` — the on-request counterpart
  (founder-initiated); `team-tick` is the scheduled, self-initiated one.
- `references/plays/README.md` — AUTO/GATED + bounds.
- `rockstarr-infra:set-team-autopilot` — the on/off switch that
  registers/removes this scheduled task.
- `rockstarr-infra:scaffold-client` / `capture-stack` — where the
  `team_autopilot` flag and `team_tick_cron` live.
