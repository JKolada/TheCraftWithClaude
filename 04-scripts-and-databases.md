# 04 — Scripts and databases

> Commandments IV and V: *dry-run is the default; the backup is the rollback.*

## Scripts

1. **Dry-run by default.** A data-changing script prints the plan (what, how many rows, where); a deliberate
   `--execute` writes.
2. **Idempotent.** Running it twice yields the same state (`INSERT OR IGNORE` / `UPSERT`).
3. **Print what you did *not* do** — truncation, sampling, skipped rows. Silence reads as "covered everything".
4. **Catalog-mutating operations stay out of automatic pipelines** (dedup, merge): dry-run → review → `--execute` by hand.
5. **The environment is written in `CLAUDE.md`** — interpreter, variables, venv. The agent doesn't guess.
6. **Absolute paths when a value crosses tools.** `/tmp` means one place to Git Bash, another to Python on
   Windows, a third to PowerShell — each tool then reads a *different file*. Pass fully-qualified paths; when
   a run "did nothing", print `os.path.abspath(p)` / `pwd -W` and compare.

## Databases and migrations

1. **Forward-only migrations.** No down-migrations; rolling back the schema = restoring the backup.
2. **Back up before every schema/data change on prod**, with a timestamp and a retention window:
   `sqlite3 data/app.db ".backup backups/pre-deploy-$(date +%F_%H%M%S).db"`
3. **Snapshot with `.backup` / `VACUUM INTO`, never `cp`/`scp` of a live database** — WAL makes the copy inconsistent.
4. **Additive before destructive.** `ADD COLUMN` is safe; `DROP`/`RENAME` waits for a later deploy, once no
   running code reads the column.
5. **Check integrity after every data operation:** `integrity_check`, `foreign_key_check`, row counts. Tell
   pre-existing noise (present before and after) from a regression (new violations).
6. **Rehearse a bulk or irreversible mutation on a fresh prod copy** — a dry-run shows the plan, not the
   outcome. `.backup` prod → run on the copy → check counts, integrity and the tricky cases → then prod.
   The deploy-level sibling of this rule → [18](18-release-rehearsal.md).

## Anti-patterns
- 🚫 A mutating script without `--dry-run`.
- 🚫 A migration deployed without a backup "because it's additive".
- 🚫 Dropping a column running code still reads.
- 🚫 `cp app.db` while the server runs.
- 🚫 A catalog-mutating step wired into the automatic pipeline.
