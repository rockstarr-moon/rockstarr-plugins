---
name: seo-site-audit
description: "This skill should be used when the user asks to \"run an SEO audit\", \"audit the client site\", \"audit the website\", \"check the SEO on the site\", \"do the site audit\", or \"find SEO issues\". Runs an impact-first, schema- and AI-search-aware audit of the client's existing website (the website_base_url in stack.md): indexability, on-page, structured data, local SEO, content and topical authority, GEO/AI-search visibility, and Core Web Vitals. Produces a prioritized findings doc at 02_inputs/seo/audit_[date].md (max 3 Critical items) plus a canonical audit_state.md punch-list for recurring rounds. The content-side findings feed seo-strategy, which folds refresh/consolidate/expand items into the backlog alongside net-new topics."
---

# seo-site-audit

Audit the client's *existing* website and produce a prioritized,
executable findings doc. This is the diagnostic counterpart to
`seo-strategy`: where `seo-strategy` plans the next two quarters of
content, this skill measures the current state of what's already
shipped and hands the content-relevant findings forward so the
strategy is grounded in reality, not a shallow homepage fetch.

> **Template convention.** Fenced code blocks below show `# ---`
> where YAML front-matter delimiters belong, to keep Cowork's
> SKILL.md parser from misreading them. **When writing the actual
> output file, emit real `---`, not `# ---`.**

## The one principle

An SEO audit is not a list of every flaw. It's a ranked list of the
five-to-ten changes that move the needle, plus the noise filtered
out. If the audit reads like a Lighthouse dump, it's wrong.

**Hard rule: no more than 3 items in Critical.** If you find ten
"critical" things, you haven't prioritized, you've listed.
Prioritization is the work.

## How this fits the content plugin

This skill is a deliberate stretch of rockstarr-content's
"pure content factory" posture. Like `seo-strategy`, it reaches the
open web (Googlebot-UA fetches, schema extraction, optional
PageSpeed API). That's sanctioned for the SEO lane only. The audit
produces two kinds of finding:

- **Dev / technical** (indexability, canonical, CDN cache, Core Web
  Vitals, structured-data markup, local SEO, backlinks) - a hand-off
  list for the client's developer. Content does NOT action these.
- **Content** (stale posts to refresh, cannibalization to
  consolidate, thin posts to expand, weak or missing topic clusters,
  site-wide FAQ/GEO gaps) - the subset that `seo-strategy` reads.

Both go in the audit doc. Only the content subset flows downstream.

## When to run

- **Onboarding** - audit the existing site before the first
  `seo-strategy` run so the initial backlog reflects what's already
  published, not just net-new ideas.
- **Quarterly** - re-audit before each quarterly `seo-strategy`
  refresh.
- **On demand** - "audit the site", "find SEO issues", a client
  concern about rankings or AI-search visibility.
- **Trigger phrases:** "run an SEO audit", "audit the client site",
  "do the site audit", "check the SEO", "find SEO issues".

## Preconditions

Tier 1 cheap existence checks first (per the
rockstarr-infra defer-expensive-preconditions pattern). Run these
before the anchor message; refuse fast if any fail:

- `/rockstarr-ai/00_intake/stack.md` exists and `website_base_url`
  is set. If not, point the user at `rockstarr-infra:capture-stack`.
  Without a URL there is nothing to audit.
- `rockstarr-infra/skills/_shared/stop-slop/` is available (the
  prose sections of the audit run through it).

Tier 2 reads (style guide, publish log, prior audit) happen inside
the work, after the anchor message - not as gatekeeping.

Network access to the open web is required for the fetch phases.

## Inputs

1. **`stack.md`** - `website_base_url` (the audit target) and any
   sub-paths or product URLs the client shared.
2. **`style-guide.md`** - read for context only, so the audit's
   prose reads like Rockstarr wrote it. Does not shape findings.
3. **`05_published/_publish.log`** if present - the slugs Rockstarr
   has published for this client. Cross-reference so content
   findings distinguish "Rockstarr-published" from "pre-existing
   client content".
4. **The prior audit** at `02_inputs/seo/audit_state.md` if present -
   the open punch-list from the last round. Recrawl before
   re-litigating; verify shipped fixes explicitly (see Phase 12).

## Workflow

