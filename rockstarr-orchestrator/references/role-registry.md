---
title: "Marketing-team role registry (the org chart)"
purpose: "The canonical map of the Rockstarr AI marketing team: the four named functions, which plugins compose each, what each owns, where its work lives in the client workspace, and the cross-role handoffs. The orchestrator's skills read this to know what to roll up and how the team fits together."
read_by:
  - "rockstarr-orchestrator/team-report (what to scan per function)"
  - "rockstarr-orchestrator/set-marketing-goals (the outcome areas to set goals against)"
do_not_fork: true
---

# Marketing-team role registry

The org chart for the Rockstarr AI marketing team. A **Team Lead**
(this plugin, `rockstarr-orchestrator`) coordinates four **functions**.
Each function is made of one or more plugins. The Team Lead does no
hands-on work itself — it reads this registry to understand the team
and to roll up what each function has done.

> **Phase A note.** This registry is **centralized** here for now.
> Later phases may have each plugin declare its own role manifest so
> the org self-assembles; until then, this file is the source of truth
> and is updated by hand when a plugin or capability is added.

## The autonomy line (applies to the whole team)

- **Auto (no gate):** internal, reversible, audience-never-sees-it work
  — audits, backlog/report refreshes, prioritization, ideation and
  planning that only *propose*.
- **Always gated (human approves):** anything audience-facing or
  irreversible — publish, outreach send/connect, social post/comment,
  email, real-CRM mutation.

As of **Phase B**, the lead **acts on the AUTO side**: `route-request`
and `run-play` auto-run the internal, reversible steps of a play and
**STOP at the first GATED step**. **Phase C** adds `team-tick` — the
same auto-run-and-stop behavior on a weekly schedule (opt-in), with
backpressure so it never floods the queue. In every case the lead never
approves, publishes, sends, posts, or mutates a real CRM record.
`team-report` and `set-marketing-goals` remain read-only / single-file.
See `plays/README.md` for the execution contract.

## The Team Lead

- **Plugin:** `rockstarr-orchestrator`
- **Owns:** the goals spine (`00_intake/marketing-plan.md`), the
  cross-role view, the founder's single pane, and the play library
  (`plays/`).
- **Skills:** `set-marketing-goals` (capture/refresh goals),
  `team-report` (read-only unified status), `route-request`
  (plain-language single pane → play), `run-play` (execute a named
  play), `team-tick` (the scheduled proactive weekly planner — Phase C).
- **DOES (Phase B+C):** interpret intent (on request) or assess goals
  (on a weekly schedule), sequence specialists, and auto-run the AUTO
  (internal, reversible) steps of a play. The schedule is additive and
  **opt-in** (`team_autopilot`, default off).
- **Does NOT:** approve, publish, send, post, or mutate a real CRM
  record — it STOPS at every audience-facing gate. It dispatches
  specialists; it never does their hands-on audience-facing work itself.

## Function 1 — Content & SEO

- **Plugins:** `rockstarr-content`
- **Owns:** SEO/GEO strategy + site audits; long-form drafting (blog,
  thought leadership, newsletters, case studies); the content master
  list; the content autopilot (`plan-month`, `content-loop`).
- **Outcome area:** organic visibility + AI-search citation
  (SEO/GEO), content authority.
- **Where its work lives (for roll-up):**
  - `02_inputs/seo/strategy_*.md`, `02_inputs/seo/backlog.md`,
    `02_inputs/seo/audit_*.md`, `audit_state.md`
  - `02_inputs/content-topics_*.md`, `02_inputs/content-calendar_*.md`
  - `03_drafts/content/` (pending drafts + outlines)
  - `05_published/_publish.log` + `05_published/blog|email|...`
  - `06_reports/master-list-of-content.xlsx`
- **Key handoffs:** approved long-form → Brand & Social (repurpose,
  LinkedIn newsletter) and → Demand Gen (proof assets for outreach/reply).

## Function 2 — Brand & Social

- **Plugins:** `rockstarr-social` (+ the content→LinkedIn-newsletter
  authority handoff)
- **Owns:** short-form social, weekly batches, LinkedIn presence +
  engagement (polls, page-invite, comment-check), Publer export.
- **Outcome area:** brand authority + engagement.
- **Where its work lives:**
  - `03_drafts/social/` (weekly batches + per-post drafts)
  - `05_published/social*`
  - the polls / engagement artifacts under `02_inputs/`/`06_reports/`
- **Key handoffs:** consumes approved content (repurpose source);
  surfaces engagement signals back to the lead.

## Function 3 — Demand Gen

- **Plugins:** `rockstarr-outreach-interceptly` OR
  `rockstarr-outreach-salesnav`, plus `rockstarr-reply` and
  `rockstarr-ops`
- **Owns:** prospecting (connects + sequences), reply handling +
  approval, meeting booking, sales-call prep, post-call ops.
- **Outcome area:** qualified leads + booked meetings (pipeline).
- **Where its work lives:**
  - `02_inputs/outreach/outreach-tasks.xlsx` (salesnav, state-of-truth)
    or `outreach-mirror.xlsx` (interceptly, audit mirror)
  - `02_inputs/replies/` (`_flags.md`), `03_drafts/replies/`
  - `05_published/outreach/`, `06_reports/` outreach weekly metrics
  - ops call-prep / agenda artifacts under `02_inputs/`/`06_reports/`
- **Key handoffs:** inbound reply → `rockstarr-reply`; booked call →
  `rockstarr-ops` prep → CRM.

## Function 4 — RevOps & Foundation

- **Plugins:** `rockstarr-crm` (when the client is on The Growth
  Amplifier) + `rockstarr-infra`
- **Owns:** the CRM/pipeline data; onboarding + the client's voice and
  knowledge base; the approve / publish-log lifecycle; the email
  notification layer; scheduled-task wiring.
- **Outcome area:** clean data + the rails the rest of the team runs on.
- **Where its work lives:**
  - `00_intake/` (client-profile, style-guide, stack, marketing-plan)
  - `04_approved/_approvals.log`, `05_published/_publish.log`
  - `01_knowledge_base/` (index + processed)
  - `_errors.md` anywhere (incident signal)
- **Key handoffs:** owns `approve` + `publish-log` that every function
  routes through; CRM records the pipeline Demand Gen creates.

## How the team grows

A new plugin or capability **joins an existing function or forms a new
one**. For now, add it to this registry by hand (its function, what it
owns, its output paths, its handoffs). A later phase will let plugins
self-declare so the org assembles automatically.
