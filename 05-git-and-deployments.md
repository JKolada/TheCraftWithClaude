# 05 — Git and deployments

> Commandments II, VI, VIII, IX. Git is the project's memory and the undo button for everything else;
> the deploy policy is where a mistake costs the most. Rehearsal on preprod → [18](18-release-rehearsal.md);
> prod database swap → [19](19-database-swap-runbook.md).

## Git habits

1. **Search the history before you implement:**
   ```bash
   git log -S"symbol" --oneline     # where a symbol/flag/column was born
   git log -G"regex" --oneline      # commits whose diff matches
   git log --grep="word" --oneline  # commit messages
   git blame <file> -L a,b          # who/when/why
   ```
2. **Keep `git status` clean.** One topic per commit. Junk (`.bak`, temp files, stray databases) goes to
   `.gitignore` early (`#` comments on their own line). A file shown as changed with an empty
   `git diff HEAD` is CRLF noise, not work — don't commit it.
3. **Orphans:** uncommitted work you didn't write (another session's) is **never swept into your commit or
   deploy** without confirmation — ask whether it's finished work or an experiment.
4. **Commit messages in English**, what + why, `refs #N` / `fixes #N`.

## Undo: you probably didn't lose it

Committed work is recoverable; git remembers every position a branch held (~90 days). **Commit early** — a
commit is free, private until pushed, and is your save point.

| Situation | Way back |
|---|---|
| Wrecked a file, not committed | `git restore <file>` |
| Undo the last commit, keep the work | `git reset --soft HEAD~1` |
| Committed on the wrong branch | `git branch <right>` here, then `git reset --hard HEAD~1` on the wrong one |
| Deleted a branch / "lost" commits | `git reflog` → find the hash → `git branch <name> <hash>` |
| A merge went wrong (not pushed) | `git reset --hard ORIG_HEAD` |
| Need a file as it was | `git show <commit>:<path>` · `git restore --source=<commit> -- <path>` |

Only three commands destroy work — and only **uncommitted** work: `git reset --hard`, `git restore .` /
`git checkout .`, `git clean -fd`. Git has no dry-run for them: **committing first is the dry-run** (→ IV).

## Parallel work: issues and short branches

"Solo" is still multi-writer: one developer routinely runs **several Claude sessions** on one repo. The
"other party" is usually another session — read "teammate" as "the other session".

1. **One task = one issue**: title = outcome, body = context + acceptance criteria. The issue number ties
   branch, commits and PR together; the **PR/merge** closes it, not a work-branch commit.
2. **Short branches** (`feat/NN-cart`, `fix/NN-login`) living hours–days; small PRs; merge, delete, sync
   with `main` often.
3. **Diff before merging into the deploy branch** — a merge ships *every* commit on the source, including
   other sessions' work: `git log <deploy>..<source> --oneline`. An urgent isolated fix is **cherry-picked**.
4. **After any cherry-pick, verify the result:** `git diff <deploy-base> HEAD --stat` must show only your
   change — a 3-way fallback can drag in a neighbour's hunk (a stray `require` → boot crash → 502).
5. **One concurrent session = one `git worktree`**, never two sessions in one checkout (→ [16](16-driving-claude.md)).

**Branching grows with the project — add each rung when a metric forces it:**
1. Solo, no live users → just `main`, committed to with discipline.
2. First production deploy → every change on a short branch, reviewed, merged to an always-deployable `main`, deploy tagged.
3. More people / parallel streams → `develop` for integration, releases `develop → main`, verified on a
   preprod copy of prod first (→ [18](18-release-rehearsal.md)).

Every change reaches `main` reviewed — solo, the reviewer is a deliberate second pass over the diff.

## Deployments — the overriding policy

> ⛔ **Never deploy to prod automatically.** Pull on the server, reload, migration, database swap, the
> maintenance flag — **only on the user's explicit "deploy".** You may propose a deploy; you wait for the
> yes. Commit and push are not a deploy. This rule beats any auto mode.

1. **The server deploys `origin/<branch>`, not your laptop.** Before every deploy: `git fetch`, then
   `git log origin/<b>..<b>` (unpushed commits → push first) and `git log <b>..origin/<b>` (another session
   pushed → pull first).
2. **Boot-check on the target before reloading:** after the pull, start the new code in a throwaway process
   (`node -e "require('./src/app')"`, with `listen` behind `require.main === module`); reload **only** on
   its OK marker. A crash then leaves the old process serving.
3. **Two deploy types.** Code-only → pull + boot-check + zero-downtime reload. Migration / dependency change
   / database swap → a **maintenance window** (branded 503 page) so nothing runs on a half-migrated schema.
4. **Tag every deploy:** `git tag -a deploy-$(date +%F) -m "<what goes live>"` + `git push --tags`.
   What's live: `git describe --tags --abbrev=0 --match 'deploy-*'`. Code rollback = checkout the tag +
   reload; schema rollback = restore the backup.
5. **Every deploy updates the public changelog** in plain language — what the user gains.
6. **Every prod incident becomes a dated, numbered lesson in the runbook** (`docs/`), read before the next
   deploy (→ [14](14-operational-resilience.md)).
7. **First real users = a nightly database backup, deploy tags and a branded maintenance page — all on day one of traffic.**

## Anti-patterns
- 🚫 Auto-deploy, "it's ready so it goes".
- 🚫 Deploying without reconciling local ⇄ `origin` — unpushed commits silently don't ship.
- 🚫 Merging a shared branch into the deploy branch without reading what it brings.
- 🚫 A long-lived "big refactor" branch; an "everything at once" PR.
- 🚫 Working without an issue — the "why" is gone a month later.
- 🚫 No deploy tag — "what's live?" becomes guesswork.
- 🚫 A deploy-script invariant with no test (`$(date)` expanded once → every backup overwrites the same file).
