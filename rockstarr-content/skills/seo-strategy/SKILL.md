---
name: seo-strategy
description: "This skill should be used when the user asks to \"run the SEO strategy\", \"do keyword research\", \"build the content plan\", or \"refresh the keyword plan\". Produces a strategic blog plan in pillar pages + supporting posts. Six-phase workflow: gather intake artifacts, research the client website + keyword landscape, generate 30 seed keywords + 50 long-tail variants, identify 5 competitor gaps, build 4-5 topic clusters (1 pillar + 4-6 supporting each), write the strategy doc + a canonical 25-32-topic backlog. When a recent seo-site-audit exists, reads it and folds refresh/consolidate/expand items for existing posts into the backlog alongside net-new topics. The backlog is read by ideate-topics monthly — strategy decides WHICH topics, ideate-topics sequences them."
---

# seo-strategy

The strategic content planning layer above the monthly cadence
flow. New in v0.5. Where `ideate-topics` answers "what should we
write this month," this skill answers "what should we be writing
across the next two quarters to build topical authority for this
client."

The output is two files. A strategy document at
`02_inputs/seo/strategy_[YYYY-MM-DD].md` carrying keyword
research, competitor gap analysis, and topic clusters. A
canonical backlog at `02_inputs/seo/backlog.md` listing 25-32
prioritized content pieces with cluster + pillar/supporting
structure, target keywords, search intent, and difficulty
estimates. `ideate-topics` reads the backlog every month and
prefers backlog items over fresh ideation.

> **Template convention.** Fenced code blocks below show `# ---`
> where YAML front-matter delimiters belong, to keep Cowork's
> SKILL.md parser from misreading them. **When writing the
> actual output file, emit real `---`, not `# ---`.**

## When to run

- **Onboarding** — every new client with `blogs_per_month >= 1`
  in stack.md gets an SEO strategy as part of intake. Run
  `seo-site-audit` first so the initial backlog reflects the
  existing site.
- **After a site audit** — when `seo-site-audit` produces a fresh
  `02_inputs/seo/audit_*.md`, re-run strategy to fold its
  content findings into the backlog.
- **Quarterly refresh** — typical cadence is once per quarter,
  on demand from the client or strategist.
- **New service line** — when the client adds a service that
  changes the content scope.
- **Backlog running thin** — when `ideate-topics` flags fewer
  than 2× monthly cadence remaining in the backlog, the
  strategist runs this skill to refill.
- **Trigger phrases:** "run the SEO strategy", "do keyword
  research", "build the content plan", "build a cluster
  strategy", "refresh the keyword plan".

## Preconditions

- `/rockstarr-ai/00_intake/client-profile.md` exists with
  audience, positioning, and offer info.
- `/rockstarr-ai/00_intake/style-guide.md` exists and is
  approved (read for context, not for voice-shaping at this
  layer — the strategy is upstream of voice).
- `/rockstarr-ai/00_intake/stack.md` exists with
  `website_base_url` set and `blogs_per_month >= 1`. If blog
  cadence is 0, refuse — there's no point in a strategy for a
  lane the client doesn't publish.
- Network access to the open web for `WebFetch` and
  `WebSearch`.

If any precondition fails, point the user at the relevant
upstream skill (`ingest-workbook`, `generate-style-guide`,
`capture-stack`) before running.

## Inputs

Read in this order:

1. **`client-profile.md`** — pull the audience definition, the
   ICP description (industry, company size, job titles, pain
   points), the core topic / niche, the offer language, and
   any phrasing the client uses to describe themselves. The
   ICP and niche fields are the spine of every keyword
   decision in this skill — if they're missing or vague, ask
   the user before proceeding.
2. **`stack.md`** — `website_base_url` for the site analysis.
   Any additional URL info (preferred sub-paths, product page
   URLs) the client has shared.
3. **`style-guide.md`** — read for context only. Influences
   word choice in the strategy doc's prose sections so the
   document reads like Rockstarr wrote it. Does NOT shape the
   keyword decisions themselves.
