---
name: set-team-autopilot
description: "This skill should be used when the user wants to turn the orchestrator's proactive weekly planning on or off, or check whether it's on — e.g. \"turn on team autopilot\", \"have the lead plan our week\", \"enable proactive planning\", \"turn off team autopilot\", \"stop the weekly team tick\", or \"is team autopilot on?\". It flips the team_autopilot flag in stack.md and registers or removes the weekly team-tick scheduled task to match — no manual config editing. Team autopilot is OFF by default and opt-in. ON requires a marketing-plan to exist (the lead needs goals to plan toward). It does not change the cron time (that's capture-stack) and never plans, drafts, approves, or publishes anything itself."
---

# set-team-autopilot

A one-prompt switch for the orchestrator's **proactive weekly planning**
(the `team-tick`). Turning it on or off should not require hand-editing
`stack.md` or fiddling with scheduled tasks — this skill does both,
consistently.

Background: team autopilot is a single scheduled task — the weekly
`rockstarr-orchestrator:team-tick`, which reads the goals, finds the
biggest gap, auto-runs the matching play's safe steps, stops at the
approval gate, and notifies the founder. It is **additive** (it does not
replace the per-plugin crons like `content-loop`) and **off by
default** — a client only gets it if they opt in here. The `team-tick`
skill checks `stack.md.team_autopilot` at runtime, so the flag is the
source of truth and this skill keeps the scheduled task in sync.

## Inputs

- `state` — `on` | `off` | `status`. If the phrasing is unambiguous
  ("turn it off"), use it; if they just ask ("is it on?"), treat as
  `status`. If genuinely unclear, ask.

## Preconditions

- `/rockstarr-ai/00_intake/stack.md` exists. If not, point the user at
  onboarding / `capture-stack` — there's no stack to toggle.

## Behavior

### status

Read `team_autopilot` from `stack.md` (**absent = OFF by default**) and
`list_scheduled_tasks` to see whether `team-tick` is registered. Report
both plainly: e.g. "Team autopilot is ON — the weekly team-tick is
scheduled for Mondays 07:00 local" or "OFF — the lead only plans when
you ask it to."

### on

1. **Check there are goals to plan toward.** If
   `/rockstarr-ai/00_intake/marketing-plan.md` does not exist, tell the
   user the lead has nothing to work toward yet — run
   `rockstarr-orchestrator:set-marketing-goals` first — and stop. Don't
   schedule a tick that will only no-op.
2. **Set the flag.** Write `team_autopilot: true` to `stack.md` (add
   the key if absent). Same kind of small config write `capture-stack`
   makes.
3. **Register the task (idempotent).** Ensure the scheduled task exists,
   using the **same spec `scaffold-client` registers** (don't invent a
   new spec — reuse the canonical one):
   - `team-tick` at `stack.md.team_tick_cron` (default `"0 7 * * 1"` —
     Monday 07:00 local).
   `list_scheduled_tasks` first; create only if missing via
   `mcp__scheduled-tasks__create_scheduled_task`; never stomp a cron the
   operator already customized.
4. **Confirm** whether the task was created vs already-existed and the
   resolved local time.

### off

1. **Set the flag.** Write `team_autopilot: false` to `stack.md`. This
   is authoritative and immediate: `team-tick` checks `team_autopilot`
   at the top of its run and exits quietly when false, so even if the
   task fires before it's removed, it does nothing.
2. **Stop the task firing (best effort).** `list_scheduled_tasks`, then
   `mcp__scheduled-tasks__update_scheduled_task` to disable (or delete
   if supported) `team-tick`. If it can't be removed, that's fine — the
   flag already makes it a no-op; just say so.
3. **Confirm** that team autopilot is off and what happened to the task.

## What this does NOT do

- It does NOT change the cron *time* — `team_tick_cron` is set via
  `capture-stack`.
- It does NOT plan, draft, approve, or publish anything. It only flips
  the switch and syncs the one scheduled task.
- It does NOT touch the per-plugin crons (`content-loop`, `plan-month`,
  `approvals-digest`, `approvals-backlog-alert`) — team autopilot is
  additive and independent of them.
- It does NOT define the task spec itself — it reuses
  `scaffold-client`'s canonical `team-tick` spec so there is a single
  source of truth.

## Related

- `rockstarr-orchestrator:team-tick` — the weekly proactive planner this
  switch controls (gated on `team_autopilot`).
- `rockstarr-infra:scaffold-client` — wires this same task at onboarding
  (only when `team_autopilot` is explicitly on); the canonical cron spec
  lives there.
- `rockstarr-infra:capture-stack` — sets the flag and the cron time
  (`team_autopilot`, `team_tick_cron`).
- `rockstarr-infra:set-content-autopilot` — the sibling switch for
  content's daily/monthly autopilot (separate, also additive).
