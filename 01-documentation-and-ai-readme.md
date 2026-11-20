# 01 — Documentation and AI_README

> Commandment I: *document for the agent, not for the archive.* The goal: the next session understands a
> directory without reading all of its code.

## Three layers, split by reader

| Layer | File | Holds |
|---|---|---|
| **Constitution** | `CLAUDE.md` (root) | what the project is, exact run commands, **policies that override default behavior**, a dated "Current state" with numbers. Loaded every session. |
| **Directory map** | `AI_README.md` in every directory with code | module index, key APIs (signature + contract), gotchas, numbers, the grep index. Read **before** touching that directory. |
| **Reference / plans** | `docs/` | architecture, data model, runbooks, `plans/`. |

`README.md` is the public front door (what it is, how to start) — not a layer for the agent. **Where does a
fact go? Ask who reads it** — and write it once; the other files link.

## Rules

1. **`CLAUDE.md` points to the `AI_README.md` maps** — without that pointer a new session doesn't know they exist.
2. **`AI_README.md` is updated before the commit**, in the same commit as the code. A test enforces the
   index (every module named, size ceiling) → [17](17-language-and-guards.md).
3. **Write the index for `grep`, not for reading.** Keyword-dense one-liners: concrete names, synonyms, both
   languages if the project is bilingual. `grep -i <topic>` should hit **one line** pointing at **one file**.
4. **One file = one topic.** A topic spread over five files is five hits and burned context.
5. **State, not intent.** Describe what the code does now; delete entries for removed code — a dead entry is
   worse than none. Numbers (records, tests) go stale → update them.
6. **`docs/` describes the current version only.** History lives in git and the `CHANGELOG`; update the doc,
   don't keep the old version beside it.
7. **`docs/plans/` is a living backlog.** Problem → options → choice → why. When a plan lands, fold the
   decision into the doc / `CLAUDE.md` it governs and **delete the plan** — git keeps the record.
8. **A new directory is created together with its `AI_README.md`** — never "later".
9. **Generated artifacts (HTML, snapshots) are derivatives:** commit them, never edit them by hand,
   regenerate on command (a skill), not on every commit.

Update the docs for: a new module/function/script/flag, a schema change, a behavior change (threshold,
fallback), changed counts. Not for: a pure bugfix with no API change, typos.

## Anti-patterns
- 🚫 "I'll update the docs at the end" — the end never comes, the docs lie.
- 🚫 An `AI_README` describing wishes instead of state.
- 🚫 The same state copied into five files — one source of truth, the rest link.
- 🚫 Generic descriptions ("helpers", "various rules") — grep misses, the agent reads everything.