4. **`05_published/_publish.log`** if it exists — pull every
   blog slug already published for this client. The strategy
   marks these as "already covered" rather than re-proposing.
5. **The current backlog at `02_inputs/seo/backlog.md`** if
   one exists. A re-run regenerates the backlog completely,
   but it's worth reading the previous version to flag items
   that have moved through the workflow (drafted, approved,
   published) so the strategist can confirm before they get
   dropped.
6. **The newest site audit at `02_inputs/seo/audit_*.md`** if
   one exists (sort by the date in the filename; read the most
   recent). Produced by `rockstarr-content:seo-site-audit`, it
   carries a "Content findings for seo-strategy" table tagging
   existing-site issues with a `work_type` of `refresh`,
   `consolidate`, `expand`, or `new`. When present, the audit
   is the **preferred** source for the website analysis in
   Phase 1A (it already crawled the site deeply) and seeds the
   "fix-existing" items in the backlog. The audit is optional —
   if absent, run Phase 1A's shallow WebFetch analysis as
   before. Treat an audit older than ~2 quarters as stale: note
   it, but re-verify against the live site rather than trusting
   it wholesale.

## Phase 1: Research

Two parallel research streams: the client's own site, and the
keyword landscape.

### 1A. Website analysis

**If a recent `02_inputs/seo/audit_*.md` exists, prefer it.** The
audit already crawled the homepage, money pages, blog index,
sitemap, and schema, and catalogued the topical-authority picture.
Read its "Content findings for seo-strategy" table and its
"Pages audited" / content sections instead of re-crawling from
scratch. Spot-check a couple of live URLs to confirm nothing major
shipped since the audit, then proceed. Skip the rest of this
sub-section's manual fetches except where the audit didn't cover
something you need.

