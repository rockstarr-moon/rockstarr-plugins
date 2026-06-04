# Rockstarr Orchestrator (the team lead)

The marketing-team **team lead**. The other Rockstarr plugins are
specialists (content, social, outreach, reply, ops, crm, infra); this
one coordinates them toward the client's goals and gives the founder a
**single pane**. Talk to it in plain language — it interprets what you
want, sequences the right specialists, runs the safe internal steps for
you, and stops at anything that needs your approval. It never publishes,
sends, posts, or approves; **humans gate every audience-facing action.**

For the full vision and the org chart in plain language, see
`_guides/Rockstarr-AI-Marketing-Team-Overview.md`.

## At a glance

- **Talk to the lead** — `route-request`: say "get us ranking" / "grow
  my pipeline" / "what should we do this week?" The lead maps it to a
  named play, runs the internal steps, and stops at the first gate.
- **Named plays** — `references/plays/`: reusable cross-role recipes.
  First play: **SEO/GEO Engine** (audit → strategy/backlog → cluster
  drafting). `run-play` executes one by name.
- **Goals spine** — `set-marketing-goals` captures
  `00_intake/marketing-plan.md`: objectives + targets (SEO/GEO, demand
  gen, brand/authority) plus priorities and constraints.
- **Single pane (read-only)** — `team-report` reads the goals + every
  function's outputs and produces one status: activity per function, the
  consolidated approval queue, progress vs goals, and flags.
- **Role registry** — `references/role-registry.md` maps the four
  functions (Content & SEO, Brand & Social, Demand Gen, RevOps &
  Foundation) to the plugins that compose them, what each owns, where its
  work lives, and the cross-role handoffs.

## Skills

| Skill | Purpose |
|-------|---------|
| `route-request` | The single-pane entry for *doing*. Interprets plain-language intent → matches a named play (or an ad-hoc plan from the role registry) → auto-runs the internal/reversible steps → **stops at the first audience-facing gate.** Never approves/publishes/sends/posts. |
| `run-play` | The play-execution engine. Runs a named play's AUTO steps by dispatching the specialist skills, then stops at the first GATED step. Use when you name a play ("run the SEO/GEO engine"). |
| `team-tick` | The *scheduled* proactive planner (opt-in, weekly). Self-initiated counterpart to `route-request`: assesses goals, picks the biggest gap, auto-runs the matching play's safe steps, stops at the gate, and notifies you. Holds off when your queue is already deep. Off by default — enable via `rockstarr-infra:set-team-autopilot`. |
| `set-marketing-goals` | Capture / refresh the goals spine (`00_intake/marketing-plan.md`). Strategic counterpart to `capture-stack`. Writes only that file. |
| `team-report` | The read-only single pane. Reads goals + role registry + each function's outputs; writes one report to `06_reports/team/`. Strictly read-only. |

## The autonomy line

The whole marketing-team model rests on one boundary:

- **Auto (no gate):** internal, reversible, audience-never-sees-it work
  — audits, strategy/backlog, ideation, and drafting to `03_drafts/`.
- **Always gated:** anything audience-facing or irreversible (publish,
  outreach send, social post, email, real-CRM change) and approval
  itself.

The lead **auto-runs the auto side and stops at the first gate.** It
never crosses the line — not even if you say "just do it." Approving and
publishing stay your decisions.

## How to use it

- **At onboarding:** run `set-marketing-goals` after the profile + stack
  are captured, so the team has goals to work toward.
- **To get things moving:** "get us ranking" / "grow my pipeline" runs
  `route-request`; "run the SEO/GEO engine" runs `run-play`. The lead
  does the internal work and leaves the approvals for you.
- **For status:** "how's the team doing?" / "what's waiting on me?" runs
  `team-report`.
- **Hands-off (optional):** turn on the weekly planner — "turn on team
  autopilot" (via `rockstarr-infra:set-team-autopilot`). Each week the
  lead works the highest-priority goal gap and leaves the approvals
  waiting for you. Off by default.

## Roadmap

- **Phase A:** role registry + goals spine + read-only team report.
- **Phase B:** founder-facing intent router (`route-request`) + the play
  engine (`run-play`) + the play library (first play: **SEO/GEO
  Engine**). The lead acts on the auto side, on request, and stops at
  every gate.
- **Phase C (this release):** proactive *scheduled* planning —
  `team-tick` runs the priority play weekly (opt-in, additive to the
  per-plugin crons), stops at the gate, and notifies you. Still never
  crosses a gate.
- **Next:** more plays (Content Flywheel, Pipeline Push, Authority
  Build).

## Install / rollout

New plugin. Registering it in the marketplace and adding it to clients'
`allowed_plugins` is a separate publish/rollout step (same flow as every
other plugin). It reads the client workspace produced by
`rockstarr-infra`; install that first.
