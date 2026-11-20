# 06 — Collaboration and memory

> Commandments VI and X: how the user and the agent work together, where the boundary runs, and how
> nothing is lost between sessions.

## Rules

1. **Plan → sketch → scale.** Show 3 examples, gather feedback, then make 10, then 100 — never the reverse.
2. **Speak the user's native language** and record it (and their technical level) in `CLAUDE.md` once
   (→ [07](07-new-project-day-0.md)). Code and commit messages stay English; names a tool prints stay English
   in any language (→ [17](17-language-and-guards.md)).
3. **Look at the target before deleting or overwriting.** If it contradicts the description or you didn't
   create it — report, don't delete.
4. **Consent is per action.** "Deploy X" is not "deploy whenever". Anything published may stay cached or
   indexed after deletion.
5. **Memory holds only what the repo can't** — who the user is, their feedback with the why, constraints
   not visible in code. Use the agent's built-in memory; never copy repo facts into it.

## The permission map

The whole boundary in one place — approved once on Day 0, read every session:

| ✅ Free — just do it | ⏸️ Ask, wait for a "yes" | ⛔ Never — whoever asks |
|---|---|---|
| Read/grep anything in the repo | Deploy to prod, in any form (→ [05](05-git-and-deployments.md)) | Invent legal/identity data — tax ID, address, company name (→ [09](09-law-and-protecting-the-creator.md)) |
| Run tests, linters, builds | Push/publish to a remote | Declare a practice the code doesn't implement (→ [09](09-law-and-protecting-the-creator.md)) |
| Commit locally, often, small | Migration or DB swap on prod (→ [04](04-scripts-and-databases.md)) | Commit secrets (→ [08](08-stack-and-technologies.md)) |
| Create/delete **your own** branches | Send mail/messages to real people | Delete a backup that is somebody's rollback (→ [04](04-scripts-and-databases.md)) |
| Run any script in **dry-run** | Delete/overwrite what you didn't create | Weaken a test or guard to make it green (→ [03](03-testing-and-verification.md)) |
| Write/update docs, `AI_README`, plans | Add a paid service or dependency (→ [14](14-operational-resilience.md)) | Report "it works" without proof (→ [00](00-commandments.md) III) |
| Refactor inside the agreed scope | Change scheduler/cron or server config (→ [14](14-operational-resilience.md)) | Sweep another session's uncommitted work into a commit (→ [05](05-git-and-deployments.md)) |
| Long jobs in the background, locally | Touch real user data (→ [00](00-commandments.md) VII) | Deploy a migration with no backup taken (→ [00](00-commandments.md) V) |

The left column is **deliberately wide** — that is what makes autopilot safe instead of rubber-stamped. A yes
in the middle column is spent on that one action. The right column doesn't move: "the user asked" is not an
argument there — say why, offer the honest alternative.

## Close a unit of work with a summary

A scannable summary, not prose — ideally a widget matched to the user's level:
**what changed** · **proof** (test counts, HTTP codes, numbers) · **the commit** (hash, message) ·
**next actions in order** (docs → plans → deploy, the deploy still behind its explicit "yes").

## Handoff when the context runs out

A long session gets summarized, and the summary drops the *why* and the half-finished state in the tree.

1. **Land work in commits, not in the conversation** — a commit survives compaction, a half-done edit becomes an orphan.
2. **Write a decision where it lives the moment it's made** (`CLAUDE.md`, ADR, `docs/plans/`, `AI_README`).
3. **Leave `git status` readable** — it *is* the handoff to the next session.
4. **When the ceiling nears, finish the current unit before opening the next.**

Test: could the next session pick this up from the repo alone, without this conversation?

## Anti-patterns
- 🚫 Scaling before review.
- 🚫 Deleting or overwriting without looking at the target.
- 🚫 Treating one-time consent as standing.
- 🚫 Memory as a dump of repo facts.
- 🚫 Ending a change with a wall of prose instead of status + commit + next steps.
