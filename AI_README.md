# AI_README — The Craft directory map

> ## ⚠️ Vendored into a host project? Then this is a **rules pack, not the host's constitution**
>
> If you found this file under a host project's `docs/rules/`, read that project's **root
> `CLAUDE.md`** first — it is in charge. Here, only the **content** travels: the numbered chapters + `intro.md`
> + `guards/` + this map. The repo mechanics described below (`build.py`, `test.py`, `pl/`, `content.js`,
> `index.html`, `CHAPTERS`) belong to the doctrine repo `ClaudeBuildCodex` and are usually absent
> from a vendored copy. **Don't read every chapter** — grep the
> **"Topic index → file"** section below and read only the chapter you need.

> Directory map for the next session / another agent. Read it **before** touching any files here.
> Repo constitution: [CLAUDE.md](CLAUDE.md). Quality test for this file: after reading it, can you
> safely change anything in this directory without scanning every file?
>
> **Meta-file split** (→ [01](01-documentation-and-ai-readme.md)): `README.md` = description for GitHub
> (public, EN). `CLAUDE.md` = repo constitution (single language, **not translated**). **`AI_README` is
> translated per language** — this file (root) is the **EN/base** version; the PL copy lives in [`pl/AI_README.md`](pl/AI_README.md).

## What this directory is

A **documentation** repository (not an application): the "Rzemiosło — The Craft" doctrine (Kolada Build).
The content is hand-written markdown; `index.html` is its viewer (a static SPA, no build step).
Goal: a rule set reusable as `/docs/rules/` in new projects **and** public material for
people starting out with Claude. Details and policies → [CLAUDE.md](CLAUDE.md).

## Core (this repo) vs Web (sibling repo)

**Split of responsibilities — do not duplicate between them:**

- **This repo (`ClaudeBuildCodex`, the "Rzemiosło" brand) = canonical core.** Form: **technical, terse, imperative;
  English is the base** (PL translation in `pl/`) — the source of truth for the rules, attached to projects as `/docs/rules/`. Optimized for
  **the agent and the technical reader**: density over approachability. This is where we version the doctrine (craft.json).
- **The sibling `ClaudeBuildCodexWeb` (the "Rzemiosło Web" brand) = the presentation project.** It takes the same doctrine and **expands
  individual topics** into a friendlier, more extensive form. **Web — not this repo — is responsible for:**
  the public site, **editions** (technical / BIZ-TECH / business), **language versions**, and **building
  `docs/rules/` packages in a specific language**. It consumes this repo's content + `craft.json` at build time.

> **This repo is ONLY a rule set.** It is not a presentation product. The `index.html` here is a
> **minimal local/dev reader** (content preview for the author and agent), **not** a public site —
> which is why we don't put edition badges, marketing, or a language switcher here. All presentation,
> editions, and multi-language packaging happen in **The Craft Web** (a separate project). If you're tempted
> to add a presentation/marketing/edition layer here — that's material for Web, not for the core.

What goes into a `docs/rules/` package (the contract with Web) → [docs/packaging.md](docs/packaging.md).

## File index

