# 17 — Language of code, and guards that keep rules alive

> Commandments I and III applied to names: a rule that lives only in someone's head is not a rule, and a
> rule without a test is a wish.

## Two languages, split by reader

| Layer | Language |
|---|---|
| **Code** — identifiers (modules, classes, functions, variables, fixtures, **test names**), code file names, DB tables and columns, CLI flags, config and API keys, enum/state values, log keys, commit messages | **English, always** |
| **Prose** — docs, plans, `AI_README`, comments, docstrings, user-facing text | **the project's language**, declared once in `CLAUDE.md` |

```
# CLAUDE.md
Code: English (identifiers, tests, DB, CLI, keys). Prose: Polish (docs, comments, docstrings, UI).
```

## Rules

1. **English code is the ecosystem's language** — tooling, autocomplete, errors and the next engineer all
   speak it; a native-language identifier is transliterated three different ways.
2. **Tests are code.** `test_<subject>_<condition>_<expected>` in English; the *why* (the incident, the date,
   the cost) goes into the docstring, in the prose language.
3. **No mixed identifiers** (`test_cost_NIE_ISTNIEJE_in_window`) — unreadable and ungreppable.
4. **Names a tool prints stay English inside prose** — a command, flag, status, file or tag (`commit`,
   `--dry-run`, `migrate.py`, `deploy-*`): that is what you grep for. The everyday word for the activity may
   be in the prose language ("wdrożenie" for deploying).
5. **A rule without a guard is a wish.** One session shipped 95 of 98 commits without touching the index
   it was told to update. Rules that must survive a long session are enforced by the test suite.

## The two guards (ready-made in `guards/`)

Copy them into the project's `tests/` as `test_ai_readme.py` and `test_code_language.py`, adjust the
directory lists, run them, commit the baseline — in the **first commit** (→ [07](07-new-project-day-0.md)).

- **[`guards/ai_readme_guard.py`](guards/ai_readme_guard.py)** — every directory with code has an
  `AI_README.md`; **every module is named in it**; a **20 kB ceiling** (past it the index stops being an index —
  split the directory, not the file); the list of guarded directories guards itself. It cannot tell whether a
  description is *current* — that stays the writer's duty.
- **[`guards/code_language_guard.py`](guards/code_language_guard.py)** — flags identifiers that look like the
  prose language (stop-list of function words + letter shape); a **ratchet** with a per-file baseline.

## The ratchet — introducing any rule into an old codebase

1. **Freeze** today's count per file in a committed baseline (empty on a new project).
2. **New files must be clean** from the day the rule is written.
3. **Counts may only fall;** when one falls, lower the baseline **on command** (`--write-baseline`), never silently.
4. **Raising a baseline by hand is weakening the guard** — the same sin as skipping a test.
5. **Exceptions are dated**, capped at today's size, and tied to the backlog item that removes them.

Vendoring into an existing project: run the code-language guard once, commit the baseline as it is, and put
"rename foreign identifiers — N left" into the backlog with the number.

## Anti-patterns
- 🚫 "Test names don't count as code."
- 🚫 Mixed-language identifiers.
- 🚫 Translating a name the tool prints (`--dry-run` written as "próba").
- 🚫 A rule in `CLAUDE.md` with no test behind it.
- 🚫 Raising the baseline to make the suite green.
- 🚫 An `AI_README` past the ceiling "because everything here matters".
