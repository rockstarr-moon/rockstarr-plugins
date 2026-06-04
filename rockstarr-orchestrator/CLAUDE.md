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

**Core invariant: it orchestrates, it does not perform.** It never
drafts, sends, posts, publishes, or mutates CRM records, and it never
approves. Those are the specialists' skills (gated by humans). If you
find yourself adding a "do the work" step here, it belongs in the role
plugin, not the lead.

## The autonomy line (the safety contract)

The whole initiative rests on one line:

- **Auto (no gate):** internal, reversible, audience-never-sees-it work.
- **Always gated:** anything audience-facing or irreversible.

**Phase A enforces the strong form: read-only.** `team-report` only
reads + summarizes; `set-marketing-goals` only writes the one goals
file. Nothing executes. Later phases will let the lead *act* on the
"auto" side of the line — but never cross it.

## Skill groupings (Phase A)

Two skills today:

1. **`set-marketing-goals`** — captures the goals spine
   (`00_intake/marketing-plan.md`). The strategic counterpart to
   `capture-stack` (which captures cadence).
2. **`team-report`** — the read-only single pane. Reads the goals + the
   role registry + each function's workspace outputs; writes one report
   to `06_reports/team/`.

Plus `references/role-registry.md` — the org chart: functions →
plugins → owned outcomes → output paths → handoffs. Both skills read it.

## Where the org model lives

The role registry is **centralized** in `references/role-registry.md`
for Phase A (hand-maintained when a plugin/capability is added). A
later phase may let each plugin self-declare a role manifest so the org
assembles automatically — when that lands, this reference becomes the
schema/aggregation point, not the hand-edited source. Keep the registry
in sync with reality until then; `team-report` trusts its output-path
map.

## Phasing (this plugin's roadmap)

- **Phase A (this version):** role registry + goals spine + read-only
  team report. No behavior change to other plugins; nothing executes.
- **Phase B:** founder-facing intent router + named cross-role plays.
- **Phase C:** proactive scheduled planning, the lead owning the
  per-role schedule (today wired by `scaffold-client`), and acting on
  the "auto" side of the autonomy line.

Don't pull Phase B/C behavior forward without the matching ticket —
the read-only guarantee is what makes Phase A safe to ship.

## What's high-risk to change

- **The read-only guarantee.** If `team-report` ever writes outside its
  report file or invokes another skill, Phase A's safety claim breaks.
- **The autonomy line.** Any future execution must classify every
  action as auto vs gated and never auto-cross into audience-facing.
- **The role registry's output-path map.** `team-report` depends on it;
  when a role plugin changes where it writes, update the registry.

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

No automated behavior tests (LLM-prompted). Manual: sideload, run
`set-marketing-goals` against a fixture workspace, then `team-report`
and confirm it (a) reads across all four functions, (b) writes only the
report, (c) never invokes another skill or approves anything. CI checks
skill-name uniqueness + the description/frontmatter guards only.

## When stuck

Ask Jon in the PR — especially anything that would have the lead *act*
rather than report (that's Phase B/C, gated on its own ticket).
