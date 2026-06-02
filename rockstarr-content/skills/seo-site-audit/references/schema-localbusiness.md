# LocalBusiness / RealEstateAgent schema reference

The single highest-leverage technical fix for any local-business client. Generic `Organization` schema is not a local-business signal — Google treats it as a catch-all and the local pack ignores it.

## When to use which @type

- **LocalBusiness** — generic catch-all if no specific subtype fits.
- **RealEstateAgent** — real estate brokerages, agents, agencies.
- **Dentist** — dental practices.
- **LegalService** — law firms.
- **MedicalBusiness** — medical practices (use child types when fitting).
- **Restaurant** — restaurants.
- **Store** — retail.
- **ProfessionalService** — accounting, consulting, IT services.

Pick the most specific subtype. Schema.org's full LocalBusiness subtype tree: https://schema.org/LocalBusiness

## Template — RealEstateAgent

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "@id": "https://CLIENT-DOMAIN/#localbusiness",
  "name": "FULL LEGAL BUSINESS NAME",
  "legalName": "FULL LEGAL BUSINESS NAME",
  "description": "One-sentence description that includes the city and the service.",
  "url": "https://CLIENT-DOMAIN/",
  "logo": "https://CLIENT-DOMAIN/path/to/logo.png",
  "image": "https://CLIENT-DOMAIN/path/to/featured-image.jpg",
  "telephone": "+1-XXX-XXX-XXXX",
  "email": "info@CLIENT-DOMAIN",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "STREET",
    "addressLocality": "CITY",
    "addressRegion": "ST",
    "postalCode": "ZIP",
    "addressCountry": "US"
  },
  "areaServed": [
    { "@type": "City", "name": "PRIMARY CITY" },
    { "@type": "City", "name": "SECONDARY CITY" },
    { "@type": "AdministrativeArea", "name": "GREATER METRO" }
  ],
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "contactType": "customer service",
      "telephone": "+1-XXX-XXX-XXXX",
      "email": "info@CLIENT-DOMAIN",
      "areaServed": "US",
      "availableLanguage": ["English"]
    }
  ],
  "founder": {
    "@type": "Person",
    "name": "FOUNDER NAME",
    "honorificSuffix": "CCIM",
    "jobTitle": "Principal Broker & President",
    "url": "https://CLIENT-DOMAIN/about/",
    "sameAs": ["https://www.linkedin.com/in/founder-linkedin-slug/"]
  },
  "sameAs": [
    "https://www.linkedin.com/company/company-slug/",
    "https://www.facebook.com/company-page/",
    "https://maps.google.com/business-profile-short-url"
  ],
  "knowsAbout": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ]
}
```

## Field-by-field — what matters

- `@id` — use a stable URL fragment like `#localbusiness`. Helps Google deduplicate when the schema appears on multiple pages.
- `name` — the legal business name as it appears in your Google Business Profile. Inconsistency between schema name and GBP name is a local-SEO leak.
- `address` — **all five fields required.** ISO codes (`"TX"`, `"US"`) are preferred over long forms but both work.
- `geo` — optional but recommended. Use Google Maps to get accurate lat/lng.
- `priceRange` — `"$"` reads as fast-food / dollar-store pricing. For professional services use `"$$"` or `"$$$"`.
- `openingHoursSpecification` — actual hours, not plugin defaults. Verify with the client; SmartCrawl/Yoast defaults are often wrong (e.g., 9pm close instead of 5pm).
- `areaServed` — geographic areas the business serves. Each as a separate `City` or `AdministrativeArea` object.
- `founder` — useful for E-E-A-T. Include `honorificSuffix` for any earned credentials (CCIM, JD, MD, PhD).
- `sameAs` — full URLs to social profiles and Google Business Profile. Empty array is fine; fake URLs are worse than missing.

## How to deploy on WordPress + SmartCrawl

1. **SmartCrawl Pro → Schema → Types Builder → Add New Type**
2. Pick **Local Business** as the parent type.
3. Pick the appropriate **Sub Type** (e.g., Real Estate Agent).
4. Give it a clear name (e.g., "REMAX Tomball office").
5. **Location** rule: usually "Show Globally" so it appears on every page.
6. After saving, **Expand item** to fill the Postal Address, Opening Hours, and any other field that defaults to "Schema Settings." Switch each to "Custom Value" and enter the real data.

Verify after deploy:
- Fetch the homepage with `curl` and grep for `"RealEstateAgent"`.
- Run https://search.google.com/test/rich-results on the live URL.
- Confirm zero warnings, all expected types detected.

## Common mistakes

1. **Defaults left in place.** SmartCrawl/Yoast schema defaults are often wrong — particularly opening hours (`closes: 21:00` is a common default) and priceRange (`$`).
2. **Generic Organization instead of LocalBusiness subtype.** Halves the local-SEO benefit.
3. **NAP inconsistency.** Address/phone in schema must match the footer, Google Business Profile, and major directories exactly.
4. **`@type: "Organization"` AND `@type: "LocalBusiness"` both emitted.** Use one. If you need both for some reason, give them distinct `@id` values.
5. **Missing the `@id`.** Without a stable `@id`, Google can't dedupe across pages.
6. **`sameAs` linking to social profiles that don't exist.** Triple-check the URLs resolve to actual profiles.
