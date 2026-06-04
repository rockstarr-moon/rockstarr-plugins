---
name: review-queue
description: "This skill should be used when the operator wants to find, preview, and act on the documents waiting for their approval — e.g. \"what do I need to approve\", \"show my approval queue\", \"review my approvals\", or \"walk me through approvals\". It scans 03_drafts/ for pending items (the approval_status: pending contract approvals-digest uses) and either (list mode) renders a channel-grouped queue where each item carries a claude://cowork/new deep-link that opens a focused task previewing the draft with approve / edit / send-back, or (guided mode) walks the operator through each pending doc one at a time. It approves only on explicit per-item confirmation via rockstarr-infra:approve; it never auto-approves, drafts, or publishes."
---

# review-queue

The operator's on-demand way to **find what needs approving, preview
it, and clear it** — without hunting through the workspace. It's the
interactive, in-app counterpart to the daily `approvals-digest` email
and the orchestrator's read-only `team-report` queue.

> **What "preview" means here.** Cowork has no separate preview pane a
> plugin can open. The preview is the agent **rendering the draft inline
> in the conversation** — opened in a focused task and shown formatted,
> with the approve action one message away. The deep-links below open
> exactly that.

## When to run

- On demand: "what do I need to approve?", "show my approval queue",
  "review my approvals", "walk me through approvals".
- Often the next step after `team-report` or the daily digest says
  there are pending items.

## Preconditions (Tier 1, cheap)

- `/rockstarr-ai/03_drafts/` exists. If not, say there's nothing staged
  to approve yet and stop.

## What it scans

The **pending queue**: every file under `03_drafts/**` whose
front-matter carries `approval_status: pending` — the exact contract
`approvals-digest` scans (`approval_status`, `awaiting_approval_since`,
`bot`, `lane`). For each, derive the same **plain-English channel label**
and **one-line context sentence** that `approvals-digest` uses (see its
"Channel label conventions" + "Per-item context line" — reuse them, do
not invent new wording). Sort most-recent-first within each channel
group. Operator-facing voice throughout (`_shared/references/client-facing-output-voice.md`).

## Mode 1 — List (default)

Render the queue as a tidy, channel-grouped list. Each item:

- the channel label + title,
- the one-line context sentence,
- a **deep-link** that opens a focused review task — the **same
  `claude://cowork/new?q=...` link shape `approvals-digest` emits**
  (single source of truth for the link; if that prompt changes, both
  follow it). The opened task previews the draft and offers approve /
  edit / send-back.

End with the count and an offer: "Want me to walk you through them now?"
(→ Mode 2).

## Mode 2 — Guided ("walk me through")

Inbox-zero. For each pending item, oldest-first:

1. **Preview** — read the draft and render it **formatted, inline** (the
   prose as the operator will see it). Lead with the channel label +
   title; keep internal QA fields (stop-slop score, `produced_by`,
   paths) out of the preview body unless asked.
2. **Decide** — ask for one of:
   - **Approve** → call `rockstarr-infra:approve` for that file (promotes
     `03_drafts/` → `04_approved/` with the approval stamp). Only on
     explicit confirmation for THIS item.
   - **Edit** → capture the requested change, apply it to the draft (or
     route to the owning skill), leave it `pending`, and move on.
   - **Send back** → leave it `pending`, note why, move on.
3. **Next** — proceed to the following item.

At the end, summarize: how many approved, edited, left pending, and
what's still waiting.

## What NOT to do

- Do NOT auto-approve. Approval is per-item and explicit — never "approve
  all" without the operator confirming each (the same guard that keeps
  the email link from punching an auto-approve hole).
- Do NOT draft, send, post, or publish. Approving promotes to
  `04_approved/`; publishing is a separate, later, human step.
- Do NOT expose internal QA/debug fields in the preview unless asked.
- Do NOT invent new channel labels or context wording — reuse
  `approvals-digest`'s.

## Related

- `rockstarr-infra:approvals-digest` — the scheduled daily email version
  (owns the canonical channel labels, context lines, and deep-link
  shape this skill reuses).
- `rockstarr-infra:approvals-backlog-alert` — the weekly strategist
  escalation when the queue gets deep.
- `rockstarr-infra:approve` — the promotion this skill calls on approval.
- `rockstarr-orchestrator:team-report` — the cross-function single pane;
  it surfaces the same queue read-only and points here to act on it.
