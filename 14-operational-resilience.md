# 14 — Operational resilience and external dependencies

> Commandments III, V, VI at runtime: prod lives in an unreliable world. The worst bugs don't shout — they
> hang, log everyone out, or drain the budget. Almost every rule here was paid for by an incident.

## Rules

1. **One bad request degrades that request, not the service:** process-level catchers for unhandled
   rejections/exceptions, async routes that forward errors, a 500 handler that leaks no stack trace. Defend
   against real edge data (an OAuth account without a password, `null` where a string is assumed).
2. **Long jobs are resumable:** checkpoint completed units, save every N, idempotent end-to-end — a crash
   costs the last batch, not the run.
3. **Match the runner to the job's lifetime:** the agent's background survives turns but dies with the
   session; anything that must outlive the conversation runs as a **detached process or OS-scheduled task**.
4. **External sources are hostile:** a timeout on every call, retry with exponential backoff and a cap, and
   **validate the response, not the status** — "200 + an error page" is a failure.
5. **The provider's network breaks working code only in prod:** e.g. outbound SMTP 465 blocked → use 587 +
   STARTTLS with hard connect/greeting timeouts. "Sent" ≠ delivered: verified sender domain (SPF/DKIM) and a
   real test send. Verify on the provider, not locally.
6. **Every paid resource sits behind a hard quota** — per user and tier, enforced server-side, with a clear
   message and the reset date shown up front.
7. **Know prod is alive:** structured logs with levels (no secrets, no full PII), `/healthz`, an external
   uptime ping, alerts on what hurts (5xx spikes, failed payments/mail, a job that didn't run), errors routed
   somewhere you'll see them.
8. **Recurring jobs: watch the result, not the runner.** Assert on the **age of the freshest record per
   source** (`MAX(updated_at)` grouped by source), not on an exit code — a green report once ran for three
   days beside 44% of the data frozen. A report covers only the paths it knows about.
9. **Scheduler settings are production and live outside the repo** (retry after a missed start, power and
   network conditions, account, working directory) — write them into the runbook and re-check after any OS,
   hardware or account change.
10. **Every incident becomes a dated, numbered lesson in the runbook** (→ [05](05-git-and-deployments.md)).

## Anti-patterns
- 🚫 No global error catcher — one bad request restarts the service for everyone.
- 🚫 A long scraper without checkpoints, run from the session background.
- 🚫 An external call without timeout and backoff.
- 🚫 A paid API without a quota.
- 🚫 Sessions in process memory — every deploy logs everyone out.
- 🚫 A recurring job watched by its own exit code.
- 🚫 Secrets or PII in logs.
