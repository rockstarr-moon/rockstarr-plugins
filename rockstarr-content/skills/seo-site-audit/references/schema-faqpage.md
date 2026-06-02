# FAQPage schema reference

The single highest-leverage move for AI-search citation rate. ChatGPT, Perplexity, Google AI Overviews, and Claude search all preferentially cite content that's structured as `FAQPage`.

## When to use

Add `FAQPage` schema to any page (blog post, service page, FAQ landing) that contains 3+ question-and-answer pairs. Even adding short FAQ sections to existing pages just to enable this markup is high-ROI.

## Template

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://CLIENT-DOMAIN/PAGE-PATH/#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Exact question text as it appears on the page",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Direct-answer-first response. Lead with the answer, then explain. Keep under 200 words per answer."
      }
    },
    {
      "@type": "Question",
      "name": "Second question",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Same shape."
      }
    },
    {
      "@type": "Question",
      "name": "Third question",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Same shape."
      }
    }
  ]
}
```

## Field-by-field

- `mainEntity` — array of `Question` objects. Order matches the visible page order.
- `name` (on Question) — **must match the visible question text verbatim**. Google penalizes mismatches.
- `acceptedAnswer.text` — must match (or closely mirror) the visible answer text. Don't write a different answer just for schema.

## Patterns that work for AI citation

1. **Direct-answer-first.** Lead each answer with the punchline. Don't bury it.
2. **Named sources, not generic phrasing.** "According to the U.S. Census Bureau" beats "studies show."
3. **Currency markers.** "As of 2026" or "Updated [date]" — AI engines downgrade undated content.
4. **Specific numbers.** "Houston's industrial absorption rate hit 14.2M sq ft in Q1 2026" beats "Houston's industrial market is strong."
5. **Plain language.** Conversational tone beats jargon. AI engines extract clearer prose more reliably.

## How to deploy on WordPress + SmartCrawl

1. **SmartCrawl Pro → Schema → Types Builder → Add New Type**
2. Pick **FAQ Page** as the type.
3. **Location** rule: target the specific page (Post = "Why Houston Is a Top Market for Industrial Real Estate Investment").
4. Inside the type editor, add a Question/Answer pair for each FAQ on the page.

Or, if SmartCrawl's UI is too clunky for many FAQs:

5. Use a Custom JSON+LD block scoped to that page.
6. Paste the full JSON-LD from the template above.

Verify after deploy:
- Fetch the page with `curl` and grep for `"FAQPage"`.
- Run https://search.google.com/test/rich-results on the live URL.
- Look for the "FAQ" rich result preview.

## Common mistakes

1. **Schema doesn't match visible text.** Google compares the schema's `name` and `text` against the rendered page. If they diverge, the rich result is suppressed.
2. **Only 1–2 Q&A pairs.** FAQPage needs at least 3 to be eligible for rich results.
3. **Marketing copy disguised as FAQ.** "Why are we the best?" → "Because we're great." is not a real FAQ. Google's manual review team is good at spotting this.
4. **Stuffing keywords into questions.** "What is the best Houston commercial real estate broker for industrial property?" is too long and unnatural. Use real questions users ask.
