# 02 — Skills and refactoring

> Commandments I and X: automate what repeats; refactor so the code reads like its neighbor.

## Skills (slash-commands)

1. **Build a skill when** a procedure repeats (≥3 times), its order is easy to get wrong (migration:
   number → SQL → apply → `AI_README` → commit), or it carries a project-specific gotcha
   (`PYTHONIOENCODING=utf-8` on Windows, `--runInBand` while a server runs).
2. **A skill has an output contract** (exit 0 = green, otherwise what failed) and **prints anything
   destructive** it does.
3. **A skill is a recipe for the agent; a hook is automation run by the harness.** "Always do X after Y" =
   a hook in config, not a skill and not a memory.
4. Starter set: `/run` (server + smoke), `/run-tests`, `/update-ai-readme`, `/add-migration` (relational DB).

## Refactoring

1. **Search for prior art first** (`git log -S`, `git blame`) — an "ugly" shape often has a reason.
2. **Refactor separately from a behavior change** — one commit is either cleanup or a feature.
3. **Reuse before rewrite** — check whether the helper already exists.
4. **Keep old entry points working** on structural moves (re-exporting shims), or update every caller in the same change.
5. **Small verified steps:** refactor → tests green → commit.
6. **Apply SOLID proportionally:** one reason to change per module; extend behind a flag rather than editing a
   hot path (→ [12](12-flexibility-and-scalability.md)); **no abstraction before the second concrete case.**
7. **Two review modes, never mixed:** simplification (reuse, clarity) vs correctness (adversarial bug-hunt).

## Anti-patterns
- 🚫 A skill for something done once.
- 🚫 A skill that silently runs something destructive.
- 🚫 A big-bang rewrite after which nobody can say what broke.
- 🚫 Five layers and a factory for a three-field CRUD.
