# HERMES-750 — LiteLLM Prompt Runtime Foundation

Status: Closed (original scope) — superseded in place by the LiteLLM + Langfuse migration, documented here rather than in a separate file
Code Branch: feature/hermes-750-portkey-prompt-runtime (original), current runtime lives on top of it via later branches
Original Code Tag: hermes-750-prompt-runtime-v1
Originally Closed: 2026-07-10
Rewritten: 2026-08-21
Server: INTEL-1 / jobfynder-intel-01

---

## 1. What this document is

This file was originally titled "Portkey Prompt Runtime Foundation." Portkey has been fully removed from Jobfynder's infrastructure — **LiteLLM (`https://gateway.jobfynder.com`) is now the sole LLM gateway**, and Langfuse now hosts the live, versioned prompt registry (38 prompts as of this rewrite, up from the original 4). This document is rewritten to describe the runtime as it actually runs today, not as it was originally built. The original closure facts are kept below for the historical record, clearly marked as historical.

---

## 2. Purpose

HERMES-750 gives Hermes a controlled prompt layer for Resume Builder, Matching explanations, Agents, and Support workflows, while keeping external LLM calls disabled by default (`HERMES_PROMPT_RUNTIME_DRY_RUN=true`).

The runtime's job is unchanged from its original design: render a prompt, decide whether it's allowed to run live, call the model, log the result, and trace it — regardless of which provider sits behind the call.

---

## 3. Current architecture (as of 2026-08-21)

```text
Hermes prompt_runtime
  -> fetches prompt definitions from Langfuse (live, not hardcoded)
      GET https://langfuse.jobfynder.com/api/public/v2/prompts
      Auth: Basic (LANGFUSE_PUBLIC_KEY : LANGFUSE_SECRET_KEY)
      Cached in-process, default TTL 300s (HERMES_LANGFUSE_PROMPT_CACHE_SECONDS)
  -> on a live run, calls LiteLLM
      POST https://gateway.jobfynder.com/v1/chat/completions
      Auth: Bearer LITELLM_API_KEY
      Model: the prompt's router alias (see §5)
  -> traces both the render and the generation back to Langfuse
      POST https://langfuse.jobfynder.com/api/public/ingestion
```

Provider name reported by the runtime: `litellm` (`app/prompt_runtime/service.py`, `PROVIDER_NAME = "litellm"`). There is no Portkey code path left in this module — `_call_litellm()` talks to LiteLLM's OpenAI-compatible `/v1/chat/completions` endpoint directly.

---

## 4. Required environment variables (current)

```bash
# LiteLLM (the only LLM gateway - Core and Frontend never hold this key)
LITELLM_API_KEY=<scoped virtual key, see hermes-capability-matrix.md HERMES-600 rows>
LITELLM_BASE_URL=https://gateway.jobfynder.com/v1/chat/completions

# Langfuse (prompt registry + tracing)
LANGFUSE_PUBLIC_KEY=<project API key, note = "hermes-production...">
LANGFUSE_SECRET_KEY=<matching secret>
LANGFUSE_BASE_URL=https://langfuse.jobfynder.com

# Runtime behavior
HERMES_PROMPT_RUNTIME_DRY_RUN=true
HERMES_PROMPT_RUN_LOG_DIR=/hermes-runtime/prompt-runs
HERMES_PROMPT_DEFAULT_MODEL=anthropic/claude-haiku-4-5
HERMES_LANGFUSE_PROMPT_CACHE_SECONDS=300
```

No `PORTKEY_*` variables exist in the current `.env.example` — they were removed as part of this rewrite's companion cleanup. `HERMES_PROMPT_DEFAULT_MODEL` is the one-time fallback model if a prompt's own router alias has no healthy deployment on LiteLLM.

---

## 5. Router aliases confirmed live on LiteLLM (verified 2026-08-21)

Checked directly against the LiteLLM admin UI (`https://gateway.jobfynder.com/ui/models-and-endpoints`):

| Router alias | Backing model | Verified |
|---|---|---|
| `generate-small` | `anthropic/claude-haiku-4-5` | ✅ present |
| `extract-fast` | `anthropic/claude-haiku-4-5` | ✅ present |
| `reasoning-small` | `anthropic/claude-haiku-4-5` | ✅ present |

Prompt definitions must reference these aliases, never a raw provider/model string — this was true under Portkey and remains true under LiteLLM. The `litellm_router_alias` field on each Langfuse-sourced prompt definition carries this through (`app/prompt_runtime/langfuse_prompts.py`).

