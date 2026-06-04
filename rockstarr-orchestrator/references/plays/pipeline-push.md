---
play: "pipeline-push"
title: "Pipeline Push"
intent_match:
  - "grow my pipeline"
  - "push pipeline"
  - "fill my pipeline"
  - "get more meetings"
  - "book more calls"
  - "more leads"
  - "run outreach"
  - "work our outreach"
functions:
  - "Demand Gen"
---

# Play: Pipeline Push

Move the demand-gen engine forward in one coordinated pass: sharpen who
we're targeting, draft the campaign, stage the next outreach batch, get
any waiting replies drafted, and prep any booked calls — leaving every
*send* and the calls themselves for a human. Demand Gen is the most
audience-facing function, so this play does a lot of preparation and
stops quickly at each send gate.

The lead dispatches the **installed outreach variant** (interceptly OR
salesnav — a client runs one), plus `rockstarr-reply` and
`rockstarr-ops`. It never sends a connection, message, or reply, and it
never runs the call.

## Preconditions

- An outreach variant installed + configured: a confirmed session, an
  ICP, and a lead list. If outreach isn't set up, say so and stop.
- `rockstarr-reply` and `rockstarr-ops` are optional — steps 4 and 5
  skip cleanly if they aren't installed or have nothing to do.
- Read `../role-registry.md` (Demand Gen output paths + the
  outreach-tasks.xlsx / outreach-mirror.xlsx state of truth) and
  `00_intake/stack.md` (outreach variant, daily cap,
  `outreach_campaign_mode`). Honor `00_intake/marketing-plan.md` (the
  demand-gen / booked-meetings objective).

## Steps

Skill names are shown as **interceptly / salesnav** — use whichever
variant is installed.

| # | Step | Specialist skill (interceptly / salesnav) | Tag | Produces |
|---|------|-------------------------------------------|-----|----------|
| 1 | Sharpen the target list (research + qualify the segment) | `qualify-lead` + ops:`audit-lead` / salesnav:`crawl-lead-list` + ops:`audit-lead` | **AUTO** | lead-list / audit notes |
| 2 | Draft / refresh the campaign messaging from the ICP | `draft-icp-campaign-interceptly` / `draft-icp-campaign` | **AUTO** | campaign draft |
| 3 | Stage + preview the next outreach batch | `daily-loop` + `preview-queue-interceptly` / `daily-connect` + `preview-queue` | **AUTO** | staged batch + a preview |
| — | **Send** the connects / sequence | the variant's send/launch (`send-message` / `launch-campaign-interceptly` ; salesnav `send-scheduled-messages`) — human | **GATED** | — |
| 4 | (If replies are pending) draft the replies | `interceptly-reply-handler` / reply:`draft-reply` (via `detect-replies`) | **AUTO** | reply drafts in `03_drafts/replies/` |
| — | **Send** the replies | reply:`present-for-approval` → salesnav `send-approved-reply` / interceptly `send-message` — human | **GATED** | — |
| 5 | (If meetings are booked) prep the upcoming call(s) | ops:`daily-call-prep` → `prep-call-1` / `build-client-agenda` | **AUTO** | call-prep docs |
| — | **Run** the call | human | **GATED** | — |

## Stop point

**STOP at every send/launch gate.** The play sharpens the list, drafts
the campaign, stages + previews the batch, drafts any pending replies,
and preps any booked calls — all internal/reversible — and leaves the
sends and the calls for a human.

Present to the founder:
- the staged outreach batch + its preview, ready to send (how many,
  against the daily cap), and how to send it (the variant's send skill),
- any reply drafts now in `03_drafts/replies/` awaiting approval,
- any call-prep docs produced for booked meetings, and
- the note that the outreach daily-loop / detect-replies cadence carries
  the steady state from here — this play is the on-demand push.

## Notes / bounds

- **Never send.** Connects, messages, replies — all GATED. The lead
  stages and drafts; humans approve and send. This holds even if the
  founder says "just send it."
- **Respect the daily cap + campaign mode.** Stage at most one batch per
  run, within the client's configured connects/day and
  `outreach_campaign_mode` (e.g. `connect_only`). Never exceed the cap.
- **One outreach variant.** Use the installed one; don't assume both.
- **Steps 4–5 are conditional + event-driven.** Only draft replies that
  are actually pending; only prep calls that are actually booked. Skip
  silently when there's nothing waiting.
- **AUTO is prep only.** Research, drafting, staging, preview, and
  call-prep are reversible + audience-never-sees-it. Every actual
  outreach action is the gate.
