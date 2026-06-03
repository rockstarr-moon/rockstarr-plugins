---
name: qualify-lead
description: "This skill should be used on every reply in the per-reply pipeline, or when the user says \"qualify this lead\", \"does this lead match our ICP\", or \"run ICP qualification on this lead\". Reads the Interceptly right-panel (title, company, Work Experience) plus optional LinkedIn fallback, checks the lead against /00_intake/icp-qualifications.md (tightened by the active campaign's per-campaign overrides), and returns one of four verdicts: target / not_target / ambiguous / unknown — with the matching rule cited. Runs on every reply, not just once per lead — title or company may have changed."
---

# qualify-lead

Per-reply qualification. The bot has no opinion on who is or
isn't a target beyond what the client wrote in
`icp-qualifications.md` plus any tightening in the active
campaign's ICP file. This skill is pure rule evaluation — it does
not draft, label, or take any action.

## When to run

- Step 1 of the per-reply pipeline, inside `process-inbox` and
  `process-my-tasks`.
- On demand when the user says "qualify `[lead]`" — useful when
  they want to sanity-check the rules against a specific lead
  before refining `icp-qualifications.md`.

## Preconditions

- `/00_intake/icp-qualifications.md` exists and has target /
  not-target / ambiguous sections. If not, refuse and point at
  `capture-icp-qualifications`.
- The lead's Interceptly right-panel is currently rendered in
  Chrome (or a mirror of its content has been passed to the
  skill).

## Inputs

- `lead_url` — Interceptly thread URL or LinkedIn profile URL
  (required).
- `right_panel_context` — structured data from the right panel:
  `{name, company, title, location, work_experience[], notes}`.
- `active_campaign_slug` — the campaign the lead is enrolled in
  (optional; if absent, skip per-campaign tightening).

## Behavior

### Step 1 — Load rule sources

1. Read `/00_intake/icp-qualifications.md`. Parse the target,
   not-target, and ambiguous rule lists.
2. If `active_campaign_slug` is provided, read
   `/02_inputs/outreach/icps/[slug].md` and layer its
   `## Per-campaign tightening` block on top. Tightenings ADD
   restrictions; they never loosen.

### Step 1.5 — Research the company before concluding (required)

**Title alone is not enough.** The right-panel title sits on top of
many business models, and it can be wrong in both directions — a lead
who looks like a target by title can fail the ICP once you see what
the company actually sells, and a lead who looks non-target by title
can turn out to run exactly the kind of practice the ICP targets (the
title is their current client, not their own business). Before
concluding `target` or `not_target` on the strength of the title +
right panel, open the **company website** and read it against the
client's ICP rules.

How:

1. Open the company website (Chrome MCP navigate to a fresh tab;
   `get_page_text` on the homepage and About page — ~60–90 seconds).
   Reading only; no clicks required, so no gated-click concern.
2. Answer, against `icp-qualifications.md`'s target / not-target
   definitions: **what does the company actually sell** (the business
   model, not the title), **who is the buyer**, **is the lead an
   owner/principal or staff**, and **what's the size**. These are what
   the ICP rules turn on — the title rarely settles them alone.
3. If the website is thin or single-page, check the LinkedIn company
   page (founded year, employee count, recent posts) and, if needed,
   the lead's LinkedIn profile (Step 3's read-only side tab).

Capture two things from this research: the **verdict input** (which
fed Step 2) and any **positioning signal** for the downstream draft
(the company's own model language, current focus, visible content
rhythm or its absence). Pass the positioning signal through in the
verdict's `notes` so `rockstarr-reply:draft-reply` can mirror the
lead's actual model rather than generic copy.

Skip this research only when the verdict is already settled without
it — e.g., the lead explicitly declined, or a not-target rule matches
on something the title alone makes unambiguous.

### Step 2 — Match the lead against rules

Run in this order, returning the first matching verdict. Match against
the **researched** context (Step 1.5), not the bare title:

1. **Not-target rules.** If any not-target rule matches
   (role, company type, behavior), return
   `{verdict: "not_target", rule: "<matching rule>",
   confidence: "high"}`.