| File | What it's for |
|------|----------|
| `index.html` | **Minimal local/dev reader** (content preview for the author/agent) — NOT a public site. Home page (decalogue + cards) + chapter view + brief + EN/PL language switcher (EN by default). |
| `intro.md` | **Short intro** — what The Craft is, who it's for, how to start (the long form lives on the website). Outside the numbered list, routed as `#intro`; there's also `pl/intro.md`. |
| `00`–`19` (root) | **EN content — canonical, base, source of truth.** Slugs/numbers = stable anchors, shared across all languages. |
| `pl/` | **PL content** — the same numbered chapters (the same file names, content in Polish). Translation of the EN. |
| `guards/` | **Ready-made test guards** from chapter 17: `ai_readme_guard.py` (index guard) and `code_language_guard.py` (ratchet). Templates copied into a project's `tests/` — deliberately not named `test_*.py`, so a host's pytest doesn't collect them from `docs/rules/`. Shipped in the package. |
| `add_chapter.py` | **Adds a chapter and wires it everywhere** (`NN-slug.md` + `pl/` skeleton, `README`, both `AI_README`, `CHAPTERS`/`CH_EN`, `craft.json` `chapters`), then `build.py` + `test.py`. Dry-run by default, `--execute` writes. **Never touches the version or CHANGELOG** — the release number is the author's (shared axis with Web). Repo tooling, not shipped. |
| `docs/` | Plans and meta decisions for the repo (not doctrine content): `docs/AI_README.md`, `docs/plans/`. |
| `content.js` | **Generated** snapshot of the `.md` embedded in JS — lets content render over `file://`. Do not edit by hand. |
| `build.py` | Build script: concatenates `.md` files → `content.js`. Run after editing content (`python build.py`). |
| `test.py` | **Smoke test** (pure Python): PL↔EN parity, dead links, `content.js` freshness, consistency of `CHAPTERS`/tables/`craft.json`, and **static `index.html` navigation** (`href="#…"` links, `data-i18n`↔`UI`, `data-bf-label`↔`BRIEF_FIELDS`). `python test.py`. |
| `CLAUDE.md` | Repo constitution: what it is, the stack, how to run it, policies, current state. |
| `AI_README.md` | This file — the directory map. |
| `README.md` | Entry point for a human: chapter list + "how to read it". |
| `craft.json` | **Release version** (`version` + `released`) + brand names (`name`/`name_short`/`name_en`). The source of the stamp for the Rzemiosło Web site. |
| `CHANGELOG.md` | Rzemiosło release history (semver, date = publication day). |
| `00-commandments.md` | **Decalogue** — 10 commandments, 7 sins, the golden rule of altitude, how to depart from a rule. The core. |
| `01-documentation-and-ai-readme.md` | Three layers (CLAUDE.md / AI_README / docs) split by reader; the grep index; docs = current state only; living plans. |
| `02-skills-and-refactoring.md` | When to build a skill (vs a hook); refactoring discipline; SOLID proportionally. |
| `03-testing-and-verification.md` | Every behavior change carries a test; proof instead of claims; smoke with markers; honest reports; a guard proven by the incident. |
| `04-scripts-and-databases.md` | Dry-run/`--execute`, idempotency, forward-only migrations, backups; absolute paths across tools; rehearse a bulk mutation on a prod copy. |
| `05-git-and-deployments.md` | Search history, undo/recover lost work, parallel sessions and branching ladder, the deploy policy (origin check, boot-check, deploy tags, changelog). |
| `06-collaboration-and-memory.md` | Plan→sketch→scale, the permission map (free/ask/never), user's language, built-in memory, change summary, handoff when context runs out. |
| `07-new-project-day-0.md` | The only checklist: wire The Craft in (plain pointer in CLAUDE.md/AGENTS.md), product brief → `project-brief.md`, Day 0 steps, `CLAUDE.md` skeleton. |
| `08-stack-and-technologies.md` | Default stack (Python by default — Go, Rust, Kotlin, TypeScript when they fit the job better; SQLite, server-rendered HTML, one-VPS monolith, Lucide) and when to depart — with an ADR. |
| `09-law-and-protecting-the-creator.md` | Never invent legal data or declare unimplemented practices; terms/policy contents; consent before trackers; security index. |
| `10-seo-and-translations.md` | hreflang + x-default, language completeness as a failing test, programmatic-page quality guards, YMYL/E-E-A-T, human review of sensitive translations, RTL. |
| `11-data-model-and-normalization.md` | Lookup dictionaries, slug instead of ID, active-row, deliberate denormalization. |
| `12-flexibility-and-scalability.md` | Separate the layers, feature flags, scale-to-zero vs always-on, don't over-engineer. |
| `13-performance-frontend-and-sql.md` | Measure first, indexes + partial index, no N+1, chat streaming, CWV, mobile viewport (dvh/visualViewport). |
| `14-operational-resilience.md` | Crash-proof runtime, resumable jobs, runner lifetime, hostile external sources, provider limits (SMTP), quotas, observability, recurring-job watchdogs, scheduler config. |
| `15-scraping-ai-and-chatbots.md` | Effective scraping (official source, shape validation, delta), AI APIs for specific tasks (contract/cache/quotas), configurable+grounded chatbots. |
| `16-driving-claude.md` | Project policy for the agent: when plan mode is required, autopilot inside the permission map, model by stakes, background vs detached, subagents, worktree per session. |
| `17-language-and-guards.md` | Code in English (incl. test names), prose in the project's language; only names a tool prints must stay English in prose; the two guards in `guards/`; the ratchet. |
| `18-release-rehearsal.md` | dev → preprod → prod: rehearse migrations and the deploy on a faithful, anonymised copy of prod. |
| `19-database-swap-runbook.md` | Swap a prod database while keeping live accounts: every FK table, slug not ID, live prod as source, maintenance window, smoke. |

