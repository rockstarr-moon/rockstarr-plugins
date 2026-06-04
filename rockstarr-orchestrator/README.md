# Rockstarr Orchestrator (the team lead)

The marketing-team **team lead**. The other Rockstarr plugins are
specialists (content, social, outreach, reply, ops, crm, infra); this
one coordinates them toward the client's goals and gives the founder a
**single pane**. It coordinates and reports — it never drafts, sends,
publishes, or approves. Humans gate every audience-facing action.

For the full vision and the org chart in plain language, see
`_guides/Rockstarr-AI-Marketing-Team-Overview.md`.

## At a glance (Phase A)

- **Role registry** — `references/role-registry.md` maps the four
  functions (Content & SEO, Brand & Social, Demand Gen, RevOps &
  Foundation) to the plugins that compose them, what each owns, where
  its work lives, and the cross-role handoffs.
- **Goals spine** — `set-marketing-goals` captures
  `00_intake/marketing-plan.md`: the objectives + targets the team works
  toward (SEO/GEO, demand gen, brand/authority) plus priorities and
  constraints.
- **Single pane** — `team-report` reads the goals + every function's
  workspace outputs and produces one unified, **read-only** status:
  activity per function, the consolidated approval queue, progress vs
  goals, and flags.

**Phase A is read-only.** Nothing here executes, drafts, sends,
publishes, or approves. It makes the team *visible* without changing how
it works.

## Skills

| Skill | Purpose |
|-------|---------|
| `set-marketing-goals` | Capture / refresh the goals spine (`00_intake/marketing-plan.md`) — objectives + targets for SEO/GEO, demand gen, brand/authority, plus priorities and constraints. Strategic counterpart to `capture-stack`. Writes only that file. |
| `team-report` | The team lead's single pane. Reads the goals + the role registry + each function's outputs; writes one report to `06_reports/team/` (activity per function, consolidated approval queue, progress vs goals, flags, advisory next moves). Strictly read-only. |

## The autonomy line

The whole marketing-team model rests on one boundary:

- **Auto (no gate):** internal, reversible, audience-never-sees-it work.
- **Always gated:** anything audience-facing or irreversible (publish,
  outreach send, social post, email, real-CRM change).

Phase A sits entirely on the safe side — it only reads and reports.
Later phases let the lead *act* on the auto side, never across the line.

## How to use it

- **At onboarding:** run `set-marketing-goals` after the profile + stack
  are captured, so the team has goals to work toward.
- **Anytime:** "how's the team doing?" / "team report" / "what's waiting
  on me?" runs `team-report`.

## Roadmap

- **Phase A (this release):** role registry + goals spine + read-only
  team report.
- **Phase B:** founder-facing intent router ("grow my pipeline") + named
  cross-role plays (content flywheel, pipeline push, authority build,
  SEO/GEO engine).
- **Phase C:** proactive scheduled planning, the lead owning the per-role
  schedule, and acting on the auto side of the autonomy line.

## Install / rollout

New plugin. Registering it in the marketplace and adding it to clients'
`allowed_plugins` is a separate publish/rollout step (same flow as every
other plugin). It reads the client workspace produced by
`rockstarr-infra`; install that first.
