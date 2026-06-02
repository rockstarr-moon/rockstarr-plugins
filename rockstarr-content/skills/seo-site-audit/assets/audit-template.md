# {CLIENT_NAME} — SEO Site Audit

**Site:** {SITE_URL}
**Brand:** {BRAND_REFERENCE}
**Audit date:** {YYYY-MM-DD}
**Auditor:** Rockstarr AI (rockstarr-content/seo-site-audit)
**Time budget honored:** ~{N} hours
**Last recrawl:** {YYYY-MM-DD HH:MM}

> **Feeds seo-strategy.** The content-side findings in this audit
> (stale posts to refresh, cannibalization to consolidate, thin
> posts to expand, weak/missing topic clusters, site-wide
> FAQ/GEO gaps) are read by `rockstarr-content:seo-strategy` on
> its next run and folded into `02_inputs/seo/backlog.md` as
> `work_type: refresh | consolidate | expand` items alongside
> net-new topics. The dev/technical findings below are a
> hand-off list for the client's developer — content does not
> action them.

---

## TL;DR — top {3-5} things to fix first

1. **{Critical #1 headline}.** {One paragraph: evidence, why it matters, what to do.}
2. **{Critical #2 headline}.** {Same shape.}
3. **{Critical #3 headline if applicable}.** {Same shape.}

---

## What's working well

Three to five bullets. Forces a look at strengths before the fix list, and softens the tone.

- **{Strength 1}** — short evidence.
- **{Strength 2}** — short evidence.
- **{Strength 3}** — short evidence.

---

## Fixed since first pass of this audit (recurring rounds only — verified on recrawl)

- ✅ **{Resolved item 1}.** Verified at {URL or location}.
- ✅ **{Resolved item 2}.** Verified at {URL or location}.

---

## CRITICAL — fix this week

Max **three** items. If a finding doesn't qualify as actively-harmful right now, move it down to High.

### 1. {Headline}

**Evidence:** {what you saw on the live site, with quotes / counts / file paths}

**Why it matters:** {one or two sentences on the actual SEO impact}

**Action:** {specific steps a dev can execute. Not "improve X" — specific commands or settings.}

### 2. {Headline}

…

### 3. {Headline}

…

---

## HIGH — fix this month

### 4. {Headline}

{Evidence + action.}

### 5. {Headline}

…

---

## MEDIUM — fix this quarter

### N. {Headline}

…

---

## LOW — nice-to-have

### N+1. {Headline}

…

---

## What I did NOT check (and why)

- **Backlink profile** — would need Ahrefs/Semrush/Moz API access.
- **Google Search Console data** — {note access status}.
- **Google Business Profile** — audit separately.
- **Mobile rendering / Core Web Vitals field data** — {PSI quota state}.
- **Form / conversion path** — out of scope for SEO; covered by the website-messaging product.

---

## Suggested execution order

| Owner | Day | Items |
|---|---|---|
| Dev / host | Today | {Critical-rank items} |
| Dev / WP | Within a week | {High-rank} |
| Content | Within 2 weeks | {Content rewrite items} |
| Dev / WP | Within a month | {URL slugs, typos, brand consistency} |
| Dev / WP | Within a quarter | {Performance, alt text, SearchAction, schema fields} |
| Content | Next 6 weeks | {External-source links, schema email, etc.} |

---

## Pages audited

| Page | Status |
|---|---|
| `/` (Home) | 200 — issues #{n}, #{n}, #{n} |
| `/services/` | 200 — issues #{n}, #{n} |
| `/who-we-are/` | 200 — issues #{n} |
| `/contact-us/` | 200 — issues #{n} |
| {…rest of audited pages…} | … |

---

## Content findings for seo-strategy

The subset of the findings above that `seo-strategy` consumes.
Each row becomes a backlog item with the given `work_type`.

| work_type | Existing URL / slug | Finding | Suggested action |
|---|---|---|---|
| refresh | {url} | {stale dated content, outdated facts} | {what to update} |
| consolidate | {url} + {url} | {cannibalization / duplicate intent} | {canonical destination + 301 source} |
| expand | {url} | {thin content under target depth} | {sections / FAQ / sources to add} |
| new | (none) | {topical-authority gap — no cluster covers X} | {pillar or supporting piece to create} |

---

## Sources used

- robots.txt: {URL}
- Sitemap index: {URL}
- Post sitemap: {URL}
- Page sitemap: {URL}
- Client style guide: 00_intake/style-guide.md
- Stack: 00_intake/stack.md (website_base_url)
