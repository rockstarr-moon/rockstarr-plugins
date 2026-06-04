---
name: run-play
description: "This skill should be used when the user names a cross-role play to run — e.g. \"run the SEO/GEO engine\", \"run the seo-geo-engine play\", \"kick off the SEO engine\", or \"run a play\". It is the team lead's play-execution engine: it reads the named play from references/plays/, runs the AUTO (internal, reversible) steps in order by dispatching each specialist skill, and STOPS at the first GATED (audience-facing) step — it never approves, publishes, sends, or posts. It then reports what ran, the drafts now awaiting approval, and the exact gated steps left for a human. For interpreting a plain-language goal into a play, use route-request instead."
---

# run-play

The team lead's **play engine**. Given a named play, run its internal,
reversible steps automatically and hand the audience-facing decisions
back to a human. The lead orchestrates the specialists named in the
play; it does not do drafting/sending/publishing itself.

> **The autonomy line is the whole point.** Read
> `references/plays/README.md` first — it defines AUTO vs GATED and the
> execution contract. Run AUTO steps; **STOP at the first GATED step.**
> Never approve, publish, send, post, or mutate a real CRM record —
> not even if the user says "just do it." Those stay human actions.

## When to run

- The user names a play: "run the SEO/GEO engine", "run the
  `seo-geo-engine` play", "kick off the SEO engine".
- If the user describes a *goal* instead of naming a play ("get us
  ranking"), that's `route-request` — it maps intent to a play, then
  uses this engine.

## Inputs

- The play file: `references/plays/[play].md`. If the named play doesn't
  exist, list the available plays (from `references/plays/README.md`)
  and stop.
- `references/role-registry.md` — to resolve which function/plugin owns
  each step and where its output lives.
- `00_intake/marketing-plan.md` (if present) — the goal the play serves;
  reference it in the summary.
- The play's own **Preconditions** — check them; if unmet (e.g. no
  approved style guide, cadence 0), do the AUTO planning steps but
  honor the play's guidance on what to skip, and say why.

## How to run a play

1. **Read the play** and restate the plan to the founder up front: the
   ordered steps, which are AUTO, and exactly where it will STOP (the
   first GATED step). One short paragraph — no need to ask permission to
   run the AUTO steps; that's what a play is.
2. **Run each AUTO step in order** by invoking the named specialist
   skill (e.g. `rockstarr-content:seo-site-audit`). Let each specialist
   do its own work and honor its own stop-at-gate. After each, **log**
   the skill and what it produced (the file paths).
3. **Respect the bounds** in `references/plays/README.md` and the play:
   cadence/backlog caps on drafting, "don't re-audit if a recent audit
   exists," client status. Never exceed one batch of drafting unless the
   play says otherwise.
4. **At the first GATED step, STOP.** Do not run it. Do not approve or
   publish on the founder's behalf.

## Output / report

Don't write a new orchestrator file — the specialists write their own
outputs. Report in chat (and you may append a short run note to the
latest `06_reports/team/` report if one exists, but do not create new
artifacts otherwise):

- **Ran (AUTO):** each step + what it produced (paths).
- **Awaiting your approval (GATED):** the drafts/items now in
  `03_drafts/` and the exact gated steps (approve, publish) left for a
  human — with how to do each (the specialist's approval/publish skill).
- **State + next:** remaining backlog/queue counts; whether the relevant
  autopilot will continue the work on cadence; any precondition that
  caused a step to be skipped.

## What NOT to do

- Do NOT run a GATED step. No approving, publishing, sending, posting,
  or real-CRM mutation — ever, regardless of user phrasing.
- Do NOT exceed the play's AUTO bounds (cadence/backlog caps).
- Do NOT re-implement specialist work; dispatch the named skill.
- Do NOT invent a play that isn't in `references/plays/`. Offer the
  available ones instead.

## Related

- `references/plays/README.md` — AUTO/GATED + the execution contract.
- `references/plays/seo-geo-engine.md` — the first play.
- `rockstarr-orchestrator/route-request` — maps plain-language intent to
  a play, then uses this engine.
- `references/role-registry.md` — function → plugin → output-path map.
