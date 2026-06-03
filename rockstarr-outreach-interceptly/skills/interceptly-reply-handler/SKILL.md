---
name: interceptly-reply-handler
description: "This skill should be used to handle ONE specific Interceptly reply on demand, when the user says \"respond to this lead\", \"what should I say to [name]\", \"handle this reply\", or \"walk me through this one\". The single-thread companion to process-inbox (which loops the whole unread queue): it locates the named thread and runs the same per-thread pipeline — confirm-session gate, scrape context, qualify-lead, hand off to rockstarr-reply (classify, draft in the client's voice, present-for-approval), then on an authorized 'send it' run send-message + apply-label + create-followup-task (or book-meeting-interceptly). No drafting logic of its own. Real coordinate clicks per the shared chrome-mcp-clicking convention; never pastes the booking URL."
---

# interceptly-reply-handler

Handle one operator-named Interceptly reply end to end, on demand.
This is the **single-thread entry point**; `process-inbox` is the
batch version that walks the whole unread queue. Both run the
**identical per-thread pipeline** — this skill does not re-implement
any of it, it just finds the one thread the operator pointed at and
runs the sequence for that thread.

## What this skill is (and is NOT)

It is a thin orchestrator. The actual work lives in skills it calls:

- ICP qualification → `qualify-lead`
- temperature, drafting in the client's voice, and the
  send-authorization gate → `rockstarr-reply` (`classify-reply` →
  `draft-reply` → `present-for-approval`)
- channel-side execution → `send-message`, `apply-label`,
  `create-followup-task`, `book-meeting-interceptly`,
  `propose-meeting-times-interceptly`

It is **NOT** a place to encode voice rules, banned words, pitch
copy, or ICP definitions. Those are client-specific and live in the
client's `style-guide.md`, `client-profile.md` / `offer.md`, and
`icp-qualifications.md` — `rockstarr-reply` and `qualify-lead` read
them. If you find yourself writing "say it like this" copy in this
skill, stop: it belongs in the client's style guide.

## When to run

- The operator names a specific lead/thread to respond to:
  "respond to this lead", "what should I say to [name]", "draft a
  reply for [name]", "handle this reply", "walk me through this one".
- Distinct from `process-inbox` — that walks every unread oldest-
  first; this handles one named thread without touching the rest of
  the queue.

## Preconditions

Same as `process-inbox`'s per-thread requirements:

- `confirm-session-interceptly` has passed in this run for the
  account that owns the thread. Wrong-account work is a reputational
  incident — if confirm-session failed, refuse.
- `00_intake/icp-qualifications.md`, `style-guide.md`, and the
  account's row in `interceptly-accounts.md` exist.
- `rockstarr-reply` is installed (it owns drafting). If not, refuse
  with a pointer — do not improvise a draft here.

## Workflow

This runs **`process-inbox`'s Steps 1–6 for a single thread.** Do not
restate that logic — follow it. The only differences are how the
thread is located (Step A) and that this skill is operator-driven
(foreground).

### Step A — Locate the named thread

The operator named a lead (name, company, or "this one" referring to
the open conversation). In Interceptly, open that thread:

- If a conversation is already open, use it.
- Otherwise search / filter the inbox for the named lead and open the
  matching thread.
- **Use real coordinate clicks** to open the conversation and any
  controls — per
  `rockstarr-infra/skills/_shared/references/chrome-mcp-clicking.md`.
  Synthetic JS clicks are dropped silently by some browsers (worst on
  Windows; AI-176). Wait for the right panel + thread body to render.

If the named lead is ambiguous (multiple matches) or not found,
surface that to the operator and stop — don't guess which thread.

### Step B — Run the per-thread pipeline

Run exactly the sequence `process-inbox` documents, for this one
thread, in **foreground mode**:

1. **Scrape context** — right panel (name, company, full title, Work
   Experience) + the full thread body. (`process-inbox` Step 2.)
2. **`qualify-lead`** — get the `icp_verdict` + matching rule.
   `qualify-lead` now includes the mandatory company-website research
   step, so a thin title is no longer enough to conclude fit.
3. **Build the handoff bundle and call `rockstarr-reply`** — the
   channel-agnostic bundle shape is the one in `process-inbox`
   Step 4. `rockstarr-reply` runs `classify-reply` → `draft-reply` →
   `present-for-approval`. Drafting voice comes from the client's
   style guide; the temperature buckets, the Warm-non-ICP three-option
   present, and the "send it" gate are all owned there.
4. **Execute the returned bundle** — `process-inbox` Step 6:
   `authorized-send` → `send-message` + `apply-label` +
   `create-followup-task`; `label-only` / `no-action` → `apply-label`;
   `flag` → flag label + review task; `book-meeting-handoff` →
   `book-meeting-interceptly`.

### Step C — Booking, if it comes up

If the thread reaches "yes, when?", use
`propose-meeting-times-interceptly` — it checks the booking source
and proposes specific times. **Never paste the booking URL into a
DM** (the standing rule; `rockstarr-reply` and the booking skills
enforce it).

## The send gate (non-negotiable)

Nothing sends without the operator's explicit "send it" (or a clear
equivalent) through `rockstarr-reply:present-for-approval`. Content
edits ("make it shorter", "different angle") trigger a redraft, never
a send. This skill never interprets a message as authorization — it
only executes an `authorized-send` bundle rockstarr-reply returns.
When in doubt, present and wait.

## What NOT to do

- Do NOT draft, classify, or define voice/ICP here — those are
  `rockstarr-reply` / `qualify-lead` / the client's intake files.
- Do NOT walk the whole inbox — that's `process-inbox`. This skill is
  one named thread.
- Do NOT use synthetic JS clicks on gated controls — real coordinate
  clicks only (shared convention).
- Do NOT paste the booking URL into a reply.
- Do NOT send without an `authorized-send` bundle from
  `present-for-approval`.

## Related

- `rockstarr-outreach-interceptly:process-inbox` — the batch version;
  this skill reuses its Steps 1–6.
- `rockstarr-reply` (`classify-reply` / `draft-reply` /
  `present-for-approval`) — owns temperature, drafting, and the gate.
- `rockstarr-outreach-interceptly:qualify-lead` — ICP verdict,
  including the company-website research step.
- `rockstarr-outreach-interceptly:create-followup-task` — closes any
  stale prior task before creating the fresh one.
- `rockstarr-infra/skills/_shared/references/chrome-mcp-clicking.md` —
  real-click convention.
