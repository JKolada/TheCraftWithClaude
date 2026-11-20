# 16 — Driving Claude

> The agent's features are documented by the agent itself; this chapter only sets **project policy** for
> using them — when they are required, and where the limits are.

## Rules

1. **Plan mode is required** when the shape of the work is open, the blast radius is wide (migration,
   tree-wide rename, URLs/redirects) or the change is hard to undo. The plan names the files, the trade-off
   and **how the result will be verified**. Skip it for a bounded fix.
2. **Autopilot is the default — inside the permission map** (→ [06](06-collaboration-and-memory.md)). The
   middle and right columns still stop it; that is what makes autopilot safe.
3. **Model by stakes:** a cheaper model for mechanical work, the strongest for architecture, hard bugs and
   anything that can lose data. Never economize on a data-losing operation.
4. **Long work in the background; anything that must outlive the session — detached** (→ [14](14-operational-resilience.md)).
5. **Fan out to subagents** when breadth, parallel independent edits or adversarial verification genuinely
   help — keep the conclusion, not the dumps. Not for a one-line fix.
6. **One concurrent session = one `git worktree`.** Two sessions in one checkout share an index: they stage
   each other's files and sweep half-done edits into commits (→ [05](05-git-and-deployments.md)).
7. **Repeated procedures become skills; "always do X after Y" becomes a hook** (→ [02](02-skills-and-refactoring.md)).

## Anti-patterns
- 🚫 A wide or irreversible change without plan mode — you review the diff instead of the decision.
- 🚫 Hand-confirming every safe edit — slow, and it trains rubber-stamping.
- 🚫 A cheap model on a migration that can lose data.
- 🚫 Two sessions in one checkout.
- 🚫 A job that must outlive the session left in the session background.