2. **Per-campaign tightening excludes.** If the campaign has
   additive exclusions, check them next. Same verdict shape.
3. **Ambiguous rules.** If the lead hits any ambiguous rule,
   return `{verdict: "ambiguous", rule: "<matching rule>",
   needs: "<what would tip it to target>"}`.
4. **Target rules.** If the lead matches target rules (role
   cluster AND company-size AND industry — intersection, not
   union, unless `icp-qualifications.md` explicitly says
   otherwise), return `{verdict: "target", rule: "<matching
   rule>", confidence: "<HIGH|MEDIUM>"}`.
5. **Unknown.** If none of the rule branches matches — the
   right-panel context is too thin to place the lead — return
   `{verdict: "unknown", needs: "more context (LinkedIn
   profile, company website, etc.)"}`.

### Step 3 — Optional LinkedIn fallback

If verdict = `unknown` AND
`icp-qualifications.md.minimum_extra_context_for_ambiguous_to_target_promotion`
specifies the kind of LinkedIn context that would help, call
`process-inbox`'s LinkedIn side-tab helper to fetch the lead's
LinkedIn profile summary (read-only). Re-run Step 2 with the
enriched context.

Do NOT send from the LinkedIn side tab. Ever.

### Step 4 — Record verdict

Append a row to the `Qualifications` sheet of
`outreach-mirror.xlsx`:

| column | value |
|---|---|
| ts | `[ISO]` |
| lead_url | `[URL]` |
| campaign_slug | `<slug or blank>` |
| verdict | `target / not_target / ambiguous / unknown` |
| rule_cited | `<the matching rule text>` |
| confidence | `HIGH / MEDIUM / LOW` |

If verdict = `not_target`, also append to
`/02_inputs/outreach/_non_icp_log.md` with the rule cited.
The Non-ICP Log is the bot's durable memory of "who the client
decided is not a target and why" — weekly reports surface these
for refinement.

### Step 5 — Return

Return the verdict object to the caller. The caller decides what
to do with it (draft, flag, skip). Include a `notes` field carrying
the positioning signal from the Step 1.5 website research (the
company's own model language, current focus, content rhythm or its
absence) so `rockstarr-reply:draft-reply` can mirror the lead's
actual business rather than generic copy. `notes` is optional/empty
when no research was needed.

## Semantics

- `target` → caller hands off to `rockstarr-reply:classify-reply`
  and `rockstarr-reply:draft-reply`.
- `not_target` → no draft (except the non-ICP yes three-option
  flow; `process-inbox` handles that branch). Label via the
  default mapping (`decline` → Not Interested; polite ack →
  Ignore). No follow-up task.
- `ambiguous` → caller hands off to
  `rockstarr-reply:flag-for-review`. No draft.
- `unknown` → caller hands off to
  `rockstarr-reply:flag-for-review` with a note asking the operator
  to supply the missing context.

## Re-qualification

`qualify-lead` runs on EVERY reply, not just once per lead. A
lead who was `not_target` last week may be `target` this week if
they changed companies. Cached verdicts in the mirror are
informational — the current run's verdict wins.

## Failure modes

- **Right-panel context is empty.** Wait 2s and retry reading the
  DOM once. On second failure, return `unknown` with `needs:
  "right-panel unreadable; retry or check Chrome MCP"`.
- **Campaign ICP file missing but slug passed.** Warn and proceed
  with baseline rules only. Write an _errors.md note.
- **Multiple rules match with conflicting verdicts.** Not-target
  wins over ambiguous wins over target. Strictness always wins.

## What NOT to do

- Do not hardcode any rule the client did not write into
  `icp-qualifications.md`. Zero baked-in opinions.
- Do not cache a `target` verdict across reply runs. Always
  re-evaluate — the world changes.
- Do not send a message, apply a label, or create a task from
  this skill. Pure rule evaluation.
- Do not paraphrase the matching rule. Cite it verbatim from
  `icp-qualifications.md` so the operator can audit the
  decision chain.
