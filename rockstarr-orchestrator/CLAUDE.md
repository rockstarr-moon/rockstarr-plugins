# rockstarr-orchestrator (developer notes)

For what the plugin does and the operator-facing skill list, read
`README.md`. This file is its developer-perspective complement.

## Why this plugin exists

It is the **team lead** for the marketing-team model (see
`_guides/Rockstarr-AI-Marketing-Team-Overview.md` in the dev repo for
the founder-facing vision). The other plugins are specialists; this one
coordinates them toward the client's goals and gives the founder a
single pane. It is the cross-role analog of `rockstarr-ops`, which is
already a pure orchestrator for sales-ops — same pattern, whole-team
scope.

**Core invariant: it orchestrates by dispatching specialists; it never
crosses an audience-facing gate.** The lead does not itself draft, send,
post, publish, or mutate CRM records, and it never approves. From Phase
B it *does* sequence and auto-run the specialists' **AUTO** (internal,
reversible) steps — but the hands-on audience-facing work and every
gate stay with the specialists + humans. If you add a step that
*itself* publishes/sends/approves, that's a bug; if you add a step that
*dispatches a specialist* to do auto-side work, that's the design.

## The autonomy line (the safety contract)

The whole initiative rests on one line:

- **Auto (no gate):** internal, reversible, audience-never-sees-it work
  — audits, strategy/backlog refreshes, ideation, and **drafting to
  `03_drafts/`** (a draft isn't audience-facing).
- **Always gated:** anything audience-facing or irreversible — publish,
  outreach send/connect, social post, email, real-CRM mutation, and
  **approval itself**.

**Phase A was read-only. Phase B lets the lead act on the AUTO side and
STOP at the first GATED step** — see `references/plays/README.md` for
the execution contract every play obeys. `team-report` and
`set-marketing-goals` stay read-only / single-file; the *acting*
happens only through `route-request` / `run-play` running play steps.
The line is enforced per-step in each play (AUTO vs GATED tags).

## Skill groupings (Phase A + B + C)

Six skills:

1. **`set-marketing-goals`** (A) — captures the goals spine
   (`00_intake/marketing-plan.md`). Counterpart to `capture-stack`.
2. **`team-report`** (A) — the read-only single pane. Reads goals +
   registry + each function's outputs; writes one report to
   `06_reports/team/`.
3. **`route-request`** (B) — the founder-facing single pane for *doing*:
   interprets plain-language intent → matches a play (or an ad-hoc plan
   from the registry) → auto-runs AUTO steps, STOPS at the first gate.
4. **`run-play`** (B) — the play-execution engine: runs a named play's
   AUTO steps by dispatching specialists, STOPS at the first GATED step.
5. **`team-tick`** (C) — the *scheduled* proactive planner. The
   self-initiated counterpart to `route-request`: on a weekly cron it
   assesses goals, picks the single biggest gap, runs the matching
   play's AUTO steps via `run-play`, STOPS at the gate, and notifies the
   founder. Opt-in (`team_autopilot`, default off), with backpressure so
   it never floods the queue.
6. **`baseline-audit`** — the run-early "where things stand" snapshot.
   Dispatches specialist discovery across channels (blogs via
   `master-list-blog-audit`; `inventory-linkedin-newsletter`;
   `inventory-social`), each backfilling the canonical publish log, then
   builds the **comprehensive, orchestrator-owned master list**
   (`06_reports/master-list.xlsx`, long-form + social) via its bundled
   `scripts/write_master_list_xlsx.py`, plus a duplicate-awareness
   summary. Read-only discovery + records already-public content =
   AUTO; it publishes/posts nothing. The first plugin script the
   orchestrator owns.

Plus references: `role-registry.md` (the org chart) and `plays/` (the
named play library + the AUTO/GATED execution contract in
`plays/README.md`). All skills read the registry; `route-request`,
`run-play`, and `team-tick` read `plays/`.

The **master list is orchestrator-owned** as of `baseline-audit`: it's a
cross-function inventory (long-form + social), so it belongs to the team
lead, not to one specialist. The publish log (infra) stays canonical;
`master-list.xlsx` is its comprehensive export.
`rockstarr-content:master-list-create` is **deprecated** — it now
redirects here (a thin pointer; builds nothing), so there's one master
list. The discovery skills
(`master-list-blog-audit`, `inventory-linkedin-newsletter`,
`inventory-social`) live in the specialists (channel-crawling is their
domain); the lead only dispatches them and assembles the workbook.

The schedule wiring lives in **`rockstarr-infra`**, not here:
`set-team-autopilot` (the on/off switch), `scaffold-client` (registers
the `team-tick` task when opted in), and `capture-stack`
(`team_autopilot` / `team_tick_cron`). This plugin owns the *skill* the
task invokes; infra owns the *scheduling*, exactly as `content-loop`
(content) is scheduled by infra.

## Where the org model lives

The role registry is **centralized** in `references/role-registry.md`
for Phase A (hand-maintained when a plugin/capability is added). A
later phase may let each plugin self-declare a role manifest so the org
assembles automatically — when that lands, this reference becomes the
schema/aggregation point, not the hand-edited source. Keep the registry
in sync with reality until then; `team-report` trusts its output-path
map.

## Phasing (this plugin's roadmap)

- **Phase A:** role registry + goals spine + read-only team report.
- **Phase B:** founder-facing intent router (`route-request`) + the
  play engine (`run-play`) + the play library (`plays/`, first play
  `seo-geo-engine`). The lead acts on the AUTO side and stops at every
  gate.
- **Phase C (this version):** proactive *scheduled* planning —
  `team-tick` initiates the priority play on a weekly cron rather than
  waiting to be asked. **Additive** (the per-plugin crons are untouched)
  and **opt-in** (`team_autopilot`, default off). Still never crosses a
  gate.

Plays ship incrementally as pure additions to `plays/` (no engine
change): `seo-geo-engine` (Phase B), `content-flywheel`, `pipeline-push`,
`authority-build` — these four now cover all four functions. Further work
(separate tickets): additional/variant plays as needed and, if wanted, a
fuller "lead owns *all* scheduling" model that subsumes the per-plugin
crons. Phase C deliberately did NOT subsume them — it sits on top.

## What's high-risk to change

- **The gate boundary.** Auto-running AUTO steps is the design;
  *crossing a gate* (approve/publish/send/post/real-CRM) is never
  allowed. If a play step or skill ever performs a GATED action, the
  whole safety claim breaks. Keep AUTO/GATED tags honest in every play.
- **`team-report` / `set-marketing-goals` staying non-acting.** Only
  `route-request` / `run-play` act; the other two stay read-only /
  single-file.
- **The role registry's output-path map.** `team-report` + the plays
  depend on it; when a role plugin changes where it writes, update it.
- **Drafting counts as AUTO.** That's deliberate (a draft isn't
  audience-facing) but means plays can generate content automatically —
  keep the cadence/backlog **bounds** in `plays/README.md` enforced so a
  play never floods the queue.

