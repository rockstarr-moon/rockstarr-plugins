---
name: publish-linkedin-newsletter
description: "This skill should be used when the user asks to \"publish the LinkedIn newsletter\", \"schedule the LinkedIn newsletter\", \"go live with the newsletter on LinkedIn\", or \"republish a TL piece as a LinkedIn newsletter\". Republishes an approved thought-leadership piece from 04_approved/content/ as a LinkedIn newsletter edition on the author's personal account, via Chrome MCP automation of the article editor. Gated on stack.md linkedin_newsletters_per_month at least 1. Confirms the right account is signed in, sets the publishing target, types the body (em-dash-free), applies formatting, then stops for the operator to upload the cover image, approve a stop-slopped 3-sentence question-led intro post, and click Schedule. Records the publish via rockstarr-infra:publish-log."
---

# publish-linkedin-newsletter

Republish an approved thought-leadership piece as a LinkedIn
newsletter edition. This realizes the lane that `ideate-topics`
and `content-calendar` already plan for: a TL piece, once
approved, gets a second life as a LinkedIn newsletter on the
author's personal account.

> **Template convention.** Fenced code blocks below show `# ---`
> where YAML front-matter delimiters belong, to keep Cowork's
> SKILL.md parser from misreading them. **When writing any output
> file, emit real `---`, not `# ---`.**

## This skill drives a browser

Most of rockstarr-content is a pure file-in / file-out content
factory. This skill is the exception the plugin always anticipated
(the deferred `publish-*` connectors): it drives the LinkedIn UI
through **Chrome MCP**. Treat the browser steps with the same care
the outreach plugins treat their sessions — the top risk is
posting to the wrong account. See "Why this is a deferred-class
skill" in the plugin CLAUDE.md.

The reusable editor mechanics (execCommand recipes, the full
gotcha catalog) live in
`references/linkedin-article-formatting.md`. Read it before the
first edition of a run.

## LinkedIn newsletters are personal-account items

A LinkedIn newsletter lives on a **person's** profile, not a
company page, and a single client workspace may have more than one
person running their own newsletter. So the account identity, the
newsletter name, and the publish day/time are NOT read from a
single client-level config — they are confirmed with the operator
at run time (see Step 0). Only the *cadence*
(`linkedin_newsletters_per_month`) is a stack.md field.

## When to run

- A `content-calendar` LinkedIn-newsletter slot's publish date is
  approaching and its source TL piece is approved.
- The operator asks to schedule / publish / go live with a
  LinkedIn newsletter, or to queue the month's editions.
- Trigger phrases: "publish the LinkedIn newsletter", "schedule
  the LinkedIn newsletter", "go live with the newsletter on
  LinkedIn", "republish [slug] as a LinkedIn newsletter".

## Preconditions

Tier 1 cheap checks first; refuse fast if any fail:

- `/rockstarr-ai/00_intake/stack.md` exists and
  `linkedin_newsletters_per_month` is at least 1. If it's 0 the
  lane is suppressed — refuse, the client doesn't publish here.
- At least one approved TL piece exists in
  `04_approved/content/` (the body source). If none, point the
  operator at the TL flow (`outline-thought-leadership` then
  `draft-thought-leadership` then `rockstarr-infra:approve`).
- Chrome MCP is available (the skill cannot run headless).

Tier 2 reads (the calendar, the approved draft, the style guide)
happen inside the work, after the anchor message.

## Inputs

1. **`02_inputs/content-calendar_[YYYY-MM].md`** — the
   LinkedIn-newsletter slot(s): the publish date and the source TL
   slug for each edition. This is the schedule of record.
2. **The approved TL piece** at
   `04_approved/content/[slug].md` named by the calendar slot. Its
   body is the newsletter body; its `title` is the edition title.
   It is already voice-locked and stop-slopped, so the body is NOT
   re-stop-slopped here — only verified em-dash-free as a safety
   net.
3. **`00_intake/stack.md`** — `linkedin_newsletters_per_month`
   (the cadence gate) and the audience timezone.
