# 10 — SEO and translations

> Commandment III applied to visibility: indexable, complete in every language, measured — not "probably OK".
> Standard on-page SEO (unique title and description, canonical, sitemap, `robots.txt`, one `h1`, clean
> slugs, OG cards) is assumed; these are the rules that are easy to get wrong.

## Rules

1. **Multilingual = reciprocal `hreflang` for every language pair + `x-default`.** Without it the search
   engine serves the wrong language.
2. **Language completeness is a failing test:** a missing key or page in any language breaks the build (→ [03](03-testing-and-verification.md)).
3. **Legal and UI pages exist in every language you ship** (→ [09](09-law-and-protecting-the-creator.md)).
4. **Programmatic pages need quality guards** (minimum items, ratings, sources) and a hand-written intro —
   a thin page generated at scale is spam.
5. **YMYL topics (health, money, safety) demand E-E-A-T:** named author and operator, cited sources, no
   regulated advice — a disclaimer and a crisis path instead.
6. **The register is part of the translation:** correct but cold copy is a bug. Machine translation is fine
   for the skeleton; **a human reviews disclaimers, crisis messages and legal copy.**
7. **RTL languages mirror the whole layout**, not just the text.
8. **Measure what converts** (Search Console, anonymized analytics) and let it pick the next page to write.
9. **Core Web Vitals are a ranking signal** → measure and fix (→ [13](13-performance-frontend-and-sql.md)).

## Anti-patterns
- 🚫 Keyword stuffing; thin programmatic pages.
- 🚫 A multilingual site without `hreflang`.
- 🚫 Unreviewed machine translation of sensitive copy.
- 🚫 An English-only legal page in a multilingual product.
