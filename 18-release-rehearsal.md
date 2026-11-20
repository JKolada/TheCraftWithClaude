# 18 — Rehearse the release: dev → preprod → prod

> Commandments V and VI: a migration or a database swap run for the **first time** in the prod
> maintenance window is tested on your users. Run the exact runbook once on a faithful copy first.

## Three environments, three jobs

| Environment | Job | Data |
|---|---|---|
| **dev** (your machine) | build, reproduce bugs | seed data, or an **anonymised** refresh from a prod backup |
| **preprod** (server clone of prod: same OS, web server, process manager, TLS) | rehearse migrations and the deploy itself | anonymised prod backup; **basic-auth gated, `noindex`** |
| **prod** | serve users | sacred — touched only on "deploy", only with steps rehearsed on preprod the same day |

Add preprod when the project reaches the third branching rung or the first risky migration (→ [05](05-git-and-deployments.md)).

## Rules

1. **Build preprod from prod the same way every time — scripted:** clone with prod's deploy key; refresh the
   database from a prod backup; **anonymise PII before it leaves prod** (→ [09](09-law-and-protecting-the-creator.md)).
2. **Environment-specific values are env-overridable, never hard-coded:** `SITE_URL`, canonical, OG, sitemap
   point at preprod — otherwise preprod leaks prod URLs or gets indexed (→ [10](10-seo-and-translations.md)).
3. **Rehearse the real runbook, not a simplified one:** run the migration, time the window, smoke-test,
   confirm it is forward-only and idempotent (→ [04](04-scripts-and-databases.md)).
4. **Expect the gotchas only a real preprod surfaces:** the ACME/Let's Encrypt `http-01` challenge must
   bypass basic-auth or renewal fails with 401; a private repo needs its SSH remote before the first pull.
5. **Preprod is a rehearsal stage, never a second prod:** no live users, a stale DB is fine, and **its
   database is never swapped back into prod** (→ [11](11-data-model-and-normalization.md)).

## Anti-patterns
- 🚫 A migration whose first run is the prod maintenance window.
- 🚫 Real, non-anonymised user data on preprod — a second copy of your PII liability on a weaker box.
- 🚫 Preprod indexed or emitting prod URLs.
- 🚫 Treating preprod's data as a source of truth.
