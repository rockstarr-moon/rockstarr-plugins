---
name: verify-linkedin-newsletter
description: "This skill should be used when the user asks to \"verify the LinkedIn newsletter went live\", \"check the newsletter posted\", \"did the LinkedIn newsletter go out\", \"confirm the newsletter is live\", or \"go-live check the newsletter\". Confirms that a scheduled LinkedIn newsletter edition actually published on or near its expected date. Reads the expected date and edition title from content-calendar and 05_published/_publish.log, confirms the right personal account is signed in, navigates to that account's authored newsletter, and checks that an article posted within ~3 days of the expected date with a matching title. Reports the result into the workspace and can route a notification via rockstarr-infra:send-notification. The companion publish-linkedin-newsletter does the scheduling."
---

# verify-linkedin-newsletter

Confirm a scheduled LinkedIn newsletter edition actually went
live. `publish-linkedin-newsletter` queues editions days or weeks
ahead; this is the after-the-fact go-live check that the edition
posted on schedule, so a silent scheduling failure doesn't go
unnoticed.

> **Template convention.** Fenced code blocks below show `# ---`
> where YAML front-matter delimiters belong. **Emit real `---` in
> any output file.**

## This skill drives a browser

Like `publish-linkedin-newsletter`, this reaches LinkedIn through
**Chrome MCP** — the deferred-class exception to the plugin's
file-in / file-out norm. It only reads (no posting), but the
account-safety check still applies: you must be looking at the
right person's profile to judge whether their newsletter posted.

## When to run

- On or shortly after a LinkedIn-newsletter slot's publish date
  from `content-calendar`.
- The operator asks to confirm a newsletter posted / went live.
- Trigger phrases: "verify the LinkedIn newsletter went live",
  "did the newsletter post", "confirm the newsletter is live",
  "go-live check the newsletter".

## Preconditions

Tier 1 cheap checks first:

- `/rockstarr-ai/00_intake/stack.md` exists and
  `linkedin_newsletters_per_month` is at least 1.
- A LinkedIn-newsletter edition to verify exists — either a slot
  in the month's `content-calendar` with a past-or-today publish
  date, or an entry in `05_published/_publish.log` with channel
  `linkedin-newsletter`.
- Chrome MCP is available.

If there's nothing to verify, say so and stop.

## Inputs

1. **`02_inputs/content-calendar_[YYYY-MM].md`** and/or
   **`05_published/_publish.log`** — the expected publish date and
   the edition title / source TL slug.
2. **`00_intake/stack.md`** — the cadence gate and audience
   timezone.

## Step 0 — Confirm which edition + account

Resolve the edition under review: its expected publish date and
title. Because newsletters are personal-account items, confirm
with the operator which person's account and which newsletter to
check (the same run-config the publish skill prompts for).

## Step 1 — Confirm the session

Navigate to `https://www.linkedin.com/feed/` and read the sidebar
profile via `get_page_text`. Confirm the signed-in name matches
the account named in Step 0. If it's someone else or logged out,
ask the operator to sign in as the correct person before
proceeding.

## Step 2 — Open the authored newsletter

From the feed, find the Newsletters section (left sidebar, or the
profile's activity area). Open the newsletter where the account
shows as **Author** (not subscriber). If the account authors more
than one, pick the one matching the newsletter name from Step 0.

## Step 3 — Validate the edition posted

Check the newsletter's article list. The edition is confirmed live
when both hold:

1. **An article exists** published within ~3 days of the expected
   date (scheduling isn't always exact).
2. **The title matches** the expected edition title (a rough match
   is fine — titles get light edits).

Capture the live article title and publish date via
`get_page_text` / `read_page` as evidence.

If no matching article is found within the window, that's a
"did not post" result — note the most recent edition that IS
present.

## Step 4 — Report

Write the result into the workspace (append to
`05_published/_publish.log` via `rockstarr-infra:publish-log` to
mark the edition confirmed-live, or note the failure). Summarize
in chat:

- **Live:** edition title as shown on LinkedIn + the publish date,
  confirming it matches the calendar.
- **Not live:** what was found instead (no article, wrong date,
  most recent edition's date), flagged for follow-up.

For a "did not post" result, offer to route an alert to the
strategist via `rockstarr-infra:send-notification` so it doesn't
sit unseen. Do NOT create ClickUp tasks — the workspace log is the
record of truth in this stack.

## Edge cases

- **Newsletters section not visible.** Layout shifts — try
  scrolling the feed, or go to the profile's activity tab.
- **No authored newsletter.** The account may not have one set up.
  Report it and flag to the operator.
- **Multiple editions near the date.** If ambiguous, note both and
  let the reviewer decide.

## Tool quick reference

| Tool | Purpose |
|------|---------|
| Chrome MCP navigate / read_page / get_page_text | Open the newsletter, read the article list + dates |
| AskUserQuestion | Confirm which edition / account |
| rockstarr-infra:publish-log | Mark the edition confirmed-live |
| rockstarr-infra:send-notification | Alert the strategist on a "did not post" |

## What NOT to do

- Do NOT check the wrong account — confirm the session (Step 1).
- Do NOT create ClickUp tasks (content's no-ClickUp rule).
- Do NOT report "live" without an article matching the date window
  and title.

## Related

- `rockstarr-content:publish-linkedin-newsletter` — schedules the
  edition this skill verifies.
- `rockstarr-content:content-calendar` — holds the expected
  publish date + source TL slug.
- `rockstarr-infra:publish-log` / `rockstarr-infra:send-notification`.