The chapters split into a **core** (`00`–`08`) and a **deep dive** (`09`–`19`). Each = one
commandment/topic, terse, ending with anti-patterns.

## Topic index → file (grep-friendly)

> **Looking for something specific? Don't read everything.** `grep -i <topic>` over this index (English
> keywords) → the file name on the same line → read **only that chapter**. That's how you save context in
> the target project (rule: [01](01-documentation-and-ai-readme.md)).
> **Native language:** a translation may live in a language subfolder (e.g. `pl/`, with its own
> `AI_README.md` and keywords in that language). If the user's native language is available there, read
> that copy — the file slug is shared across all languages.

- **`00-commandments.md`** — commandments, decalogue, ten commandments, seven deadly sins, golden rule, altitude, doctrine core, rule zero, bootstrap, departing from a rule, deviation, exception, precedence, rule conflict, the floor, non-negotiable.
- **`01-documentation-and-ai-readme.md`** — documentation, AI_README, CLAUDE.md, README, docs, /docs, plans, docs/plans, grep, keyword index, context economy, one file one topic, current state only, generated artifact, folder structure.
- **`02-skills-and-refactoring.md`** — skill, slash-command, /run, /add-migration, automation, hook, refactoring, prior-art, reuse, backward-compat, shim, SOLID, single responsibility, open/closed, dependency inversion, /simplify, /code-review.
- **`03-testing-and-verification.md`** — test, testing, TDD, test-first, test pyramid, unit, integration, e2e, Playwright, pytest, Jest, smoke test, verify don't declare, regression, CI, guard, watchdog, replay the incident, boundary test, off-by-one, false calm.
- **`04-scripts-and-databases.md`** — script, mutation, dry-run, --execute, idempotency, migration, forward-only, backup, restore, retention, seed, backfill, database, absolute path, path portability, /tmp mismatch, tool boundary, Git Bash vs Python path, rehearse mutation on prod copy, snapshot, integrity_check, foreign_key_check.
- **`05-git-and-deployments.md`** — git, git log -S, pickaxe, blame, history, .gitignore, CRLF, orphans, uncommitted work, commit message, undo, recover lost work, reflog, git restore, reset --soft, ORIG_HEAD, recover deleted branch, restore a file from an old commit, stash, save point, I lost my commits, git is scary, issue, issues, GitHub Issues, branch, branching, branching ladder, trunk-based, feature branch, develop, PR, pull request, review, parallel sessions, concurrent AI sessions, solo developer, cherry-pick, merge sweeps other session's work, deploy, deployment, deploy policy, never auto-deploy, origin vs local, unpushed commits, boot-check before reload, maintenance window, zero-downtime, deploy tag, rollback, changelog, runbook, incident lessons, nightly backup.
- **`06-collaboration-and-memory.md`** — collaboration, plan iterate review, memory, confirm irreversible, report honestly, feedback, change summary, widget, next actions, native language, permission map, permissions table, what may I do, free/ask/never, boundary, standing authorization, per-action consent, handoff, context runs out, compaction, summarized session, long session, resume, pick up where it left off, state in the tree.
- **`07-new-project-day-0.md`** — new project, Day 0, checklist, brief, product brief, project-brief.md, monetization, onboarding, setup, wire The Craft, docs/rules, submodule, pointer, AGENTS.md, CLAUDE.md skeleton, technical level, languages spoken, technologies known, language policy, minimal Day 0.
- **`08-stack-and-technologies.md`** — Go, Golang, Rust, Kotlin, TypeScript, choose the language by fit, language choice, rewrite for speed, stack, technologies, Python, Node.js, FastAPI, SQLite, PostgreSQL, Docker, nginx, pm2, Hetzner, VPS, monolith, serverless, scale-to-zero, ADR, Lucide, baseline, Claude Code, GitHub, Git, GitHub Issues, TDD.
- **`09-law-and-protecting-the-creator.md`** — law, terms of service, ToS, privacy policy, GDPR, consent, cookie, trackers, disclaimer, jurisdiction, governing law, sole proprietorship, placeholder, invented tax ID, age gate, 18+, data retention, user rights, account deletion, protecting the creator, security checklist, IDOR, authorization.
- **`10-seo-and-translations.md`** — SEO, hreflang, JSON-LD, schema, canonical, sitemap, meta, OG, Open Graph, E-E-A-T, YMYL, programmatic SEO, translations, i18n, l10n, language parity, RTL, localization.
- **`11-data-model-and-normalization.md`** — data model, normalization, denormalization, lookup table, controlled vocabulary, slug, slug not ID, active-row, expired_at, partial index, junction, M:N, foreign key, ERD, schema.
- **`12-flexibility-and-scalability.md`** — flexibility, scalability, separate layers, boundaries, feature flag, ship dark, ramp, scale-to-zero, always-on, cold start, cache, invalidation, over-engineering, ADR.
- **`13-performance-frontend-and-sql.md`** — performance, measure first, Lighthouse, Core Web Vitals, CWV, LCP, CLS, INP, index, partial index, EXPLAIN QUERY PLAN, N+1, SELECT *, WAL, WebP, cache busting, lazy load, streaming, SSE, pagination, mobile, viewport, dvh, 100vh, visualViewport, on-screen keyboard, safe-area, flex-basis, responsive, device emulator, getBoundingClientRect, device-profile test.
- **`14-operational-resilience.md`** — resilience, runtime, crash, unhandledRejection, uncaughtException, restart loop, retry, backoff, timeout, 429, rate limit, rotation, User-Agent, resumable, checkpoint, scraper, long jobs, SMTP, 587, STARTTLS, deliverability, SPF, DKIM, email, quota, cost, abuse, sessions, MemoryStore, recurring job, nightly, cron, scheduler, scheduled task, watchdog, data freshness, stale data, silent failure, runner lifetime, detached process.
- **`15-scraping-ai-and-chatbots.md`** — scraping, scraper, crawler, robots.txt, selector, parsing, BeautifulSoup, requests, fuzzy match, rapidfuzz, dedup, delta, incremental, AI API, LLM, model, JSON schema, tool use, output contract, cache, quota, chatbot, assistant, system prompt, grounding, RAG, prompt injection, hallucination, eval, golden set, disclaimer.
- **`16-driving-claude.md`** — Claude Code, plan mode, planning, autopilot, auto-accept, autonomous, permission map, model choice, model by stakes, background, detached, long jobs, subagent, fan-out, parallel, adversarial verification, git worktree, concurrent sessions, shared checkout, skill, hook.
- **`17-language-and-guards.md`** — language, English, code language, prose language, naming, identifiers, test names, test naming, Polish identifiers, bilingual, mixed language, docstring language, comments language, CLAUDE.md language policy, wdrożenie, technical terms in prose, names a tool prints, guard, guards, guards/, rule enforcement, AI_README guard, index guard, every module in the index, size ceiling, 20 kB, code-language guard, ratchet, baseline, --write-baseline, dated exception, Day 0 wiring.
- **`18-release-rehearsal.md`** — preprod, staging, dev/preprod/prod, three environments, rehearse deploy, dress rehearsal, rehearse migration, anonymised refresh, basic-auth, noindex, ACME bypass, SITE_URL override, env-overridable, deploy key
- **`19-database-swap-runbook.md`** — database swap, swap prod database, preserve accounts, users tables, FK order, slug remap, live prod source, maintenance window, pm2 stop, backup before swap, integrity_check, foreign_key_check, sessions.db, gitignored assets, rsync, smoke after swap, runbook, incident lessons