If there is **no** audit (or it's stale), do the analysis directly.
Use `WebFetch` to pull the client's homepage. Extract:

- Services or products offered.
- Positioning (tagline, value prop, headline).
- Audience claims (who they say they serve).
- Content topics already covered (visible from navigation,
  service pages, blog/insights index).

`WebFetch` the blog or insights page if it exists (try
`/blog`, `/insights`, `/resources`, `/articles` in that
order). List every blog post title visible. These are
de-duplication targets — the strategy must NOT propose topics
that are already covered.

`WebSearch` `site:[client_domain] [core topic]` to see
indexed pages Google has crawled.

### 1B. Keyword landscape

Run these searches in parallel:

- `[core topic] keywords [current year] SEO`
- `[core topic] for [ICP description] keywords high volume low difficulty`
- `"[core topic]" "[ICP descriptor]" content gaps competitors miss SEO`

Pull insights about:

- Search volume expectations for this niche.
- Trending content formats (long-form guides, listicles,
  data reports, etc.).
- What competitors are producing.
- Underserved angles or audience segments.

Capture the top 3-5 ranking competitor articles per major
seed keyword cluster. These feed the gap analysis in Phase 3.

## Phase 2: Generate keywords

### 2A. Seed keywords (30 total)

Generate 30 seed keywords with this intent mix:

- **Informational** (12-15): "what is", "how to", "why",
  educational topics, definition queries.
- **Commercial** (8-10): "best", "vs", "comparison",
  template, tool-focused, "X for Y" comparisons.
- **Transactional** (5-8): "hire", "agency", "cost",
  "pricing", "services", buy-intent queries.

For each seed, capture: the keyword, intent type, estimated
monthly volume (directional — note this is not from a paid
SEO tool), and a one-line note about why it matters for this
specific client's ICP.

Tailor every keyword to the ICP. Generic keywords waste
effort. If the ICP is small business owners, the keywords
reflect small-business language, budgets, and concerns. If
the ICP is enterprise CTOs, the keywords reflect enterprise
terminology.

### 2B. Long-tail expansion

Take the top 10 seeds (highest ICP relevance) and generate 5
long-tail variations each. Total: 50 long-tail keywords.

For each long-tail variant, classify:

- **Search intent** — Informational / Navigational /
  Commercial / Transactional.
- **Estimated difficulty** — Low / Medium / High.

Long-tail keywords tend to be longer, more specific, and
lower-volume but higher-intent. They're where most quick
wins live.

### 2C. Quick wins

Identify 8-12 keywords (from across the seed list and the
long-tail expansion) that combine high ICP relevance with
low estimated difficulty. These are the first posts to
publish — they earn ranking faster and feed traffic that
helps the harder pillar topics rank later.

Mark each quick win with a ⭐ in the strategy doc and the
backlog.

## Phase 3: Build the strategy

### 3A. Competitor gap analysis (5 gaps)

Identify 5 content gaps competitors in this space
consistently miss. For each gap:

1. **What competitors do.** Describe the dominant approach
   in the existing ranking content (cite specific articles
   from Phase 1B).
2. **Why it falls short.** What audience segment, angle, or
   format is underserved.
3. **The opportunity.** What this client could write to
   capture the gap.
4. **Target keywords.** 2-3 keywords from Phase 2 that map
   to this gap.

Avoid generic gaps ("competitors don't write enough
content"). Be specific about audience, angle, format, or
depth. Generic gaps don't ship as differentiated content.

### 3B. Topic clusters (4-5 clusters)

Group all keywords (seeds + long-tail) into 4-5 logical
topic clusters. Each cluster gets:

- **Cluster name** — short, descriptive.
- **Pillar page** — one comprehensive guide, 2,500-4,000
  word target. The pillar is the cluster's anchor, scoped
  to one cluster topic thoroughly (not the entire niche).
  Pillar titles are scoped: "B2B Marketing Strategy for
  Small Businesses" works; "Complete Guide to B2B
  Marketing" is too broad.
- **4-6 supporting posts** — each targeting a specific
  long-tail or specific seed keyword in the cluster. Total
  per cluster: 1 pillar + 4-6 supports = 5-7 pieces.
- **Internal linking plan** — pillar links to every
  supporting post. Each supporting post links back to the
  pillar AND to 2-3 peer supporting posts in the same
  cluster.

Total content pieces across the strategy:
4 clusters × 5-7 pieces = **20-28 pieces** typical.
5 clusters × 5-7 pieces = **25-35 pieces** typical.

Aim for 25-32 pieces total — enough to feed 6-12 months of
output at typical monthly cadence (1-3 blogs/month).

Every cluster piece is `work_type: new` unless the audit
(below) maps it to existing content.

### 3C. Fix-existing items from the audit

If a site audit was read in the Inputs step, its "Content
findings for seo-strategy" table lists existing-site issues
already tagged with a `work_type`. Fold each into the backlog
as its own item, attached to the most relevant cluster:

- **`refresh`** — an existing post with stale dated content or
  outdated facts. The action is an update, not a rewrite.
- **`consolidate`** — two or more posts cannibalizing one
  keyword. Name the canonical destination and the 301 source.
- **`expand`** — a thin post, or one missing an FAQ section /
  currency markers / cited sources (a content-actionable GEO
  gap from audit Phase 7). The action is to deepen it.

These coexist with the `new` cluster pieces. A typical
audit-informed strategy is mostly `new` with a handful of
fix-existing items — don't let fix-existing crowd out the
net-new authority-building plan.

**Slug rule (load-bearing).** Refresh / consolidate / expand
items get their OWN unique backlog slug — append a
`-refresh-[YYYY]`, `-consolidate`, or `-expand` suffix. NEVER
reuse the published post's slug. `ideate-topics` filters out
backlog items whose slug appears in `05_published/_publish.log`;
a fix-existing item that reused the published slug would be
silently dropped from monthly ideation. Each fix-existing item
also carries an `existing_url` pointing at the post it acts on,
so downstream skills and the operator know what's being changed.

### 3D. Implementation notes

End the strategy doc with:

- **Recommended publishing priority** — which clusters
  ship first based on quick wins, ICP urgency, gap-capture
  speed.
- **Content format recommendations** — pillar word counts
  (2,500-4,000), supporting post word counts (1,200-1,800),
  FAQ section per piece (per blog-seo-geo reference).
- **Publishing cadence** — at the client's stack.md
  cadence, the backlog feeds 6-12 months. Note this.
- **Internal linking structure summary** — confirms the
  pillar↔support pattern is wired correctly.

## Phase 4: Write deliverables

### 4A. Strategy document

Write to
`/rockstarr-ai/02_inputs/seo/strategy_[YYYY-MM-DD].md`. If a
file with the same date exists, append `-2`, `-3`. Never
overwrite a previous strategy doc — keep them all for audit.

Required front-matter:

```yaml
# ---
client_id: [from client.toml]
client_name: [from client.toml]
strategy_run_date: "YYYY-MM-DD"
core_topic: "..."
icp_summary: "one-line ICP statement from client-profile.md"
website_url: "from stack.md"
audit_source: "02_inputs/seo/audit_<YYYY-MM-DD>.md or null"
total_items_in_backlog: 28
cluster_count: 4
quick_win_count: 10
produced_by: "rockstarr-content/seo-strategy@0.8.0"
produced_at: "ISO timestamp"
style_guide_version: "matched from style-guide.md front-matter"
# ---
```

Body sections in this order:

1. **Executive summary** (one short paragraph — what this
   strategy covers and why now).
2. **Seed keyword table** (30 rows: keyword, intent, est.
   volume, note).
3. **Long-tail expansion tables** (10 small tables, 5 rows
   each, with intent and difficulty).
4. **Quick wins summary** (8-12 starred keywords flagged
   for first-publish priority).
5. **Competitor gap analysis** (5 gaps, each with
   competitor approach, opportunity, mapped keywords).
6. **Topic cluster maps** (4-5 clusters, each with pillar
   title, supporting post titles, target keywords per
   piece, internal linking summary).
7. **Fix-existing items** (only when an audit was read — the
   `refresh` / `consolidate` / `expand` items derived from the
   audit, each with its existing URL and the audit finding that
   motivated it). Omit this section entirely if no audit fed
   the run.
8. **Implementation notes** (priority, format, cadence,
   linking).

Run stop-slop on every prose section (executive summary,
gap descriptions, cluster summaries, implementation notes)
before writing. Keyword tables and structured maps are
exempt — they're data, not prose.

### 4B. Backlog file

Write to `/rockstarr-ai/02_inputs/seo/backlog.md`. This file
is **canonical** — one per client. Each `seo-strategy` run
regenerates it completely. Prior strategy docs (the dated
files from 4A) preserve audit history; the backlog reflects
the latest plan.

Required front-matter:

```yaml
# ---
client_id: [from client.toml]
strategy_run_at: "ISO timestamp"
strategy_doc_source: "02_inputs/seo/strategy_<YYYY-MM-DD>.md"
audit_source: "02_inputs/seo/audit_<YYYY-MM-DD>.md or null if no audit was read"
total_items: 28
work_type_counts: { new: 24, refresh: 2, consolidate: 1, expand: 1 }
clusters:
  - { name: "Cluster A", role_count: { pillar: 1, supporting: 5 } }
  - { name: "Cluster B", role_count: { pillar: 1, supporting: 6 } }
  - { name: "Cluster C", role_count: { pillar: 1, supporting: 4 } }
  - { name: "Cluster D", role_count: { pillar: 1, supporting: 5 } }
quick_win_count: 10
produced_by: "rockstarr-content/seo-strategy@0.8.0"
# ---
```

Body structure: one section per cluster, items grouped by
role (pillar first, then supporting), each item formatted
as a structured block.

```markdown
# SEO content backlog — [Client name]

Last refreshed: [date]. Source strategy:
[strategy_<YYYY-MM-DD>.md].

This backlog feeds `ideate-topics` each month. Items here
are NOT in the monthly slate yet — `ideate-topics` picks
from this list and adds them to the month's
`content-topics_<YYYY-MM>.md` with `Pick: yes`. Status of
each item is inferred from the workflow files (drafts,
approved, published) — no mutations to this file are
needed beyond a full re-run via `seo-strategy`.

---

## Cluster 1: [Cluster name]

### [PILLAR] [Pillar page title]
- **Slug:** kebab-cased-pillar-slug
- **Work type:** new
- **Cluster role:** pillar
- **Cluster:** Cluster 1 — [Cluster name]
- **Target keyword:** [primary keyword]
- **Search intent:** Informational
- **Difficulty:** Medium
- **Word-count target:** 2500-4000
- **Quick win:** false
- **Supporting posts in cluster:**
  - [supporting-slug-1]
  - [supporting-slug-2]
  - ...
- **Notes:** [why this pillar matters for the client]

### [Supporting post title]
- **Slug:** kebab-cased-supporting-slug
- **Work type:** new
- **Cluster role:** supporting
- **Cluster:** Cluster 1 — [Cluster name]
- **Parent pillar:** [PILLAR] [Pillar page title] (slug: pillar-slug)
- **Target keyword:** [keyword]
- **Search intent:** Commercial
- **Difficulty:** Low
- **Word-count target:** 1200-1800
- **Quick win:** true ⭐
- **Notes:** [why this supports the pillar]

### [Refresh of an existing post] (audit-sourced)
- **Slug:** existing-post-slug-refresh-2026
- **Work type:** refresh
- **Existing URL:** https://CLIENT-DOMAIN/blog/existing-post/
- **Cluster role:** supporting
- **Cluster:** Cluster 1 — [Cluster name]
- **Parent pillar:** [PILLAR] [Pillar page title] (slug: pillar-slug)
- **Target keyword:** [keyword]
- **Search intent:** Informational
- **Difficulty:** Low
- **Word-count target:** [keep existing, add ~300-500]
- **Quick win:** true ⭐
- **Notes:** [audit finding — stale 2023 figures; what to update]

(repeat for each item in the cluster; `consolidate` and
`expand` items follow the same shape as the refresh block,
with their own suffixed slug and `existing_url`)

---

## Cluster 2: [Cluster name]

(same structure)

---
```

Every backlog item carries a unique `slug`. The slug is the
key that ties a backlog item to its eventual outline,
draft, approved, and published files (which all carry their
own slug field too). This is how `ideate-topics`
de-duplicates against the publish log and how the workflow
threads through.

### 4C. Note items already in the workflow

While writing the backlog, cross-check item slugs against:

- `05_published/_publish.log` — items already published.
- `04_approved/content/` — items approved, awaiting
  publish.
- `03_drafts/content/` — items currently being drafted.

If a backlog candidate slug already exists in any of those,
add a `**Already covered:** [status]` line under that
item's notes (don't drop it — the strategy doc still
benefits from showing the comprehensive plan, but the
backlog reader knows to skip it). `ideate-topics` filters
on this implicitly when it reads the workflow files.

## Phase 5: Verify and report

After writing both files:

1. **Item count check.** Confirm the strategy doc lists
   the same items as the backlog. Mismatches mean
   something got dropped between Phase 3 and Phase 4 —
   surface to the user.
2. **Cluster integrity check.** Every supporting post
   points to a pillar in the same cluster. Every pillar
   lists its supporting posts. Mismatches → fix or
   surface.
3. **Slug uniqueness check.** No duplicate slugs across
   the backlog.
4. **Fix-existing slug-safety check** (when fix-existing
   items exist). Every `refresh` / `consolidate` / `expand`
   item's slug must be suffixed (e.g. `-refresh-2026`) and
   must NOT equal any slug present in
   `05_published/_publish.log`. A fix-existing item whose
   slug matches a published slug would be silently filtered
   out by `ideate-topics` — surface and fix any that collide.
   Confirm each fix-existing item carries an `existing_url`.
5. **Quick win count check.** 8-12 quick wins total,
   distributed across clusters (no single cluster should
   monopolize quick wins).
6. **Already-covered count.** Note how many backlog items
   are already in publish_log / approved / drafts. If
   more than ~30% are already covered, the re-run is
   producing a lot of duplicate planning — surface to the
   user with a recommendation to scope tighter.

Print a one-paragraph summary in chat:

> Strategy run for [Client name]. [N] clusters, [N] total
> items in backlog ([N] pillar + [N] supporting),
> [N] quick wins flagged. Strategy doc:
> `02_inputs/seo/strategy_[YYYY-MM-DD].md`. Backlog:
> `02_inputs/seo/backlog.md`. `ideate-topics` will draw
> from this backlog on the next monthly run.

If items were flagged as already covered, list how many
in the summary so the user knows the strategy isn't
proposing 28 fresh topics — it's proposing 28 total of
which N are already in the workflow.

## Quality checklist

Before the final write, run this checklist on the
strategy doc and backlog. Surface any failures to the
user before saving.

1. Every keyword in the seed table maps to one of the 4-5
   clusters.
2. Every cluster has exactly one pillar page.
3. Every supporting post points to a parent pillar in the
   same cluster.
4. Internal linking plan is internally consistent (pillar
   lists supports; supports point at pillar + peers).
5. Every keyword recommendation passes the test "would
   the ICP person actually search for this?"
6. Pillar page titles are scoped, not encyclopedic.
7. Quick wins are 8-12 and span 2+ clusters.
8. The strategy doc's prose sections passed stop-slop.
9. Total backlog item count is 25-32 (more is fine for
   high-cadence clients; less means scope tighter).
10. Volume and difficulty estimates are noted as
    directional, not exact, with a recommendation to
    validate top picks in a paid SEO tool.

## What NOT to do

- Do NOT create ClickUp tasks. The backlog file is the
  production-tracking artifact in this stack. ClickUp is
  a Rockstarr-internal workflow detail, not a client-
  facing concern.
- Do NOT paraphrase external research findings into the
  client's voice. The strategy is upstream of voice; the
  client's first-party voice integrity rule continues
  to apply when downstream skills (outline-blog,
  draft-blog) draw from the backlog.
- Do NOT propose topics already in `05_published/`,
  `04_approved/`, or `03_drafts/`. Cross-check slugs
  before writing. If a candidate slug is already covered,
  flag it inline (`**Already covered:**`) and skip it
  from the active proposal count.
- Do NOT invent customer stories, named clients, or
  revenue figures in the strategy doc or implementation
  notes. The strategy is keyword + structure; the voice
  and proof-points come at outline / draft time.
- Do NOT generate fewer than 4 clusters. Authority builds
  through cluster depth — a single-cluster strategy is
  not a strategy.
- Do NOT generate more than 5 clusters. More than 5
  fragments the topical authority signal and dilutes
  internal-linking effectiveness.
- Do NOT mutate the canonical backlog file mid-month.
  Re-runs of `seo-strategy` regenerate it completely;
  in between runs, treat it as read-only. Status of
  individual items is inferred from workflow files, not
  written back here.
- Do NOT skip the WebFetch site analysis step. A strategy
  that doesn't know what the client's site already
  covers will propose duplicate topics.
- Do NOT skip the stop-slop pass on prose sections.
  Strategy docs that read like AI wrote them undermine
  the strategist's authority when the client reads them.
- Do NOT propose volumes or difficulty as exact numbers
  pulled from a tool. They're directional. Surface this
  in the strategy doc's notes so the human knows to
  validate top picks in Ahrefs / SEMrush before
  committing significant production effort.

## Related

- `rockstarr-content:seo-site-audit` — audits the existing
  site and writes `02_inputs/seo/audit_[YYYY-MM-DD].md`, whose
  content findings this skill folds into the backlog.
- `02_inputs/seo/strategy_[YYYY-MM-DD].md` — strategy doc
  output (audit trail, dated files preserved).
- `02_inputs/seo/backlog.md` — canonical backlog
  (single-file, regenerated per run).
- `rockstarr-content:ideate-topics` — reads the backlog
  monthly to populate the slate.
- `rockstarr-content:content-calendar` — sequences
  backlog-derived picks (pillar before supports within
  a cluster).
- `rockstarr-content:outline-blog` — uses cluster + parent
  pillar info from the backlog to default the internal
  linking plan.
- `rockstarr-infra/skills/_shared/references/blog-seo-geo.md`
  — the rules `outline-blog` and `draft-blog` enforce
  downstream of this skill's planning.
