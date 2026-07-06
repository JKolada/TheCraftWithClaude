# 05 — Git and Deployments

> Commandments II, VI, VII, VIII, IX. The densest chapter, because a mistake here is the most expensive.

## Git — two habits for most tasks

### A. Search the history BEFORE you implement
```bash
git log --oneline -- <path>           # history of a file/directory
git log -S"symbol" --oneline          # pickaxe: where a symbol/flag/column was born
git log -G"regex" --oneline           # commits whose DIFF matches the regex
git log --grep="word" --oneline       # search commit messages (that's where features are described)
git blame <file> -L a,b               # who/when/why
git show <commit>                     # the full change + context
```
Combine this with a grep over the tree + the directory's `AI_README.md`. History + code + docs = the full
picture in a minute. It pays off with: unfamiliar code, a hunch of "haven't we done this
already?", a column/flag of unknown origin, dating a regression, and before every refactor.

### B. A clean, coherent `git status`
- **Separate unrelated changes** into distinct commits (one topic = one commit).
- **Catch junk early:** `.bak`, temp files, accidental databases (`web/_Proj…db`),
  a file named `-w` from a botched `curl`. Add the patterns to `.gitignore` (note: gitignore
  **has no inline comments** — put the `#` on its own line).
- **Tell a real diff from CRLF noise:** `git status` shows a file as changed but
  `git diff HEAD` is empty → it's only EOL, not work. Don't commit the noise.
- **Orphans (uncommitted work in the background)** — in a project run across multiple sessions
  ("user + Claude"), other sessions leave changes in the tree. Before a deploy: is this real, complete
  work (commit/confirm it), or a WIP/experiment (leave it)? **Don't sweep someone else's uncommitted work
  into a deploy without confirmation.**

### What finishes a commit
- Messages in English, descriptive (what + why), `fixes #N`/`refs #N` to the issue.
- Link the PR/issue with the full URL, not "PR #123".

## Coordinating parallel work: issues and simple branches

