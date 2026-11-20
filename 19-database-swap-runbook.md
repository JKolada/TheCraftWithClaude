# 19 — Database swap runbook

> Commandment VII at its hardest: replace the prod database wholesale (e.g. a rebuilt catalog) **while
> keeping every live account and everything users created.** Rare — and where most traps are.

## Rules that save user data

1. **"Users" is many tables.** Enumerate **every** table with a foreign key to the user (accounts, carts,
   reviews, likes, badges, sessions, chat sessions + messages + limits, feedback…). A table without
   `user_id` is mapped through its parent. Gate each on the table/column existing.
2. **Map by a stable key (slug → new id), never by the old id.** A missing slug is skipped and logged.
3. **The source of truth for accounts is live prod**, read after `stop` inside the maintenance window — not an
   older snapshot that loses the last hour's registrations.
4. **FK-safe order:** delete children before parents, insert parents before children.
5. **Back up live prod right before the swap** (`.backup replaced-prod-<ts>.db`) — that is the rollback.
6. **Verify the merged database:** account count = prod, 0 dangling references, `integrity_check: ok`, FK
   violations not above the pre-existing level.
7. **Sessions live in their own store** (e.g. `sessions.db`), never in the swapped database and never in
   process memory — otherwise the swap or any restart logs everyone out (→ [14](14-operational-resilience.md)).

## Sequence

1. **Live phase:** push the code; copy git-ignored assets **before** the window (rsync / tar over ssh, only
   the delta) — they don't ride with `git pull`; upload the new snapshot to the server.
2. **Window (seconds, atomic, `set -e`):** flag ON → pull → stop → back up live prod → migrate users
   (source = prod) → swap the file (remove `-wal`/`-shm`, move, re-enable WAL) → start → **smoke** → flag OFF.
3. **Smoke via `localhost`** (bypasses the maintenance page): key pages 200, redirects, row counts, process
   logs clean. A trivial, safe bug found in the window is fixed in the window — don't release a known 500.
4. **After:** tag the deploy, clean temp files, write the lessons into the runbook (→ [05](05-git-and-deployments.md)).

## Anti-patterns
- 🚫 A swap "except accounts" that only keeps the `users` table — reviews, badges and chat are lost.
- 🚫 Mapping user data by id — reviews land on the wrong product.
- 🚫 Migrating accounts from an old snapshot.
- 🚫 Moving gigabytes of assets inside the window.
- 🚫 `scp` of a live `.db` — use `.backup`; WAL holds the fresh pages.
