# 07 — New project: Day 0

> The checklist Claude runs when a project starts — the **only** checklist in the doctrine; other chapters
> link here. Goal: every later session stands on solid ground.

## Wire The Craft in (once)

1. **Place the rules in `docs/rules/`** — a submodule (updatable) or a plain copy:
   `git submodule add https://github.com/JKolada/TheCraftWithClaude docs/rules`
2. **Put a plain pointer at the top of `CLAUDE.md` and `AGENTS.md`** (create them if missing). If you see
   `docs/rules/` and the pointer isn't there — add it, don't wait to be asked:
   > This project follows the build rules in `docs/rules/` (The Craft); they override default behavior.
   > Read `docs/rules/00-commandments.md` first, then `grep -i <keyword> docs/rules/AI_README.md` and read
   > only the matched chapter. This `CLAUDE.md` remains the project's constitution.

   A pointer, not a paste — the rules live in one place. No `SYSTEM` labels (→ [00](00-commandments.md)).
3. **Pick the rules' language** — English at the root, Polish in `pl/`.

## 0. Product brief — ask before anything is built

Ask in short groups; where the user doesn't know, propose a default and **mark it as an assumption**:

- **Technical level and reporting style** (ask first — it sets the register: non-technical → no jargon,
  closed questions with a recommendation).
- **Languages the user speaks; technologies they know.**
- **Target languages and markets** (i18n from day one? RTL? currencies) → [10](10-seo-and-translations.md).
- **MVP vs later; accounts and roles; integrations** (payments, AI, mail, maps).
- **Monetization** (free / paid / subscription / ads; when; provider; invoices/VAT) → [09](09-law-and-protecting-the-creator.md).
- **Visual direction and feel** (existing brand? light/dark? animation budget, `prefers-reduced-motion`, WCAG?).
- **Value proposition and tone** (one sentence; name and domain set?).

The answer lands as **`project-brief.md` in the project root** (next to `docs/rules/`, not inside it), or is
pasted as the first message. The brief view in the reader generates it.

## Checklist

1. **Recon:** read existing `CLAUDE.md` / `AI_README` / `README`; `git log --oneline -20`, `git status`
   (orphans, junk); identify stack, run command, where the data lives.
2. **`CLAUDE.md`** from the brief (skeleton below): stack + exact run commands, policies, the user's language
   and level, the permission map (→ [06](06-collaboration-and-memory.md)), a dated "Current state".
3. **Language policy** — two lines in `CLAUDE.md`: code English (identifiers, tests, DB, CLI, keys), prose in
   the project's language (→ [17](17-language-and-guards.md)).
4. **Repo hygiene:** `.gitignore` (deps, local DBs, `*.bak`, generated, temp); commit and deploy-tag convention;
   tasks in GitHub Issues / `docs/plans/`.
5. **`AI_README.md` in every directory with code**; `docs/` for architecture and data model.
6. **Tests:** a test skeleton + a smoke test with markers; Playwright on a separate port if there's a UI;
   **both guards from [17](17-language-and-guards.md) in the first commit**, baseline committed.
7. **Skills:** `/run` + smoke, `/run-tests`, `/update-ai-readme`, `/add-migration` (→ [02](02-skills-and-refactoring.md)).
8. **Data:** forward-only migrations, a `backups/` directory with retention, dry-run by default (→ [04](04-scripts-and-databases.md)).
9. **Before the first real user:** global error handler and a 500 that leaks nothing, timeouts on every
   external call, quotas on paid endpoints, a durable session store in its own file (→ [14](14-operational-resilience.md));
   AI calls with an output contract and a cache (→ [15](15-scraping-ai-and-chatbots.md)).
10. **Production (prepared, not fired):** deploy runbook, branded maintenance page, rollback plan (tag +
    backup), public changelog, nightly backup from the first real user (→ [05](05-git-and-deployments.md)).
11. **Legal:** terms, privacy policy and disclaimers with `[to be filled]` placeholders; consent before
    trackers (→ [09](09-law-and-protecting-the-creator.md)).
12. **Baselines:** Lighthouse after the first working page; indexes on filter columns from the first migration (→ [13](13-performance-frontend-and-sql.md)).
13. **Architecture decisions** only where you depart from the default stack — one ADR each (→ [08](08-stack-and-technologies.md), [12](12-flexibility-and-scalability.md)).

**Minimal Day 0:** brief → `CLAUDE.md` → `.gitignore` → `/run` with a smoke test → test skeleton with the
guards → `backups/`. The rest grows with the project.

## `CLAUDE.md` skeleton

```
# CLAUDE.md — <Project>
<pointer to docs/rules/ — see above>

## What this is
<one paragraph: what it does, for whom>

## Stack & how to run
<layer → tech → location>
run: <exact command>

## Policies (override default behavior)
- Never deploy/push without an explicit "deploy". Commit freely; confirm the irreversible (permission map: docs/rules/06).
- Dry-run by default. Prod is sacred; user data is inviolable.
- Talk to me in <language>; I know <languages / technologies>.
- Code: English (identifiers, tests, DB, CLI, keys). Prose: <language>.
- <project-specific hard rules: privacy, domain constraints>

## Current state (<date>)
- <counts, migrations applied, what's live>
```

## Anti-patterns
- 🚫 Code before the brief — language, monetization and brand added later are a rewrite.
- 🚫 Thirty questions at once — ask what changes the plan, propose the rest as defaults.
- 🚫 Silent assumptions ("probably Polish only", "probably free").
- 🚫 Jargon aimed at a non-technical user.
