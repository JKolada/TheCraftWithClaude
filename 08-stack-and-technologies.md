# 08 — Stack and technologies

> The golden rule of altitude applied to tools: *the simplest thing that meets today's requirement*; add
> complexity when a metric forces it (→ [12](12-flexibility-and-scalability.md)).

## Defaults (depart deliberately, with an ADR)

| Layer | Default | Switch when |
|---|---|---|
| Agent / process | **Claude Code** + **Git** + **GitHub** (repo, PRs, Issues) | — |
| Backend, scripts, data | **Python** (FastAPI for an API, pytest) — the widest ecosystem for scripts, data and AI glue | the job is done better elsewhere: **Go** (concurrent network services, one static binary), **Rust** (hot paths, memory safety, small footprint), **Kotlin** (JVM libraries, Android), **TypeScript/Node** (the web layer is already JS) |
| Database | **SQLite** (WAL) | concurrent writes, roles, heavy relations → **PostgreSQL** |
| Web / front | server-rendered HTML + a little vanilla JS | genuinely rich interaction → a framework (e.g. Next.js) |
| API | REST/JSON with an explicit contract (OpenAPI) | — |
| Cache / queue | none | a measured traffic profile → Redis |
| Packaging | Docker where dependencies hurt | a dependency-free script → no container |
| Hosting | **one VPS** (e.g. Hetzner) + nginx + `systemd`/`pm2` — a **monolith** | uneven/global traffic, cold start acceptable → serverless |
| Icons | **Lucide only** (one geometry, one sprite) | — |
| LLM | Claude via the official SDK, streamed (→ [13](13-performance-frontend-and-sql.md)) | — |

## Rules

1. **The monolith is the default architecture:** one app, one database, one server — one deploy, one log,
   one backup, one rollback. Split into services only when traffic, team or failure isolation demands it.
2. **The language is chosen by fit, not by habit.** Python is the default, not a dogma: switch when
   efficiency, concurrency, deployability or a library that only exists in another ecosystem decides — and
   say which, with a number or the missing library, in an ADR. One language per layer, not one per mood; a
   rewrite "for speed" needs a measurement first (→ [13](13-performance-frontend-and-sql.md)).
3. **Testable from the first line beats trendy.** A technology you can't cover with fast, deterministic
   tests is the wrong choice (→ [03](03-testing-and-verification.md)).
4. **Boring and mature over new:** ecosystem, documentation and testability decide, not hype.
5. **Reproducible environments:** pinned dependencies (lock file), a virtual environment / image.
6. **Secrets live in env or a secret store — never in the repo.**
7. **Every non-default choice gets an ADR:** the why and the rejected alternatives, in `docs/`.

## Anti-patterns
- 🚫 Microservices, Kubernetes or a distributed database for an MVP.
- 🚫 A stack chosen for the CV.
- 🚫 A heavy SPA where server-rendered HTML would do.
- 🚫 Mixing icon libraries.
- 🚫 Unpinned dependencies — "it worked yesterday".
- 🚫 Python forced onto a job it serves badly (a hot path, a concurrent service, a library that lives on the JVM) — or a rewrite in a "faster" language with no measurement behind it.