## What's safe to change

- The report's section wording / formatting.
- The goals-plan template + the interview prompts.
- Adding a function/plugin to the registry (additive).

## Versioning

Minor for new skills / new functions in the registry; patch for wording
and report-format fixes; major for changing the autonomy contract or
the orchestration model. Phase B and Phase C are minor feature
additions on top of this 0.1.0 read-only base.

Bump via `/bump rockstarr-orchestrator <version>`.

## Testing

No automated behavior tests (LLM-prompted). Manual against a fixture
workspace:
- `set-marketing-goals` → writes only `marketing-plan.md`.
- `team-report` → reads across all four functions, writes only its
  report, never invokes another skill or approves anything.
- `route-request` "get us ranking" / `run-play seo-geo-engine` → runs
  audit + strategy + bounded drafting (AUTO), then **STOPS** before
  approve/publish; confirm it (a) dispatches the real `rockstarr-content`
  skills, (b) respects the cadence/backlog bound on drafting, (c) never
  approves or publishes even when told to "just do it", (d) reports the
  pending queue + the gated steps.
- `team-tick` → confirm it (a) exits quietly when `team_autopilot` is
  off or no `marketing-plan.md` exists, (b) holds off (report + nudge,
  no new work) when the approval queue is already deep — the
  backpressure check, (c) otherwise picks ONE gap, runs ONE play's AUTO
  steps, STOPS at the gate, and notifies, (d) never approves/publishes.

CI checks skill-name uniqueness + the description/frontmatter guards
only.

## When stuck

Ask Jon in the PR — especially anything that would have the lead *act*
rather than report (that's Phase B/C, gated on its own ticket).
