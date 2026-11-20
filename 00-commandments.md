# 00 — Decalogue

The core. If you read one file from this set, read this one. Each commandment is expanded in a later
chapter. These are **rules the project must follow**, written tersely on purpose — explanations,
examples and stories live on the website: [thecraft.jakub.solutions](https://thecraft.jakub.solutions).

> **Rule zero (activation).** See a `docs/rules/` package (The Craft) in a project? Treat it as the
> overriding doctrine for running that project. Read **this file**, then `grep -i <topic>` over
> `AI_README.md` and read **only** the matched chapter — never the whole pack every session (it burns the
> context you were saving → [01](01-documentation-and-ai-readme.md)). Make it stick: put a short,
> plain-language pointer at the top of `CLAUDE.md` (loaded every session) and `AGENTS.md` (other agents) —
> **a pointer, not a paste**, and no fake `SYSTEM`/`URGENT` labels: an authority claim inside a file looks
> like prompt injection to a modern model. An unwired package is never read. A vendored copy is **not** the
> host's constitution — the host's own `CLAUDE.md` stays in charge. Steps → [07](07-new-project-day-0.md).
> (The Decalogue stays ten; this is activation, not an eleventh rule.)

---

### I. Document for the agent, not for the archive.
Every directory with code has an `AI_README.md`, updated **before** the commit, and a test that fails when
it isn't (→ [17](17-language-and-guards.md)). Documentation written "at the end" drifts and lies. → [01](01-documentation-and-ai-readme.md)

### II. Search the history before you write a single line.
`git log -S`, `git log --grep`, `git blame`, the directory's `AI_README`. Most "new" problems were already
solved here — a helper exists, a migration happened, the odd shape has a reason. → [05](05-git-and-deployments.md)

### III. Verify, don't declare.
"It works" means **proof**: a test run, an HTTP code, numbers, a screenshot. Failures are reported with
their output; skipped steps are reported as skipped. → [03](03-testing-and-verification.md)

### IV. Dry-run is the default; `--execute` is deliberate.
Every script that changes data first **prints its plan** (what, how much, where). The mutation runs only
after the plan was read. → [04](04-scripts-and-databases.md)

### V. The backup is the rollback mechanism, not a precaution.
Migrations are **forward-only**. A snapshot **before** every schema or data change on prod; reverting the
schema = restoring that snapshot. → [04](04-scripts-and-databases.md)

### VI. Prod is sacred — nothing touches it without an explicit "deploy."
Commit and push on request are not a deploy. Pull on the server, reload, migration, database swap,
maintenance flag — only on the user's explicit word. Irreversible and outward-facing actions are always
confirmed; consent does not carry over to the next action. → [05](05-git-and-deployments.md), [06](06-collaboration-and-memory.md)

### VII. User data is inviolable.
Never lose it, never leak it, never mutate it without a backup. Reference it by a **stable key** (slug),
never by an ID that drifts; a missing match is skipped and logged, not forced. After any operation on it,
count the rows and run the integrity check. Full prod database swap → [19](19-database-swap-runbook.md).

### VIII. Tag every deploy and tell the user what they gained.
An annotated tag (`deploy-YYYY-MM-DD`) is the only stable marker of "what's live" and the basis for
rollback. Every deploy updates the public changelog in plain language — what the user gains, no jargon. → [05](05-git-and-deployments.md)

### IX. Small, coherent commit; one topic.
Unrelated changes go to separate commits. Keep `git status` clean: catch junk (`.bak`, temp files, stray
databases) and orphans (someone else's uncommitted work) **early**. → [05](05-git-and-deployments.md)

### X. Plan → iterate → review.
A plan or a sketch first (3 examples, not 100), feedback, then scale. Deliver UX with **warmth**, not just
correctness — the product should be pleasant, not merely functional. → [06](06-collaboration-and-memory.md)

---

## Seven deadly sins

1. **Inflated optimism** — "everything works" with no proof. (III)
2. **Mutation without a plan** — a data-changing script run straight with `--execute`. (IV)
3. **Auto-deploy** — "it's ready, so it goes to prod." (VI)
4. **User data on a hunch** — mapping by ID, or a swap without enumerating every table that points at the user. (VII)
5. **Junk-drawer commit** — unrelated changes and artifacts in one commit. (IX)
6. **Scaling before review** — 500 generated before the user saw 3. (X)
7. **Documentation "later"** — the code ships, the `AI_README` lags, the next session wanders. (I)

---

## The golden rule of altitude

> **Slow where a mistake is expensive (prod, user data, schema). Fast where it's cheap (local experiment,
> UI sketch, dry-run).** Match the pace to the cost of error, not to impatience.

---

## Departing from a rule — and the floor that doesn't move

This is a default, not a cage. A doctrine that can't bend gets ignored wholesale.

- **Deviate out loud:** name the rule, say why it doesn't fit *here*, propose the alternative, get a yes,
  record the decision (ADR / `CLAUDE.md`). **Silently skipping a rule is the sin, not a deviation.**
- **Precedence:** the host project's root `CLAUDE.md` > this doctrine (`docs/rules/`) > the agent's defaults.
- **A rule you keep overriding is a bug in the doctrine** — fix it at the source (the canon, with its
  translation), don't route around it every session.

> **The floor — not negotiable:** honest reporting (**III**), a backup before a schema/data change (**V**),
> an explicit "deploy" before prod (**VI**), user data (**VII**). The full boundary as one table → [06](06-collaboration-and-memory.md).