> **This doctrine is written for a project run by ONE developer with AI — not an enterprise team.** But
> "solo" no longer means "one writer": a single developer routinely runs **several Claude sessions at
> once** on the same repo (a fix in one, a feature in another, a review in a third). That is already a
> multi-writer situation — and here the "second party" is usually **another agent session**, not a human
> teammate. So the moment you go past one live session you need the same two things a team does: a
> **shared task list** (issues) and **lightweight branching** — so parallel sessions don't step on each
> other, don't sweep each other's half-finished work, and "who's doing what" stays visible. Read the
> rest of this section with that lens: **"the other session" wherever it says "teammate"**, and the
> hazards below (unpushed commits, a merge that sweeps another session's work, orphaned WIP in the tree)
> are things that bite a *solo* developer the instant a second Claude session is open on the same repo.

### Issues = units of work (one source of "what and why")
- **One task = one issue.** Title = the outcome ("Cart drops items after refresh"), body = context,
  acceptance criteria, links. This is where the **why** lives — not in your head, not in chat.
- **The issue number ties the work together:** branch, commits (`refs #N`), PR, and discussion.
  `fixes #N` in the PR **closes** the issue on merge (→ "What finishes a commit").
- **Issue before code** for anything non-trivial or someone else's report — so scope and decision are
  written down before a diff exists. Small, concrete issues > one big "epic for everything".
- **The backlog is a list, not memory.** Labels (`bug`/`feat`/`chore`, priority); close what's stale.
  An issue dead for weeks = a decision to make (do it / drop it), not a zombie.

### Simple branches (parallel sessions, trunk-based)
- **`main` is always deployable.** With more than one live session, don't commit straight to `main` —
  it's the shared table holding what goes to prod.
- **A short branch per task:** `feat/NN-cart`, `fix/NN-login` (NN = issue number). It lives
  **hours–days, not weeks** — the longer it lives, the more painful the merge.
- **A small PR > a big PR.** One topic, reviewable in fifteen minutes. Nobody reads a giant PR
  carefully — it passes "on trust", i.e. without review.
- **Merge, then delete the branch.** Once it's in `main`: delete the branch, pull `main`, start the
  next one fresh. Stale branches are debt and a lie about the project's state.
- **Know what a merge ships — diff BEFORE you merge into the deploy branch.** A merge brings **every**
  commit on the source branch, not just yours — including work **other sessions** already merged there.
  So before a release/merge into your always-deployable branch: `git log <deploy-branch>..<source> --oneline`
  and read the list. For an **urgent, isolated fix**, **cherry-pick that one commit** onto a clean deploy
  branch instead of full-merging a shared integration branch you haven't vetted — a blind merge can sweep
  an unfinished feature to prod riding behind your fix. This is the committed-work sibling of the
  uncommitted-**orphans** rule above: both are "don't ship what you didn't mean to."
- **A cherry-pick across diverged branches isn't clean either — verify the RESULT, not the intent.** When
  the target lacks context the commit's parent had, cherry-pick falls back to a 3-way merge and can pull in
  **neighbouring hunks** from the source branch — e.g. a mount for a file that doesn't exist on the target
  (`require("./routes/feed")` → `MODULE_NOT_FOUND` at boot → prod 502). After ANY cherry-pick to a deploy
  branch: `git diff <deploy-base> HEAD --stat` **and read the app-wiring diff** — it must show ONLY your
  change. A "10 files, +320" that includes one stray `app.use(require(...))` is the tell.
- **Sync with `main` often** (merge/rebase into your branch) — small, frequent conflicts instead of
  one giant conflict at the end.

### Branching grows with the project — don't start at the top
Match the workflow to where the project actually is; escalate only when a real trigger forces it:

1. **Solo, no live users → just `main`.** Commit straight to it, with discipline. No branches, no ceremony —
   the simplest thing that works (→ [12](12-flexibility-and-scalability.md): don't over-engineer).
2. **First production deploy (even solo) → short branches that merge straight to `main`.** Now `main` *is*
   "what's live", so keep it **always-deployable**: do each change on a `feat/`/`fix/` branch, review the
   diff, merge to `main`, tag the deploy (→ *Tag every deploy*). Trunk-based, no long-lived branches.
3. **Project grows / more people / parallel streams → add `develop` + a `preproduction` environment.**
   Feature branches merge into **`develop`** (integration); a release goes `develop → main`. Deploy to a
   **`preproduction` that is a copy of production** (same schema, config, a realistic data sample) and verify
   there **before** prod — the last gate that catches "works in dev, breaks in prod".

Each rung is added **when a metric forces it** (real users → 2; a teammate or parallel work → 3), never
preemptively. Don't run a three-environment GitFlow for a solo prototype — and don't stay on bare `main`
once real users depend on it.

> **Review isn't a formality — it's a second pair of eyes before prod.** On a team every PR has a
> reviewer; solo, the "reviewer" is a deliberate second pass over the diff (and Claude as devil's
> advocate). A change lands on `main` reviewed, not "because it works on my machine".

### Anti-patterns
- 🚫 Committing straight to `main` while someone else is in the project → their work lands on a half-done state.
- 🚫 A long-lived "my big refactor" branch → merge hell and weeks of drift from `main`.
- 🚫 Working without an issue → scope and the "why" vanish; a month later nobody knows why it exists.
- 🚫 `fixes #N` in a commit to a work branch → the issue closes prematurely (the **PR/merge** closes it, not every commit).
- 🚫 An "everything at once" PR → review becomes fiction, regressions slip through.
- 🚫 Merging a shared/integration branch into the deploy branch **without diffing it first** → someone
  else's merged-but-not-ready work rides your fix to prod. `git log <deploy>..<source>` before every
  merge-to-deploy; cherry-pick an isolated urgent fix instead of sweeping the whole branch.

## Deployments — THE OVERRIDING POLICY

> ⛔ **Never deploy to prod automatically.** `git pull` on the server, `pm2 reload`,
> a database swap, `migrate.py` on prod, the maintenance flag — **only when the user says so
> explicitly** ("ship it", "deploy"). You may **proactively propose** a deploy when it's ready — but
> you wait for an explicit "yes". Commit + push on request is **not** a deploy. This rule beats "auto mode".

### The deploy ships `origin/<branch>`, not your local branch — verify it's pushed FIRST
A deploy script pulls **`origin/<branch>`** on the server; it never sees your laptop's working copy.
So committed-but-**unpushed** work does not ship — most dangerously in a **shared repo where a
parallel session committed to the branch but hasn't pushed**. You deploy, the server pulls the older
`origin` tip, and the "latest changes" are silently absent (a renamed label still shows the old text,
a new feature isn't there). Before every deploy: `git fetch && git log origin/<branch>..<branch>` —
if it's **non-empty**, your (or someone's) local commits aren't on `origin` yet; `git push` first (a
clean fast-forward when the branch only moved forward), then deploy. The reverse, `git log
<branch>..origin/<branch>`, catches the opposite — `origin` moved ahead of you (the parallel session
pushed) and you're about to deploy a *stale* tree; pull before you act. In one line: **reconcile local
⇄ origin before a deploy, because the server only ever sees `origin`.**

### Boot-check on the target BEFORE you reload
A require-time error (a missing module, a bad import) only surfaces when the process **boots** — and
`pm2 reload` boots the new code by killing the old. So the crash lands on your users as a 502. Gate the
reload: after `git pull`, boot the new code in a **throwaway** process first —
`node -e "require('./src/app')"` (guard `app.listen` behind `require.main === module` so this doesn't bind
the port) — and `pm2 reload` **only** if it prints your OK marker. If it throws, the running process is
untouched (prod stays up on the old code) and you fix forward with zero downtime. Do this on the **target**
(real `node_modules` + env), not your laptop — a worktree without `node_modules` gives a false "it boots".

### Two deploy types
- **Code-only (no migrations/dependencies)** → zero-downtime: `git pull` + **boot-check** + `pm2 reload`.
- **With a migration/dependency change/database swap** → a **maintenance window** (nginx flag → 503 +
  branded page), a few seconds of downtime, a guarantee the app isn't running on a half-migrated schema.

### Tag EVERY deploy
```bash
git tag -a deploy-$(date +%F) -m "What goes to prod: <one sentence>"   # -2/-3 for the next one that day
git push --tags
```
- What's live: `git describe --tags --abbrev=0 --match 'deploy-*'`.
- Rollback of code: `git checkout <deploy-tag> && pm2 reload`.
- Rollback of schema: restore the backup (forward-only!).

### A changelog with every deploy
A public "What's new" — **in plain language, no jargon** (no scraper/migration/commit). Write
**what the user gains**. Bump the `updated:` date. It's part of the deploy checklist, not optional.

---

## Rehearse the deploy: dev → preprod → prod

> A migration or a database swap tested for the **first time** in the prod maintenance window is tested **on
> your users.** The fix is a rung between your laptop and prod: a **preprod** that is a faithful copy of prod,
> where you run the *exact* runbook **once before you run it for real.**

**Three environments, three jobs:**
- **dev** (your machine) — throwaway/seed data, or an **anonymised refresh from a prod backup** when you need
  realistic data shapes to reproduce a bug. Fast, disposable, no users.
- **preprod** — a real **server clone of prod**: same OS, nginx, `pm2`, TLS — but no live users,
  **basic-auth gated** and **noindex**. Its one job is **rehearsing migrations and the deploy itself.**
- **prod** — sacred. Touched only on an explicit "deploy", and only with steps you've already run on preprod the same day.

**Build preprod from prod the same way every time** (script it → [04](04-scripts-and-databases.md)):
- clone the repo using **prod's own deploy key** (private-repo auth without minting new credentials);
- refresh the database from a **prod backup**, and **anonymise PII before it leaves prod** (emails, names →
  tombstones) — a non-prod box must never hold real user data (→ [09](09-law-and-protecting-the-creator.md));
- make environment-specific values **env-overridable, never hard-coded:** `SITE_URL`/canonical/OG must point
  at preprod, so it neither leaks prod URLs nor gets the staging box indexed (→ [10](10-seo-and-translations.md)).

**Then rehearse the real runbook on preprod** — not a simplified version: run `migrate.py`, **time the
window**, smoke-test, confirm the migration is **forward-only and idempotent** (→ [04](04-scripts-and-databases.md)).
A migration that fails on preprod is a Tuesday; the same failure on prod is an incident with users on a 503.

**Gotchas only a *real* preprod surfaces** (a fake one won't): the ACME/Let's-Encrypt `http-01` challenge must
**bypass the basic-auth gate** or cert renewal 401s; a private repo needs its SSH remote wired before the first
`pull`; canonical/OG/sitemap must be env-gated or preprod emits prod links. You want to hit these on the box
**nobody is using** — not discover them mid-deploy.

> **Preprod is a rehearsal stage, not a second prod.** No live users, a stale/anonymised DB is fine, and **its
> database is never swapped back into prod.** The moment you treat it as authoritative you've created a second
> source of truth to keep in sync (→ [11](11-data-model-and-normalization.md)).

## Database swap preserving accounts — the runbook (the hardest operation)

A full swap of the prod database (e.g. a local catalog with all the work) **while preserving live
accounts**. This is where most of the traps lie. Lessons from the reference project:

### Rules that save user data (Commandment VII)
1. **"Users" is many tables, not one `users`.** Enumerate **every** table with an FK to the
   user: accounts, carts, reviews, likes, badges, games, chat (sessions +
   messages + limits), feedback, sessions. Map a table without `user_id` (e.g. `chat_messages`)
   through its parent (`session_id`). Gate each one on the existence of the column/table.
2. **Map by a STABLE key (slug), not by ID.** `product_id` drifts between
   databases after merges — a user's review must land via `slug → new_id`, and a missing
   slug is **skipped and logged**, not pushed in blindly.
3. **The source of truth for accounts is LIVE prod**, not an old snapshot — so you don't lose
   registrations from the last hour. Run the migration **in the maintenance window, after `pm2 stop`**,
   reading the stopped, consistent prod database.
4. **FK-safe order**: WIPE children before parents, INSERT parents before children
   (e.g. `reviews` before `review_likes`; `chat_sessions` before `chat_messages`).
5. **Back up live prod BEFORE the swap** (`.backup replaced-prod-<ts>.db`) — that's your rollback.
6. **Verify the merged database**: account count = prod, 0 dangling reviews (slug-remap OK),
   `integrity_check: ok`, FK violations ≤ the pre-existing state (no more).
7. **Sessions are separate, ephemeral state — don't mix them into the swapped database.** Keep the session
   store in a **separate file** (e.g. `sessions.db`) from the catalog database you sometimes swap wholesale —
   otherwise the swap zeroes out logged-in users. An in-process memory store logs everyone out on **every**
   restart/deploy and leaks memory (→ [14](14-operational-resilience.md)).

### The sequence (non-invasive phase → window → finalization)
**Phase 1 (the service is live):**
- push code to GitHub;
- **copy gitignored images/assets separately** (rsync or tar-over-ssh, **not** through git),
  BEFORE the window — they're inert until you swap the database. Send only the delta (count what's missing).
- pre-upload a clean catalog snapshot to the server (`/tmp`).

**Phase 2 (maintenance window, a dozen-odd seconds), atomically (`set -e`):**
`flag ON → git pull → pm2 stop → back up live prod → migrate-users (source = prod) →
swap the file (rm wal/shm, mv, PRAGMA journal_mode=WAL) → pm2 start → SMOKE TEST → flag OFF`.

**Phase 3:** tag `deploy-…-2` + push, FB/SEO re-scrape if applicable, clean up `/tmp` and local temp.

### Smoke test after the swap (before you drop the flag)
Via `localhost` (bypasses the nginx maintenance): home/catalog/detail → 200, og:image →
the right file, redirects (e.g. merged → 301 to the survivor), numbers in the database (accounts/records),
**`pm2 logs` for errors**. If you find a trivial, safe bug — fix it in the window and ship it
(commit → pull → reload) instead of releasing a known 500.

### Gitignored assets and the deploy
Images/files that are in `.gitignore` **don't ride along with `git pull`**. Either sync them
(rsync/tar) or generate them on the server (if it has the tooling). In the reference project the call was
**to copy from local**, because the server has no Pillow and the swap changes the catalog.

## Anti-patterns
- 🚫 Auto-deploy / "it's ready, so I'm shipping it".
- 🚫 A swap "except accounts" = only `users` → loss of reviews/badges/chat.
- 🚫 Mapping user data by ID instead of slug → reviews land on the wrong product.
- 🚫 A migration on an old snapshot → loss of fresh registrations.
- 🚫 No deploy tag → "what's live?" becomes a guessing game.
- 🚫 Deploying without reconciling local ⇄ `origin` → the server pulls `origin` and your (or a parallel session's) **unpushed** commits never ship; `git log origin/<branch>..<branch>` before every deploy.
- 🚫 Transferring 1.5 GB of assets **inside** the maintenance window → long downtime (do it before the window).
- 🚫 Sessions in a swapped database (or in process memory) → the deploy logs everyone out.
- 🚫 A deploy-script invariant left untested — e.g. `$(date)` expanded once at file-creation time
  (so every backup overwrites the same file). Lock the deploy script's invariants down with a test.
- 🚫 A migration's **first run** is the prod maintenance window → you're debugging on users; rehearse it on preprod.
- 🚫 Preprod holding **real, non-anonymised** user data → a second copy of your PII liability on a less-guarded box.
- 🚫 Preprod **indexed by search engines / emitting prod URLs** → duplicate content + leaked staging (env-gate `SITE_URL`, noindex, basic-auth).

> **The runbook is the memory of incidents, not your head.** Every prod failure → an entry in the runbook
> with a date and a numbered lesson (e.g. "never SCP a live `.db` — use `.backup`; WAL holds fresh pages").
> The next swap reads the runbook, doesn't repeat the mistake (→ [06](06-collaboration-and-memory.md), [14](14-operational-resilience.md)).

## Shared infrastructure
Projects can share a single **Hetzner VPS**: static sites (a `dist/` build) go via
`scp`/`rsync` + an nginx vhost; Node apps via `git pull` + `pm2 reload` behind
nginx. One server = a shared `backups/` directory and the same habits (deploy tag, maintenance
flag). A new project on the same box: a separate vhost + a separate directory, the same rules.

## In practice
Deploy the critical path (e.g. login) with a test and a full smoke (registration, login,
logout, session persistence). At the first real user traffic, set up immediately: a nightly database
backup, deploy tagging, a branded maintenance page. → [03](03-testing-and-verification.md)
