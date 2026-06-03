---
name: set-content-autopilot
description: "This skill should be used when the user wants to turn scheduled content production on or off, or check whether it's on — e.g. \"turn on content autopilot\", \"enable scheduled content\", \"turn off content autopilot\", \"pause the content schedule\", \"stop auto-drafting my content\", or \"is content autopilot on?\". It flips the content_autopilot flag in stack.md and registers or removes the two content scheduled tasks (the daily content-loop and the monthly plan-month) to match — no manual config editing. ON requires a content cadence in stack.md; OFF takes effect immediately because the autopilot skills check the flag at runtime. It does not change cron times (that's capture-stack) and never drafts, approves, or publishes anything itself."
---

# set-content-autopilot

A one-prompt switch for scheduled content production. Turning it on or
off should not require hand-editing `stack.md` or fiddling with
scheduled tasks — this skill does both, consistently.

Background: content autopilot is two scheduled tasks wired by
`scaffold-client` — the daily `rockstarr-content:content-loop`
(produces drafts to the human gate) and the monthly
`rockstarr-content:plan-month` (proposes the month's calendar). Both
are gated on `stack.md.content_autopilot` and check it at runtime, so
the flag is the source of truth and this skill keeps the scheduled
tasks in sync with it.

## Inputs

- `state` — `on` | `off` | `status`. If the user's phrasing is
  unambiguous ("turn it off"), use it; if they just ask about it
  ("is autopilot on?"), treat as `status`. If genuinely unclear, ask.

## Preconditions

- `/rockstarr-ai/00_intake/stack.md` exists. If not, point the user at
  onboarding / `capture-stack` — there's no stack to toggle.

## Behavior

### status

Read `content_autopilot` from `stack.md` (absent = on by default) and
`list_scheduled_tasks` to see whether `content-loop` and `plan-month`
are registered. Report both plainly: e.g. "Content autopilot is ON —
the daily content-loop and monthly plan-month tasks are scheduled" or
"OFF — the flag is false and the tasks are not firing."

### on

1. **Check there's something to schedule.** If every content cadence
   in `stack.md` (`blogs_per_month`, `thought_leadership_per_month`,
   `email_newsletters_per_month`) is 0, tell the user there's no
   content lane to automate yet (set a cadence in `capture-stack`
   first) and stop — don't register idle tasks.
2. **Set the flag.** Write `content_autopilot: true` to `stack.md`
   (add the key if absent). This is a small front-matter / config
   write, the same kind `capture-stack` makes.
3. **Register the tasks (idempotent).** Ensure the two scheduled
   tasks exist, using the **same specs `scaffold-client` registers in
   its step 8** (don't invent new specs — reuse the canonical ones):
   - `content-loop` at `stack.md.content_loop_cron` (default
     `"30 5 * * *"`).
   - `plan-month` at `stack.md.content_plan_cron` (default
     `"0 6 1 * *"`).
   `list_scheduled_tasks` first; create only the missing ones via
   `mcp__scheduled-tasks__create_scheduled_task`; never stomp a cron
   the operator already customized.
4. **Confirm** which tasks were created vs already-existed and the
   resolved local times.

### off

1. **Set the flag.** Write `content_autopilot: false` to `stack.md`.
   This is authoritative and immediate: `content-loop` and
   `plan-month` both check `content_autopilot` at the top of their run
   and exit quietly when it's false, so even if a task fires before
   it's removed, it does nothing.
2. **Stop the tasks firing (best effort).** Remove or disable the
   `content-loop` and `plan-month` scheduled tasks so they don't run
   pointlessly — `list_scheduled_tasks`, then
   `mcp__scheduled-tasks__update_scheduled_task` to disable them (or
   delete if the environment supports it). If they can't be
   removed/disabled, that's fine — the flag already makes them no-ops;
   just say so.
3. **Confirm** that autopilot is off and what happened to the tasks.

## What this does NOT do

- It does NOT change the cron *times* — `content_loop_cron` /
  `content_plan_cron` are set via `capture-stack`.
- It does NOT draft, approve, or publish anything. It only flips the
  switch and syncs the scheduled tasks.
- It does NOT touch the approval-notification tasks
  (`approvals-digest`, `approvals-backlog-alert`) — those are always
  on and unrelated to content autopilot.
- It does NOT define the task specs itself — it reuses
  `scaffold-client`'s canonical content-loop / plan-month specs so
  there is a single source of truth.

## Related

- `rockstarr-infra:scaffold-client` — wires these same tasks at
  onboarding (autopilot is on by default); the canonical cron specs
  live there.
- `rockstarr-infra:capture-stack` — sets the cadence and the cron
  times (`content_autopilot`, `content_loop_cron`, `content_plan_cron`).
- `rockstarr-content:content-loop` / `plan-month` — the daily and
  monthly autopilot drivers gated on `content_autopilot`.
