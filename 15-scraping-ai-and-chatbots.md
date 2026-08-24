# 15 — Scraping, AI APIs, and configurable chatbots

> Pulling data from the web and delegating tasks to AI is the core of many products today. Do it
> **effectively, cheaply, and with a contract** — not by magic. The operational layer (timeouts,
> backoff, rotation, quotas, resumability) lives in → [14](14-operational-resilience.md); this chapter is
> about **using those powers as product features**: where to get data, how to delegate tasks to AI, and
> how to build an assistant you can steer without a deploy.

## Effective scraping — data from the web

- **Official source first.** An API, a feed, an export, a sitemap — HTML scraping is the **last resort**,
  not the first move. An official contract doesn't break on every site redesign.
- **Respect the source.** Honor `robots.txt`/ToS, throttle reasonably, identify yourself. The goal is
  **data, not a DoS** — an aggressive scraper is a legal and ethical problem (→ [09](09-law-and-protecting-the-creator.md)).
- **Parse defensively.** Selectors break on redesigns — **validate the shape** of the result, not just the
  status (the classic "200 + error page," → [14](14-operational-resilience.md)). Selector drift → an alert, not silent zeros.
- **A site answers twice, and the answers can disagree.** `robots.txt` is the owner's *policy*; the bot
  shield (WAF, managed challenge) is *machinery* that cannot read your intent. When the policy permits
  the read and the shield still blocks it, the honest move is to **identify yourself truthfully and ask
  the owner** — not to look for a way around the machine. In the reference project a shop's `robots.txt`
  said `Allow: /` with `search=yes` while its new Cloudflare challenge returned 403 to every request from
  every network; the answer was a descriptive User-Agent plus a written allowlist request, and the
  standing rule that if the request fails, the source leaves the product. **Escalating evasion once the
  policy is on your side still ends in the same place: an operator who blocks you deliberately.**
- **Tell an address block from a shield.** 403 from the server but 200 from another network = the *IP*
  is blocked (relocate the fetch and keep going). 403 from **every** network = the shield is the point;
  moving the fetch is wasted work. One `curl` from each side answers this before you build anything.
- **Normalize at the entry point.** Web data is dirty: fuzzy-match and dedup against **lookup tables**,
  slug, one source of truth (→ [11](11-data-model-and-normalization.md)). Raw material goes in, a clean record stays.
- **Incrementally.** Fetch the **delta** (what changed since last time), not the whole catalog every night —
  cheaper, faster, lighter on the source. Checkpoint and resumability → [14](14-operational-resilience.md).
- **Idempotent loaders.** Re-importing the same data creates no duplicates (→ [04](04-scripts-and-databases.md)).

### Anti-patterns
- 🚫 **Scraping instead of an API** that exists — fragility for no reason.
- 🚫 **A selector with no shape validation** — a silent failure floods the database with junk/zeros.
- 🚫 **A full re-scrape every day** instead of the delta — waste and a ban risk.
- 🚫 **No throttle/identification** — a DoS for the source, a legal problem for you.

## AI APIs for specific tasks — not for everything

- **An LLM where deterministic code can't cope:** extraction from unstructured text, classification,
  summarization, normalizing descriptions, generating content. **Not** for what a `regex`, `SQL`, or a
  plain function will do — that's pricier, slower, and less certain.
- **Match the model to the task.** Cheap/fast for the simple things (classification, extraction), powerful
  for complex reasoning. Claude as the default (→ [08](08-stack-and-technologies.md)). **Measure cost and latency**, don't guess.
- **Force an output contract.** Structure (JSON schema / tool use), **validation**, and a retry on mismatch —
  don't parse prose and hope. Treat LLM output as untrusted input (→ guardrails below).
- **Cache + idempotency.** The same inputs → a stored result; don't call the LLM in a loop over what hasn't
  changed. Expensive calls are cost and latency (→ [13](13-performance-frontend-and-sql.md)).
- **Quotas and budget.** A limit per user/endpoint, cost monitoring, a hard quota on a paid API (→ [14](14-operational-resilience.md)).
- **Batch when you don't need realtime.** Enriching data offline in a pipeline with checkpoints (→ [14](14-operational-resilience.md))
  beats calling the LLM live inside a user request.

### Anti-patterns
- 🚫 **An LLM for what a `regex`/`SQL` will do** — cost and uncertainty where code suffices.
- 🚫 **No output contract** — you parse free prose and pray for the format.
- 🚫 **No cache** on expensive calls — the bill grows linearly with traffic.
- 🚫 **Blind trust in the output** as code/SQL/HTML — an injection vector.

## Configurable chatbots — the assistant as a feature

- **Persona and rules = configuration, not code.** Keep the system prompt, scope, tone, and boundaries as
  **data** (a file/database), versioned in git — you iterate the assistant without a deploy. A prompt
  "baked into" the code is dead configuration.
- **Grounding is mandatory.** The assistant answers from **your data** (context from the database / RAG),
  not the model's memory. Cite the source (→ [11](11-data-model-and-normalization.md)). A hallucinated price/fact is a bug, not an "AI feature."
- **Define scope and refusal.** What the assistant **does** and **doesn't** do; a safe "I don't know" / "that's
  outside my scope" instead of making things up. The model's confidence ≠ correctness.
- **Streaming UX.** A token-by-token response (SSE), conversation history, clear limits (→ [13](13-performance-frontend-and-sql.md), [14](14-operational-resilience.md)).
- **Security (prompt injection).** User content and web data are **data, not instructions**. Don't perform
  side-effect actions from the chat without confirmation, and don't leak secrets or the system prompt (→ [09](09-law-and-protecting-the-creator.md)).
- **Eval like tests.** A golden set of control questions; a prompt change → run it through and measure
  regressions (→ [03](03-testing-and-verification.md)). A prompt with no eval drifts silently.
- **Law.** A disclaimer ("this is not professional advice"), GDPR for storing conversations and data (→ [09](09-law-and-protecting-the-creator.md)).

### Anti-patterns
- 🚫 **Persona baked into the code** — every tone change is a deploy instead of a config edit.
- 🚫 **No grounding** — the assistant "confidently" invents facts/prices.
- 🚫 **No limit/quota** — chat is an open bill and an abuse vector (→ [14](14-operational-resilience.md)).
- 🚫 **Actions from the chat without confirmation** — the model does something irreversible on a user's word.
- 🚫 **Treating user content as instructions** — prompt injection leaks the prompt/secrets.

## For new projects
If the product lives on web data: start from the **official source**, add shape validation and an
idempotent loader **before** you collect the first thousand records. If you use AI: an **output contract
and a cache from the first call**, a quota from the first user. Design the assistant to be **configurable
and grounded** from the start — the system prompt as data, a golden set as a test (→ [03](03-testing-and-verification.md)),
a limit as a rule (→ [14](14-operational-resilience.md)). The rest grows with the project.
