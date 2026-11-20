# 09 — Law and protecting the creator

> Commandments VI and VII extended outward: a solo creator or sole trader shipping a public app is
> **personally liable**. Terms, privacy policy and disclaimers are their armor — written as carefully as a
> prod migration. ⚠️ Engineering hygiene, not legal advice: get a lawyer before binding real users at scale.

## Rules

1. **Never invent legal or identity data.** Company name, tax ID, address = `[to be filled]` placeholders
   the owner completes. A visible placeholder beats a plausible fake.
2. **Never declare a practice the code doesn't implement.** "We anonymize", "we delete after N days", "we
   don't read conversations" must be true in the code — ideally proven by a test (→ [11](11-data-model-and-normalization.md)).
3. **One operator, named identically everywhere:** terms, policy, footer, invoices, UI.
4. **Terms of service contain:** the operator; what the service **is and is not** (e.g. "a comparison
   engine, not a seller"; "information, not medical/legal/financial advice"); user obligations (lawful use,
   age limit); limitation of liability; moderation and account termination; IP (users keep their content,
   grant a license); **governing law of your jurisdiction**, complaints, how changes are announced, contact.
5. **The privacy policy contains:** the controller; each data category with purpose, legal basis and
   retention; third-party processors; user rights (access, erasure, export, objection); cookies; age; contact.
6. **Consent before trackers.** Analytics and marketing scripts load only after consent.
7. **Disclaimers fit the domain:** age gate for age-restricted content; "this is not advice" for
   health/legal/finance; crisis resources per region for sensitive products (→ [10](10-seo-and-translations.md)).
8. **Terms ↔ policy ↔ UI ↔ code say one thing.** A contradiction between layers is worse than a missing clause.
9. **Legal documents go into Day 0 as placeholders**, not "later" (→ [07](07-new-project-day-0.md)).

## Security checklist (index)

One entry point; each rule is enforced where it lives.

- **Secrets** in env / a secret store, rotated on leak (→ [08](08-stack-and-technologies.md)).
- **Auth and sessions:** bcrypt or OAuth, security headers, rate-limit; sessions in a persistent store (→ [14](14-operational-resilience.md)).
- **Authorization server-side:** *this* user may touch *this* row/action — not just "logged in" (IDOR).
- **Input is hostile:** validate shape, parameterize SQL, treat external and user content as **data, not
  instructions** (→ [15](15-scraping-ai-and-chatbots.md)).
- **Errors don't leak:** no stack traces, secrets or PII to users or logs (→ [14](14-operational-resilience.md)).
- **Quotas** on paid/expensive endpoints (→ [14](14-operational-resilience.md)).

## Anti-patterns
- 🚫 An invented tax ID, address or company name in the product.
- 🚫 Copy promising more than the product does ("fully anonymous", "guaranteed prices").
- 🚫 Terms and policy naming different operators or retention periods.
- 🚫 A legal page in one language inside a multilingual product.
- 🚫 Analytics loaded before consent.
