---
name: route-request
description: "This skill should be used when the founder talks to the marketing team in plain language and wants the team lead to act on it — e.g. \"grow my pipeline\", \"get us ranking\", \"we need more authority\", \"what should the team do this week\", or \"handle our marketing this month\". The single-pane entry to the orchestrator: it interprets the intent, maps it to a named play (references/plays/) or composes an ad-hoc plan from the role registry, then AUTO-RUNS the internal, reversible steps up to the first audience-facing gate and STOPS — it never approves, publishes, sends, or posts. To run a play by name instead, use run-play; for a status read-out, use team-report."
---

# route-request

The founder's **single pane** for *doing* — "talk to the lead." Say
what you want in plain language; the team lead figures out which
function(s) it touches, picks the right play, runs the safe internal
steps automatically, and stops at the first thing that needs your
approval.

> **Autonomy line (read `references/plays/README.md`).** The lead
> auto-runs AUTO (internal, reversible, audience-never-sees-it) steps
> and **STOPS at the first GATED (audience-facing) step.** It never
> approves, publishes, sends, posts, or mutates a real CRM record — even
> if you say "just do it." Those stay your decisions.

## When to run

- The founder expresses a goal or asks the team to act: "grow my
  pipeline", "get us ranking", "build our authority", "what should we do
  this week?", "handle content this month".
- For a pure status read-out ("how's the team doing?"), use
  `team-report`. For "run the X play" by name, use `run-play`.

## How to route

1. **Read the map.** `references/role-registry.md` (functions →
   plugins → outputs), `references/plays/README.md` + the play files
   (`intent_match`), and `00_intake/marketing-plan.md` if present (the
   goals to serve).
2. **Interpret the intent** and match it:
   - **A play fits** (intent matches a play's `intent_match`, e.g. "get
     us ranking" → `seo-geo-engine`): confirm the match in one line,
     then run it via the **`run-play`** contract (AUTO steps in order,
     STOP at the first GATED step). Available plays are listed in
     `references/plays/README.md` (`seo-geo-engine`, `content-flywheel`,
     `pipeline-push`, `authority-build`).
   - **A foundational orchestrator skill fits** — route "where do we
     stand / what content already exists / build our master list" to
     `baseline-audit`; "set/update our goals" to `set-marketing-goals`;
     "how's the team doing" to `team-report`; "what do I need to approve
     / show my approval queue / walk me through approvals" to
     `rockstarr-infra:review-queue`. (For a brand-new client,
     `baseline-audit` is usually the right first move — and if no
     `06_reports/master-list.xlsx` exists yet, suggest it.)
   - **No play fits, but the request maps cleanly to function work**
     (e.g. "draft this week's posts"): compose a short ad-hoc plan from
     the role registry — list the specialist skills, tag each AUTO or
     GATED — then run the AUTO steps and STOP at the first gate, same
     contract. Keep ad-hoc plans tight; don't sprawl across functions.
   - **Ambiguous or out of scope:** don't guess. Lay out the options
     ("this could mean A or B"), or say what the team can/can't do, and
     ask one clarifying question. Never improvise an audience-facing
     action to resolve ambiguity.
3. **Honor all bounds** from `references/plays/README.md`: cadence/
   backlog caps, client status, "don't re-audit if recent," and the
   absolute STOP at the first gate.

## Output / report

Lead with the interpretation ("I read this as: build the SEO/GEO
engine"), then report exactly as `run-play` does:

- **Plan:** the steps, AUTO vs GATED, and where it stops.
- **Ran (AUTO):** each step + what it produced (paths).
- **Awaiting your approval (GATED):** the pending drafts/items + the
  gated steps left for you, and how to do each.
- **Next:** remaining queue/backlog; whether an autopilot continues it.

Do not create new orchestrator artifacts; the specialists write their
own outputs. (A short run note appended to the latest `06_reports/team/`
report is fine; new files are not.)

## What NOT to do

- Do NOT run a GATED step — no approving, publishing, sending, posting,
  or real-CRM mutation, regardless of phrasing.
- Do NOT improvise audience-facing actions to resolve ambiguity — ask.
- Do NOT exceed AUTO bounds (cadence/backlog caps).
- Do NOT re-implement specialist work; dispatch the named skills.

## Related

- `rockstarr-orchestrator/run-play` — the play-execution engine this
  delegates to once a play is matched.
- `references/plays/README.md` — AUTO/GATED + the execution contract.
- `references/role-registry.md` — the function → plugin → output map.
- `rockstarr-orchestrator/team-report` — the read-only status pane (the
  companion to this "do something" entry).
