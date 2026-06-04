---
title: "Plays — the team lead's named cross-role recipes"
purpose: "The library of named plays the orchestrator can run, plus the play schema and the auto-run execution contract that route-request and run-play both follow. A play is a documented, ordered sequence of specialist skills (across one or more functions) with every step tagged AUTO or GATED."
read_by:
  - "rockstarr-orchestrator/run-play (executes a named play)"
  - "rockstarr-orchestrator/route-request (maps intent to a play, then runs it)"
do_not_fork: true
---

# Plays

A **play** is a named, reusable recipe the team lead runs on the
founder's behalf: an ordered list of specialist skills (possibly across
several functions) that together accomplish a goal — "build the SEO/GEO
engine," "push pipeline," "spin the content flywheel."

Plays are how Phase B turns a plain-language request ("get us ranking
for our category") into coordinated specialist work — without the lead
itself doing any drafting, sending, or publishing. The lead
**dispatches** the specialists named in the play; the specialists do
the work.

## The autonomy line — the rule every play obeys

This is the safety contract of the whole orchestrator. Every step in
every play is tagged exactly one of:

- **AUTO** — internal, reversible, audience-never-sees-it. Audits,
  strategy/backlog refreshes, prioritization, ideation, and **drafting
  to `03_drafts/`** (a draft is not audience-facing; the gate is
  approve→publish, not draft). The lead runs these automatically.
- **GATED** — audience-facing or irreversible: publish, outreach
  send/connect, social post/comment, email, real-CRM mutation, and
  **approval itself**. The lead NEVER does these. It stops at the first
  GATED step and hands the decision to a human.

> **The execution contract (both skills follow this):** run AUTO steps
> in order by invoking the named specialist skill for each. At the first
> GATED step, **STOP** — do not run it, do not approve, do not publish.
> Present what ran, what was produced (the pending approval queue), and
> the exact gated step(s) waiting on a human. Acting past a gate is a
> bug, not a feature.

The lead never approves and never crosses a gate even if the founder
says "just do it" — approval and publishing remain human actions. If
the founder wants to approve, point them at the specialist's approval
skill; the lead won't do it for them.

## Bounds (don't run away)

- **Respect cadence + caps.** A play's AUTO drafting is bounded by the
  client's `stack.md` cadence / backlog batch — don't draft an unbounded
  cluster. Default to one batch (or a sane small N) and log what's left.
- **Respect each specialist's own stop-at-gate.** The drafting skills
  already draft to `03_drafts/` and stop; the play relies on that — it
  does not re-implement their work.
- **Honor client status.** A paused/inactive client's plays still only
  produce internal artifacts; nothing audience-facing ever auto-fires.
- **Log every AUTO step** you run (skill + what it produced) so the
  founder sees exactly what happened automatically.

## Play schema

Each play is one markdown file in this directory with front-matter:

```yaml
# ---
play: "[kebab-name, matches filename]"
title: "[human name]"
intent_match: ["phrases the router maps to this play"]
functions: ["which role-registry functions it spans"]
# ---
```

Body: a **Steps** table (order | step | specialist skill | AUTO/GATED |
produces), then **Stop point** (where the first gate is and what awaits
approval), **Preconditions**, and **Notes/bounds**.

## Available plays

| Play | Spans | What it does |
|------|-------|--------------|
| `seo-geo-engine` | Content & SEO | Site audit → SEO/GEO strategy + backlog → bounded cluster drafting to `03_drafts/`. Stops at the publish gate. |

(More plays — Content Flywheel, Pipeline Push, Authority Build — land in
later increments. Add a new play by dropping a file here that follows
the schema and listing it in this table; no skill changes needed.)

## How the two skills use this

- **`run-play`** — given a play name, follows the execution contract
  above for that play's steps.
- **`route-request`** — interprets the founder's plain-language intent,
  matches it to a play via `intent_match` (or composes an ad-hoc plan
  from `../role-registry.md` when no play fits), then runs the matched
  play under the same contract. When nothing fits, it proposes a plan
  and stops — it does not improvise audience-facing actions.
