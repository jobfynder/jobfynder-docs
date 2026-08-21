# HERMES-775 — LiteLLM Production Runtime and Multi-Model Routing

Status: Retired — original scope never built, premise superseded by the LiteLLM migration
Originally: "Portkey Production Runtime and Multi-Model Routing," Status: Open, zero code written
Rewritten: 2026-08-21

---

## 1. What happened to this module

HERMES-775 was opened to build production Portkey integration with multi-model routing, budgets, circuit breakers, and PII redaction. As of this rewrite, its own doc stated: *"No application implementation changes, production Portkey calls, or external LLM execution have been enabled."* Zero code was ever written under `feature/hermes-775-prompt-runtime-production` beyond the plan itself.

Before any of it was built, Portkey was removed from the project entirely and replaced with LiteLLM. HERMES-775's entire premise — production *Portkey* integration — is gone. This document is not a like-for-like LiteLLM port of the old plan; it's an honest accounting of what's still needed versus what LiteLLM already gives Jobfynder for free.

---

## 2. What LiteLLM already provides natively (verified 2026-08-21 against the live admin UI at `https://gateway.jobfynder.com/ui/`)

A meaningful chunk of what HERMES-775 planned to hand-build is a *configuration*, not an *engineering task*, once you're on LiteLLM's proxy:

- **Per-key spend tracking and budgets** — confirmed live: every virtual key (`hermes-desktop-agent`, `jf-hermes-production`, etc.) shows real-time spend against a budget cap with a reset schedule (e.g. "$1.8170 of $20", "Budget Reset: Aug 31"). This is exactly the "per-request, per-user daily, per-tenant monthly... budgets" HERMES-775 originally scoped as custom work.
- **Model access groups per key** — each key is scoped to specific router aliases (e.g. `jf-hermes-production` → `jf-fast, jf-structured, jf-reasoning`, +2 more), not a blanket "any model." This covers the "capability allowlists" requirement.
- **Router aliases decoupled from provider/model names** — `generate-small`, `extract-fast`, `reasoning-small` all map to `anthropic/claude-haiku-4-5` today and can be repointed without touching Hermes code, satisfying "no hardcoded provider/model dependency."
- **Multiple backend providers already registered** — the Models page lists DeepInfra, DeepSeek, Google Gemini, and OpenAI models alongside Anthropic, meaning multi-provider routing infrastructure already exists at the gateway level; Hermes doesn't need to build its own provider abstraction.

## 3. What's still genuinely open (not covered by LiteLLM's proxy features)

- **Claim-level evidence verification** — LiteLLM has no concept of "did this generated resume bullet invent a fact." This is Hermes application logic (see `app/resume_builder/` safety guardrails, HERMES-800) and stays Hermes's responsibility regardless of gateway.
- **Prompt-injection protection** — gateway-level rate limiting isn't the same as content-level injection defense. Still open, still Hermes's job.
- **PII and secret redaction before logging/tracing** — not something LiteLLM or Langfuse does for you by default; still needs explicit handling in `send_langfuse_trace()` (`app/prompt_runtime/service.py`) if sensitive resume/candidate content shouldn't be traced verbatim.
- **Circuit breaker / provider failure handling beyond the single fallback** — the current runtime does one fallback attempt to a default model (`_call_litellm()` in `app/prompt_runtime/service.py`), not a full circuit breaker with backoff. Adequate for current volume; would need real engineering if call volume or provider instability grows.

## 4. Recommendation

Given the budget/routing/allowlist pieces are now solved by LiteLLM's own admin surface, re-scoping this module as originally written would mean re-building things that already exist. If this module is picked back up, it should be re-scoped narrowly to the four genuinely-open items in §3 — evidence verification, prompt-injection defense, PII redaction, and (if warranted by scale) real circuit-breaking — not the full original checklist.

## 5. Status

Retired as originally scoped. No code exists to close or carry forward. Re-opening this stream should start from §3, not from the original Portkey-era backlog.