## `index.html` architecture (contract)

A single file, no build dependencies. Mechanics:

- **`CHAPTERS`** (an array in `<script>`) — **the single source** of the chapter list. From it are generated:
  the cards on the home page, the `<select>` in the reader, prev/next navigation. Fields: `file, no, group
  ("core"|"deep"), title, desc`.
- **Hash routing:** `#NN-name` → chapter view; empty/`#` → home page. `route()`
  reacts to `hashchange`.
- **Language (content + the whole chrome):** `LANG` (`en`/`pl`, default **`en`**, saved in `localStorage` `rzemioslo-lang`).
  Chapter content from `file` (EN, root) or `pl/`+`file` (PL). **The chrome is fully bilingual** —
  the `UI` dictionary (`data-i18n`/`data-i18n-html`) + `CH_EN` (chapter titles/descriptions) + `BRIEF_FIELDS`
  (brief fields); `applyChrome()` redraws everything at startup and on `#langToggle`. Add a
  string to the chrome → add a key to `UI` (both languages), otherwise it stays in Polish.
- **Render (two-track):** first `fetch(langPath(file))` (fresh `.md`, when served); on a fetch
  error (`file://`) — the `window.RZEMIOSLO_DOCS[LANG][slug]` snapshot from `content.js`. The result →
  `marked.parse()` → `.prose`, cached in memory (`cache[LANG+":"+file]`).
