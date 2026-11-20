# 17 — Language of Code, and Guards That Keep Rules Alive

> Commandments I and III applied to *names*: a rule that lives only in someone's head is not a
> rule, and a rule without a test is a wish.

## Two languages, split by reader — never by mood

Every repository has two audiences, and each layer is written for exactly one of them.

| Layer | Who reads it | Language |
|-------|--------------|----------|
| **Code** — identifiers (module, class, function, variable, fixture and **test** names), file names of code, DB tables and columns, CLI flags, config and API/JSON contract keys, enum and state values, log keys, commit subject lines | the machine, `grep`, CI output, every future engineer and agent | **English. Always. No exceptions.** |
| **Prose** — documentation, plans, `AI_README`, comments and docstrings, user-facing text (UI labels, CLI output for a human, e-mails, changelog) | the owner and their users | **the project's language**, declared **once** in `CLAUDE.md` |

English for code is not a preference — it is the language of the ecosystem: every library, error
message, Stack Overflow answer and the agent's own training. A Polish (or German, or Spanish)
identifier is a word the tooling has never seen, that autocomplete won't suggest, that the next
engineer will transliterate three different ways. Prose is the opposite: the owner reads it, thinks
in it, and the *why* behind a decision loses precision in a second language. So the split follows
the **reader**, and it is fixed at the start:

```
# CLAUDE.md
Code: English (identifiers, tests, DB, CLI, keys). Prose: Polish (docs, comments, docstrings, UI).
```

**Names a tool prints stay English inside prose** — a command, flag, status, file or tag (`commit`,
`--dry-run`, `migrate.py`, `deploy-*`): that is what you grep for. The everyday word for the activity may
be in the prose language ("wdrożenie" for deploying) — this doctrine's own PL translation does exactly that.

### Tests are code

A test name is an identifier: the runner prints it, CI greps it, the 3 a.m. failure report is made
of nothing else. `test_<subject>_<condition>_<expected>`, in English. The *why* — the incident, the
date, the price of the bug — goes into the **docstring**, in the prose language, where it belongs:

```python
# before — reads like code to the eye and like nothing to anyone
def test_koszt_wobec_zysku_brutto_NIE_ISTNIEJE_w_stratnym_podoknie(conn): ...

# after
def test_cost_share_is_none_in_a_losing_window(conn):
    """Źródło 30% `NULL` w kolumnie kosztu z pomiaru 2026-09-26: miara to koszt / zysk
    brutto, więc w stratnym podoknie mianownik nie istnieje — silnik oddaje `None` z zamiarem."""
```

**Mixed identifiers are the worst of both worlds.** `test_cost_NIE_ISTNIEJE_in_window` is neither
searchable nor readable. Fixtures, helpers and parametrize ids follow the same rule — a fixture
called `szablon_bazy` is a bilingual API.

## A rule without a guard is a wish

"Every directory has an `AI_README`, updated **before** the commit" has been Commandment I of this
doctrine from day one. In the reference project, one session still shipped **95 of 98 code commits
without touching the index** — not out of malice: the agent read the constitution (which delegates
to the maps) and never opened the commandment that says *update before commit*. Documentation and
naming rules compete with the task at hand, and they lose every time unless something red stops the
commit. **The only rules that survive contact with a long session are the ones the test suite
enforces.** So every rule in this chapter ships with a guard: stdlib-only pytest, copy-paste portable,
wired in on Day 0 (→ [07](07-new-project-day-0.md)).

### Guard 1 — the `AI_README` index guard

What it enforces:

1. every directory with code modules has an `AI_README.md`;
2. **every module in that directory is named in it** — the index exists for `grep`, and a module
   absent from the index is invisible to the next session (→ [01](01-documentation-and-ai-readme.md));
3. the list of guarded directories guards itself: a new directory with modules and an index must be
   added to the list, or the test fails;
4. **a size ceiling — 20 kB.** An `AI_README` is a grep target, not a novel; past the ceiling it
   stops being an index. Over the limit, split the **directory** (→ [12](12-flexibility-and-scalability.md)),
   not the file.

What it **cannot** check: whether a description is *current*. A stale sentence passes. The duty to
update before the commit stays with the writer — the guard only removes the worst failure, absence.