4. **`00_intake/style-guide.md`** — voice for the NEW prose this
   skill writes (the intro post). Read the LinkedIn / short-form
   channel-adaptation section.

## Step 0 — Confirm the run config (ask, don't assume)

Because newsletters are personal-account items, confirm with the
operator before touching LinkedIn:

- **Which account / person** this edition publishes under.
- **The newsletter name** (e.g. the title shown in the editor's
  publishing target).
- **Publish day + time** (default: the date from the calendar
  slot, at a B2B-friendly time like 7:00 AM in the audience
  timezone). Confirm the time once; reuse it across the batch.

If the operator is scheduling several editions, present the
resolved list (edition title, source slug, publish date) as a
table and let them confirm or trim before any browser action.

## Step 1 — Confirm the session (account safety)

Navigate the Chrome MCP tab to `https://www.linkedin.com/feed/`
and read the left sidebar profile via `get_page_text`. Confirm
the signed-in name matches the account named in Step 0.

If it shows anyone else, a logged-out screen, or a different
account, **STOP** and ask the operator to sign in as the correct
person. Wrong-account publishing is the top reputational risk in
this workflow. (This mirrors the outreach plugins' session-confirm
pattern.)

## Step 2 — Per edition, run the scheduling loop

Default to one edition per call; batch only when the operator
asked to queue several. For each edition:

### 2a. Open a fresh article
Navigate to `https://www.linkedin.com/article/new/`.

### 2b. Verify the publishing target
The editor must target the author's newsletter, not "Individual
article" (it resets between editions). Fix via the publishing-
target dropdown. See gotcha #1 in the formatting reference.
**Re-check on every edition.**

### 2c. Type the title
The `title` from the approved TL piece, verbatim.