Twelve phases. Skip phases that don't apply to the scope. Always run
Phase 0 first. The bundled scripts live under this skill's
`scripts/` directory.

### Phase 0 - Scope and intake (mandatory)

Before fetching anything, confirm via `AskUserQuestion` when
ambiguous:

1. **Deliverable scope?** Site-wide, top-pages-only, blog-only,
   technical-only, local-only, or GEO/AI-only.
2. **The client's actual concern?** "Not ranking for X", "AI search
   isn't citing us", "local pack invisible" - that focus sharpens
   the audit.
3. **What access exists?** WordPress admin, Search Console, a
   PageSpeed API key, an Ahrefs/Semrush seat. Note what's reachable;
   it dictates what can actually be checked.

### Phase 1 - Capture the surface

Fetch once, parse many. Use `scripts/fetch_site.py` to pull the
homepage, top money pages, sitemap, and robots.txt with a Googlebot
user agent into a working folder so later phases operate on cached
files.

```bash
python3 scripts/fetch_site.py https://CLIENT-DOMAIN/ --out /tmp/audit-[slug] \
  --extra services about contact blog
```

### Phase 2 - Indexability fundamentals

The "can Google crawl and index this at all" check. Nothing else
matters if these are broken. Run `scripts/check_indexability.py`:

```bash
python3 scripts/check_indexability.py https://CLIENT-DOMAIN/
```

It covers robots.txt sanity, sitemap freshness, canonical
self-reference, accidental noindex on money pages, http-to-https
single-hop, www canonicalization, and cache integrity across user
agents.

