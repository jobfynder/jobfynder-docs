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
  -> fetches prompt definitions from Langfuse (live), merged with a small
     local fallback registry for two prompts since 2026-09-07 (see §11)
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

**A separate performance issue found in the same investigation, fixed 2026-08-21:** the registry fetch took **~33 seconds** on a cache miss, because `_refresh_cache()` in `app/prompt_runtime/langfuse_prompts.py` fetched the prompt list, then fetched each of the 38 prompts individually in a sequential loop (N+1 pattern) — one HTTP round-trip per prompt, no batching or parallelism. The cache lasts 5 minutes, so this only bit once per window, but any caller with a normal HTTP timeout (10–30s) hitting that window would see a failure even though the underlying fetch would have succeeded given more time.

Fixed on branch `perf/hermes-750-langfuse-concurrent-prompt-fetch`: prompt details now fetch concurrently via a `ThreadPoolExecutor` (stdlib, no new dependency), default concurrency 8, tunable via `HERMES_LANGFUSE_PROMPT_FETCH_CONCURRENCY`. Verified live against the real Langfuse instance: **33.59s → 7.55s** for the same 38 prompts, correct `prompt_count` both times. A single failed detail fetch still only drops that one prompt, same as before — it never aborts the whole refresh (covered by a dedicated test in the new check script, `scripts/hermes-750-langfuse-concurrent-fetch-check.py`).

---

## 7. Historical closure record (original scope, 2026-07-10)

Kept for the record — this is what HERMES-750 looked like when it first closed, before the Portkey→LiteLLM migration and the Langfuse dynamic-registry work layered on top of it.

