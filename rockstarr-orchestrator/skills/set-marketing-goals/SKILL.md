---
name: set-marketing-goals
description: "This skill should be used when the user wants to set or update the marketing goals the team works toward, or when onboarding a client — e.g. \"set our marketing goals\", \"what are we optimizing for\", \"update the marketing plan\", \"set this quarter's targets\", or \"refresh our OKRs\". It captures a short marketing plan (objectives + targets for SEO/GEO, demand gen, and brand/authority, plus priorities and constraints) into 00_intake/marketing-plan.md — the goals spine the orchestrator's team-report and (later) the team lead's planning read. It only writes that one file; it never drafts, sends, publishes, or runs other plugins."
---

# set-marketing-goals

Capture the goals the marketing team works toward. This is the **goals
spine** — the single artifact that says what success looks like for
this client, so the team lead can prioritize and the team report can
measure against it.

Set it at onboarding and refresh it quarterly (or when priorities
shift). It is the strategic counterpart to `stack.md` (which says what
the client *publishes*) — this says what the client is *trying to
achieve*.

## When to run

- Onboarding, after the profile + stack are captured.
- Quarterly, or when the founder's priorities change.
- Trigger phrases: "set our marketing goals", "update the marketing
  plan", "what are we optimizing for", "set this quarter's targets".

## Preconditions

- `/rockstarr-ai/00_intake/client-profile.md` exists (the goals should
  fit the business — read it for context). If it doesn't, point the
  user at onboarding first.

## Inputs

Read `client-profile.md` for context (positioning, ICP, offers), and
`stack.md` for the lanes the client actually runs (don't set a content
goal for a client with `blogs_per_month: 0`). Then interview the user
one area at a time — keep it short; a good plan is a page, not a
binder.

## The outcome areas

Capture an objective + a few concrete targets for each area the client
is active in. Skip an area cleanly if it doesn't apply.

- **SEO / GEO** — organic visibility and AI-search citation. (e.g.
  "rank top-3 for [cluster] terms," "get cited by AI answers for
  [topic]," "N quality blogs/quarter toward the cluster plan.")
- **Demand Gen** — leads and booked meetings. (e.g. "N booked calls /
  month from outreach," "reply-to-meeting rate," "ICP focus.")
- **Brand / Authority** — presence and engagement. (e.g. "publish N
  thought-leadership pieces / month," "grow LinkedIn engagement,"
  "establish a POV on [theme].")
- **Priorities** — if you could only move one thing this quarter, what
  is it? Rank the areas so the lead knows the trade-offs.
- **Constraints / do-nots** — topics to avoid, competitors not to
  name, channels off-limits, pace limits.

Push gently for *specific, checkable* targets, but accept directional
goals — this is a compass for the lead, not a contract. Don't invent
numbers the founder didn't give; mark a target `[TBD]` if they want to
set it later.

## Output

Write `/rockstarr-ai/00_intake/marketing-plan.md`. If one exists,
archive the prior version to `99_archive/` (keep the history) and write
the new one. Front-matter:

```yaml
# ---
client_id: "[from client.toml]"
set_at: "[ISO timestamp]"
set_by: "[founder | strategist]"
horizon: "[e.g. Q3 2026]"
review_cadence: "quarterly"
produced_by: "rockstarr-orchestrator/set-marketing-goals@0.1.0"
# ---
```

(Emit real `---`, not `# ---`, in the file.)

Body: one short section per active outcome area (objective + targets),
then **Priorities** (ranked) and **Constraints**. Keep it to ~a page.

After writing, summarize the plan in chat and note that `team-report`
will measure the team's activity against it.

## What NOT to do

- Do NOT draft, send, publish, or run other plugins. This skill only
  writes the goals file.
- Do NOT set goals for lanes the client doesn't run (cadence 0 in
  stack.md).
- Do NOT invent targets the founder didn't provide — use `[TBD]`.
- Do NOT overwrite the prior plan without archiving it.

## Related

- `rockstarr-orchestrator/team-report` — reads this plan to report
  progress vs goals.
- `references/role-registry.md` — the outcome areas map to the team's
  functions.
- `rockstarr-infra:capture-stack` — the companion that captures what
  the client publishes (cadence), vs this skill's what-they-want-to-achieve.