```python
# tests/test_ai_readme.py — stdlib + pytest, adjust GUARDED and SKIPPED to the project
import pathlib, pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARDED = ("app", "app/core", "scripts", "tests")          # directories with code AND an index
SKIPPED = {"__init__.py", "conftest.py"}                    # nothing to describe
INDEX_MAX_BYTES = 20_000

def modules(d): return sorted(p.name for p in (ROOT / d).glob("*.py") if p.name not in SKIPPED)
def index(d):   return (ROOT / d / "AI_README.md").read_text(encoding="utf-8")

@pytest.mark.parametrize("d", GUARDED)
def test_every_module_is_in_the_index(d):
    text = index(d)
    missing = [m for m in modules(d) if m not in text and m.removesuffix(".py") not in text]
    assert not missing, f"{d}/AI_README.md does not mention: {missing}"

@pytest.mark.parametrize("d", GUARDED)
def test_index_fits_the_grep_ceiling(d):
    assert (ROOT / d / "AI_README.md").stat().st_size <= INDEX_MAX_BYTES

def test_guarded_list_is_complete():
    with_index = {str(p.parent.relative_to(ROOT)) for p in ROOT.rglob("AI_README.md")
                  if list(p.parent.glob("*.py"))}
    assert with_index <= set(GUARDED), f"add to GUARDED: {with_index - set(GUARDED)}"
```

### Guard 2 — the code-language guard (a ratchet)

A heuristic per token, not a dictionary: split the identifier on `_` and CamelCase, flag a token that
is on a **stop-list of the prose language's function words** (for Polish: `nie`, `jest`, `bez`,
`gdy`, `czy`, `dla`…) or has that language's **letter shape** (Polish: `cz`/`rz`/`sz`/`dz` inside,
endings `-uje`, `-osci`, `-anie`, `-owy`, `-nych`). Keep an explicit look-alike list (`ego`, `media`,
`wizard`) and accept that it misses some words: it is a ratchet, not a court.

```python
# tests/test_code_language.py — the core; the reference project ships the full version
import ast, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
SCANNED = ("app", "scripts", "tests")
BASELINE = ROOT / "tests" / "code_language_baseline.json"       # {"path": count}
STOP = {"nie", "jest", "bez", "gdy", "czy", "dla", "przy", "tylko", "albo", "oraz"}
SHAPE = re.compile(r"cz|rz|sz|dz|(?:uje|osci|anie|enie|owy|owa|owe|nych|nego)$")

def tokens(name): return [t.lower() for t in re.split(r"_+|(?<=[a-z0-9])(?=[A-Z])", name) if t]
def looks_foreign(name): return any(t in STOP or (len(t) >= 4 and SHAPE.search(t)) for t in tokens(name))
def names(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [path.stem] + [n.name for n in ast.walk(tree)
                          if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
def scan():
    return {p.relative_to(ROOT).as_posix(): [n for n in names(p) if looks_foreign(n)]
            for top in SCANNED for p in (ROOT / top).rglob("*.py") if any(looks_foreign(n) for n in names(p))}

def test_ratchet():
    base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    now = {k: len(v) for k, v in scan().items()}
    assert not {k for k in now if k not in base}, "new files must be clean"
    assert not {k for k in now if now[k] > base.get(k, 0)}, "a file gained foreign names"
    assert not {k for k in base if now.get(k, 0) < base[k]}, "tighten the baseline (--write-baseline)"
```

### The ratchet — how to introduce any rule into an old codebase

1. **Freeze** the current count per file in a baseline and commit it (on a green-field project it is
   empty).
2. **New files must be clean.** The rule is absolute from the day it is written.
3. **Counts may only fall.** Every touch of a file is an occasion to tighten; nobody is asked to
   rewrite two thousand names in one go, and nobody gets to add a two-thousand-and-first.
4. **When a count falls, lower the baseline on command** (`--write-baseline`), never silently.
   A baseline looser than the code lets the old number creep back without a word.
5. **Raising a baseline number by hand is weakening the guard** — the same sin as skipping a test.
6. **Dated exceptions** (an oversized index waiting for a directory split) carry the date, a ceiling
   equal to *today's* size, and the backlog item that removes them.

## Day 0 wiring

- Declare the prose language in `CLAUDE.md` (two lines — see above). → [07](07-new-project-day-0.md)
- Copy both guards into `tests/` **in the first commit**; run them; commit the baseline.
- Vendoring this doctrine into an existing project: run guard 2 once, commit the baseline as it is,
  and put "rename foreign identifiers to English — N left" into the backlog with the number. The
  reference project started at 2 938 identifiers in 129 files, almost all of them test names.
- Put the guards' file names into `tests/AI_README.md` — they are subject to guard 1 like any module.

## Anti-patterns

- 🚫 "Tests aren't real code, so their names can be in my language." — the runner disagrees.
- 🚫 Mixed-language identifiers (`test_cost_NIE_ISTNIEJE_in_window`) — unreadable *and* ungreppable.
- 🚫 Translating a name the tool prints — a flag, status, file or tag (`--dry-run` written as "próba",
  a `deploy-*` tag as "wdrozenie-*") — it stops matching what you grep for.
- 🚫 A rule stated in `CLAUDE.md` with no test behind it — the next session breaks it in good faith.
- 🚫 Raising the baseline to make the suite green.
- 🚫 An `AI_README` that grows past the ceiling because "everything here matters" — it stopped
  being an index the moment `grep` returns the whole file.
