# LinkedIn article editor — formatting recipes + gotcha catalog

The reusable engine for driving LinkedIn's article/newsletter
editor via Chrome MCP. Every gotcha below caused a real failure
during the first production run of the newsletter workflow. This
reference exists so subsequent runs avoid them.

This is a reference, not a skill. `publish-linkedin-newsletter`
reads it; the procedural flow (what to do when) lives in that
skill's SKILL.md.

---

## The editor

- New article URL: `https://www.linkedin.com/article/new/`
- The body is a single `contenteditable="true"` element.
- After a newsletter is scheduled, the page resets to a fresh
  `/article/new/` state — but the publishing target resets too
  (see gotcha #1).

---

## Applying formatting via execCommand (preferred)

Driving the Style dropdown through clicks is slow, layout-shift
sensitive, and occasionally drops events. Use
`document.execCommand` directly via the Chrome MCP
`javascript_tool`.

```js
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();

// Apply a block format to the paragraph whose text matches `target`.
// blockType: 'h2' = Heading, 'h3' = Subheading, 'blockquote' = quote
function applyBlock(target, blockType) {
  const para = [...editor.querySelectorAll('p')]
    .find(p => p.textContent.trim() === target);
  if (!para) return false;
  const range = document.createRange();
  range.selectNodeContents(para);
  range.collapse(true);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  return document.execCommand('formatBlock', false, blockType);
}

applyBlock('What "one platform" means here.', 'h2');
applyBlock('One knowledge base.', 'h3');
applyBlock('The chatbot interface is a phase. What stays...', 'blockquote');
```

Ordered / unordered lists — select a span of paragraphs first:

```js
const paras = [...editor.querySelectorAll('p')];
const firstP = paras.find(p => p.textContent.startsWith('Content: long-form'));
const lastP  = paras.find(p => p.textContent.startsWith('Ops: CRM hygiene'));
const range = document.createRange();
range.setStartBefore(firstP);
range.setEndAfter(lastP);
const sel = window.getSelection();
sel.removeAllRanges();
sel.addRange(range);
document.execCommand('insertOrderedList');   // or 'insertUnorderedList'
```

Bold / italic — select a Range, then
`document.execCommand('bold')` / `'italic'`.

Verify after formatting (and confirm zero em dashes survived):

```js
({
  h2: editor.querySelectorAll('h2').length,
  h3: editor.querySelectorAll('h3').length,
  blockquotes: editor.querySelectorAll('blockquote').length,
  ol: editor.querySelectorAll('ol').length,
  ul: editor.querySelectorAll('ul').length,
  emDashes: (editor.textContent.match(/—/g) || []).length, // must be 0
});
```

---

## Gotcha catalog

### 1. Publishing target resets to "Individual article"

Every fresh `/article/new/` page after the first one defaults to
publishing as an **Individual article**, NOT to the newsletter.
Posting an edition as an individual article instead of the
newsletter is a major drift.

Verify the top-left of the editor reads the newsletter, e.g.:

```
[Author name] ▾
[Newsletter name truncated]...
```

If wrong: click the dropdown next to the author name → under
"Publish as" select the author (radio at the right of the row) →
under "Publish to" select the newsletter. Re-check on EVERY
edition, even mid-batch.

### 2. Leading "1. " on a subheading triggers an auto-list

LinkedIn's editor auto-converts a line starting with "1. " into a
numbered list and grabs every paragraph that follows. If the
source article numbers its subsections ("1. Positioning",
"2. Audience..."), type the H3s WITHOUT the numbers — the
Subheading style provides hierarchy. (25 paragraphs got
accidentally listed on one edition before this was caught.)

### 3. Time field — triple_click, never cmd+a

To set the schedule time, click the Time field and use
`triple_click` to select the existing value, then type the time
(e.g. "07:00 AM") and click the suggestion in the dropdown.

**Never use `cmd+a` in the Time field.** If the click misses the
input by a few pixels and lands on the parent dialog, `cmd+a`
selects the entire intro-post text — and the typed time replaces
it. The intro post is wiped silently; the schedule still goes
through with an empty post body. `triple_click` is scoped to the
field and cannot escape to the post body. (This wiped two
editions before it was understood.)

### 4. Back / Escape inside the schedule dialog = Discard

The "Back" button on the schedule dialog sits right next to
"Next". Misclicking it (or pressing Escape inside the dialog)
triggers a "Discard draft" prompt. If "Discard draft" appears,
click **"Go back"**, never "Discard" — Discard wipes the whole
article AND the post.

### 5. Single newline between paragraphs

Use a single `\n` between paragraphs, not `\n\n`. Double newlines
create empty paragraphs in LinkedIn's editor, showing as visible
whitespace gaps.

### 6. Clock icon, not Publish

To schedule, click the **clock icon** at the bottom-right of the
Next dialog — NOT the blue "Publish" button (which publishes
immediately).

### 7. Long-body type timeouts

Bodies over ~1500 words sometimes hit the type tool's 30-second
timeout. The text usually completes despite the error. Wait 5
seconds, screenshot, and verify via JS before assuming failure.

### 8. Cover image preview check

After clicking Next, the dialog should show the cover image
prominently below the "Tell your network..." field. If you see
only an article-card preview with a small thumbnail, the cover
wasn't uploaded — close with X, re-upload, retry.

### 9. Auto-linked phrases

LinkedIn sometimes auto-links plain-text phrases to a search-
results URL. Usually harmless. If flagged, find via JS and unlink.

### 10. The 90-day scheduling cap

LinkedIn refuses to schedule more than ~90 days out. Past the cap,
the calendar may not let you select the date or the submission
fails. Stop at the cap and report which editions weren't
scheduled — they go in the next batch.

---

## Em-dash transformation map (safety net)

In the Rockstarr pipeline the article body comes from an
already-approved, already-stop-slopped draft, so it should carry
zero em dashes at source. Keep the verify-zero check (above) as a
safety net. If an em dash is found (e.g. when transcribing
older published copy), strip it inline using this map:

- Em dashes bracketing a list of items → wrap the list in
  parentheses. "the work — drafting, queuing, reporting — is" →
  "the work (drafting, queuing, reporting) is"
- Em dashes bracketing an aside / appositive → commas. "people
  who matter — the people in whose name — will" → "people who
  matter, the people in whose name, will"
- Trailing / explanatory em dash → colon. "It tries to do it:
  press a button..." (was "do it — press a button...")
- One-off em dash before an elaboration → comma. "stance, one we
  made explicit" (was "stance — one we made explicit")
