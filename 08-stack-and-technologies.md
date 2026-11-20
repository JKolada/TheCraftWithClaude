# 08 — Stack and technologies

> The golden rule of altitude applied to tools: *the simplest thing that meets today's requirement*; add
> complexity when a metric forces it (→ [12](12-flexibility-and-scalability.md)).

## Defaults (depart deliberately, with an ADR)

| Layer | Default | Switch when |
|---|---|---|
| Agent / process | **Claude Code** + **Git** + **GitHub** (repo, PRs, Issues) | — |
| Backend, scripts, data | **Python** (FastAPI for an API, pytest) | the web layer is already JavaScript → **Node.js + Express**, one language per layer |
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
2. **Testable from the first line beats trendy.** A technology you can't cover with fast, deterministic
   tests is the wrong choice (→ [03](03-testing-and-verification.md)).
3. **Boring and mature over new:** ecosystem, documentation and testability decide, not hype.
4. **Reproducible environments:** pinned dependencies (lock file), a virtual environment / image.
5. **Secrets live in env or a secret store — never in the repo.**
6. **Every non-default choice gets an ADR:** the why and the rejected alternatives, in `docs/`.

## Anti-patterns
- 🚫 Microservices, Kubernetes or a distributed database for an MVP.
- 🚫 A stack chosen for the CV.
- 🚫 A heavy SPA where server-rendered HTML would do.
- 🚫 Mixing icon libraries.
- 🚫 Unpinned dependencies — "it worked yesterday".
