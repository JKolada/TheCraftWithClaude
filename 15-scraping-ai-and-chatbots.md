# 15 — Scraping, AI APIs and configurable chatbots

> Web data and AI as product features — effective, cheap, and **under a contract**. The operational layer
> (timeouts, backoff, quotas, resumability) → [14](14-operational-resilience.md).

## Scraping

1. **An official source first** (API, feed, export, sitemap); HTML scraping is the last resort.
2. **Respect the source:** `robots.txt`/ToS, a reasonable throttle, a truthful User-Agent (→ [09](09-law-and-protecting-the-creator.md)).
3. **A site answers twice — policy and machinery.** When `robots.txt` allows the read but a bot shield
   blocks it, identify yourself and **ask the owner**; never engineer a way around the shield. If the request
   fails, the source leaves the product.
4. **Tell an IP block from a shield before building anything:** 403 here but 200 from another network = the
   address is blocked (relocate the fetch); 403 from every network = the shield is the point.
5. **Validate the shape of the result**, not the status — selector drift raises an alert, never silent zeros.
6. **Normalize at the entry point** against lookup tables (→ [11](11-data-model-and-normalization.md)); fetch
   the **delta**, not the whole catalog; loaders are idempotent (→ [04](04-scripts-and-databases.md)).

## AI APIs

7. **An LLM only where deterministic code can't cope** (unstructured extraction, classification, summaries) —
   never for what a regex, SQL or a function does.
8. **Force an output contract:** JSON schema / tool use, validation, retry on mismatch. LLM output is untrusted input.
9. **Cache identical inputs; quota every paid call; enrich offline in a checkpointed batch** rather than live in
   a user request. Measure cost and latency per task.

## Chatbots

10. **Persona, scope and rules are configuration** (versioned data), not code — tuned without a deploy.
11. **Grounded in your data, with the source cited**; a safe "I don't know" instead of invention.
12. **User and web content are data, never instructions** (prompt injection): no side-effect action without
    confirmation, no leaking the system prompt or secrets.
13. **A golden set of questions runs like tests** on every prompt change.
14. **A disclaimer and a privacy basis for stored conversations** (→ [09](09-law-and-protecting-the-creator.md)).

## Anti-patterns
- 🚫 Scraping when an API exists; a full re-scrape every night.
- 🚫 Evading a bot shield the owner put up.
- 🚫 Parsing free prose and hoping for the format.
- 🚫 No cache and no quota on paid calls.
- 🚫 A persona baked into the code; an ungrounded assistant.
- 🚫 Acting on a chat message without confirmation.