**Cache anomalies on the first fetch can mimic real bugs.** Always
re-verify with multiple UAs and a cache-buster before flagging
Critical. (A transient Cloudflare cache HIT was once mis-flagged as
Critical and had to be retracted - don't repeat it.)

### Phase 3 - On-page SEO

Run `scripts/extract_on_page.py` over the cached folder and look for
outliers - don't read pages by hand.

```bash
python3 scripts/extract_on_page.py /tmp/audit-[slug] --host CLIENT-DOMAIN
```

Look for: title length 50-60 chars with brand and primary keyword;
meta description 120-160 chars that sells the click; exactly one H1
per page matching intent; correct heading nesting (stat numbers,
button labels, and decorative elements should never be headings);
descriptive alt text on meaningful images and empty alt on
decorative ones; 5+ internal links per page; at least one external
authoritative outbound link on content pages for E-E-A-T.

### Phase 4 - Schema / structured data

The **highest-leverage technical work** most audits underweight. Run
`scripts/extract_schema.py` to catalogue the JSON-LD types per page:

```bash
python3 scripts/extract_schema.py /tmp/audit-[slug]
python3 scripts/extract_schema.py /tmp/audit-[slug] --type RealEstateAgent
```

Check per page type:

- **Local business** - a specific subtype (`RealEstateAgent`,
  `Dentist`, `LegalService`), not generic `Organization`. See
  `references/schema-localbusiness.md` for a ready-to-paste template.
- **Blog/article pages** - `Article` with a real author Person (not a
  WordPress account leak like "admin"), with `sameAs` to the author's
  LinkedIn.
- **Pages with FAQs** - `FAQPage`. The single highest-leverage move
  for AI-search citation rate. See `references/schema-faqpage.md`.
- **Step-by-step content** - `HowTo`.
- **Address, hours, social, breadcrumbs, site search** - covered in
  the references.

Validate fixes after deploy with the Google Rich Results Test.

### Phase 5 - Local SEO (skip if no geography)

If the client doesn't serve a specific geography, skip this phase.
Otherwise check: complete `LocalBusiness` schema (address,
telephone, geo, hours, priceRange, areaServed, sameAs); NAP
consistency across footer, schema, and Google Business Profile;
city/region keyword in titles and H1s on geo pages; one unique page
per location for multi-location businesses; a claimed, populated
Google Business Profile.

### Phase 6 - Content and topical authority

**This is the heart of what feeds seo-strategy.** It requires
judgment, not tooling. Catalogue:

- **Stale dated content** - year-in-URL or year-in-title older than
  12 months. Refresh, consolidate-and-301, or noindex. Don't delete.
  -> `work_type: refresh`.
- **Cannibalization** - multiple posts targeting the same keyword.
  -> `work_type: consolidate` (name the canonical destination and
  the 301 source).
- **Thin content** - under ~400 words, or below the topic's depth
  floor. -> `work_type: expand`.
- **Topical clustering** - is the blog a pillar/cluster model or a
  graveyard of one-offs? Gaps where no cluster covers an
  ICP-relevant topic -> `work_type: new` (a net-new pillar or
  support seo-strategy should plan).
- **Outdated facts**, **URL slug hygiene**, and **internal-linking
  pattern** (top-of-funnel linking down to bottom-of-funnel and back).

Tag every content finding with its `work_type` so Phase 11's
"Content findings for seo-strategy" table is a direct lift.

### Phase 7 - AI search visibility / GEO

GEO is governed by the canonical reference at
`rockstarr-infra/skills/_shared/references/blog-seo-geo.md` (the same
reference `outline-blog` and `draft-blog` enforce at draft time). Do
NOT keep a competing GEO checklist in this skill - read that one. Its
"GEO audit checklist" section lists the site-wide, diagnostic checks
this phase runs: site-wide FAQ-schema coverage, author-entity leaks
(author = "admin"), currency markers, TL;DR-at-top, direct-answer
patterns, named sources, and the AI-prompt citation tests.

Surface three to five specific GEO moves. Where they're
content-actionable (add an FAQ section, add currency markers), tag
them as `work_type: expand` on the relevant existing post so they
flow to seo-strategy too.

### Phase 8 - Performance / Core Web Vitals

Run PageSpeed Insights for mobile and desktop on the homepage plus
one heavy template page; note LCP, INP, CLS.

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2FSITE%2F&strategy=mobile&category=PERFORMANCE" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print({k:v.get('score') for k,v in d['lighthouseResult']['categories'].items()})"
```

The PSI API has a daily quota. If exhausted, infer from HTML signals
(head size, render-blocking script count, native lazy-load, image
formats). Pick the top 3 issues that would move LCP/INP measurably -
not a 50-item list. This is a dev hand-off finding, not a content one.

### Phase 9 - Backlinks (only if tool access)

If Ahrefs/Semrush/Moz access exists: referring-domain trend, toxic
links, lost links in the last 90 days, anchor distribution,
top-linked pages. If no access, note as "not audited - requires
backlink tool access". Don't fabricate findings. Dev/off-page, not
content.

### Phase 10 - Synthesis and prioritization

Sort every finding into four buckets:

| Bucket | Definition | Treatment |
|---|---|---|
| **Critical** (max 3) | Active SEO harm right now | Fix this week |
| **High** | Significant opportunity, under 1 hour each | This month |
| **Medium** | Best-practice, modest impact | This quarter |
| **Low** | Polish that won't move rankings | Backlog |

**Hard rule again: no more than 3 items in Critical.** Add an
execution table (owner, timeframe, items). Add "What's working"
(3-5 bullets) at the top and "What I did NOT check" at the bottom.

### Phase 11 - Delivery

Use `assets/audit-template.md` as the structure. Write to
`/rockstarr-ai/02_inputs/seo/audit_[YYYY-MM-DD].md`. If a file with
the same date exists, append `-2`, `-3` - never overwrite a prior
audit (the dated files are the audit trail, like `seo-strategy`'s
dated strategy docs).

Front-matter:

```yaml
# ---
client_id: [from client.toml]
client_name: [from client.toml]
audit_date: "YYYY-MM-DD"
website_url: "from stack.md"
scope: "site-wide | top-pages | blog-only | technical-only | local-only | geo-only"
critical_count: 3
content_findings_count: 9
produced_by: "rockstarr-content/seo-site-audit@0.8.0"
produced_at: "ISO timestamp"
feeds: "02_inputs/seo/backlog.md (via seo-strategy)"
# ---
```

Required body sections, in order: TL;DR (top 3-5); What's working;
Fixed since last pass (recurring rounds only); Critical (max 3);
High; Medium; Low; **Content findings for seo-strategy** (the
`work_type`-tagged table); What I did NOT check; Suggested execution
order; Pages audited; Sources used.

**Run stop-slop** on the narrative sections (TL;DR, What's working,
each finding's rationale prose) before writing, per the plugin's
mandatory final pass. The data tables (per-page table, the
content-findings table, execution order, pages audited) are
structural artifacts and are exempt.

### Phase 12 - Recurring audit hygiene

State lives in the **client workspace**, not in personal memory.

- At session end, write or update the canonical
  `/rockstarr-ai/02_inputs/seo/audit_state.md` with the open
  punch-list: which findings shipped (resolved), which are still
  open, and the date of this recrawl. One file per client,
  overwritten each round - it mirrors how `backlog.md` is canonical.
- On the next round, **recrawl before drafting**. Don't re-litigate
  fixes the client shipped between rounds.
- Verify wins explicitly and mark them in the "Fixed since last
  pass" section. Momentum matters.

## How this informs seo-strategy

`seo-strategy` reads the newest `02_inputs/seo/audit_*.md` when one
exists (and is recent). It uses the **Content findings for
seo-strategy** table to:

- Seed `backlog.md` items with `work_type: refresh | consolidate |
  expand` for existing posts, alongside the usual `work_type: new`
  topics.
- Ground the competitor-gap analysis in the site's real topical
  coverage rather than a single homepage fetch.

**Slug rule for downstream safety:** refresh / consolidate / expand
items get their OWN unique backlog slug (e.g. a `-refresh-YYYY`
suffix), never the published post's slug. `ideate-topics` filters
backlog items whose slug appears in the publish log; reusing the
published slug would silently drop the refresh from monthly
ideation. Each such item carries an `existing_url` pointer to the
post it acts on. The audit is optional input - `seo-strategy` still
runs without one (its older shallow Phase 1A site analysis), so this
is purely additive.

## Common mistakes (red flags in your own draft)

1. Lighthouse-dump audits - 50 unprioritized items.
2. Generic recommendations ("improve your meta descriptions") instead
   of a specific page, element, and fix.
3. Claims you can't verify (no Search Console access, but asserting
   search-performance numbers). Note as out-of-scope.
4. Missing the cache/CDN check - some of the worst problems live at
   the edge, not in the HTML.
5. Skipping schema - the highest-leverage technical work.
6. No execution plan - without an owner/timeframe table, nothing
   ships.
7. Auditing the wrong site - confirm the URL against `stack.md`.
8. Over-investing in performance - a missing LocalBusiness schema
   usually moves rankings faster than shaving 200ms off LCP.
9. Treating first-fetch anomalies as live state without re-verifying.
10. Forgetting `work_type` tags - then the content findings can't
    feed seo-strategy.

## Sanity checklist before writing

- [ ] All findings re-tested against the live site within the hour
- [ ] No more than 3 items in Critical
- [ ] Each finding names the specific page, element, and fix
- [ ] Each content finding carries a `work_type` tag
- [ ] "What's working" at top, "What I did NOT check" at bottom
- [ ] Prose sections passed stop-slop
- [ ] Written to `02_inputs/seo/audit_[date].md` (date in filename)
- [ ] `audit_state.md` updated with the open punch-list
- [ ] Recurring client: prior round's wins explicitly verified

## Bundled resources

- `scripts/fetch_site.py` - homepage + top pages + sitemap + robots
  with Googlebot UA into a working folder.
- `scripts/check_indexability.py` - Phase 2 fundamentals.
- `scripts/extract_on_page.py` - title/meta/heading/alt/link/schema
  extraction across cached HTML.
- `scripts/extract_schema.py` - JSON-LD parsing and type cataloguing.
- `assets/audit-template.md` - the canonical output structure.
- `references/schema-localbusiness.md` - LocalBusiness/RealEstateAgent
  JSON-LD template.
- `references/schema-faqpage.md` - FAQPage JSON-LD template.

GEO checks are NOT bundled here - they read the canonical
`rockstarr-infra/skills/_shared/references/blog-seo-geo.md`.

## Related

- `rockstarr-content:seo-strategy` - consumes this audit's content
  findings into `02_inputs/seo/backlog.md`.
- `rockstarr-content:ideate-topics` - draws monthly picks from the
  backlog (including audit-sourced refresh/expand items).
- `rockstarr-infra/skills/_shared/references/blog-seo-geo.md` - the
  canonical SEO/GEO reference, including the GEO audit checklist.
- `rockstarr-infra:capture-stack` - sets `website_base_url`.