---

## 6. Incident found and fixed during this rewrite: wrong Langfuse key

While verifying this document, the server's configured `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` turned out to be a personal "Claude Code" API key, not the dedicated `hermes-production` key — a mistake from an earlier session, not a Portkey-related issue. Fixed 2026-08-21:

1. Rotated a fresh key pair in Langfuse (`hermes-production-2`, since the original `hermes-production` key's secret was unrecoverable — Langfuse only shows a secret once, at creation).
2. Updated `.env` on `jobfynder-intel-01` and recreated the `hermes-api` container (`docker compose up -d --force-recreate hermes-api` — a plain `restart` does **not** reload `.env` for an existing container; this cost real debugging time and is worth remembering).
3. Verified live: `list_prompts()` now successfully loads all 38 Langfuse prompts.

**A separate, still-open performance issue found in the same investigation:** the registry fetch takes **~33 seconds** on a cache miss, because `_refresh_cache()` in `app/prompt_runtime/langfuse_prompts.py` fetches the prompt list, then fetches each of the 38 prompts individually in a sequential loop (N+1 pattern) — one HTTP round-trip per prompt, no batching or parallelism. The cache lasts 5 minutes, so this only bites once per window, but any caller with a normal HTTP timeout (10–30s) hitting that window will see a failure even though the underlying fetch would have succeeded given more time. **Not fixed as part of this rewrite** — recommended fix: fetch prompt details concurrently (e.g. a small thread pool or `asyncio.gather`), or extend the cache TTL, or warm the cache on container startup instead of on first request.

---

## 7. Historical closure record (original scope, 2026-07-10)

Kept for the record — this is what HERMES-750 looked like when it first closed, before the Portkey→LiteLLM migration and the Langfuse dynamic-registry work layered on top of it.

- runtime_version: `hermes_prompt_runtime_v1`
- registry_version: `hermes_prompt_registry_v1` (static, 4 hardcoded prompts — since replaced by `hermes_langfuse_prompt_registry_v1`, 38 prompts, fetched live)
- dry_run_default: true
- external_llm_call: false at close

Original completed scope:

- Prompt runtime package
- Static prompt registry (4 prompts: Resume Builder summary improvement, Resume Builder bullet rewrite, Matching fit explanation, Support reply draft)
- Dry-run execution path
- Resume no-fabrication safety guardrail
- Required-variable validation
- Human-review-first policy
- JSONL prompt run logging
- RBAC-protected `/prompts` APIs
- Prompt runtime validation scripts and API fixtures

The original prompt IDs from this closure (`resume_builder.summary_improve`, `resume_builder.bullet_rewrite`) **no longer exist** under those names — the Langfuse-hosted registry uses a different naming convention (`jf.*`, e.g. `jf.resume.section.polish`, `jf.jobs.fit.explain`). This is why the original closure check scripts (`hermes-750-prompt-runtime-check.py`, and by extension parts of `hermes-800-foundation-check.py`) fail today — they assert on prompt IDs that were retired when the registry moved to Langfuse. **Open item:** these scripts need updating to the current prompt IDs, or retiring in favor of a check against the live Langfuse registry contents.

---

## 8. Current API surface (unchanged shape, different backing provider)

- `GET /prompts/health` — requires `agents:read`. Reports `provider: "litellm"`, `litellm_configured`, `langfuse_configured`, `dry_run_default`.
- `GET /prompts/registry` — requires `agents:read`. Lists all prompts currently cached from Langfuse.
- `GET /prompts/{prompt_id}` — requires `agents:read`.
- `POST /prompts/run` — requires `agents:run`. `mode: "dry_run"` (default) renders without calling LiteLLM. `mode: "live"` executes for real if the server-wide dry-run default allows it.

---

## 9. Resume Builder safety (unchanged)

Hermes may improve wording and clarity.

Hermes must not invent employers, dates, degrees, certifications, projects, tools, clients, work authorization, metrics, years of experience, job titles, or achievements.

If evidence is missing, Hermes must ask a question or mark the field as missing.

---

## 10. Status

The prompt runtime foundation itself is production-safe: dry-run-first, RBAC-protected, human-review-required. The provider underneath it changed from Portkey to LiteLLM without changing this contract. Two open items carried forward from this rewrite: the N+1 registry-fetch performance issue (§6) and the stale prompt-ID check scripts (§7).
