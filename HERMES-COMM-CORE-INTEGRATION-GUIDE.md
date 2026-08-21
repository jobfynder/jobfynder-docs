# Hermes (INTEL-1) + COMM (COMM-1) — Consolidated Integration Guide for Jobfynder CORE

**Audience:** Backend and Frontend developers integrating with Hermes and/or COMM
**Status:** Active — canonical integration reference for both servers
**Servers covered:**
- **INTEL-1** (`jobfynder-intel-01`) — runs Hermes, the intelligence layer. API base `https://hermes.jobfynder.com` (internal: `http://localhost:8000`).
- **COMM-1** (`152.42.219.165`) — runs the COMM Gateway, the communication layer. Public entry point `https://comm.jobfynder.com` (internal: `http://localhost:8080`).

**Last verified against running code:** 2026-08-21 (Hermes commit state per `hermes-core-integration-guide.md`; COMM Gateway commit `0c33580` on `jobfynder-infra`, redeployed and live-verified same day).

**Scope note:** This document does not describe Portkey in any capacity. LiteLLM is the only LLM gateway referenced anywhere in this document, per current architecture.

---

## Table of Contents

1. [Change Log](#1-change-log)
2. [Executive Summary](#2-executive-summary)
3. [System Overview and Architecture](#3-system-overview-and-architecture)
4. [Authentication Flow — Hermes and COMM](#4-authentication-flow--hermes-and-comm)
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
| 2026-08-21 | First edition. Consolidates the verified state of Hermes (HERMES-000 through HERMES-850) and, for the first time, the COMM Gateway (COMM-100/410/500/900/1000) into a single integration reference covering both servers. Built directly from `hermes-core-integration-guide.md`, the `comm/` module docs, and a live inspection of both INTEL-1 and COMM-1. No Portkey references — LiteLLM only. |

Update this table whenever this document changes materially. This file lives in `jobfynder/jobfynder-docs`, not inside either code repo — that is the enforced rule for all Hermes and COMM documentation (`hermes/HERMES-documentation-map.md`, `comm/COMM-documentation-map.md`).

---

## 2. Executive Summary

Jobfynder's backend is split into three cooperating systems, each with one job:

- **Jobfynder CORE** (NestJS, Postgres, PM2) — owns all persistent business data. The only system with direct write access to the production database.
- **Hermes** (FastAPI, INTEL-1) — the intelligence layer. Parses, matches, normalizes, and — only when genuinely necessary — generates, via a single controlled path to an LLM.
- **COMM Gateway** (FastAPI, COMM-1) — the communication layer. Receives inbound messages from external channels (Telegram today; Email/WhatsApp/Slack/Teams/Google Chat are Hermes-side contracts with no COMM-side receiver yet), normalizes them, and forwards them to Hermes over a signed internal contract.

**The two non-negotiable rules that shape every integration decision in this document:**

1. **CORE and the Frontend never talk to an LLM directly, and never hold an LLM API key.** Every generative or parsing task goes through Hermes, which decides — deterministically wherever possible — whether an LLM call is even needed. LiteLLM is the only gateway through which any call reaches a model provider.
2. **The Frontend never talks to Hermes or COMM directly.** All Hermes calls are proxied through CORE, which holds the Hermes bearer token. COMM is not called by CORE or the Frontend at all in the current architecture — it only receives inbound webhooks from external providers (Telegram) and calls out to Hermes.

**What's actually built and verified, as of this document:**

- **Hermes:** 106+ live API endpoints across understanding (resume/JD parsing), matching, taxonomy, submission workflow, integrations, multi-agent (dry-run only), prompt runtime, resume builder, and channel intake. RBAC enforced on almost every route via bearer token — with one confirmed, still-open gap (Section 9.1).
- **COMM:** a small (5-file) FastAPI service, live in production, handling the Telegram channel end to end (webhook receipt → normalize → HMAC-sign → forward to Hermes → deliver reply). As of 2026-08-21: resilient to a slow/unreachable Hermes (no longer crashes silently), rate-limited (120 req/min per IP), and backed by automated daily volume backups.

**What's not yet true, so nobody is surprised by it:**

- Hermes does not write directly into Jobfynder's production database — CORE must consume its structured output/drafts and persist them itself.
- COMM has no queueing, no retry, and no idempotency of its own on the inbound webhook path (Section 7.4). RabbitMQ runs on COMM-1 today but is not wired into any code path.
- Only Telegram is a live COMM channel. Email/WhatsApp/Slack/Teams/Google Chat exist only as Hermes-side normalized contracts, with nothing on COMM-1 to receive them yet.
- One RBAC gap remains open on two Hermes route groups (Section 9.1), and the deployed COMM code branch has not been merged to `jobfynder-infra`'s `main` (Section 8.1).

**Success metrics for this integration:**

- Every CORE call to Hermes carries a bearer token scoped to the minimum permission it needs.
- No raw resume, job description, or recruiter message text is ever passed directly to an LLM prompt variable without first going through a Hermes Context Card or deterministic parser.
- CORE never holds an LLM API key or a Langfuse secret key; the Frontend never holds a Hermes or COMM credential.
- A cold-start Hermes or COMM deployment passes the recommended test plan (Section 12) before being pointed at production traffic.
- A message sent to the Telegram bot produces either a real reply or an explicit "could not process" reply within the request timeout — never silence (this specific guarantee was not true before the 2026-08-21 fix; see Section 8.4).

---

## 3. System Overview and Architecture

### 3.1 High-level diagram (textual)

```text
┌─────────────┐      ┌──────────────────────────┐      ┌───────────────┐
│  Frontend    │      │      Jobfynder CORE        │      │    Hermes     │
│ (React/Vite) │─────▶│  (NestJS, Postgres, PM2)   │─────▶│ (FastAPI,     │
│              │◀─────│                            │◀─────│  INTEL-1)     │
└─────────────┘      └──────────────────────────┘      └───────┬───────┘
                                                                  │
                          ┌───────────────────────────────────────┼────────────────────────┐
                          │                                       │                          │
                          ▼                                       ▼                          ▼
                  ┌───────────────┐                     ┌────────────────┐         ┌──────────────────┐
                  │   LiteLLM      │                     │   Langfuse      │         │  COMM Gateway      │
                  │   Gateway      │                     │  (prompt store  │         │  (FastAPI, COMM-1) │
                  │  (LLM calls    │                     │   + tracing)    │         │  Telegram is live; │
                  │   only)        │                     │                 │         │  other channels not│
                  └───────────────┘                     └────────────────┘         └─────────┬──────────┘
                                                                                                │  webhook
                                                                                                ▼
                                                                                     ┌────────────────────┐
                                                                                     │  Telegram Bot API   │
                                                                                     └────────────────────┘
```

**Key structural fact:** COMM is not in the Frontend/CORE request path at all. It is a separate ingress point that receives events from external channels and pushes them *into* Hermes — the arrow between COMM and Hermes is COMM-initiated (`POST /internal/comm/intake`), not the other way around. CORE never calls COMM, and COMM never calls CORE directly; anything that reaches CORE from a Telegram conversation does so via Hermes, exactly as if it originated inside Hermes's own understanding pipeline.

### 3.2 Key components

| Component | Server | Runtime | Role |
|---|---|---|---|
| **Hermes** | INTEL-1 (`jobfynder-intel-01`) | Single Docker container (`hermes-api`), FastAPI/Python. Persistent runtime volume `/hermes-runtime` (drafts, prompt-run logs, taxonomy suggestion queue, event logs). | Parsing, matching, taxonomy, submission workflow, generation (via LiteLLM), multi-agent (dry-run only), resume builder, and normalized intake from all channels. |
| **COMM Gateway** | COMM-1 (`152.42.219.165`) | Single Docker container (`jobfynder-comm-gateway`), built from `Dockerfile.comm-gateway`, FastAPI/Python, 5 source files total. Stateless — no database. | Receives Telegram webhooks, normalizes to a canonical intake shape, HMAC-signs and forwards to Hermes, delivers Hermes's reply back to the user. |
| **Jobfynder CORE** | separate server | NestJS, Postgres-backed, PM2-managed (not containerized). | Owns all persistent business data (Users, Jobs, Candidates, Submissions). Calls Hermes for anything requiring parsing, matching, taxonomy, or generation. Never calls COMM. |
| **LiteLLM** | separate (Elestio-hosted) | Gateway service, `https://gateway.jobfynder.com`. | The sole LLM gateway. Only Hermes's Prompt Runtime module calls it. Router aliases (`generate-small`, `extract-fast`, `reasoning-small`) decouple prompt definitions from any specific provider/model. |
| **Langfuse** | self-hosted on INTEL | `https://langfuse.jobfynder.com`, v4.1.0. | Hosts the live, versioned prompt registry (38 prompts as of this document) and receives execution traces. |
| **Nginx Proxy Manager** | COMM-1 | Docker container `jobfynder-npm`. | TLS termination and reverse proxy for `comm.jobfynder.com` → `comm-gateway:8080`. |
| **RabbitMQ, Redis (COMM-1)** | COMM-1 | Docker containers, 6+ weeks uptime. | **Provisioned, not used.** Zero queues, zero keys, zero code references as of this document — capacity, not active infrastructure. Do not assume messages flow through them. |

### 3.3 Authentication/authorization flow overview

Three distinct auth schemes coexist, none of them OAuth2 against Hermes or COMM themselves (full detail in Section 4):

1. **CORE → Hermes:** static bearer token, RBAC-checked per route.
2. **Telegram → COMM:** pre-shared static secret in a header (`X-Telegram-Bot-Api-Secret-Token`), not a computed signature.
3. **COMM → Hermes:** computed HMAC-SHA256 signature over a timestamp + request body — a different, stronger mechanism than either of the above, used specifically for this one server-to-server hop.

### 3.4 Data path (typical requests)

**CORE-initiated request:**
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

**COMM-initiated request (a Telegram message):**
```text
1. User sends a message to the Telegram bot
2. Telegram -> COMM POST /providers/telegram/webhook (secret-token header)
3. COMM: normalize_telegram_update() -> canonical intake shape
4. COMM -> Hermes POST /internal/comm/intake (HMAC-signed)
5. Hermes: parse / taxonomy-extract / draft-create (same understanding pipeline as any other intake)
6. Hermes's response flows back to COMM
7. COMM -> Telegram sendMessage (chunked if long, per Section 6.3)
8. User sees the reply
```

Note what does *not* happen in the COMM-initiated path: CORE is not in this loop at all unless and until something downstream (a scheduled job, a human reviewing a draft, a future integration) reads whatever Hermes produced from that intake and turns it into a CORE record. Do not assume a Telegram message automatically becomes a CORE database row — verify with the CORE integration owner for any given flow (same caveat as Section 7.2 Case 4 below).

### 3.5 Error handling philosophy

Both Hermes and COMM distinguish **business-logic outcomes** from **real errors**, but they do it differently — this is a real, important asymmetry, not an inconsistency to "fix":

- **Hermes:** business outcomes (`blocked`, `needs_review`, `rejected`, `duplicate`) return **HTTP 200** with the outcome named explicitly in the response body. Only genuine failures use non-200 status (`401`/`403` auth, `404` missing resource, `422` malformed request, `500` server error). **Never infer success from HTTP status alone** — check the `decision`, `execution_mode`, or equivalent outcome field.
- **COMM:** because COMM's job is to always acknowledge the webhook sender (Telegram) rather than surface an outcome to a caller waiting on a response body, COMM's webhook handler returns `200 processed` even when the underlying Hermes call failed — the *failure itself* is represented inside the response body's `hermes` field (`{"status": "error", "reason": "..."}`) and, more importantly, in what the user actually receives on Telegram (a fixed "could not process this message" reply). If you're debugging a COMM issue, do not assume a `200` from the webhook endpoint means the Hermes call succeeded — check the `hermes` field in the response body, or check what the Telegram user actually received.

---

## 4. Authentication Flow — Hermes and COMM

### 4.1 Hermes: bearer-token RBAC

Hermes uses **bearer-token RBAC, not a full OAuth2 flow.** There is no user-facing login screen for Hermes itself — tokens are provisioned server-side by Jobfynder-Infra and handed to whichever system needs to call Hermes (CORE, n8n, the COMM bridge for the one HMAC-signed exception below, admin tooling).

```http
Authorization: Bearer <token>
```

Tokens map to a set of permission strings, checked with wildcard-or-exact matching (`app/security/rbac.py`). A token scoped to `*` satisfies every permission check; a token scoped to specific strings (e.g. `understanding:parse`, `matching:evaluate`) only passes those specific checks.

**How CORE obtains a token:** there is no self-service token-issuance endpoint. Request a scoped token from Jobfynder-Infra, specifying exactly which permission strings your integration needs (Section 6.3 has the full permission list by module). Do not request a wildcard token for a service that only needs a handful of scopes.

**Token lifetime and rotation:** tokens do **not** expire on a fixed schedule in the current implementation — they are long-lived until explicitly revoked. Treat them as long-lived secrets: never commit one to a repository, never expose one to the Frontend (it must stay server-side in CORE), and rotate immediately (contact Jobfynder-Infra) if one may have leaked.

**No OAuth2 for Hermes itself.** OAuth2 *does* appear elsewhere in the system — the LinkedIn provider integration, and the Gmail/Microsoft Graph email connectors (Section 7.5) — but that is OAuth2 against those *external* providers, not against Hermes.

### 4.2 COMM: webhook secret + outbound Telegram token

COMM has no bearer-token RBAC of its own — it authenticates in the *inbound* direction differently for each supported channel, and in the *outbound* direction using a fixed provider API token:

- **Inbound (Telegram → COMM):** `POST /providers/telegram/webhook` requires a pre-shared static secret in the `X-Telegram-Bot-Api-Secret-Token` header, compared byte-for-byte against `TELEGRAM_WEBHOOK_SECRET`. This is Telegram's own webhook-security mechanism, not a Jobfynder-specific scheme — Telegram sends this header on every webhook call once you've configured a secret when registering the webhook.
- **Outbound (COMM → Telegram):** COMM calls `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendMessage` using a static bot token (`TELEGRAM_BOT_TOKEN`), the same credential Telegram's Bot API has always used — there is no per-request signing on this leg.
- **`GET /health` and `GET /providers/telegram/status`** are both unauthenticated reads (rate-limited as of 2026-08-21, not access-controlled). The status endpoint reveals which secrets are *configured* (booleans only, never values).

### 4.3 COMM → Hermes: the signed server-to-server contract

This is the one leg of the whole system that uses neither bearer tokens nor a provider-native scheme — it's a Jobfynder-specific HMAC contract, and it is the only way anything from outside Hermes's own process can write into its understanding pipeline via the internal route:

```text
POST /internal/comm/intake   (on Hermes, INTEL-1)

Required headers:
  X-Jobfynder-Timestamp: <unix timestamp, seconds>
  X-Jobfynder-Signature: HMAC-SHA256(shared_secret, timestamp + "." + raw_body)
```

Both sides implement this identically and were cross-verified against each other's source during this document's construction: `hermes/HERMES-450-channel-intake.md` (Hermes side) and `comm_gateway/hermes_client.py` (COMM side, `build_signature()`) produce and expect the exact same signature. The shared secret is `HERMES_COMM_SHARED_SECRET`, configured independently on both servers — it must match on both sides or every COMM-originated intake will be rejected.

**This is deliberately not a bearer token.** A long-lived bearer token would be a worse fit for a fixed, known server-to-server relationship where request integrity (not just authentication) matters — the HMAC signature also proves the request body hasn't been tampered with in transit, which a bearer token alone does not.

### 4.4 Summary table

| Leg | Scheme | Header(s) | Notes |
|---|---|---|---|
| CORE → Hermes | Bearer token | `Authorization: Bearer <token>` | Long-lived, RBAC-scoped, no rotation schedule |
| Telegram → COMM | Pre-shared static secret | `X-Telegram-Bot-Api-Secret-Token` | Telegram's own webhook-security mechanism |
| COMM → Telegram | Static bot token (in URL) | — | Telegram Bot API convention, not per-request signed |
| COMM → Hermes | Computed HMAC-SHA256 | `X-Jobfynder-Timestamp`, `X-Jobfynder-Signature` | The only signed (not just token-based) leg in the system |
| Frontend → CORE | CORE's own auth | — | Out of scope for this document; see CORE's own docs |
| Frontend → Hermes/COMM | **Never happens** | — | Both are always reached through CORE (Hermes) or an external provider webhook (COMM) — never directly from the Frontend |

---

## 5. Login/Auth Endpoints and Example API Calls

Neither Hermes nor COMM has a `/login` endpoint — both are entirely credential-based (Section 4), not session-based. This section covers the endpoints you'll actually call to verify auth is working, for both servers.

### 5.1 Hermes: `GET /health`

The only public, unauthenticated Hermes endpoint.

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

### 5.2 Hermes: `GET /security/rbac/status`

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
{ "detail": "Missing access token" }
```

**Response — 403 Forbidden (token present, wrong scope):**
```json
{ "detail": "Insufficient permission: requires security:read" }
```

### 5.3 COMM: `GET /health`

The only endpoint on either server that has never required any credential and is not the subject of any security control beyond the 2026-08-21 rate limiter.

**Request:**
```http
GET /health HTTP/1.1
Host: comm.jobfynder.com
```

**Response — 200 OK:**
```json
{
  "status": "healthy",
  "service": "jobfynder-comm-gateway",
  "environment": "production"
}
```

### 5.4 COMM: `GET /providers/telegram/status`

Confirms which secrets are configured on COMM. No auth required (a scoping gap noted in Section 9.2) — booleans only, no secret values ever appear in this response.

**Request:**
```http
GET /providers/telegram/status HTTP/1.1
Host: comm.jobfynder.com
```

**Response — 200 OK:**
```json
{
  "provider": "telegram",
  "configured": true,
  "has_bot_token": true,
  "has_webhook_secret": true,
  "has_hermes_secret": true,
  "hermes_base_url": "https://hermes.jobfynder.com"
}
```

### 5.5 Quick auth smoke test (curl, both servers)

```bash
# Hermes: should return 200 with no auth
curl -s https://hermes.jobfynder.com/health

# Hermes: should return 401 - no token
curl -s -o /dev/null -w "%{http_code}\n" https://hermes.jobfynder.com/security/rbac/status

# Hermes: should return 200 with a valid, correctly-scoped token
curl -s -H "Authorization: Bearer <YOUR_SCOPED_TOKEN>" \
  https://hermes.jobfynder.com/security/rbac/status

# COMM: should return 200 with no auth
curl -s https://comm.jobfynder.com/health

# COMM: should return 200 with no auth, revealing configuration booleans only
curl -s https://comm.jobfynder.com/providers/telegram/status

# COMM: sending a fake webhook without the correct secret should return 403
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://comm.jobfynder.com/providers/telegram/webhook \
  -H "Content-Type: application/json" -d '{}'
```

---

## 6. Developer Documentation

### 6.1 Authentication and Authorization (recap for implementers)

- **Hermes:** every route requires `Authorization: Bearer <token>` — including `/understanding/*` and `/submissions/evaluate*` as of 2026-08-21 (Section 9.1); only `/health` stays public.
- **COMM:** `/providers/telegram/webhook` requires the Telegram secret-token header (Section 4.2); `/health` and `/providers/telegram/status` require nothing. There is no permission-string model on COMM at all — it's a single-purpose service, not a multi-tenant API.

### 6.2 Error Handling and Troubleshooting

See Section 11 for the full guide. Day-to-day summary:

| Symptom | System | Likely cause | Where to look |
|---|---|---|---|
| 401 on every Hermes call | Hermes | Missing/malformed `Authorization` header | Confirm `Bearer <token>`, not just `<token>` |
| 403 on some Hermes calls, not others | Hermes | Token lacks the permission that route requires | Cross-reference Section 6.3's permission column |
| 200 from Hermes but `requires_review: true` / `decision: "needs_review"` | Hermes | Not an error — a genuine business outcome | Read `reasons`/`risks` in the body |
| Slow response (~30s) on a prompt-related Hermes call | Hermes | Langfuse cold-cache fetch — **fixed 2026-08-21**, see Section 8.4 | Section 11.3 |
| COMM webhook returns 403 | COMM | Telegram secret mismatch | Section 11.4 |
| Telegram user gets "could not process this message" | COMM/Hermes boundary | Hermes returned non-200, or (pre-2026-08-21) Hermes was unreachable and COMM crashed silently — now returns this message instead | Section 11.5 |
| Telegram user gets no reply at all | COMM | **Should no longer happen as of 2026-08-21** — if it does, this is a regression, escalate immediately (Section 11.5) |

### 6.3 Data Models and API Contracts

**Hermes** has two response shapes by design:

**Legacy shape** — endpoints built before the 2026-08-15 architecture freeze keep their own typed response (`UnderstandingResult`, `ResumeTailoringResponse`, etc.).

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

Always check `execution_mode`/`llm_required` (envelope) or `decision`/`fallback.llm_fallback` (legacy) to know whether a call actually incurred LLM cost — never assume from HTTP status.

**Full Hermes endpoint index by module and required permission:**

| Module | Sample routes | Typical permission | Shape |
|---|---|---|---|
| Understanding (HERMES-200) | `POST /understanding/parse-text`, `/understanding/parse-file` | `understanding:parse` (currently unenforced — Section 9.1) | Legacy |
| Taxonomy (HERMES-400) | `GET /understanding/taxonomy/skills`, `POST /understanding/taxonomy/normalize`, `POST /understanding/taxonomy/suggestions`, `GET /understanding/taxonomy/suggestions/queue` | `understanding:read` / `understanding:parse` | Legacy + custom |
| Matching (HERMES-300) | `GET /matching/policy`, `POST /matching/resume-to-job` | `matching:evaluate` | Legacy |
| Submission Intelligence (HERMES-500) | `GET /submissions/workflow-policy`, `POST /submissions/evaluate`, `POST /submissions/evaluate/from-handoff` | none currently enforced — Section 9.1 | Legacy |
| Integrations (HERMES-600) | `GET /integrations/health`, `POST /integrations/events/normalize`, `POST /integrations/jobfynder/submission-handoff/evaluate` | varies | Legacy |
| Agents (HERMES-700) | `GET /agents/registry`, `POST /agents/dry-run` — **dry-run only, no exceptions** | `agents:read` / `agents:run` | Custom |
| Prompt Runtime (HERMES-750) | `GET /prompts/registry`, `POST /prompts/run` | `agents:read` / `agents:run` | Custom |
| Resume Builder (HERMES-800) | `POST /resume-builder/analyze`, `/summary/suggest`, `/bullets/suggest`, `/tailor`, `/quality/analyze` | `resume_builder:read` / `:analyze` / `:suggest` | Custom |
| Context Cards | `POST /context/candidate-card/build`, `/job-card/build`, `/relationship-card/build`, `/conversation/compress` | scoped, wildcard-satisfiable | Canonical envelope |
| Channels/Providers (HERMES-450/850) | `POST /channels/intake`, `/channels/telegram/webhook`, `/providers/email/webhook`, `/providers/gmail/push`, `/providers/microsoft-graph/webhook` | varies; webhook routes use signature auth, not bearer | Legacy |
| **Internal COMM intake** | `POST /internal/comm/intake` | HMAC signature, not bearer (Section 4.3) | Legacy |

For the always-current, machine-readable route list: `GET /openapi.json` against the running Hermes service.

**COMM's data model — the canonical intake shape** (produced by `normalize_telegram_update()`, the same shape any future channel adapter must produce):

```json
{
  "channel": "telegram",
  "source_message_id": "12345",
  "sender": { "sender_id": "987654321", "sender_name": "Jane Doe", "username": "janedoe" },
  "conversation_id": "987654321",
  "content_type": "text",
  "text": "Looking for Python roles in Dallas",
  "attachments": [],
  "metadata": { "telegram_update_id": 100200300, "telegram_chat_type": "private", "telegram_chat_id": 987654321 }
}
```

**Known gap in this shape:** only Telegram `document` attachments are extracted into `attachments` — photo, voice, video, and sticker message types are not handled by the current normalizer and will produce an empty `attachments` array even when the original message had media. Not confirmed to have caused real data loss, but worth a live test before relying on attachment handling for non-document media.

**COMM's only three endpoints, complete (this is the entire public API surface of the COMM Gateway):**

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | none | Liveness check |
| GET | `/providers/telegram/status` | none | Reports which Telegram/Hermes secrets are configured (booleans only) |
| POST | `/providers/telegram/webhook` | Telegram secret-token header | Receives an inbound Telegram update, normalizes, forwards to Hermes, replies to the user |

### 6.4 Rate Limits and Throttling

- **Hermes** does not enforce request-rate limiting at the application layer. Rate limiting for LLM calls happens one layer down, at LiteLLM: every virtual key carries a spend budget (verified live — e.g. a key showing "$1.82 of $20" with a monthly reset date). If a Hermes capability escalates to an LLM call and the underlying LiteLLM key's budget is exhausted, expect that call to fail — build retry/backoff and a clear user-facing message, don't assume LLM calls always succeed.
- **COMM: fixed 2026-08-21.** An in-memory, per-IP, per-path sliding-window limiter (`comm_gateway/ratelimit.py`) now caps every COMM endpoint at 120 requests/60 seconds per client IP, live-tested (114/125 rapid requests passed, 11 correctly rejected with `429` at the threshold). **Known limitation, stated in the code's own docstring:** this is in-memory and per-instance — fine for the current single-container deployment; if COMM Gateway is ever scaled to multiple replicas, the counters need to move to the Redis instance already running alongside it rather than staying in-process. A caller hitting `429 {"detail": "rate_limited"}` should back off, not retry immediately.

### 6.5 Security Considerations and Compliance Notes

See Section 9 for the full treatment. Key points for implementers:

- Never construct a Hermes request that puts raw resume/JD/message text directly into a prompt variable — always go through a Context Card builder or a deterministic parser first.
- Never log a Hermes bearer token, a COMM webhook/HMAC secret, or a Langfuse/LiteLLM key, even in debug output.
- PII handling: Hermes does not currently redact PII before sending it to Langfuse for tracing — if a prompt's input variables contain candidate PII, that PII is visible in the Langfuse trace.
- COMM's public endpoint has already received unsolicited scanner traffic (probes for `/.env`, `/.git/HEAD`, `/terraform.tfstate`, all correctly 404'd, nothing exposed) — treat COMM as internet-facing and adversarial-traffic-exposed, because it demonstrably is.

### 6.6 Versioning and Deprecation Strategy

- **Hermes:** endpoints don't carry a version prefix except the legacy `/v1/*` routes (`/v1/jobs/parse`, `/v1/messages/understand`, etc.), which predate the rest of the API and are kept for backward compatibility — prefer the non-versioned equivalents for new integrations. The canonical envelope (Section 6.3) is the intended long-term response contract; migrating a legacy-shaped endpoint to it is a breaking change and is not done without an explicit, documented decision. Module-level versioning happens through HERMES-XXX stream numbering and git tags (e.g. `hermes-800-resume-builder-foundation-v1`).
- **COMM:** version `0.1.0` (from `FastAPI(title="Jobfynder COMM Gateway", version="0.1.0")`), no versioned route prefixes at all — the entire API surface is 3 endpoints (Section 6.3), and there is no deprecation history yet to speak of.

---

## 7. End-to-End Integration with Jobfynder CORE

### 7.1 Provisioning checklist (new environment)

**Hermes side:**
1. Confirm the Hermes container is deployed and `/health` responds.
2. Confirm `LITELLM_API_KEY` and `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are set on Hermes's `.env` — and that they are the correct, dedicated keys for this environment, not a personal or ad-hoc key (this exact mistake happened once already; see Section 11.3).
3. Request a scoped Hermes bearer token for CORE from Jobfynder-Infra (Section 4.1).
4. Set that token in CORE's own environment config — never in a client-visible config file.
5. Run the Hermes smoke test (Section 12.1) before pointing real traffic at it.

**COMM side (only relevant if this environment needs live Telegram — or any future channel — intake):**
1. Confirm the COMM Gateway container is deployed and `/health` responds.
2. Confirm `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, and `HERMES_COMM_SHARED_SECRET` are set on COMM's `.env` — and that `HERMES_COMM_SHARED_SECRET` matches the value configured on the Hermes side (Section 4.3); a mismatch here fails silently from COMM's perspective (Hermes just rejects the signature) and needs both sides checked.
3. Register the Telegram webhook (via Telegram's `setWebhook` API) pointed at `https://comm.jobfynder.com/providers/telegram/webhook`, with the same secret as `TELEGRAM_WEBHOOK_SECRET`.
4. Run the COMM smoke test (Section 12.1) — including a real end-to-end Telegram message — before treating this environment as live.

### 7.2 Data flow for the integration cases

**Case 1 — Resume Builder (CORE-initiated).** Frontend → CORE → Hermes `POST /understanding/parse-text` (or `/parse-file`) → Hermes `POST /resume-builder/*` for suggestions/analysis → CORE persists the structured resume, holds any AI-suggested content as a **suggestion pending human approval** (no auto-publish, no auto-rewrite — a hard rule, not a preference).

**Case 2 — Job Board matching (CORE-initiated).** CORE has structured job + resume data (or raw text) → Hermes `POST /matching/resume-to-job` (or `/from-understanding`) → deterministic score, no LLM → CORE stores the match result and surfaces `submit`/`review`/`reject`.

**Case 3 — Job Tracker / submission workflow (CORE-initiated).** CORE has a submission stage transition or event → Hermes `POST /submissions/evaluate` (or `/from-handoff`) → Hermes returns a recommended stage, conflicts, follow-up instructions → **CORE persists the actual stage change; Hermes never writes to CORE's database directly.** Follow the integration safety rules in Section 7.3.

**Case 4 — Email intake (HERMES-850, CORE-initiated indirectly).** Inbound email → provider connector normalizes it (Telegram is live via COMM, not email; Gmail/Graph are built and tested but require OAuth credentials before real email reaches them — Section 7.5) → Hermes parses it deterministically → a draft object is created in Hermes's own storage (`/drafts/{draft_id}`) → whether CORE polls or is pushed these drafts, and turns them into real Candidate/Job records, is integration work whose completeness on the CORE side should be confirmed with the integration owner before this flow is assumed to be end-to-end.

**Case 5 — Telegram conversational intake (COMM-initiated, the one flow with no CORE step by default).** Telegram user sends a message → COMM normalizes and HMAC-forwards it to Hermes (Section 3.4) → Hermes runs it through the same understanding/taxonomy/draft pipeline as any other intake → Hermes's response is delivered straight back to the Telegram user by COMM. **CORE is not involved unless something else consumes whatever Hermes produced from that intake** — a Telegram conversation, by itself, does not create a CORE record. If your integration needs Telegram-sourced data to reach CORE, that consumption logic needs to exist and be verified separately; it is not implied by the fact that COMM successfully delivered the message to Hermes.

### 7.3 Integration safety rules (submission workflow specifically)

Written into the HERMES-500 closure record; treat as hard rules for any CORE code consuming this endpoint:

1. Never blindly overwrite a terminal stage (`placed`, `closed_lost`, etc.).
2. If the response's `conflicts` array is non-empty, require human review before acting.
3. If `stage_changed` is `false`, do not update the tracker stage.
4. If `follow_up.required` is `true`, create a follow-up task with the given priority.
5. If `recommended_stage` is `duplicate_risk`, block auto-submission.
6. If `outcome.outcome_type` is `placed`, mark the workflow complete.
7. Store the full Hermes response for audit/debugging — don't discard fields you don't immediately use.

### 7.4 Dependency map and failure modes

**CORE → Hermes:**
```text
1. Network/DNS to hermes.jobfynder.com          -> CORE should retry with backoff
2. Hermes auth (401/403)                        -> not retryable, fix the token/scope
3. Hermes deterministic processing (rare)        -> 500, check Hermes logs
4. Hermes escalates to LLM, and:
   a. Langfuse prompt fetch fails/times out      -> Hermes returns a "failed" decision, not a crash
   b. LiteLLM call fails (budget, provider down) -> same: "failed" decision, retryable once by Hermes itself
5. Response reaches CORE, but represents a business rejection, not a failure -> not an error path, handle it as data
```

**Telegram → COMM → Hermes (the whole chain, including the 2026-08-21 fix):**
```text
1. Telegram webhook secret mismatch              -> COMM returns 403, request never reaches Hermes
2. COMM's normalization step (rare, malformed
   Telegram payload)                             -> would surface as a 422/500 from COMM itself
3. COMM -> Hermes call:
   a. Timeout / connection error (Hermes slow
      or unreachable)                             -> FIXED 2026-08-21: caught in comm_gateway/
                                                       hermes_client.py, returns a structured
                                                       {"status": "error", "reason": "..."} instead
                                                       of raising. User gets the existing "could not
                                                       process this message" reply. BEFORE this fix,
                                                       this path crashed unhandled and the user got
                                                       no reply at all -- if you ever see silence
                                                       again on this path, treat it as a regression,
                                                       not expected behavior.
   b. Hermes returns non-200                      -> same "could not process" reply
4. COMM's own reply-delivery step (Telegram
   sendMessage) fails                             -> NOT caught with the same rigor -- no retry/
                                                       backoff on this specific call (Section 9.2).
                                                       This is a known, smaller, still-open gap.
5. No queueing anywhere in this chain             -> a slow Hermes call makes the whole webhook
                                                       request slow; COMM does not buffer via the
                                                       RabbitMQ instance running alongside it (it's
                                                       provisioned, not wired in -- Section 9.2).
```

Hermes's own internal fallback: if a prompt's primary router alias has no healthy deployment on LiteLLM, it attempts exactly one fallback to `HERMES_PROMPT_DEFAULT_MODEL`. No further retries, no silent escalation — by design, to keep cost and behavior predictable.

### 7.5 Email provider OAuth flow (Gmail / Microsoft Graph) — when activated

Not live yet (Section 7.2, Case 4), documented here so whoever activates it has the shape ready. **This is entirely on the Hermes side** — COMM has no role in email intake as currently built.

**Gmail:** register an OAuth application in Google Cloud Console, grant it Gmail API read access to the target mailbox, configure Cloud Pub/Sub push notifications pointed at `POST /providers/gmail/push` (on Hermes). Set `HERMES_GMAIL_CLIENT_ID`, `HERMES_GMAIL_CLIENT_SECRET`, `HERMES_GMAIL_REFRESH_TOKEN`, `HERMES_GMAIL_PUBSUB_TOPIC`.

**Microsoft Graph:** register an app in Microsoft Entra/Azure AD, grant `Mail.Read` permission, create a Graph subscription pointed at `POST /providers/microsoft-graph/webhook` (on Hermes) — that endpoint already implements the required `validationToken` handshake Graph performs at subscription creation. Set `HERMES_MS_GRAPH_CLIENT_ID`, `HERMES_MS_GRAPH_CLIENT_SECRET`, `HERMES_MS_GRAPH_TENANT_ID`.

Both connectors' message-normalization code is built and unit-tested against realistic sample payloads; only the authenticated fetch-from-provider-API step remains to be implemented once real credentials exist.

---

## 8. Deployment and Operational Considerations

### 8.1 Environment and deployment model

**Hermes (INTEL-1):**
- Single Docker container (`hermes-api`), built from `/opt/hermes`, via `docker-compose.yml` in that directory.
- **Important operational pattern:** the git workflow is branch-per-module, not merge-to-main. Each `feature/hermes-XXX-*` branch is built on top of the previous module's closure tag, and the server runs whichever branch was last built into the image — `main` is largely unused for deployment purposes. Check the currently-deployed branch/commit with `git -C /opt/hermes log -1` before assuming `main` reflects reality.
- **Config-change gotcha:** `docker compose restart hermes-api` does **not** reload `.env` for an already-created container. Use `docker compose up -d --force-recreate hermes-api` after any `.env` change.

**COMM (COMM-1):**
- Single Docker container (`jobfynder-comm-gateway`), built from `/opt/jobfynder-infra/communication`, via `docker-compose.yml` in that directory, alongside `jobfynder-npm` (Nginx Proxy Manager), `jobfynder-rabbitmq`, and `jobfynder-redis`.
- Deployed branch: `feature/comm-telegram-message-chunking` (as of 2026-08-21, includes commit `0c33580`, the resilience/rate-limit/backup fix). **This branch has not been merged to `main`** on `jobfynder-infra` — a merge was attempted 2026-08-21 and deliberately not forced through, because `main` has diverged with unrelated infra restructuring (a different `intelligence/docker-compose.yml`, and two stray SSH public keys committed at the repo root — public keys only, no private key exposure, but still needing a deliberate reconciliation pass rather than an automatic merge). Check `git -C /opt/jobfynder-infra log -1` on COMM-1 before assuming `main` reflects reality here too — same caution as the Hermes side.
- Same `--force-recreate` requirement applies to `.env` changes.

### 8.2 CI/CD

No automated CI/CD pipeline was found wired to either repo as of this document — deployment is manual on both servers (SSH in, pull/checkout the target branch, `docker compose build`, `docker compose up -d --force-recreate`). For rollback: check out the previous known-good tag/commit and rebuild — always back up `.env` before any config change (`cp .env .env.bak-$(date +%Y%m%d%H%M%S)` on both servers).

### 8.3 Observability

**Hermes:**
- **Logging:** `docker logs hermes-api`. Prompt execution also writes structured JSONL logs to `/hermes-runtime/prompt-runs`.
- **Tracing:** every live prompt execution is traced to Langfuse (trace + generation events, including token usage and exact model used).
- **Metrics/alerting:** no dedicated stack found wired to Hermes specifically. LiteLLM's own dashboard provides spend/usage per virtual key.
- **Health checks:** `GET /health` (liveness only). For a real dependency check, `GET /prompts/health` reports `litellm_configured` and `langfuse_configured` booleans.

**COMM:**
- **Logging:** `docker logs jobfynder-comm-gateway` — plain uvicorn access logs, no structured log format. Confirmed useful for confirming inbound scanner/abuse traffic (Section 9.2) as well as normal request flow.
- **Tracing:** none — COMM does not participate in Langfuse tracing; a request's Hermes-side trace exists, but there's no COMM-side span linking the two.
- **Metrics/alerting:** none. Portainer (`portainer/portainer-ce:lts`) is installed on COMM-1 for manual Docker inspection, not automated alerting.
- **Health checks:** `GET /health` (liveness only, no dependency check — a healthy COMM response does not guarantee Hermes is reachable).

### 8.4 Performance and load considerations

**Hermes — fixed 2026-08-21:** the Langfuse prompt-registry fetch (`_refresh_cache()` in `app/prompt_runtime/langfuse_prompts.py`) used to fetch all prompts sequentially, one HTTP call per prompt — measured at ~33 seconds for 38 prompts on a cold cache. Now fetches concurrently (`ThreadPoolExecutor`, default 8 workers, tunable via `HERMES_LANGFUSE_PROMPT_FETCH_CONCURRENCY`) — verified live at 7.55 seconds for the same 38 prompts. The cache lasts 5 minutes (`HERMES_LANGFUSE_PROMPT_CACHE_SECONDS`), so only the first request after expiry pays this cost.

**COMM — fixed 2026-08-21:** the unhandled-exception gap (Section 7.4) meant a slow/unreachable Hermes call could hang a webhook request up to the full 30-second `httpx` timeout with no recovery. Now returns a structured error immediately on `httpx.TimeoutException`/`httpx.RequestError` rather than propagating the exception — the *user-facing* latency for a failure case is now bounded by the 30s timeout at worst (unchanged) but the *outcome* is now a defined reply instead of an unhandled crash. Rate limiting (Section 6.4) also caps burst load at 120 req/min/IP/path — live-tested and confirmed the service stays healthy under a 125-request burst.

---

## 9. Security and Compliance Notes

### 9.1 Hermes: RBAC gap — closed 2026-08-21

`/understanding/*` and `/submissions/evaluate*` previously had **no RBAC check at all**. Fixed and deployed 2026-08-21 (commit `9dc69d5` on `jobfynder/hermes`, branch `fix/hermes-100-close-rbac-gap`): `understanding:parse`/`understanding:read` on every `/understanding/*` route, `submissions:evaluate` on `POST /submissions/evaluate` and `/evaluate/from-handoff` — scoped to exactly the documented gap, not expanded to `/submissions/workflow-policy` or the tracker/status extract endpoints.

**Confirmed safe before deploying, not assumed:** live Hermes traffic logs showed zero hits on either route group (5000-line window), and a grep of the entire `jobFynder-BE-nestJS` codebase found no code calling these Hermes endpoints at all — the only Hermes↔CORE integration actually built was the reverse direction (CORE's `/hermes/*` controller, called *by* Hermes/agents). Live-verified post-deploy: `401` with no token, `403` with a token scoped to a different permission, `200` with a new `jobfynder-core` token (permissions: `understanding:parse`, `understanding:read`, `submissions:evaluate`) — including a full resume-parse call that correctly escalated to the LLM via LiteLLM on low-confidence input.

### 9.2 COMM: security posture, confirmed gaps and fixes

- **Rate limiting: fixed 2026-08-21** (Section 6.4). Was previously fully unlimited on every endpoint including the public webhook.
- **`fail2ban` on COMM-1 is scoped to SSH only**, not HTTP — unchanged by the 2026-08-21 fix. The application-level rate limiter is the first line of HTTP-layer defense; Nginx Proxy Manager itself has no access lists or additional rate limits configured on the `comm.jobfynder.com` proxy host.
- **Host firewall (`ufw`) is inactive on COMM-1.** Host-level traffic control is currently just Docker's default `iptables` behavior plus `fail2ban` on SSH.
- **Confirmed real-world exposure, not theoretical:** live logs (pre- and post-fix) show unsolicited scanner traffic probing `/.env`, `/.git/HEAD`, `/terraform.tfstate`, `/login` against the public endpoint — all correctly 404'd, no secrets exposed. The rate limiter now bounds how much of this traffic can hit the app in a burst; it does not stop the probing or alert anyone to the pattern.
- **`GET /providers/telegram/status` is unauthenticated** and reveals which secrets are configured (booleans only) — low severity, still worth eventually gating.
- **Backups: fixed 2026-08-21.** A daily cron (3am, 14-day retention) now backs up all four COMM-1 Docker volumes (RabbitMQ, Redis, NPM data + certs). No restore has been tested against these backups yet — a backup that has never been restored is a hypothesis, not a guarantee, and this remains a real, smaller open item.
- **RabbitMQ and Redis on COMM-1 remain fully unused** — provisioned capacity only, zero code references, zero queues, zero keys, as of this document. Do not assume any COMM traffic passes through either.

### 9.3 Data at rest / in transit

- All external traffic (CORE↔Hermes, Telegram↔COMM, COMM↔Hermes, Hermes↔LiteLLM, Hermes↔Langfuse) is over HTTPS.
- Hermes holds no persistent database of its own — `/hermes-runtime` stores drafts, taxonomy suggestions, prompt-run logs, and intake/event records as JSON files on the host filesystem, not currently encrypted at rest beyond whatever the underlying host disk provides. Treat it as containing sensitive data (parsed resumes, candidate PII) and scope host-level file access accordingly.
- COMM holds no persistent database at all — it is stateless per-request. The only persistent COMM-1 data is the (currently unused) RabbitMQ/Redis volumes and the NPM certificate/config volumes, now covered by the daily backup (Section 9.2).
- No dedicated key-management service (e.g. a vault) was found in use on either server — secrets live in `.env` files on each host. Rotate any secret that may have been exposed.

### 9.4 Access control principles

- Least privilege: request only the Hermes permission strings an integration actually needs (Section 4.1), never a wildcard token for a narrow-purpose integration.
- Server-to-server intake (`/internal/comm/intake`) and the Telegram webhook use signature/secret-based auth, not bearer tokens — appropriate for machine-to-machine calls where a long-lived bearer token would be a worse fit (Section 4.3).
- Multi-agent capabilities (HERMES-700) are **dry-run only, with no exception path** — agents cannot submit candidates, message recruiters, change production data, or take any other high-risk action automatically, regardless of what a caller requests. Enforced in code (`app/agents/service.py` policy checks), not just documented as convention.

### 9.5 Compliance references

No formal PCI-DSS or GDPR compliance audit was found documented for either server as of this writing. If Jobfynder needs to make a compliance claim (e.g. GDPR right-to-erasure for candidate data stored in `/hermes-runtime`, or for any Telegram conversation content that passed through COMM), that requires a dedicated review — this document does not constitute one. Flagged here as an open item, not resolved.

### 9.6 PII in traces

Repeating from Section 6.5 because it's easy to miss: Langfuse traces capture full prompt inputs and outputs by default. If a prompt's rendered content includes candidate PII, that PII is visible to anyone with Langfuse project access. There is no redaction step in the current `send_langfuse_trace()` implementation. COMM does not participate in Langfuse tracing at all, so this specific risk is Hermes-only — but any PII that flows Telegram → COMM → Hermes is subject to it once it reaches Hermes's prompt runtime.

---

## 10. API Samples and Code Blocks

### 10.1 Hermes: parse a resume (deterministic, auto-escalates to LLM below confidence 0.70)

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

**Field name correction, 2026-08-21:** the `RawDocument` model takes `content`, not `text` — confirmed with a live call using the new `jobfynder-core` RBAC token during the HERMES-100 RBAC-fix verification.

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
    "normalized_skills": ["Python", "Django", "PostgreSQL", "AWS"]
  }
}
```

### 10.2 Hermes: score a resume against a job

**Request:**
```http
POST /matching/resume-to-job HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
Content-Type: application/json

{
  "resume": { "skills": ["Python", "Django", "AWS"], "years_experience": 8, "work_authorization": "citizen", "location": "Dallas, TX" },
  "job": { "required_skills": ["Python", "Django"], "preferred_skills": ["AWS", "Kubernetes"], "years_experience": 5, "work_authorization": "citizen", "location": "Dallas, TX" }
}
```

**Response — 200 OK:**
```json
{
  "match_score": 88.5,
  "decision": "submit",
  "matched_required_skills": ["Python", "Django"],
  "missing_required_skills": [],
  "matched_preferred_skills": ["AWS"],
  "reasons": ["All required skills matched.", "8 years exceeds 5 year requirement."],
  "risks": [],
  "recommendation": "Strong match, submit.",
  "matcher_version": "basic_local_matcher_v1"
}
```

### 10.3 Hermes: evaluate a submission workflow event

**Request:**
```http
POST /submissions/evaluate HTTP/1.1
Host: hermes.jobfynder.com
Authorization: Bearer <YOUR_SCOPED_TOKEN>
Content-Type: application/json

{ "current_stage": "matched", "event_type": "intro_requested" }
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

### 10.4 COMM: inbound Telegram webhook (as sent by Telegram, and what happens next)

**Request Telegram sends to COMM:**
```http
POST /providers/telegram/webhook HTTP/1.1
Host: comm.jobfynder.com
X-Telegram-Bot-Api-Secret-Token: <TELEGRAM_WEBHOOK_SECRET>
Content-Type: application/json

{
  "update_id": 100200300,
  "message": {
    "message_id": 42,
    "from": { "id": 987654321, "first_name": "Jane", "username": "janedoe" },
    "chat": { "id": 987654321, "type": "private" },
    "date": 1755763200,
    "text": "Looking for Python roles in Dallas"
  }
}
```

**Response COMM returns to Telegram — 200 OK (success path):**
```json
{
  "status": "processed",
  "normalized": {
    "channel": "telegram",
    "source_message_id": "42",
    "sender": { "sender_id": "987654321", "sender_name": "Jane", "username": "janedoe" },
    "conversation_id": "987654321",
    "content_type": "text",
    "text": "Looking for Python roles in Dallas",
    "attachments": []
  },
  "hermes": { "status_code": 200, "response": { "outbound_messages": [{ "text": "Found 3 matching roles in Dallas..." }] } },
  "telegram_outbound": { "status_code": 200, "response": { "ok": true } },
  "telegram_outbound_messages": [{ "status_code": 200, "response": { "ok": true } }]
}
```

**Response COMM returns to Telegram — 200 OK, but Hermes was unreachable (post-2026-08-21-fix failure path — note: this is still HTTP 200 from COMM's perspective, per Section 3.5; the failure is inside the body and, more importantly, in what the Telegram user receives):**
```json
{
  "status": "processed",
  "normalized": { "...": "same shape as above" },
  "hermes": { "status": "error", "reason": "hermes_request_timeout" },
  "telegram_outbound": { "status_code": 200, "response": { "ok": true } },
  "telegram_outbound_messages": [{ "status_code": 200, "response": { "ok": true } }]
}
```
In this case, the Telegram user receives: *"Jobfynder could not process this message. Please try again."* — a defined, real reply, not silence. **Before the 2026-08-21 fix, this exact scenario (Hermes timeout) crashed the request unhandled and the user received nothing at all.**

**Response COMM returns — 403 Forbidden (wrong/missing secret):**
```json
{ "detail": "invalid_telegram_webhook_secret" }
```

**Response COMM returns — 503 Service Unavailable (webhook secret not configured on this environment):**
```json
{ "detail": "telegram_webhook_secret_not_configured" }
```

**Response COMM returns — 429 Too Many Requests (rate limit, added 2026-08-21):**
```json
{ "detail": "rate_limited" }
```

### 10.5 COMM → Hermes: the resulting signed intake call (server-to-server, not client-facing — shown for completeness)

```http
POST /internal/comm/intake HTTP/1.1
Host: hermes.jobfynder.com
Content-Type: application/json
X-Jobfynder-Timestamp: 1755763201
X-Jobfynder-Signature: <hex HMAC-SHA256 of "1755763201." + the exact JSON body below>

{"channel":"telegram","source_message_id":"42","sender":{"sender_id":"987654321","sender_name":"Jane","username":"janedoe"},"conversation_id":"987654321","content_type":"text","text":"Looking for Python roles in Dallas","attachments":[],"metadata":{"telegram_update_id":100200300,"telegram_chat_type":"private","telegram_chat_id":987654321}}
```

### 10.6 Error code reference (both servers)

| Code | System | Meaning | Typical cause |
|---|---|---|---|
| 200 | Hermes | Success **or** a valid business outcome (`blocked`, `needs_review`, `rejected`) | Check the body's decision field, not just the status |
| 200 | COMM | Webhook was processed — **does not guarantee the Hermes call succeeded** | Check the `hermes` field in the body (Section 3.5) |
| 401 | Hermes | Missing or malformed bearer token | `Authorization` header absent or not `Bearer <token>` |
| 403 | Hermes | Token valid but lacks the required permission | Check permission scope (Section 6.3) |
| 403 | COMM | Telegram webhook secret mismatch or missing | Check `X-Telegram-Bot-Api-Secret-Token` against `TELEGRAM_WEBHOOK_SECRET` |
| 404 | Hermes | Resource not found (unknown `prompt_id`, unknown draft ID) | Verify the ID via the corresponding list/registry endpoint first |
| 422 | Hermes | Request body failed schema validation | Check required fields against the endpoint's model |
| 429 | COMM | Rate limit exceeded (120 req/min/IP/path, added 2026-08-21) | Back off; do not retry immediately |
| 500 | Hermes | Genuine server error | Check `docker logs hermes-api`; not a business-logic outcome |
| 503 | COMM | Telegram webhook secret not configured on this environment | Set `TELEGRAM_WEBHOOK_SECRET` in COMM's `.env`, `--force-recreate` |

---

## 11. Troubleshooting Guide

### 11.1 "Every Hermes call returns 401"

Confirm the header is exactly `Authorization: Bearer <token>` — not `Authorization: <token>`, not `Bearer: <token>`. Confirm the token hasn't been revoked (ask Jobfynder-Infra).

### 11.2 "Some Hermes calls work, others return 403"

Your token doesn't carry the permission the specific route requires. Cross-reference against Section 6.3. If you believe the route *should* be unprotected, check Section 9.1 first — two route groups genuinely have no RBAC at all, a separate, tracked issue, not something to route around by requesting a wildcard token.

### 11.3 "A Hermes prompt-related call is very slow or times out"

This was the Langfuse N+1 fetch issue (Section 8.4), fixed 2026-08-21 — a cold-cache fetch now takes ~7-8s instead of ~33s. If a call is still taking 20s+ after that fix is deployed, the cache likely isn't holding — check `HERMES_LANGFUSE_PROMPT_CACHE_SECONDS` is set and the container hasn't been restarted recently (a restart clears the in-process cache), or that `HERMES_LANGFUSE_PROMPT_FETCH_CONCURRENCY` hasn't been set too low.

**If it looks like an outright auth failure (HTTP 403 with `error code: 1010` in the body):** this is Cloudflare's bot-protection layer in front of `langfuse.jobfynder.com`, not a Langfuse credential problem — triggered by requests with no recognizable User-Agent header. Production code sets one (`User-Agent: Hermes-PromptRuntime/1.0`); this only bites ad-hoc debugging scripts that omit it.

**If Langfuse calls fail outright:** verify `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` match a key actually issued for this purpose (check the Langfuse project's API-keys settings for a key whose note identifies it as the Hermes production key). Remember `docker compose restart` won't pick up a key rotation — use `--force-recreate`.

### 11.4 "COMM's Telegram webhook returns 403"

Expected behavior if the secret doesn't match — this is the security control working, not a bug. Confirm the caller sends `X-Telegram-Bot-Api-Secret-Token` matching `TELEGRAM_WEBHOOK_SECRET`. **Do not "fix" a 403 here by disabling the check** — the fix is always to send the correct secret, never to weaken verification.

**Regression-safe testing pattern (replaces any stale, non-regression-safe reference):** a test script that previously omitted the secret header and treated the resulting 403 as a bug has since been corrected. The current, correct pattern lives in two places and both must be run, not just one:
- On the Hermes side: `scripts/hermes-450-channel-intake-check.py` — sends the real secret on the positive-path test, and separately asserts `403` on a dedicated negative-path test with a deliberately wrong/missing secret, so a real regression (the check silently passing even when the secret verification is broken) can't hide behind an "expected rejection."
- On the COMM side: `communication/scripts/comm-telegram-onboarding-route-check.py` and `communication/scripts/comm-telegram-message-chunking-check.py` cover COMM's own webhook-handling logic; `communication/scripts/comm-hermes-client-resilience-check.py` (added 2026-08-21) specifically covers the timeout/connection-error path described in Section 7.4 — run this one explicitly if you're investigating a "no reply" report, since that's exactly the regression it exists to catch.

Do not accept "the webhook returned 403 once during testing" as sufficient regression coverage for this path — both the positive path (correct secret → 200, message processed) and the negative path (wrong secret → 403, message rejected) must be exercised every time this code changes, or a broken secret check could silently pass unnoticed in either direction.

### 11.5 "Telegram user gets 'could not process this message' or no reply at all"

- **"Could not process this message"** is the expected, defined failure reply as of the 2026-08-21 fix (Section 7.4) — it means COMM's call to Hermes returned an error or a non-200 status. Check COMM's logs (`docker logs jobfynder-comm-gateway`) for the `hermes` field in the corresponding request's response, and check Hermes's own logs/health for what actually went wrong upstream.
- **No reply at all** should not happen as of the 2026-08-21 fix. If you observe this, it is a regression — either the fix was reverted, a new unhandled code path was introduced in `hermes_client.py` or `main.py`'s webhook handler, or the failure is happening *after* the Hermes call succeeds, in the Telegram-delivery step itself (`send_telegram_message` in `telegram.py`), which does **not** have the same exception-handling rigor applied to it (Section 7.4, step 4) — check that specific call's logs before assuming the fix regressed.

### 11.6 "A Hermes submission/matching call succeeds but nothing changed in CORE's database"

Very likely working as designed, not a bug — Hermes proposes, CORE executes (Section 3.5, 7.2 Case 3). Confirm CORE's own integration code actually reads the Hermes response and calls its own persistence layer. Hermes returning `recommended_stage` does not mean CORE's tracker stage updated automatically.

### 11.7 "Draft object created in Hermes (via email or Telegram intake), but no corresponding record in Jobfynder's live data"

Same root cause as 11.6, applies to both the email-intake flow (Section 7.2 Case 4) and the Telegram flow (Case 5). Check `GET /drafts/{draft_id}` on Hermes to confirm the draft exists, then confirm with the CORE integration owner whether the consuming logic that turns drafts into real records is deployed in this environment.

### 11.8 "Hermes agent execution returns `needs_review` for everything"

Expected — HERMES-700 agents are dry-run only by design (Section 9.4). There is no "execute" mode to switch on; this isn't a misconfiguration.

### 11.9 "COMM is responding slowly or returning 429 under normal traffic"

Check whether the 120 req/min/IP/path rate limit (Section 6.4, added 2026-08-21) is being hit legitimately — a single high-volume IP (e.g. a shared corporate NAT with many real users) could plausibly hit this. If so, the limiter's threshold is a config value in `comm_gateway/main.py` (`app.add_middleware(RateLimitMiddleware, limit=120, window_seconds=60)`) and can be raised; do not disable the limiter outright given the confirmed scanner traffic in Section 9.2.

---

## 12. Recommended Testing Plan

### 12.1 Unit-level (per module, run inside the relevant container)

**Hermes** — run the existing verification scripts for whichever modules your integration touches:
```bash
docker exec -w /app hermes-api sh -c 'PYTHONPATH=/app python3 scripts/<script-name>.py'
```
Every module has at least one script under `scripts/hermes-<module>-*.py`. **Success criterion: exit code 0 and the script's own final `PASSED`/`OK` line.**

**COMM** — run the existing verification scripts, same pattern:
```bash
docker exec -w /app jobfynder-comm-gateway sh -c 'python3 scripts/<script-name>.py'
```
Current scripts: `comm-telegram-message-chunking-check.py`, `comm-telegram-onboarding-check.py`, `comm-telegram-onboarding-route-check.py`, `comm-hermes-client-resilience-check.py` (2026-08-21, mocked timeout/connection-error/missing-secret cases — **run this one whenever touching `hermes_client.py`, not optionally**). **Success criterion: same as Hermes — exit code 0, script's own pass line, no exceptions surfaced.**

### 12.2 Integration-level (CORE ↔ Hermes, and COMM ↔ Hermes)

**CORE ↔ Hermes:**
1. Confirm `GET /health` returns `healthy` from CORE's network path (not just from the Hermes host itself).
2. Confirm a real bearer token issued for CORE passes `GET /security/rbac/status`.
3. Run one real request per integration case in Section 7.2 (Cases 1-4) against a non-production Hermes environment, and confirm CORE correctly persists (or correctly declines to persist, per Section 7.3) the result.
4. Confirm a deliberately malformed request (e.g. missing required field) returns 422, not a 500 or a silent wrong answer.

**COMM ↔ Hermes:**
1. Confirm `GET /health` on COMM returns `healthy`.
2. Confirm `GET /providers/telegram/status` reports all three secrets configured (`true`/`true`/`true`) in the target environment.
3. Send a real Telegram message through a test bot/chat and confirm: (a) COMM's webhook returns 200, (b) the `hermes` field in COMM's response shows `status_code: 200`, (c) the Telegram user actually receives a reply.
4. **Regression test, explicitly required, not optional:** temporarily point `HERMES_BASE_URL` at an unreachable address (or block the route) and confirm the Telegram user receives the "could not process this message" reply, not silence — this is the specific behavior the 2026-08-21 fix guarantees, and it must be re-verified after any future change to `hermes_client.py` or the webhook handler in `main.py`.
5. Send a webhook request with a wrong/missing `X-Telegram-Bot-Api-Secret-Token` and confirm 403, not 200 (Section 11.4's regression-safe pattern — both positive and negative paths, every time).

**Success criteria:** all cases produce the expected CORE-side or user-facing outcome; no case silently succeeds with wrong data; the timeout-regression test (COMM step 4) and the auth-regression test (COMM step 5) both pass explicitly, not just "the happy path worked."

### 12.3 End-to-end (Frontend → CORE → Hermes → CORE → Frontend, and Telegram → COMM → Hermes → COMM → Telegram)

1. Resume upload → parse → suggestion → human approval → published resume reflects the approved change, not the raw suggestion.
2. Job posting → match → submission → tracker stage updates only when `stage_changed: true`.
3. (Once live) Inbound hotlist email → parsed → appears as a reviewable item somewhere in CORE's UI, not silently in Hermes only.
4. A real Telegram conversation with the bot → user receives a coherent, correctly-chunked reply (test with a message long enough to trigger the 3800-char chunking logic in `telegram_outbound.py`) → if the flow is meant to produce a CORE-visible record, confirm that record actually appears, per the caveat in Section 7.2 Case 5.

**Success criteria:** a non-technical reviewer using the Jobfynder UI (or a real Telegram conversation) can complete each flow without needing to inspect raw Hermes/COMM API responses.

### 12.4 Regression checklist before any Hermes or COMM deployment change

- [ ] All module verification scripts for changed modules pass (12.1), on whichever server changed.
- [ ] `GET /health` and `GET /prompts/health` (Hermes) both report healthy/configured.
- [ ] `GET /health` and `GET /providers/telegram/status` (COMM) both report healthy/configured.
- [ ] LiteLLM remains the only LLM gateway referenced anywhere in the diff (grep for any reference to a retired provider before merging).
- [ ] `.env` changes on either server verified with `--force-recreate`, not `restart`.
- [ ] If Hermes RBAC-related code changed, explicitly test both an authorized and an unauthorized call.
- [ ] If COMM's `hermes_client.py` or webhook handler changed, explicitly re-run the timeout-regression test (12.2, COMM step 4) — do not assume the 2026-08-21 fix is still in place just because it was once verified.
- [ ] If COMM's webhook secret verification changed, explicitly re-run both the positive- and negative-path auth tests (12.2, COMM step 5).

---

## 13. Glossary

| Term | Meaning |
|---|---|
| **Bearer token** | The `Authorization: Bearer <token>` credential used for all authenticated Hermes calls. |
| **Canonical envelope** | The standard Hermes response shape (`request_id`, `execution_mode`, `structured_data`, etc.) used by every capability built after 2026-08-15. |
| **Canonical intake shape** | COMM's normalized message format (Section 6.3) that every channel adapter must produce — currently only implemented for Telegram. |
| **COMM / COMM Gateway** | The FastAPI service on COMM-1 that receives inbound channel messages (Telegram today) and forwards them to Hermes over the HMAC-signed intake contract. |
| **COMM-1** | The communication-plane server (`152.42.219.165`). Not to be confused with any other historical use of that name — see the canonical documentation's terminology-reconciliation note if that comes up. |
| **Context Card** | A bounded, pre-parsed summary object (Candidate Card, Job Card, Relationship Card, Conversation Context) that stands in for raw text when calling a generative prompt — enforces "raw documents never reach the LLM." |
| **CORE** | Jobfynder's main NestJS backend — owns the production database, the only system with direct write access to business data. |
| **Deterministic-first** | The design principle that a rule-based/statistical approach is always attempted before falling back to an LLM. |
| **Draft object** | An object Hermes creates in its own storage (`/drafts/{id}`) representing a proposed record — not a live Jobfynder database row until CORE explicitly consumes and persists it. |
| **Dry-run** | A prompt or agent execution mode that renders/validates without actually calling an LLM or taking a real-world action — the default and, for agents, the only mode. |
| **HMAC intake contract** | The signed server-to-server scheme (`X-Jobfynder-Timestamp` + `X-Jobfynder-Signature`) used exclusively for COMM → Hermes calls to `/internal/comm/intake`. |
| **INTEL-1** | The intelligence-plane server (`jobfynder-intel-01`) that runs Hermes. |
| **Langfuse** | Hosts the live, versioned prompt registry and receives execution traces. |
| **LiteLLM** | The sole LLM gateway (`gateway.jobfynder.com`). The only path through which any Hermes call reaches a language model. |
| **RBAC** | Role-based access control — Hermes's permission-string-based authorization model. Not used by COMM. |
| **Router alias** | A named model reference (e.g. `generate-small`) that decouples a prompt from any specific provider/model — configured on LiteLLM, referenced by name in prompt definitions. |
| **HERMES-XXX** | The module/stream numbering scheme used to track Hermes's build history (e.g. HERMES-400 = Taxonomy). |
| **COMM-XXX** | The equivalent numbering scheme for COMM (e.g. COMM-410 = Telegram Channel Adapter). |

---

## 14. References

**Hermes:**
- `hermes/hermes-architecture-frozen-v1.md` — architectural decisions and reasoning behind the current Hermes design.
- `hermes/hermes-complete-developer-guide.md` — per-endpoint use-case guide.
- `hermes/hermes-capability-matrix.md` — current build status of every Hermes capability.
- `hermes/hermes-api-route-inventory.md` — the full Hermes route table.
- `hermes/HERMES-documentation-map.md` (archived — see `JOBFYNDER-HERMES-COMM-CANONICAL.md`) — historical module closure list.
- `hermes/HERMES-750-litellm-prompt-runtime-foundation.md` — the LiteLLM migration record and the Langfuse incident referenced in Section 11.3.
- `hermes/HERMES-850-email-parsing-foundation.md` — the email intake flow referenced in Section 7.2 Case 4 and 7.5.
- `hermes/HERMES-450-channel-intake.md` — the Hermes-side closure record for channel intake, including the internal COMM endpoint contract.
- `hermes/hermes-core-integration-guide.md` — the Hermes-only predecessor to this document; this document supersedes it for anyone integrating with both servers, but it remains a valid, more detailed Hermes-only reference.
- `GET /openapi.json` on the running Hermes service — the always-current, machine-readable API contract.

**COMM:**
- `comm/COMM-000-architecture-governance.md` — COMM governance and module index, including the COMM-1 naming correction.
- `comm/COMM-100-core-communication-platform.md` — the COMM Gateway service, deployment, configuration.
- `comm/COMM-410-telegram-channel-adapter.md` — the Telegram adapter in full detail.
- `comm/COMM-500-ingress-intake.md` — the full webhook-to-Hermes pipeline, including the 2026-08-21 resilience fix.
- `comm/COMM-300-900-1000-infrastructure-posture.md` — RabbitMQ/Redis status, reliability gaps and fixes, operations posture.
- `comm/COMM-documentation-map.md` — the COMM documentation index.

**Platform-wide:**
- `JOBFYNDER-HERMES-COMM-CANONICAL.md` — the document of truth for module-by-module production-readiness status across both servers; this document is the developer-facing integration companion to it, not a replacement.
