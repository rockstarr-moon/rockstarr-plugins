---
title: "Chrome MCP clicking convention"
purpose: "Canonical rule for HOW to click when a Rockstarr skill drives a web app through Chrome MCP. Click gated action controls with REAL coordinate clicks; reserve javascript_tool for reading and non-gated DOM work. Prevents the silent-click-failure class that breaks Sales Nav / LinkedIn flows, worst on Windows."
applies_to: "Every skill in any Rockstarr plugin that drives a browser through Chrome MCP — outreach (both variants), social, the content LinkedIn-newsletter publish lane, and any future browser-driving skill."
read_by:
  - "rockstarr-outreach-salesnav (daily-connect, send-scheduled-messages, book-meeting, send-approved-reply, register-campaign/crawl-lead-list)"
  - "rockstarr-outreach-interceptly (send-message, apply-label, book-meeting-interceptly, process-inbox, and the rest of the daily loop)"
  - "rockstarr-social (invite-page-followers, li-comment-check)"
  - "rockstarr-content (publish-linkedin-newsletter, verify-linkedin-newsletter)"
do_not_fork: true
---

# Chrome MCP clicking convention

When a skill drives a web app through Chrome MCP, **how** it clicks
matters as much as **where**. This reference is the canonical rule.
Skills reference it; they do not restate the rationale.

## The rule

**Click gated action controls with a REAL click** — the Chrome MCP
`computer` / click tool (e.g. `left_click`) or a `find`-then-click.
Cowork issues these as real Chrome DevTools Protocol mouse events
(`Input.dispatchMouseEvent`): a trusted event (`isTrusted = true`)
with the full hover → mousedown → mouseup → click sequence at the
element's location.

The property that matters is **trusted vs synthetic**, not *how you
located the control*. Prefer locating by accessible name / role via
`find` (robust to layout changes) over hard-coded pixel coordinates;
either way the click itself is a real CDP event. (Some skills, e.g.
rockstarr-social's, sensibly forbid raw pixel coordinates and locate
by accessible name — that's fully consistent with this rule.)

**Reserve `javascript_tool` for non-click work:**

- Reading and extraction — querying the DOM, reading text / attributes
  / accessible names, counting elements, pulling a sheet's data.
- Non-gated DOM operations — `scrollIntoView`, reading an input's
  value, hydration polling.
- Rich-text formatting on a `contenteditable` (e.g.
  `document.execCommand('formatBlock' | 'bold' | 'insertOrderedList')`)
  where you are formatting text, not activating an app button.

A "gated action control" is anything the web app treats as a real
user action: Connect, Send, Invite, Submit, Post, a "…" overflow
menu, a menu item inside it, a dialog's primary button, a tab that
loads data, a row/name that opens a preview.

## Why — two failure modes, one fix

1. **Trusted-event gating.** A synthetic JS click —
   `element.click()` or `element.dispatchEvent(new MouseEvent('click'))`
   — produces an UNtrusted event (`isTrusted = false`). LinkedIn and
   Sales Nav (and many SPAs) gate their real actions (Connect, Send,
   the overflow menu) on trusted pointer events, so a synthetic click
   **fails silently** — the DOM looks clicked, nothing happens. This
   is worst on Windows. (Surfaced by a client running
   rockstarr-outreach-salesnav on Windows — ClickUp AI-176. Their
   Cowork environment moved Chrome MCP to real CDP clicks and the
   whole flow started working: side preview opens → in-preview
   overflow → Connect → Send → Pending.)

2. **Stale element refs.** Refs captured from `read_page` /
   `browser_snapshot` go stale in a long-running SPA session — by the
   third or fourth action the captured node is detached and the click
   lands nowhere. A real coordinate click clicks a **live screen
   position**, not a captured ref, so it sidesteps this too.

A real CDP coordinate click fixes **both**. A pure-JS click fixes only
(2) and reintroduces (1) — which is why the old "pure-JS one-shot
click" workaround is deprecated as a primary method.

## Discipline that still applies

- **Re-locate immediately before clicking.** Take a fresh screenshot /
  `find` and click the current position. Never click a coordinate or
  ref captured more than one action ago in a fast-mutating SPA.
- **Verify the effect, every time.** Gated clicks can still miss
  (overlay, layout shift, timing). After the click, confirm the
  expected state change — the modal opened, the row now reads
  "Pending", the composer cleared — before treating it as done.
  Synthetic-click failures are silent; don't assume success.
- **Match trusted UI strings exactly,** including non-ASCII. Sales
  Nav's confirmed-send marker is `Connect — Pending` with an em-dash
  (U+2014); a regex with an ASCII hyphen produces false negatives on
  every confirmed send.

## Fallback ladder

1. **Real coordinate click** (primary) — re-locate, then click the
   live position.
2. **Fresh `find` + coordinate click** — if the control can't be
   located from the current view, re-find it and click; still a real
   click.
3. **JS click — last resort only,** and only for a control that is
   genuinely not reachable by coordinate (rare). If you fall back to a
   JS click on a gated control, **log that you did** and **verify the
   action actually took effect** — it may register on the DOM without
   the app acting on it.

## What this does NOT change

- `javascript_tool` for reading/extraction stays the right tool — it's
  fast and precise for pulling data (e.g. the `gviz` sheet read, row
  hydration polling, degree-badge reads).
- `execCommand` for contenteditable formatting stays fine — that's
  text formatting, not an app-button activation.
- Pacing, page-refresh, session-confirm, and per-app skip rules are
  unchanged — this reference is only about the click mechanism.
