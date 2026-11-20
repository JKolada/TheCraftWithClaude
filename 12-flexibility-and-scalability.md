# 12 — Flexibility and scalability

> The golden rule of altitude applied to architecture: change without a rewrite, grow without a rebuild —
> and scale only when a metric demands it, never "just in case".

## Rules

1. **Separate the layers by a contract, not by shared code:** data ↔ ingest ↔ web, bound by the schema
   (→ [11](11-data-model-and-normalization.md)) or an explicit API contract. Either side can then be replaced.
2. **Changes are additive and backward-compatible:** a new column, endpoint or language doesn't break what works.
3. **Feature flags arrive with the first risky change that reaches live users** — ship dark, then ramp.
   Not on Day 0 of a prototype; never skipped once real users are at risk.
4. **Keep the process stateless where you can**; sessions and state go to a store (→ [14](14-operational-resilience.md)).
5. **Platform is a recorded trade-off:** always-on VPS (fixed cost, no cold start) vs scale-to-zero (pay per
   use, cold start) — chosen by traffic profile and budget, written down as an ADR.
6. **Every cache has explicit invalidation** and a stated lifetime.
7. **Pipelines are composable and idempotent:** each stage runs alone, a re-run is safe (→ [04](04-scripts-and-databases.md)).
8. **Global product = i18n from the first commit**, not bolted on (→ [10](10-seo-and-translations.md)).
9. **Scale by the numbers:** SQLite → PostgreSQL, monolith → services, only when latency, cost or size measurably
   demand it — with an ADR (→ [13](13-performance-frontend-and-sql.md)).

## Anti-patterns
- 🚫 Microservices, Kafka or Kubernetes for a hundred users.
- 🚫 State in process memory that blocks restarts and scaling.
- 🚫 A big-bang rewrite instead of additive steps.
- 🚫 A risky change for live users with no flag and no ramp.
- 🚫 Migrating to PostgreSQL "just in case" while SQLite hasn't broken a sweat.
