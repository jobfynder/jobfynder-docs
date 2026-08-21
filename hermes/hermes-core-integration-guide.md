# Hermes ↔ Jobfynder CORE Integration Guide

Status: Active — canonical integration reference
Owner: Jobfynder-Infra
Audience: Backend and Frontend developers integrating with Hermes
Server: INTEL-1 (`jobfynder-intel-01`), API base `https://hermes.jobfynder.com` (internal: `http://localhost:8000`)
Last verified against running code: 2026-08-21

---

## Table of Contents

1. [Change Log](#1-change-log)
2. [Executive Summary](#2-executive-summary)
3. [System Overview and Architecture](#3-system-overview-and-architecture)
4. [Authentication Flow for the Hermes API](#4-authentication-flow-for-the-hermes-api)
5. [Login/Auth Endpoints and Example API Calls](#5-loginauth-endpoints-and-example-api-calls)
6. [Developer Documentation](#6-developer-documentation)
7. [End-to-End Integration with Jobfynder CORE](#7-end-to-end-integration-with-jobfynder-core)
8. [Deployment and Operational Considerations](#8-deployment-and-operational-considerations)
9. [Security and Compliance Notes](#9-security-and-compliance-notes)
10. [API Samples and Code Blocks](#10-api-samples-and-code-blocks)
11. [Troubleshooting Guide](#11-troubleshooting-guide)
12. [Recommended Testing Plan](#12-recommended-testing-plan)
13. [Glossary](#13-glossary)
14. [References](#14-references)

---

## 1. Change Log

| Date | Change |
|---|---|
| 2026-08-21 | First edition. Consolidates verified state across all Hermes modules (HERMES-000 through HERMES-850) into a single integration reference. LiteLLM is the only LLM gateway described here. |

Update this table, not just the body text, whenever this document changes materially. Follow the Hermes Documentation Map's rule: this file lives in `jobfynder/jobfynder-docs`, not inside the code repo.

---

## 2. Executive Summary

Hermes is Jobfynder's intelligence layer. It sits between Jobfynder CORE and any LLM, and its one non-negotiable rule is: **CORE and the Frontend never talk to an LLM directly, and never hold an LLM API key.** Every generative or parsing task CORE needs goes through Hermes, which decides — deterministically wherever possible — whether an LLM call is even necessary.

**What's actually built and verified, as of this document:**

- 106+ live API endpoints across understanding (resume/JD parsing), matching, taxonomy, submission workflow, integrations, multi-agent (dry-run only), prompt runtime, resume builder, and channel intake (Telegram live; Email/Gmail/Microsoft Graph built and tested but not yet connected to real credentials; WhatsApp/Slack/Teams/Google Chat contract-ready).
- Deterministic-first design confirmed in code and by direct testing: resume/JD parsing, matching, taxonomy normalization, and submission workflow all run without calling an LLM in the common case. An LLM is only invoked when deterministic confidence is too low, and only through the single controlled Prompt Runtime module.
- RBAC enforced on almost every route via bearer token and permission strings — with one confirmed, still-open gap (Section 9).

**What's not yet true, so nobody is surprised by it:**

- Hermes does not write directly into Jobfynder's production database. It produces structured output and, for some flows, an internal draft object. Turning that into a real Candidate/Job/Submission record in CORE's database is CORE's job, and that consuming logic's completeness on the CORE side is outside this document's verification scope — check with the CORE integration owner before assuming it's wired end to end for a given flow.
- Two real, currently-open issues are documented here rather than hidden: a Langfuse prompt-registry fetch that takes ~30+ seconds on a cold cache (Section 11), and one RBAC gap on two endpoint groups (Section 9).

**Success metrics for this integration:**

- Every CORE call to Hermes carries a bearer token scoped to the minimum permission it needs.
- No raw resume, job description, or recruiter message text is ever passed directly to an LLM prompt variable without first going through a Hermes Context Card or deterministic parser.
- CORE never holds `LITELLM_API_KEY` or a Langfuse secret key.
- A cold-start Hermes deployment passes the recommended test plan (Section 12) before being pointed at production traffic.

---

## 3. System Overview and Architecture

### 3.1 Component map (textual diagram)

```text
┌─────────────┐      ┌──────────────────────────────┐      ┌───────────────┐
│  Frontend    │      │        Jobfynder CORE          │      │    Hermes     │
│ (React/Vite) │─────▶│  (NestJS, Postgres, PM2)       │─────▶│ (FastAPI,     │
│              │◀─────│                                │◀─────│  Python)      │
└─────────────┘      └──────────────────────────────┘      └───────┬───────┘
                                                                     │
                                    ┌────────────────────────────────┼────────────────────────┐
                                    │                                │                          │
                                    ▼                                ▼                          ▼
                            ┌───────────────┐              ┌────────────────┐         ┌──────────────────┐
                            │   LiteLLM      │              │   Langfuse      │         │  Channel providers │
                            │   Gateway      │              │  (prompt store  │         │  Telegram (live)   │
                            │  (LLM calls    │              │   + tracing)    │         │  Gmail/Graph (built,│
                            │   only)        │              │                 │         │  not live)          │
                            └───────────────┘              └────────────────┘         └──────────────────┘
```

**Frontend never talks to Hermes directly.** All Hermes calls are proxied through Jobfynder CORE, which holds the Hermes bearer token. This is the same shape as the LLM-access rule one layer up: Frontend never holds a Hermes token, CORE never holds an LLM key.

### 3.2 Key components

- **Hermes** — FastAPI service, deployed as a single Docker container (`hermes-api`) on `jobfynder-intel-01`. Stateless except for an in-process cache and a persistent runtime volume (`/hermes-runtime`, bind-mounted from the host — survives container restarts, holds drafts, prompt-run logs, taxonomy suggestion queue, event logs).
- **Jobfynder CORE** — NestJS backend, Postgres-backed, PM2-managed (not containerized). Owns all persistent business data (Users, Jobs, Candidates, Submissions). Calls Hermes for anything requiring parsing, matching, taxonomy, or generation.
- **LiteLLM** — the sole LLM gateway (`https://gateway.jobfynder.com`). Only Hermes's Prompt Runtime module calls it. Router aliases (`generate-small`, `extract-fast`, `reasoning-small`) decouple prompt definitions from any specific provider/model.
- **Langfuse** — hosts the live, versioned prompt registry (38 prompts as of this document) and receives execution traces. Hermes fetches prompt definitions from Langfuse at runtime rather than hardcoding them.
- **Channel providers** — normalize inbound messages (Telegram, Email/Gmail/Graph, WhatsApp, Slack, Teams, Google Chat) into one common intake shape before they reach the parsing/understanding layer.

### 3.3 Data path (typical request)

```text
1. User action in Frontend
2. Frontend -> CORE (CORE's own API, CORE's own auth)
3. CORE -> Hermes (Bearer token, Hermes RBAC permission check)
4. Hermes: deterministic parse/normalize/match first
5. IF and only if confidence is too low or the task is genuinely generative:
   Hermes Prompt Runtime -> Langfuse (fetch prompt) -> LiteLLM (generate) -> Langfuse (trace)
6. Hermes returns structured output (or a draft object reference) to CORE
7. CORE persists the result into Postgres, or requires human review first
8. CORE -> Frontend
```

### 3.4 Error handling philosophy

Hermes distinguishes **business-logic outcomes** from **real errors**:

- Business outcomes (`blocked`, `needs_review`, `rejected`, `duplicate`) return **HTTP 200** with the outcome named explicitly in the response body. This is deliberate — a duplicate submission or a low-confidence parse is not a system failure.
- Only genuine failures use non-200 status: `401`/`403` for auth, `404` for missing resources, `422` for malformed requests, `500` for server errors.
- **Never infer success from HTTP status alone.** Always check the `decision`, `execution_mode`, `intake_status`, or equivalent outcome field in the body.

---

## 4. Authentication Flow for the Hermes API

### 4.1 Token model

Hermes uses **bearer-token RBAC**, not a full OAuth2 flow. There is no user-facing login screen for Hermes itself — tokens are provisioned server-side by Jobfynder-Infra and handed to whichever system needs to call Hermes (CORE, n8n, the internal COMM bridge, admin tooling).

```http
Authorization: Bearer <token>
```

Tokens map to a set of permission strings, checked with wildcard-or-exact matching (`app/security/rbac.py`). A token scoped to `*` (wildcard) satisfies every permission check. A token scoped to specific strings (e.g. `understanding:parse`, `matching:evaluate`) only passes those specific checks.

### 4.2 How CORE obtains a token

There is no self-service token-issuance endpoint. Request a scoped token from Jobfynder-Infra, specifying exactly which permission strings your integration needs (see Section 6.3 for the full permission list by module). Do not request a wildcard token for a service that only needs a handful of scopes — least privilege applies here the same as anywhere else.

### 4.3 Token lifetime, rotation

Tokens do not expire on a fixed schedule in the current implementation — they are long-lived until explicitly revoked. **Treat them as long-lived secrets:**

- Never commit a Hermes token to a repository.
- Never expose a Hermes token to the Frontend — it must stay server-side in CORE.
- Rotate a token immediately if it may have leaked (log exposure, accidental commit, etc.) — contact Jobfynder-Infra to revoke and reissue.

### 4.4 No OAuth2 for Hermes itself

Hermes does not implement an OAuth2 authorization-code or client-credentials flow for its own API. (OAuth2 *does* appear elsewhere in the system — e.g. the LinkedIn provider integration, and the Gmail/Microsoft Graph email connectors described in Section 7.5 — but that's OAuth2 against those *external* providers, not against Hermes itself.)

### 4.5 Special case: signed server-to-server intake

One endpoint uses a different auth scheme entirely: `POST /internal/comm/intake`, used by the COMM-1 bridge server, is authenticated via HMAC signature rather than a bearer token:

```text
Required headers:
  X-Jobfynder-Timestamp: <unix timestamp>
  X-Jobfynder-Signature: HMAC-SHA256(shared_secret, timestamp + "." + raw_body)
```

The same HMAC scheme also protects the Telegram webhook, but via a different header pair (`X-Telegram-Bot-Api-Secret-Token`, checked against a pre-shared static secret rather than a computed HMAC — see Section 7.4).

---

## 5. Login/Auth Endpoints and Example API Calls

There is no `/login` endpoint on Hermes — authentication is entirely bearer-token-based (Section 4). This section covers the endpoints you'll actually call to verify auth is working.

### 5.1 `GET /health`

The only public, unauthenticated endpoint.

**Request:**
```http
GET /health HTTP/1.1
Host: hermes.jobfynder.com
```

**Response — 200 OK:**
```json
{
  "status": "healthy",
  "service": "Hermes",
  "version": "0.2.3",
  "environment": "production"
}
```

### 5.2 `GET /security/rbac/status`

Confirms RBAC is enforced and reports configured user/token count. Requires a valid token with `security:read`.

**Request:**
```http
GET /security/rbac/status HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
```

**Response — 200 OK:**
```json
{
  "rbac_enforcement": "enabled",
  "configured_users": 8
}
```

**Response — 401 Unauthorized (missing token):**
```json
{
  "detail": "Missing access token"
}
```

**Response — 403 Forbidden (token present, wrong scope):**
```json
{
  "detail": "Insufficient permission: requires security:read"
}
```

### 5.3 Quick auth smoke test (curl)

```bash
# Should return 200 with no auth
curl -s https://hermes.jobfynder.com/health

# Should return 401 - no token
curl -s -o /dev/null -w "%{http_code}\n" https://hermes.jobfynder.com/security/rbac/status

# Should return 200 with a valid, correctly-scoped token
curl -s -H "Authorization: Bearer <YOUR_SCOPED_TOKEN>" \
  https://hermes.jobfynder.com/security/rbac/status
```

---

## 6. Developer Documentation

### 6.1 Authentication and Authorization (recap for implementers)

- Every route except `/health` requires `Authorization: Bearer <token>`.
- **Fixed 2026-08-21** (was previously an open gap): `/understanding/*` and `/submissions/evaluate*` now require `Authorization: Bearer <token>` with the appropriate scope, same as every other route. See Section 9.1 for what changed and why it was safe to enable without breaking anything live.
- Permission strings are checked per-route. A single token can carry multiple permission strings (space- or comma-delimited, depending on how it was issued) or a wildcard.

### 6.2 Error Handling and Troubleshooting

See Section 11 for the full troubleshooting guide. The short version for day-to-day integration work:

| Symptom | Likely cause | Where to look |
|---|---|---|
| 401 on every call | Missing or malformed `Authorization` header | Confirm the header is `Bearer <token>`, not just `<token>` |
| 403 on some calls, not others | Token doesn't carry the permission that specific route requires | Check the permission column in Section 6.3 against your token's scopes |
| 200 response but `requires_review: true` or `decision: "needs_review"` | Not an error — a genuine business outcome | Read the `reasons`/`risks` field in the response body |
| Slow response (~30s) on a prompt-related call | Langfuse prompt-registry cold-cache fetch (known issue) | Section 11.3 |
| Webhook returns 403 | Signature/secret mismatch | Section 11.4 |

### 6.3 Data Models and API Contracts

Two response shapes coexist by design, not by accident:

**Legacy shape** — endpoints built before the 2026-08-15 architecture freeze keep their own typed response (`UnderstandingResult`, `ResumeTailoringResponse`, etc.). Documented per-endpoint in the module sections below.

**Canonical envelope** — everything built after that freeze returns this exact shape:

```json
{
  "request_id": "req_abc123",
  "capability": "hermes.context.build_candidate_card",
  "execution_mode": "hermes_only",
  "confidence": 0.9,
  "llm_required": false,
  "llm_prompt_name": null,
  "structured_data": {},
  "unresolved_fields": [],
  "warnings": [],
  "proposed_actions": [],
  "trace_metadata": {}
}
```

Always check `execution_mode`/`llm_required` (envelope shape) or `decision`/`fallback.llm_fallback` (legacy shape) to know whether a call actually incurred LLM cost — never assume from HTTP status.

**Full endpoint index by module and required permission:**

| Module | Sample routes | Typical permission | Shape |
|---|---|---|---|
| Understanding (HERMES-200) | `POST /understanding/parse-text`, `/understanding/parse-file` | `understanding:parse` (currently unenforced — see 9.1) | Legacy |
| Taxonomy (HERMES-400) | `GET /understanding/taxonomy/skills`, `POST /understanding/taxonomy/normalize`, `POST /understanding/taxonomy/suggestions`, `GET /understanding/taxonomy/suggestions/queue`, `POST /understanding/taxonomy/suggestions/{id}/approve` | `understanding:read` / `understanding:parse` | Legacy + custom |
| Matching (HERMES-300) | `GET /matching/policy`, `POST /matching/resume-to-job` | `matching:evaluate` | Legacy |
| Submission Intelligence (HERMES-500) | `GET /submissions/workflow-policy`, `POST /submissions/evaluate`, `POST /submissions/evaluate/from-handoff` | none currently enforced — see 9.1 | Legacy |
| Integrations (HERMES-600) | `GET /integrations/health`, `POST /integrations/events/normalize`, `POST /integrations/jobfynder/submission-handoff/evaluate`, `POST /integrations/retry-decision`, `POST /integrations/events/identity` | varies | Legacy |
| Agents (HERMES-700) | `GET /agents/registry`, `POST /agents/dry-run` — **dry-run only, by design, no exceptions** | `agents:read` / `agents:run` | Custom |
| Prompt Runtime (HERMES-750) | `GET /prompts/registry`, `POST /prompts/run` | `agents:read` / `agents:run` | Custom |
| Resume Builder (HERMES-800) | `POST /resume-builder/analyze`, `/summary/suggest`, `/bullets/suggest`, `/tailor`, `/quality/analyze` | `resume_builder:read` / `:analyze` / `:suggest` | Custom |
| Context Cards | `POST /context/candidate-card/build`, `/job-card/build`, `/relationship-card/build`, `/conversation/compress` | scoped, resolves for wildcard tokens | Canonical envelope |
| Channels/Providers (HERMES-450/850) | `POST /channels/intake`, `/channels/telegram/webhook`, `/providers/email/webhook`, `/providers/gmail/push`, `/providers/microsoft-graph/webhook` | varies; webhook routes use signature auth, not bearer (Section 4.5) | Legacy |

For the always-current, machine-readable route list, use `GET /openapi.json` against the running service — this table is a snapshot, the OpenAPI schema is the source of truth.

### 6.4 Rate Limits and Throttling

Hermes itself does not currently enforce request-rate limiting at the application layer. Rate limiting for LLM calls happens one layer down, at LiteLLM: every virtual key carries a spend budget (verified live against the LiteLLM admin dashboard — e.g. a key showing "$1.82 of $20" with a monthly reset date). If a Hermes capability escalates to an LLM call and the underlying LiteLLM key's budget is exhausted, expect that call to fail — build retry/backoff and a clear user-facing message for this case, don't assume LLM calls always succeed.

### 6.5 Security Considerations and Compliance Notes

See Section 9 for the full treatment. Key points for implementers:

- Never construct a request that puts raw resume/JD/message text directly into a prompt variable — always go through a Context Card builder or a deterministic parser first. This is the mechanism (not just a policy) behind "raw documents never reach the LLM directly."
- Never log a Hermes bearer token or a Langfuse/LiteLLM key, even in debug output.
- PII handling: Hermes does not currently redact PII before sending it to Langfuse for tracing. If a prompt's input variables contain candidate PII, that PII is visible in the Langfuse trace. Treat Langfuse access as PII-sensitive access.

### 6.6 Versioning and Deprecation Strategy

- Endpoints don't currently carry a version prefix except the legacy `/v1/*` routes (`/v1/jobs/parse`, `/v1/messages/understand`, etc.), which predate the rest of the API and are kept for backward compatibility — new integrations should prefer the non-versioned equivalents where one exists (e.g. `/understanding/parse-text` over `/v1/jobs/parse` for job parsing).
- Response schema changes: the canonical envelope (Section 6.3) is the intended long-term contract for new capabilities. Migrating a legacy-shaped endpoint to the envelope is a breaking change and is not done without an explicit, documented decision — check `hermes-architecture-frozen-v1.md` Section 6 before assuming any endpoint's response shape is stable across a migration.
- Module-level versioning happens through the HERMES-XXX stream numbering and git tags (e.g. `hermes-800-resume-builder-foundation-v1`) — see `HERMES-documentation-map.md` for the authoritative closed/open module list.

---

## 7. End-to-End Integration with Jobfynder CORE

### 7.1 Provisioning checklist (new environment)

1. Confirm the Hermes container is deployed and `/health` responds.
2. Confirm `LITELLM_API_KEY` and `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are set on the Hermes server's `.env` — **and that they are the correct, dedicated keys for this environment**, not a personal or ad-hoc key (this exact mistake happened once already; see Section 11.3).
3. Request a scoped Hermes bearer token for CORE from Jobfynder-Infra (Section 4.2).
4. Set that token in CORE's own environment config — never in a client-visible config file.
5. Run the smoke test (Section 12.1) against the new environment before pointing real traffic at it.

### 7.2 Data flow for the four integration cases

**Case 1 — Resume Builder.** Frontend → CORE → Hermes `POST /understanding/parse-text` (or `/parse-file`) → Hermes `POST /resume-builder/*` for suggestions/analysis → CORE persists the structured resume, holds any AI-suggested content as a **suggestion pending human approval** (Resume Builder's safety rule: no auto-publish, no auto-rewrite).

**Case 2 — Job Board matching.** CORE has structured job + resume data (or raw text) → Hermes `POST /matching/resume-to-job` (or `/from-understanding` if starting from raw text) → deterministic score, no LLM → CORE stores the match result and surfaces `submit`/`review`/`reject`.

**Case 3 — Job Tracker / submission workflow.** CORE has a submission stage transition or event → Hermes `POST /submissions/evaluate` (or `/from-handoff` when chaining directly from Understanding/Matching output) → Hermes returns a recommended stage, conflicts, follow-up instructions → **CORE persists the actual stage change; Hermes never writes to CORE's database directly.** Follow the integration safety rules in Section 7.3.

**Case 4 — Email intake (HERMES-850).** Inbound email → provider connector normalizes it (Telegram is live; Gmail/Graph are built and tested but require OAuth credentials before real email reaches them — see Section 7.5) → Hermes parses it deterministically → a draft object is created in Hermes's own storage (`/drafts/{draft_id}`) → **whether CORE polls or is pushed these drafts, and turns them into real Candidate/Job records, is integration work whose completeness on the CORE side should be confirmed with the integration owner before this flow is assumed to be end-to-end.**

### 7.3 Integration safety rules (submission workflow specifically)

These are written into the HERMES-500 closure record and should be treated as hard rules by any CORE code consuming this endpoint:

1. Never blindly overwrite a terminal stage (`placed`, `closed_lost`, etc.).
2. If the response's `conflicts` array is non-empty, require human review before acting.
3. If `stage_changed` is `false`, do not update the tracker stage.
4. If `follow_up.required` is `true`, create a follow-up task with the given priority.
5. If `recommended_stage` is `duplicate_risk`, block auto-submission.
6. If `outcome.outcome_type` is `placed`, mark the workflow complete.
7. Store the full Hermes response for audit/debugging — don't discard fields you don't immediately use.

### 7.4 Dependency map and failure modes

```text
CORE's request to Hermes can fail at:
  1. Network/DNS to hermes.jobfynder.com          -> CORE should retry with backoff
  2. Hermes auth (401/403)                        -> not retryable, fix the token/scope
  3. Hermes deterministic processing (rare)        -> 500, check Hermes logs
  4. Hermes escalates to LLM, and:
     a. Langfuse prompt fetch fails/times out      -> Hermes returns a "failed" decision, not a crash
     b. LiteLLM call fails (budget, provider down) -> same: "failed" decision, retryable once by Hermes itself
  5. Response reaches CORE, but represents a business rejection, not a failure -> this is not an error path, handle it as data
```

Hermes's own internal fallback: if a prompt's primary router alias has no healthy deployment on LiteLLM, it attempts exactly one fallback to `HERMES_PROMPT_DEFAULT_MODEL`. No further retries, no silent escalation — by design, to keep cost and behavior predictable.

### 7.5 Email provider OAuth flow (Gmail / Microsoft Graph) — when activated

This is not live yet (Section 7.2, Case 4), but documented here so whoever activates it has the shape ready:

**Gmail:** register an OAuth application in Google Cloud Console, grant it Gmail API read access to the target mailbox, configure Cloud Pub/Sub push notifications pointed at `POST /providers/gmail/push`. Set `HERMES_GMAIL_CLIENT_ID`, `HERMES_GMAIL_CLIENT_SECRET`, `HERMES_GMAIL_REFRESH_TOKEN`, `HERMES_GMAIL_PUBSUB_TOPIC`.

**Microsoft Graph:** register an app in Microsoft Entra/Azure AD, grant `Mail.Read` permission, create a Graph subscription pointed at `POST /providers/microsoft-graph/webhook` — that endpoint already implements the required `validationToken` handshake Graph performs when the subscription is created. Set `HERMES_MS_GRAPH_CLIENT_ID`, `HERMES_MS_GRAPH_CLIENT_SECRET`, `HERMES_MS_GRAPH_TENANT_ID`.

Both connectors' message-normalization code is built and unit-tested against realistic sample payloads; only the authenticated fetch-from-provider-API step remains to be implemented once real credentials exist.

---

## 8. Deployment and Operational Considerations

### 8.1 Environment and deployment model

- Single Docker container (`hermes-api`), built from `/opt/hermes` on `jobfynder-intel-01`, via `docker-compose.yml` in that directory.
- **Important operational pattern specific to this repo:** the git workflow is branch-per-module, not merge-to-main. Each `feature/hermes-XXX-*` branch is built on top of the previous module's closure tag, and the server runs whichever branch was last built into the image — `main` is largely unused for deployment purposes. Check the currently-deployed branch/commit with `git -C /opt/hermes log -1` before assuming `main` reflects reality.
- Env vars come from a real `.env` file on the server (not committed — `.env.example` is the template).
- **Config-change gotcha, confirmed the hard way:** `docker compose restart hermes-api` does **not** reload `.env` for an already-created container. Use `docker compose up -d --force-recreate hermes-api` after any `.env` change.

### 8.2 CI/CD

No automated CI/CD pipeline was found wired to this repo as of this document — deployment is manual (SSH in, pull/checkout the target branch, `docker compose build`, `docker compose up -d --force-recreate`). If a rollback is needed: check out the previous known-good tag (e.g. `hermes-800-resume-builder-foundation-v1`) and rebuild — always back up `.env` before any config change (`cp .env .env.bak-$(date +%Y%m%d%H%M%S)`).

### 8.3 Observability

- **Logging:** application logs via standard Docker container logs (`docker logs hermes-api`). Prompt execution specifically also writes structured JSONL logs to `/hermes-runtime/prompt-runs`.
- **Tracing:** every live prompt execution is traced to Langfuse (trace + generation events), including token usage and the exact model used.
- **Metrics/alerting:** no dedicated metrics/alerting stack was found wired to Hermes specifically as of this document. LiteLLM's own dashboard provides spend and usage visibility per virtual key.
- **Health checks:** `GET /health` (liveness only, no dependency checks — a healthy response does not guarantee Langfuse or LiteLLM are reachable). For a real end-to-end check, use `GET /prompts/health`, which reports `litellm_configured` and `langfuse_configured` booleans.

### 8.4 Performance and load considerations

- **Fixed 2026-08-21:** the Langfuse prompt-registry fetch (`_refresh_cache()` in `app/prompt_runtime/langfuse_prompts.py`) used to fetch all prompts sequentially, one HTTP call per prompt — measured at ~33 seconds for 38 prompts on a cold cache. Now fetches concurrently (`ThreadPoolExecutor`, default 8 workers, tunable via `HERMES_LANGFUSE_PROMPT_FETCH_CONCURRENCY`) — verified live at 7.55 seconds for the same 38 prompts. The cache still lasts 5 minutes (`HERMES_LANGFUSE_PROMPT_CACHE_SECONDS`), so only the first request after expiry pays this cost at all.
- The in-process runtime cache (`GET /runtime/cache/stats`) covers resume/JD/profile-import parse results only, 24h TTL, and does not survive a container restart.

---

## 9. Security and Compliance Notes

### 9.1 RBAC gap — closed 2026-08-21

`/understanding/*` and `/submissions/evaluate*` previously had **no RBAC check at all**. Fixed 2026-08-21 (commit `9dc69d5`, branch `fix/hermes-100-close-rbac-gap`, deployed and live-verified): `understanding:parse`/`understanding:read` added to every `/understanding/*` route, `submissions:evaluate` added to `POST /submissions/evaluate` and `/evaluate/from-handoff` specifically (scoped to exactly what was documented as the gap — `/submissions/workflow-policy`, `/tracker-update/extract`, and `/status/extract` are unchanged, not silently swept in).

**Why this was safe to flip on without warning:** verified first, not assumed — live Hermes traffic logs showed zero hits on either route group in the preceding 5000 log lines, and a grep of `jobFynder-BE-nestJS` found no code anywhere calling these Hermes endpoints (the only Hermes↔CORE integration actually built at the time was the reverse direction — CORE's `/hermes/*` controller receiving calls *from* Hermes/agents, not CORE calling out to Hermes). Nothing live was depending on these routes staying open.

A new `jobfynder-core` RBAC user was provisioned (scoped: `understanding:parse`, `understanding:read`, `submissions:evaluate`) via `scripts/hermes-access-control.py`, ready for whenever CORE integration actually starts calling these routes — token stored at `/root/hermes-token-jobfynder-core.txt` on INTEL-1, never printed or committed.

### 9.2 Data at rest / in transit

- All external traffic (CORE↔Hermes, Hermes↔LiteLLM, Hermes↔Langfuse) is over HTTPS.
- Hermes holds no persistent database of its own — the `/hermes-runtime` volume stores drafts, taxonomy suggestions, prompt-run logs, and intake/event records as JSON files on the host filesystem. This volume is not currently encrypted at rest beyond whatever the underlying host disk provides — treat it as containing sensitive data (parsed resumes, candidate PII) and scope host-level file access accordingly.
- No dedicated key-management service (e.g. a vault) was found in use — secrets live in `.env` files on the host. Rotate any secret that may have been exposed (Section 4.3).

### 9.3 Access control principles

- Least privilege: request only the permission strings an integration actually needs (Section 4.2), never a wildcard token for a narrow-purpose integration.
- Server-to-server intake (`/internal/comm/intake`) and the Telegram webhook use signature-based auth, not bearer tokens — appropriate for machine-to-machine calls where a long-lived bearer token would be a worse fit.
- Multi-agent capabilities (HERMES-700) are **dry-run only, with no exception path** — agents cannot submit candidates, message recruiters, change production data, or take any other high-risk action automatically, regardless of what a caller requests. This is enforced in code (`app/agents/service.py` policy checks), not just documented as a convention.

### 9.4 Compliance references

No formal PCI-DSS or GDPR compliance audit was found documented for this system as of this writing. If Jobfynder needs to make a compliance claim (GDPR right-to-erasure for candidate data stored in `/hermes-runtime`, for instance), that requires a dedicated review — this document does not constitute one. Flagged here as an open item, not resolved.

### 9.5 PII in traces

Repeating from Section 6.5 because it's easy to miss: Langfuse traces capture full prompt inputs and outputs by default. If a prompt's rendered content includes candidate PII, that PII is visible to anyone with Langfuse project access. There is no redaction step in the current `send_langfuse_trace()` implementation.

---

## 10. API Samples and Code Blocks

### 10.1 Parse a resume (deterministic, auto-escalates to LLM below confidence 0.70)

**Request:**
```http
POST /understanding/parse-text HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
Content-Type: application/json

{
  "document_kind": "resume",
  "content": "Jane Doe\nSenior Backend Engineer\n8 years experience...\nSkills: Python, Django, PostgreSQL, AWS"
}
```

**Field name correction, 2026-08-21:** this sample previously showed `"text"` instead of `"content"` — the actual `RawDocument` model (`app/understanding/models.py`) takes `content`, confirmed against a live call during the RBAC-fix verification pass (§9.1). If you copy-pasted this sample before today, update it.

**Response — 200 OK (deterministic path, no LLM cost):**
```json
{
  "decision": "parsed",
  "confidence": 0.91,
  "fallback": { "llm_fallback": false },
  "structured_data": {
    "name": "Jane Doe",
    "title": "Senior Backend Engineer",
    "years_experience": 8,
    "skills": ["Python", "Django", "PostgreSQL", "AWS"],
    "normalized_skills": ["Python", "Django", "PostgreSQL", "AWS"],
    "taxonomy_signals": { "...": "..." }
  }
}
```

### 10.2 Score a resume against a job

**Request:**
```http
POST /matching/resume-to-job HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
Content-Type: application/json

{
  "resume": {
    "skills": ["Python", "Django", "AWS"],
    "years_experience": 8,
    "work_authorization": "citizen",
    "location": "Dallas, TX"
  },
  "job": {
    "required_skills": ["Python", "Django"],
    "preferred_skills": ["AWS", "Kubernetes"],
    "years_experience": 5,
    "work_authorization": "citizen",
    "location": "Dallas, TX"
  }
}
```

**Response — 200 OK:**
```json
{
  "match_score": 88.5,
  "decision": "submit",
  "score_breakdown": { "required_skills": 55.0, "preferred_skills": 7.5, "experience": 15.0, "work_auth": 10.0, "location": 5.0 },
  "matched_required_skills": ["Python", "Django"],
  "missing_required_skills": [],
  "matched_preferred_skills": ["AWS"],
  "reasons": ["All required skills matched.", "8 years exceeds 5 year requirement."],
  "risks": [],
  "recommendation": "Strong match, submit.",
  "matcher_version": "basic_local_matcher_v1"
}
```

### 10.3 Evaluate a submission workflow event

**Request:**
```http
POST /submissions/evaluate HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
Content-Type: application/json

{
  "current_stage": "matched",
  "event_type": "intro_requested"
}
```

**Response — 200 OK:**
```json
{
  "recommended_stage": "intro_requested",
  "stage_changed": true,
  "conflicts": [],
  "follow_up": { "required": true, "priority": "medium", "suggested_action": "Follow up with receiving recruiter" },
  "outcome": null,
  "next_actions": ["Wait for recruiter response", "Escalate if no reply in 48h"]
}
```

### 10.4 Run a prompt (dry-run — the default, no cost)

**Request:**
```http
POST /prompts/run HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
Content-Type: application/json

{
  "prompt_id": "jf.jobs.fit.explain",
  "mode": "dry_run",
  "variables": { "job_card": { "card_version": "hermes_job_card_v1", "...": "..." }, "candidate_card": { "card_version": "hermes_candidate_card_v1", "...": "..." } }
}
```

**Response — 200 OK:**
```json
{
  "run_id": "prompt-run-abc123",
  "prompt_id": "jf.jobs.fit.explain",
  "mode_requested": "dry_run",
  "mode_effective": "dry_run",
  "provider": "litellm",
  "decision": "completed",
  "output_text": "[dry-run] Prompt jf.jobs.fit.explain rendered successfully. No external LLM call was made. Human review is required before use.",
  "safety": { "allowed": true, "human_review_required": true }
}
```

### 10.5 Error code reference

| Code | Meaning in Hermes | Typical cause |
|---|---|---|
| 200 | Success **or** a valid business outcome (`blocked`, `needs_review`, `rejected`) | Check the body's decision field, not just the status |
| 401 | Missing or malformed bearer token | `Authorization` header absent or not `Bearer <token>` |
| 403 | Token valid but lacks the required permission; or signature verification failed on a webhook route | Check permission scope (Section 6.3), or webhook secret (Section 7.4/11.4) |
| 404 | Resource not found (e.g. an unknown `prompt_id`, an unknown draft ID) | Verify the ID exists via the corresponding list/registry endpoint first |
| 422 | Request body failed schema validation | Check required fields against the endpoint's model |
| 500 | Genuine server error | Check Hermes container logs; not a business-logic outcome |

---

## 11. Troubleshooting Guide

### 11.1 "Every call returns 401"

Confirm the header is exactly `Authorization: Bearer <token>` — not `Authorization: <token>`, not `Bearer: <token>`. Confirm the token hasn't been revoked (ask Jobfynder-Infra).

### 11.2 "Some calls work, others return 403"

Your token doesn't carry the permission the specific route requires. Cross-reference against Section 6.3. If you believe the route *should* be unprotected, check Section 9.1 first — two route groups genuinely have no RBAC at all, which is a separate, tracked issue, not something to route around by requesting a wildcard token.

### 11.3 "A prompt-related call is very slow or times out"

This was the Langfuse N+1 fetch issue (Section 8.4), fixed 2026-08-21 — a cold-cache fetch now takes ~7-8s instead of ~33s. If a call is still taking 20s+ after that fix is deployed, the cache likely isn't holding at all — check that `HERMES_LANGFUSE_PROMPT_CACHE_SECONDS` is set and that the container hasn't been restarted recently (a restart clears the in-process cache), or that `HERMES_LANGFUSE_PROMPT_FETCH_CONCURRENCY` hasn't been set too low.

**If it looks like an outright auth failure (HTTP 403 with `error code: 1010` in the body)** — this is Cloudflare's bot-protection layer in front of `langfuse.jobfynder.com`, not a Langfuse credential problem. It gets triggered by requests with no recognizable User-Agent header. The production code already sets one (`User-Agent: Hermes-PromptRuntime/1.0`); this only bites ad-hoc debugging scripts that omit it. If you're writing a diagnostic script against Langfuse directly, set a real User-Agent header or you'll misdiagnose this as a credentials problem (confirmed the hard way — see the HERMES-750 doc's incident record for the full story).

**If Langfuse calls fail outright (not just slow):** verify `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` on the server match a key actually issued for this purpose in the Langfuse project (check `https://langfuse.jobfynder.com/project/<project-id>/settings/api-keys` — look for a key whose *note* clearly identifies it as the Hermes production key, not a personal or ad-hoc key). If you rotate the key, remember: Langfuse only shows a secret key once, at creation — copy it immediately, and remember `docker compose restart` won't pick up the change (Section 8.1) — use `--force-recreate`.

### 11.4 "Telegram/email webhook returns 403"

Expected behavior if the signature/secret doesn't match — this is the security control working, not a bug. For Telegram: confirm the caller sends `X-Telegram-Bot-Api-Secret-Token` matching the server's `HERMES_TELEGRAM_WEBHOOK_SECRET`. **Do not "fix" a 403 here by disabling the check** — if you're debugging and see this, the fix is to send the correct secret, never to weaken the verification. (A test script that previously omitted this header and treated the resulting 403 as a bug has since been corrected — see `scripts/hermes-450-channel-intake-check.py` for the current, correct pattern: send the real secret on the positive-path test, and assert 403 on a dedicated negative-path test so a real regression can't hide behind an expected rejection again.)

### 11.5 "A submission/matching call succeeds but nothing changed in CORE's database"

This is very likely working as designed, not a bug — Hermes proposes, CORE executes (Section 3.4, 7.2 Case 3). Confirm CORE's own integration code actually reads the Hermes response and calls its own persistence layer. Hermes returning `recommended_stage` does not mean CORE's tracker stage updated automatically.

### 11.6 "Draft object created in Hermes, but no corresponding record in Jobfynder's live data"

Same root cause as 11.5, specific to the email-intake flow (Section 7.2 Case 4). Check `GET /drafts/{draft_id}` to confirm the draft exists in Hermes, then confirm with the CORE integration owner whether the consuming logic that turns drafts into real records is deployed in this environment.

### 11.7 "Agent execution returns `needs_review` for everything"

Expected — HERMES-700 agents are dry-run only by design (Section 9.3). There is no "execute" mode to switch on; this isn't a misconfiguration.

---

## 12. Recommended Testing Plan

### 12.1 Unit-level (per module, run inside the Hermes container)

Run the existing verification scripts for whichever modules your integration touches:

```bash
docker exec -w /app hermes-api sh -c 'PYTHONPATH=/app python3 scripts/<script-name>.py'
```

Every module has at least one script under `scripts/hermes-<module>-*.py`. **Success criterion: exit code 0 and the script's own final `PASSED`/`OK` line.**

### 12.2 Integration-level (CORE ↔ Hermes)

1. Confirm `GET /health` returns `healthy` from CORE's network path (not just from the Hermes host itself).
2. Confirm a real bearer token issued for CORE passes `GET /security/rbac/status`.
3. Run one real request per integration case in Section 7.2 against a non-production Hermes environment, and confirm CORE correctly persists (or correctly declines to persist, per the safety rules in 7.3) the result.
4. Confirm a deliberately malformed request (e.g. missing required field) returns 422, not a 500 or a silent wrong answer.

**Success criteria:** all four cases produce the expected CORE-side outcome; no case silently succeeds with wrong data.

### 12.3 End-to-end (Frontend → CORE → Hermes → CORE → Frontend)

1. Resume upload → parse → suggestion → human approval → published resume reflects the approved change, not the raw suggestion.
2. Job posting → match → submission → tracker stage updates only when `stage_changed: true`.
3. (Once live) Inbound hotlist email → parsed → appears as a reviewable item somewhere in CORE's UI, not silently in Hermes only.

**Success criteria:** a non-technical reviewer using the Jobfynder UI can complete each flow without needing to inspect raw Hermes API responses.

### 12.4 Regression checklist before any Hermes deployment change

- [ ] All module verification scripts for changed modules pass (12.1).
- [ ] `GET /health` and `GET /prompts/health` both report healthy/configured.
- [ ] LiteLLM remains the only LLM gateway referenced (grep the diff for any references to a retired provider before merging).
- [ ] `.env` changes verified with `--force-recreate`, not `restart` (Section 8.1).
- [ ] If RBAC-related code changed, explicitly test both an authorized and an unauthorized call.

---

## 13. Glossary

| Term | Meaning |
|---|---|
| **Bearer token** | The `Authorization: Bearer <token>` credential used for all authenticated Hermes calls. |
| **Canonical envelope** | The standard response shape (`request_id`, `execution_mode`, `structured_data`, etc.) used by every Hermes capability built after 2026-08-15. |
| **Context Card** | A bounded, pre-parsed summary object (Candidate Card, Job Card, Relationship Card, Conversation Context) that stands in for raw text when calling a generative prompt — the mechanism that enforces "raw documents never reach the LLM." |
| **CORE** | Jobfynder's main NestJS backend — owns the production database, the only system with direct write access to business data. |
| **Deterministic-first** | The design principle that a rule-based/statistical approach is always attempted before falling back to an LLM. |
| **Dry-run** | A prompt execution mode that renders and validates a prompt without actually calling an LLM — the default mode everywhere in Hermes. |
| **Drafts** | Objects Hermes creates in its own storage (`/drafts/{id}`) representing a proposed record — not a live Jobfynder database row until CORE explicitly consumes and persists it. |
| **LiteLLM** | The sole LLM gateway (`gateway.jobfynder.com`). The only path through which any Hermes call reaches a language model. |
| **Langfuse** | Hosts the live, versioned prompt registry and receives execution traces. |
| **Router alias** | A named model reference (e.g. `generate-small`) that decouples a prompt from any specific provider/model — configured on LiteLLM, referenced by name in prompt definitions. |
| **RBAC** | Role-based access control — Hermes's permission-string-based authorization model. |
| **HERMES-XXX** | The module/stream numbering scheme used to track Hermes's build history (e.g. HERMES-400 = Taxonomy). See `HERMES-documentation-map.md` for the full closed/open list. |

---

## 14. References

- `hermes-architecture-frozen-v1.md` — the architectural decisions and reasoning behind the current design.
- `hermes-complete-developer-guide.md` — per-endpoint use-case guide.
- `hermes-capability-matrix.md` — current build status of every capability, module by module.
- `hermes-api-route-inventory.md` — the full route table.
- `HERMES-documentation-map.md` — the authoritative list of closed/open modules and where each one's official doc lives.
- `HERMES-750-litellm-prompt-runtime-foundation.md` — the LiteLLM migration record and the Langfuse incident referenced in Section 11.3.
- `HERMES-850-email-parsing-foundation.md` — the email intake flow referenced in Section 7.2 Case 4 and 7.5.
- `GET /openapi.json` on the running Hermes service — the always-current, machine-readable API contract.
