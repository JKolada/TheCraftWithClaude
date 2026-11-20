# 11 — Data model and normalization

> Commandments V and VII at the root: the schema is the contract of the whole system. Normalize first;
> denormalize deliberately, with a named source of truth.

## Rules

1. **Controlled vocabularies live in lookup tables** (countries, types, tags) plus a `CHECK` where values are
   fixed — never free text in a column.
2. **Many-to-many goes through a junction table**, never `primary_x` + `secondary_x` columns.
3. **The stable identifier is the slug, not the numeric id.** Ids drift after merges; user data is mapped
   `slug → new id`, a missing slug is skipped and logged (→ [19](19-database-swap-runbook.md)).
4. **Active row instead of overwrite where history matters:** expire the old row (`expired_at`), insert the
   new one; a partial unique index (`WHERE expired_at IS NULL`) enforces one active row per key. Audit for free.
5. **Computed values are computed, not stored** (e.g. a display name from its parts) — stored, they drift.
6. **A cache or snapshot names its source of truth** and falls back to it when stale; never two sources for one fact.
7. **Migrations are forward-only and additive**, scripts gate on a column/table existing, and every data
   operation ends with `foreign_key_check` (→ [04](04-scripts-and-databases.md)).
8. **The schema is documented:** an ERD plus the allowed values of every controlled field, in `docs/`.
9. **Declared privacy is enforced by the model:** sensitive processing runs as a separate idempotent
   pipeline on **anonymized** data, with a test that re-identification is impossible (→ [09](09-law-and-protecting-the-creator.md)).

## Anti-patterns
- 🚫 Free text where a lookup belongs ("USA", "U.S.A.", "United States").
- 🚫 One fact stored in two places without synchronization.
- 🚫 User data mapped by a mutable id.
- 🚫 A stored computed value that drifts.
- 🚫 A destructive migration under running old code.