### 2d. Type the body
Take the body from the approved TL draft (it's already approved
prose — do not rewrite it). Type it into the body field with two
transformations applied inline:
- **Drop leading "1. " on subheadings** so LinkedIn doesn't
  auto-convert them into a numbered list (gotcha #2).
- **Single newline between paragraphs** (gotcha #5).

Then run the verify-zero-em-dashes JS check (formatting
reference). The body came from a stop-slopped draft, so this
should already be 0; if not, strip inline using the em-dash map
and re-verify. Do NOT re-run the full stop-slop pass on the body —
it was already stop-slopped at draft time.

### 2e. Apply formatting
Use the `document.execCommand` recipes in the formatting reference
(Heading, Subheading, blockquote, lists) — faster and more
reliable than the toolbar. Verify with the counts snippet.

### 2f. STOP — operator uploads the cover image
The cover art is a local file only the operator has. Ask for it as
its own clean stop point — do NOT bundle it with any other ask
(gotcha #8 / bundling caused a skipped upload):

> Please upload the cover image now: click "Upload from computer"
> at the top of the editor, pick the newsletter cover file, and
> tell me when it's loaded.

Wait for explicit confirmation.

### 2g. Click Next, verify the cover renders
Open the Next dialog. Confirm the cover image preview shows (not
just a small article-card thumbnail). If missing, close and retry
the upload.

### 2h. STOP — draft and get approval on the intro post
The "Tell your network..." text becomes the post that appears on
subscribers' feeds alongside the edition. It is **new prose**, so
it runs the full pipeline: write it per the rules below, run
`rockstarr-infra/skills/_shared/stop-slop/SKILL.md` on it, then
present to the operator and wait for explicit approval before
typing it.

Intro post rules (3 sentences):
- **Lead with questions.** Two stacked questions is canonical.
  Never lead with a thesis or summary.
- **Conversational**, like the author talking to a friend.
- **Zero em dashes** (commas or parens).
- **No "Most..." opener, no X-not-Y structure** (per the style
  guide's banned structures).
- **Vary the third sentence** across editions — don't reuse the
  same "Wrote down..." opener every time. Mix: "New piece on...",
  "Latest one digs into...", "Just shipped a piece on...", etc.
- **Tease, don't summarize.** Pull the curiosity gap, not the
  answer; don't echo the body.

If the operator pushes back on tone, redraft (re-run stop-slop)
and re-present.

### 2i. Type the approved intro post, verify it landed
Type it into the post field. Screenshot to confirm the text is in
the field before touching the schedule controls (save-your-bacon
check before the time-field gotcha).

### 2j. Open the schedule dialog — clock icon, NOT Publish
Click the clock icon (gotcha #6). Do not click the blue Publish
button (it publishes immediately).

### 2k. Set date and time
Date: navigate the calendar to the target month, click the target
day (the calendar slot's publish date). Time: click the Time
field, `triple_click` to select, type the time, click the
suggestion. **Never `cmd+a` in the Time field** (gotcha #3 — it
silently wipes the intro post). Never click Back or press Escape
in the dialog (gotcha #4).

### 2l. Verify, then hand the final click to the operator
Confirm the dialog header shows the correct day + time + timezone.
The operator clicks the final Next then Schedule — the skill
prepares everything up to that point but does not commit:

> Schedule confirmed: [day, date, time, tz]. Ready for you to
> click Next then Schedule.

### 2m. Record the publish
After the operator confirms the edition is scheduled, record it
via `rockstarr-infra:publish-log` (channel `linkedin-newsletter`,
the edition title, the source TL slug, the scheduled publish
date). This keeps `ideate-topics` dedup and reporting accurate and
gives `verify-linkedin-newsletter` something to check against.

### 2n. Loop
The page resets to a fresh `/article/new/`. Return to 2a for the
next edition. Re-verify the publishing target (2b) every time.

## Edge cases

- **90-day cap.** LinkedIn refuses dates more than ~90 days out.
  Stop at the cap and report which editions weren't scheduled —
  they go in the next batch.
- **Source TL piece not approved yet.** If the calendar slot's
  source slug isn't in `04_approved/content/`, pause and tell the
  operator — the TL piece must be approved first.
- **No calendar slot.** If the operator points directly at an
  approved TL piece with no calendar slot, confirm the target
  publish date with them before scheduling.
- **Cover image skipped.** If the Next dialog shows no cover
  preview, close, re-upload, retry.
- **Wrong publishing target.** Resets to "Individual article"
  between editions — always re-verify (2b).

## Tool quick reference

| Tool | Purpose |
|------|---------|
| Chrome MCP navigate / find / computer | Drive the LinkedIn editor, click, type |
| Chrome MCP javascript_tool | Apply formatting via execCommand; verify counts + em-dash zero |
| Chrome MCP get_page_text | Confirm the signed-in account (Step 1) |
| AskUserQuestion | Confirm run config, intro-post approval, edge cases |
| rockstarr-infra:publish-log | Record the scheduled edition |
| TaskCreate / TaskUpdate | Track per-edition progress through the loop |

## What NOT to do

- Do NOT publish under the wrong account. Verify the session every
  run (Step 1).
- Do NOT click the blue Publish button — always schedule via the
  clock icon.
- Do NOT use `cmd+a` in the Time field.
- Do NOT bundle the cover-image ask with any other ask.
- Do NOT rewrite the approved TL body — it shipped through the
  approval gate already. Only the inline editor transformations
  (subheading numbering, single newlines) and em-dash verification
  apply.
- Do NOT skip stop-slop on the intro post — it's new prose.
- Do NOT press the final Schedule yourself. The operator commits.
- Do NOT schedule editions for a lane whose
  `linkedin_newsletters_per_month` is 0.

## Related

- `rockstarr-content:draft-thought-leadership` — produces the
  approved TL piece this skill republishes (carries
  `linkedin_newsletter_eligible` when flagged).
- `rockstarr-content:content-calendar` — slots the edition's
  publish date against the source TL slug.
- `rockstarr-content:verify-linkedin-newsletter` — confirms the
  edition actually went live on the scheduled date.
- `rockstarr-infra:publish-log` — records the publish.
- `references/linkedin-article-formatting.md` — execCommand
  recipes + the full gotcha catalog.
