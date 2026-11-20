# The Craft — Rzemiosło <sub>(Kolada Build)</sub>

> **Hard rules for building and running an application end-to-end with Claude** — a terse doctrine the
> agent reads and follows, so a vibe-coded project stays understandable, testable, safe to change and
> trustworthy, from the first commit to production with real users.

Start with **[What The Craft is](intro.md)** or the whole doctrine on one screen: **[00 — Decalogue](00-commandments.md)**.
Explanations, examples and stories live on the website: **[thecraft.jakub.solutions](https://thecraft.jakub.solutions)**.

## Adopt it in your project

The Craft is meant to be dropped into a project as `docs/rules/`, so the agent reads it from Day 0:

```bash
git submodule add https://github.com/JKolada/TheCraftWithClaude docs/rules
# or just copy the files into docs/rules/
```

Then put a plain pointer at the top of your project's `CLAUDE.md` and `AGENTS.md` (full steps →
[07 — New project: Day 0](07-new-project-day-0.md)):

> This project follows the build rules in `docs/rules/` (The Craft); they override default behavior.
> Read `docs/rules/00-commandments.md` first, then `grep -i <keyword> docs/rules/AI_README.md` and read
> only the matched chapter.

The ready-made test guards from chapter 17 are in [`guards/`](guards/).

## Languages

**English is the base** — the canonical doctrine lives in the repo root. **Polski** is a 1:1 translation
under [`pl/`](pl/00-commandments.md) (same chapters, same filenames). The in-browser reader
([index.html](index.html)) renders the `.md` and has an **EN | PL** switch (default EN). On GitHub the
`.md` files render natively — just click the links below.

## Chapters

| # | Chapter | What it covers |
|---|---------|----------------|
| 00 | [Decalogue](00-commandments.md) | 10 commandments — the doctrine's core, to memorize |
| 01 | [Documentation and AI_README](01-documentation-and-ai-readme.md) | `AI_README` in every directory, `CLAUDE.md` as source of truth, the grep index, docs as code |
| 02 | [Skills and refactoring](02-skills-and-refactoring.md) | When to build a skill/slash-command, refactoring discipline, SOLID |
| 03 | [Testing and verification](03-testing-and-verification.md) | Every behavior change carries a test, "verify, don't declare", guards proven by the incident |
| 04 | [Scripts and databases](04-scripts-and-databases.md) | Idempotency, dry-run/--execute, forward-only migrations, backups |
| 05 | [Git and deployments](05-git-and-deployments.md) | Search history, undo, parallel sessions and branching, the deploy policy and deploy tags |
| 06 | [Collaboration and memory](06-collaboration-and-memory.md) | Plan→sketch→scale, the permission map (free/ask/never), change summary, handoff when context runs out |
| 07 | [New project: Day 0](07-new-project-day-0.md) | Wire The Craft in + product brief + a concrete startup checklist |
| 08 | [Stack and technologies](08-stack-and-technologies.md) | Defaults: Python, SQLite, server-rendered HTML, one VPS monolith — and when to depart |
| 09 | [Law and protecting the creator](09-law-and-protecting-the-creator.md) | Terms, privacy policy, disclaimers as the creator's armor |
| 10 | [SEO and translations](10-seo-and-translations.md) | hreflang, JSON-LD, programmatic SEO, E-E-A-T/YMYL, language parity as a test |
| 11 | [Data model and normalization](11-data-model-and-normalization.md) | Lookup tables, slug instead of ID, active-row, deliberate denormalization |
| 12 | [Flexibility and scalability](12-flexibility-and-scalability.md) | Separate the layers, feature flags, scale-to-zero vs always-on, don't over-engineer |
| 13 | [Performance: frontend and SQL](13-performance-frontend-and-sql.md) | Measure before/after, cache-busting per deploy, streaming, mobile viewport (dvh/visualViewport) |
| 14 | [Operational resilience](14-operational-resilience.md) | Crash-proof runtime, resumable jobs, hostile external sources, provider limits, quotas, recurring-job watchdogs |
| 15 | [Scraping, AI APIs, and chatbots](15-scraping-ai-and-chatbots.md) | Effective scraping, AI for specific tasks (contract + cache), configurable & grounded assistants |
| 16 | [Driving Claude](16-driving-claude.md) | Project policy for plan mode, autopilot, model choice, background work, subagents, worktrees |
| 17 | [Language of code and guards](17-language-and-guards.md) | Code in English (identifiers, tests, DB, CLI), prose in the project's language; the `AI_README` index guard and the code-language ratchet |
| 18 | [Rehearse the release](18-release-rehearsal.md) | dev → preprod → prod: rehearse migrations and the deploy on a faithful, anonymised copy of prod. |
| 19 | [Database swap runbook](19-database-swap-runbook.md) | Swap a prod database while keeping live accounts: every FK table, slug not ID, live prod as source, maintenance window, smoke. |

## The philosophy in one sentence

> **Build like a craftsman — slow where a mistake is expensive, fast where it's cheap; and leave behind a
> workshop where the next person (human or agent) immediately knows where everything is.**

---

*A living document — updated after every project that taught us something. A doctrine that doesn't change
is dead.* Version 1.1.1 was reviewed and tightened with **Claude Opus 5.5**. · Part of **[jakub.solutions](https://jakub.solutions)** — Jakub Kolada.
Maintainer/build docs: [CLAUDE.md](CLAUDE.md) · [AI_README.md](AI_README.md).