- runtime_version: `hermes_prompt_runtime_v1`
- registry_version: `hermes_prompt_registry_v1` (static, 4 hardcoded prompts — replaced 2026-08-21 by `hermes_langfuse_prompt_registry_v1`, 38 prompts, fetched live; the string `hermes_prompt_registry_v1` was reused 2026-09-07 for an unrelated, non-static merged registry — see §11, don't confuse the two)
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
- `GET /prompts/registry` — requires `agents:read`. Lists all prompts currently cached from Langfuse, merged with the local fallback registry (see §11).
- `GET /prompts/{prompt_id}` — requires `agents:read`.
- `POST /prompts/run` — requires `agents:run`. `mode: "dry_run"` (default) renders without calling LiteLLM. `mode: "live"` executes for real if the server-wide dry-run default allows it.

---

## 9. Resume Builder safety (unchanged)

Hermes may improve wording and clarity.

Hermes must not invent employers, dates, degrees, certifications, projects, tools, clients, work authorization, metrics, years of experience, job titles, or achievements.

If evidence is missing, Hermes must ask a question or mark the field as missing.

---

## 10. Status

The prompt runtime foundation itself is production-safe: dry-run-first, RBAC-protected, human-review-required. The provider underneath it changed from Portkey to LiteLLM without changing this contract. The N+1 registry-fetch performance issue (§6) is fixed. The local-fallback-registry leak (§11) is fixed as of commit `a745fed`, 2026-09-08 (code-verified, not live-verified). One open item remains: the stale prompt-ID check scripts (§7) — note that `hermes-750-prompt-runtime-api-check.py` specifically was already corrected as part of the §11 fix.

---

## 11. Update 2026-09-07 — local fallback prompt registry

Commit `8319c43` on `jobfynder/hermes` `main` (`feat(understanding): extract resume sections and international phones without an LLM`) adds a small local prompt registry alongside the Langfuse one, so two fallback-extraction prompts stay available even when Langfuse is unreachable:

- New file `app/prompt_runtime/local_prompts.py` — loads `app/prompt_runtime/registry.json`'s `prompts` array into `PromptDefinition` objects (`get_local_prompt()`, `list_local_prompts()`).
- `registry.json` gains two entries: `jf.onboarding.profile-import.extract` (v2) and `jf.resume.parse` (v2), both `default_model: anthropic/claude-haiku-4-5`, both `metadata.source: "local"`, both carrying `safety_policy: hermes_resume_no_fabrication_v1` and `human_review_required: true` (same safety posture as every other fallback-extraction prompt — see §9).
- `app/prompt_runtime/langfuse_prompts.py`: `list_prompts()` and `get_prompt()` now merge sources — when Langfuse is not configured, only the local registry is returned; when it is, Langfuse's cached entries take precedence over local ones with the same `prompt_id` (`{**local, **cache}`). `list_prompts()`'s `registry_version` field changed from `hermes_langfuse_prompt_registry_v1` to `hermes_prompt_registry_v1`.

**Correction (2026-09-08, this line originally said the opposite).** The claim above — "does not add new prompts to the catalog count" — does not hold for `list_prompts()`, and is worth walking through carefully because the mistake is easy to make from the diff alone. `app/prompt_runtime/registry.json` is not new in this commit; it already existed with **four** prompts from the original 2026-07-10 closure (`resume_builder.summary_improve`, `resume_builder.bullet_rewrite`, `matching.fit_explanation`, `agents.support_reply_draft` — confirmed via `git show a837505:app/prompt_runtime/registry.json`), but until this commit nothing in the runtime ever loaded that file — `local_prompts.py` did not exist, and `langfuse_prompts.py` had no reference to `registry.json`. Commit `8319c43` does two things at once: it adds 2 new entries to that file (`jf.onboarding.profile-import.extract`, `jf.resume.parse`), **and** it wires the whole 6-entry file into `list_prompts()`/`get_prompt()` for the first time via `_merged_prompts()` (`{**local, **langfuse_cache}` — a union, not a Langfuse-first-with-local-only-as-fallback lookup for `list_prompts()`).

Verified locally (Langfuse unconfigured, so the merge falls through to local-only): `list_prompts()` returns `prompt_count: 6`, not the 2 this document's earlier wording implied — all six IDs from `registry.json`, including the four §7 already documents as retired from the Langfuse-hosted registry. Because the merge is a union, those four are not conditional on Langfuse being down: once this ships, they resurface in `GET /prompts/registry` **any time Langfuse is reachable too**, since Langfuse's current 38 prompts don't contain those four IDs to override them. Expect the deployed `prompt_count` to read up to 42 (38 Langfuse + 4 resurfaced local-only), not 38 — `hermes-parsing-and-prompts-api-guide.md` has been flagged with the same caveat, not silently corrected, since neither number has been live-confirmed.

**New open item, not fixed by this commit:** decide whether those four retired IDs belong in `registry.json` at all now that the file is live-wired — if not, they should be removed before/at deploy rather than left to resurface as an accidental side effect.

**No live verification performed for this update** — based on the commit diff, direct inspection of `registry.json`'s pre-commit content via `git show`, and running the accompanying tests locally (`tests/prompt_runtime/test_local_resume_extract.py`, `pytest tests/prompt_runtime/` → 6 passed) only; no SSH/API check was run against INTEL-1 to confirm the deployed `registry_version` or `prompt_count` live.

**Fixed 2026-09-08, commit `a745fed` on `jobfynder/hermes` `main`** (`fix(prompt-runtime): remove 4 dead legacy prompts leaking into every registry listing`). The "new open item" immediately above is resolved by deletion, not by changing the merge behavior: the four retired IDs (`resume_builder.summary_improve`, `resume_builder.bullet_rewrite`, `matching.fit_explanation`, `agents.support_reply_draft`) were removed outright from `app/prompt_runtime/registry.json`, which now holds only the two legitimate fallback entries (`jf.onboarding.profile-import.extract`, `jf.resume.parse`). The merge in `list_prompts()`/`get_prompt()` is still a union, but there is nothing left in the local file to leak. The same commit updated the one check script (`scripts/hermes-750-prompt-runtime-api-check.py`) and one fixture (`docs/hermes-750/api-fixtures/prompt-run-dry-run-request.json`) that still referenced `resume_builder.summary_improve`, pointing both at `jf.resume.summary.generate` instead (same "resume" domain, so the fabrication-safety-blocking assertion still exercises `app/prompt_runtime/safety.py`'s domain-based check).

Verified locally this run (Langfuse unconfigured, so `list_prompts()` falls through to local-only): `list_local_prompts()` and `list_prompts()` both now return `prompt_count: 2` (`jf.onboarding.profile-import.extract`, `jf.resume.parse`), down from the pre-fix 6 — confirming the four dead entries are actually gone from the source file, not just hidden. `pytest tests/prompt_runtime/` → 6 passed against the fixed code. Since both surviving local entries share their `prompt_id` with an existing Langfuse-hosted prompt, Langfuse's version wins on merge whenever Langfuse is healthy — so the live `GET /prompts/registry` `prompt_count` is expected to read 38 again once this deploys, not 42. **Not live-verified** — no SSH/API credentials configured in this environment to re-pull `GET /prompts/registry` against INTEL-1 and confirm 38 directly; treat "38" as expected-from-code, not live-confirmed, until someone with server access re-checks it.
