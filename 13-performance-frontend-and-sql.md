# 13 — Performance: frontend and SQL

> Commandment III applied to speed: "feels faster" doesn't exist — **before/after numbers** do. Standard
> hygiene is assumed (indexes on hot `WHERE`/`JOIN` columns, no N+1, no `SELECT *`, WebP + `srcset`, lazy
> loading below the fold, self-hosted fonts with `font-display: swap`, server-side pagination).

## Rules

1. **Measure first, prove after.** Lighthouse / Core Web Vitals (LCP, CLS, INP) for the front,
   `EXPLAIN QUERY PLAN` for SQL — reported **before and after**. No optimization without a number; an
   unmeasured "optimization" can be a regression in disguise.
2. **A Lighthouse baseline right after the first working page** — otherwise there's nothing to compare to.
3. **Cache-bust per deploy:** statics are `immutable` with a long `max-age`, so every asset URL carries
   `?v=<git-short-hash>` — otherwise users run the old app until a hard refresh (→ [05](05-git-and-deployments.md)).
4. **Stream LLM responses** token by token (SSE) — never a blank screen until generation ends (→ [15](15-scraping-ai-and-chatbots.md)).
5. **Expensive aggregates are cached** (a stats snapshot with a live fallback), not recounted on every request.

## Mobile: the viewport is a moving target

6. **`100dvh`, not `100vh`, for full-screen sheets** — declare `100vh` first as a fallback, then `100dvh`
   (the last rule an engine understands wins).
7. **Keyboard-sticky elements anchor to `visualViewport`** (`height`/`offsetTop`, re-read on its
   `resize`/`scroll`), not `position: fixed; bottom: 0`. Snap to the new size; don't animate the keyboard.
8. **Reset `flex-basis` where the main axis flips** — a row's `flex: 1 1 220px` becomes a 220px-tall empty
   box in a column (`flex: 0 0 auto` at that breakpoint).
9. **The emulator lies:** measure real geometry (`getBoundingClientRect`) and keep a device-profile test
   (e.g. a Playwright project pinned to a phone): no horizontal overflow, key element above the fold.

## Anti-patterns
- 🚫 Optimizing without a measurement.
- 🚫 Recomputing `COUNT(*)` over the whole database on every request.
- 🚫 Blocking the UI until the full LLM response arrives.
- 🚫 `100vh` sheets and `fixed; bottom: 0` inputs on mobile.
- 🚫 "Fixing" mobile from a desktop-emulator screenshot.
