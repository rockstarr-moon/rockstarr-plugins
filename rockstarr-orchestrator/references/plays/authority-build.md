---
play: "authority-build"
title: "Authority Build"
intent_match:
  - "build our authority"
  - "establish our POV"
  - "more thought leadership"
  - "become a thought leader"
  - "grow our brand"
  - "grow our LinkedIn engagement"
  - "build our reputation"
  - "authority build"
functions:
  - "Content & SEO"
  - "Brand & Social"
---

# Play: Authority Build

Build the founder's authority on a theme: produce a thought-leadership
piece with a real point of view, then stage the social amplification and
engagement around it — so the POV lands as a publishable piece *and* as
the social conversation that carries it. Where the **Content Flywheel**
amplifies a piece you've *already* approved, Authority Build *creates*
the authority content and tees up its distribution.

The lead dispatches `rockstarr-content` (thought leadership) and
`rockstarr-social` (amplification + engagement). It never posts,
publishes, sends invites, or comments — it stages and stops at the gate.

## Preconditions

- A scaffolded workspace with an approved `00_intake/style-guide.md`.
- The client runs thought leadership (`thought_leadership_per_month` >= 1
  in `stack.md`) — or has a brand/authority objective in
  `00_intake/marketing-plan.md`. If neither, surface the gap and stop.
- `rockstarr-social` installed for the amplification steps; if not,
  produce the thought-leadership piece (steps 1–3) and note that social
  staging is unavailable.
- Read `../role-registry.md` (Content & SEO + Brand & Social paths) and
  `00_intake/marketing-plan.md` (the authority theme/POV this serves) +
  `stack.md` (social channels + cadence).

## Steps

| # | Step | Specialist skill | Tag | Produces |
|---|------|------------------|-----|----------|
| 1 | Ideate thought-leadership angles on the theme (with the enemy/POV field) | `rockstarr-content:ideate-topics` (TL lane) | **AUTO** | TL angles in `02_inputs/` |
| 2 | Outline the chosen angle (forces thesis, counter-argument, opening, quotable line, proprietary term) | `rockstarr-content:outline-thought-leadership` | **AUTO** | outline in `03_drafts/content/` |
| 3 | Draft the thought-leadership piece (runs the TL rubric, then stop-slop) | `rockstarr-content:draft-thought-leadership` | **AUTO** | TL draft in `03_drafts/content/` |
| 4 | Stage social amplification — a LinkedIn post + a poll on the theme | `rockstarr-social:draft-social` + `draft-polls` | **AUTO** | social drafts in `03_drafts/social/` |
| — | **Approve + publish** the TL piece | (human via `rockstarr-infra:approve` + publish flow) | **GATED** | — |
| — | **Publish** as a LinkedIn newsletter, if used | `rockstarr-content:publish-linkedin-newsletter` (human-in-loop) | **GATED** | — |
| — | **Post / schedule** the social + poll | `rockstarr-social:publer-export` (human-run) | **GATED** | — |
| — | **Engagement** — page-follower invites, comment replies | `rockstarr-social:invite-page-followers` / `li-comment-check` (human-run) | **GATED** | — |

## Stop point

After drafting the TL piece and staging the social amplification (steps
1–4), **STOP.** Publishing, posting/scheduling, sending invites, and
replying to comments are all GATED — the lead stages, the human ships.

Present to the founder:
- the TL draft now in `03_drafts/content/` (with its rubric + stop-slop
  scores) awaiting approval,
- the social post + poll staged in `03_drafts/social/`,
- the gated next steps — approve/publish the piece, optionally republish
  it as a LinkedIn newsletter, post the social/poll, and run engagement
  (invites, comment replies) — and how to do each, and
- the note that the **Content Flywheel** play can later fan the *approved*
  piece out further, and the social autopilot carries the cadence.

## Notes / bounds

- **One TL piece per run.** Respect `thought_leadership_per_month`; don't
  draft a backlog of pieces in a single fire.
- **Owned POV only.** The thought leadership is the client's perspective,
  drawn from first-party material — never third-party reference framed as
  theirs.
- **Engagement never auto-fires.** Page invites and comment replies are
  audience-facing — always GATED. The lead can stage/prepare, never send.
- **Respect social config.** Only stage for enabled `social_channels`,
  within `social_posts_per_week` / `polls_cadence`. Skip step 4 cleanly
  if social is off.
- **AUTO is create + stage only.** Ideation, outlining, drafting, and
  staging are reversible + audience-never-sees-it; publishing, posting,
  and engagement are the gates.