- **`rewriteLinks()`** after render: `*.md` links → `#slug` (SPA navigation), `index.html` → `#`,
  external `http(s)` → `target=_blank`; tables wrapped in `.tablewrap` for scrolling on mobile.
- **Theme:** `[data-theme]` on `<html>` (`light`/`dark`); no attribute = follow the system. The switcher
  in the topbar saves the choice in `localStorage` (`rzemioslo-theme`); a script in `<head>` sets it
  before render (no flash).
- **Fallback note** shows only when **both** sources fail (no `content.js` and `file://`).

## Gotchas

- **`file://` blocks `fetch`** — which is why content works from a double-click **only** from the
  `content.js` snapshot. After editing `.md` run `python build.py`, otherwise `file://` will show stale content.
  When served (`http(s)://`, GitHub Pages) it always takes the fresh `.md`; on GitHub the `.md` renders natively.
- **`content.js` is generated** — don't edit it by hand (the build will overwrite it). Commit it so `file://`
  works after the repo is cloned.
- **`marked` is loaded from a CDN** — without network the render won't work (there's a soft fallback to `<pre>`).
- **`index.html` does NOT contain chapter content** — it reads `.md`/`content.js`. Don't paste content into the HTML.
- **Add a chapter → `python add_chapter.py NN slug --title-en … --title-pl … --desc-en … --desc-pl … --keywords-en … --keywords-pl …`**
  (dry-run; `--execute` writes) — it wires every place at once and runs `build.py` + `test.py`. It only appends
  the next number; it never changes the version. Editing one place by hand = a dead entry; `test.py` catches it.
- **Format of a chapter:** a one-line lead (which commandment), **Rules** (numbered, imperative, one line +
  why), **Anti-patterns**. No lectures and no "In practice" closers — explanation lives on the website, the
  only checklist is `07`.
- **EN↔PL parity:** changing a rule in any chapter (EN, canon) requires updating the counterpart in `pl/` (the same
  list, the same file names). PL is a **translation**, not a separate doctrine. `content.js` holds both languages.
- **File names = stable anchors** (`#NN-name`, targets of relative links), **shared between EN and PL**.
  We don't localize file names — only the content inside. Don't change them without reason.
- **Brand:** make color changes on the CSS variables (`--accent`, `--accent-2`, `--grad`), not on the
  values at the point of use. Light and dark mode must both look good.
- **Content is generic, not "for one project".** Specific projects serve
  only as illustration (`e.g. …`, "reference project"), never as the topic. Don't make any project the hero of the doctrine.
- **Two languages: EN (canon, root, base) + PL (`pl/`).** Write rules translatably. Direction and convention →
  [docs/packaging.md](docs/packaging.md). Per-language packages are assembled by Web.

## Numbers

- 20 chapters (`00`–`19`) + `README.md`, in **two languages** (EN root = base + PL `pl/`).
  Core: 9 files (00–08). Deep dive: 11 (09–19).
- `index.html`: 1 file; runtime from a CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (EN: 22 docs ~66k chars; PL: 21 docs ~61k chars — chapters + `intro` + README; structure `{lang:{slug:md}}`).
- **Special documents (outside the numbered list):** `intro.md` (short intro, route `#intro`) and the
  brief view (`#brief`) — routed separately, not present in the `CHAPTERS` array.
- **Smoke test:** `python test.py` (PL↔EN parity, dead links, `content.js` freshness, consistency of
  `CHAPTERS`/tables/`craft.json`, static `index.html` navigation: `href="#…"` links + `data-i18n`↔`UI` +
  `data-bf-label`↔`BRIEF_FIELDS`). Plus a "manual test" = preview via a server **and** from a double-click
  (`file://`) + clicking through chapters and the EN/PL switcher (runtime JS behavior the smoke test doesn't catch).
