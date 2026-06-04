---
play: "content-flywheel"
title: "Content Flywheel"
intent_match:
  - "spin the content flywheel"
  - "amplify our content"
  - "amplify this post"
  - "repurpose our content"
  - "turn our blog into social"
  - "get more out of our content"
  - "distribute our content"
  - "promote our latest piece"
functions:
  - "Content & SEO"
  - "Brand & Social"
---

# Play: Content Flywheel

Get more mileage out of long-form the client has already approved: take
one approved piece and fan it across channels — social posts, a
newsletter mention — so a single blog or thought-leadership piece drives
reach on LinkedIn and in the inbox, which in turn pulls the audience
back to the long-form. The flywheel: long-form → derivatives →
distribution → audience back to long-form → signal for the next topic.

The lead dispatches `rockstarr-content` (repurposing, newsletter) and
`rockstarr-social` (social staging). It does not post or schedule
anything itself — it stages the derivatives and stops at the gate.

## Preconditions

- A scaffolded workspace with an approved `00_intake/style-guide.md`.
- **At least one approved long-form piece** to amplify (in `04_approved/`
  or the publish log). If there is none, the flywheel has no fuel —
  point the founder at the **SEO/GEO Engine** play or drafting first,
  and stop. (Don't repurpose third-party material — owned/approved
  only.)
- `rockstarr-social` installed for the social steps. If it isn't,
  produce the content-side derivatives (step 2) and note that social
  staging is unavailable.
- Read `../role-registry.md` (Content & SEO + Brand & Social output
  paths) and `00_intake/stack.md` (social channels + cadence, newsletter
  cadence). Honor `00_intake/marketing-plan.md` if present (the
  authority/brand objective this serves).

## Steps

| # | Step | Specialist skill | Tag | Produces |
|---|------|------------------|-----|----------|
| 1 | Pick the source piece (most recent approved long-form not yet repurposed, or the one the founder names) | — (read-only selection) | **AUTO** | the chosen piece |
| 2 | Fan it into derivatives (LinkedIn post, newsletter highlight, thread, video script if `records_videos`) | `rockstarr-content:repurpose` | **AUTO** | derivatives in `03_drafts/` |
| 3 | Stage the social post(s) into the weekly batch | `rockstarr-social:draft-social` (or `fill-week` for the batch) | **AUTO** | social drafts in `03_drafts/social/` |
| 4 | (If `email_newsletters_per_month` >= 1) fold the piece in as a newsletter CTA | `rockstarr-content:draft-newsletter` | **AUTO** | newsletter draft in `03_drafts/content/` |
| — | **Approve** the derivatives + social batch | (human via `rockstarr-infra:approve`) | **GATED** | — |
| — | **Schedule / export** to the social scheduler | `rockstarr-social:publer-export` (human-run) | **GATED** | — |
| — | **Publish** the LinkedIn newsletter, if used | `rockstarr-content:publish-linkedin-newsletter` (human-in-loop) | **GATED** | — |

## Stop point

After staging (steps 2–4), **STOP.** Approving, scheduling/exporting,
and any LinkedIn-newsletter publish are GATED — the lead never posts,
schedules, or publishes.

Present to the founder:
- the derivatives now in `03_drafts/` and the social batch in
  `03_drafts/social/` awaiting approval (the pending queue),
- which channels the social posts target (per `social_channels`), and
- the note that once approved, `publer-export` is how the batch reaches
  the scheduler, and that the weekly social autopilot (`fill-week`, if
  the client runs it) carries the cadence from here.

## Notes / bounds

- **One source piece per run.** Don't repurpose the whole backlog in a
  single fire — pick the highest-value recent piece.
- **Owned content only.** Never repurpose third-party/reference material
  as if the client said it (respect `kb_scope` / approval state).
- **Respect social config.** Only stage for channels enabled in
  `social_channels`; respect `social_posts_per_week` so the batch isn't
  overstuffed. Skip step 3 cleanly if social is off.
- **Skip step 4** when the client has no email newsletter cadence.
- **AUTO only through staging.** Drafting derivatives and staging the
  batch are reversible + audience-never-sees-it; posting/scheduling/
  publishing are the gates. The play halts there.
