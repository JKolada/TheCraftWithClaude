# 03 — Testing and verification

> Commandment III: *verify, don't declare.* Tests are the net you run again and again; verification is
> observed proof that **this** change does what it should. Both are mandatory.

## Rules

1. **Every commit that changes behavior carries a test.** New endpoint → route test; new threshold or
   fallback → threshold test; fixed bug → a test that reproduced it first. A behavior change without a test
   is an **incomplete** commit. TDD (red → green → refactor) is the default mode.
2. **Show proof, don't ask the user to check:** HTTP code / redirect, a confirming HTML fragment, numbers
   from the database (`integrity_check: ok`), a screenshot for visual changes.
3. **Smoke tests check the right page, not just `200`** — a marker proving the expected content rendered.
   Test auth from both sides: anonymous is bounced, logged-in sees the content.
4. **After a deploy, smoke the live server** (via `localhost` behind the maintenance flag).
5. **Report honestly:** failures with their output; skipped steps as skipped; a failure caused by data drift
   (stale fixture) named as such, with a follow-up — not hidden, not used as a blocker.
6. **Numbers come from the source**, not from memory or docs: `SELECT COUNT(*)` doesn't lie.
7. **A guard is proven by the incident, not by the fixture.** A check written after an outage is replayed
   against that outage's **real data** before it's trusted — fixtures share the author's blind spot (a
   freshness check once passed nine green tests and missed its own outage: `>` where `>=` was needed). Then
   freeze the boundary in a fixture, with a test **on** the boundary.
8. **Test the contract, not the implementation; keep the suite fast and deterministic** (isolate I/O, seed
   randomness, serialize tests that share a port/DB). **CI gates** merge and deploy.
9. **Web projects carry by default:** per-page SEO meta, canonical + hreflang, JSON-LD, colour contrast and
   keyboard navigation, **language parity as a failing test**, no dead internal links.

## Anti-patterns
- 🚫 "Should work" as a conclusion.
- 🚫 One test run, "suite green" declared.
- 🚫 No smoke after deploy "because the tests passed".
- 🚫 "It compiles" confused with "it works for the user".
- 🚫 Weakening a test or guard to make it green.
