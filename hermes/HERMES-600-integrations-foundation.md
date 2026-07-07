# HERMES-600 — Integrations Foundation

Status: Active  
Started from: HERMES-500 closed baseline  
Baseline code tag: `hermes-500-foundation-v1`  
Baseline code commit: `2d8c1ab`

---

## 1. Purpose

HERMES-600 builds the integration foundation for Hermes.

The goal is to make Hermes easy and safe for Jobfynder backend, n8n, and future ingestion channels to call.

---

## 2. Simple Definition

HERMES-600 answers this question:

> How does Jobfynder reliably send data into Hermes and receive clean, predictable results back?

---

## 3. Scope

HERMES-600 includes:

1. Integration request/response contract foundation
2. Internal integration client/service layer
3. Jobfynder API handoff readiness
4. n8n handoff readiness
5. Webhook/event payload foundation
6. Integration health checks
7. Retry/error contract foundation
8. API fixtures and verification scripts

---

## 4. Out of Scope

HERMES-600 does not include:

1. Full production authentication rollout
2. External SaaS integrations
3. Paid third-party connector implementation
4. Background job queue deployment
5. Full UI implementation
6. Database persistence redesign

---

## 5. Target Integrations

Initial integration targets:

1. Jobfynder backend API
2. n8n workflows
3. Email ingestion workflows
4. Telegram/WhatsApp ingestion workflows
5. Future webhook/event consumers

---

## 6. Design Principles

HERMES-600 should stay:

1. Simple
2. Deterministic
3. Easy to test
4. Easy for Jobfynder backend to call
5. Safe on failure
6. Clear in errors and retries

---

## 7. Initial Implementation Backlog

1. Inspect current API, routers, services, and config.
2. Create integration package.
3. Add integration models.
4. Add integration health/status endpoint.
5. Add integration event envelope contract.
6. Add n8n/jobfynder handoff examples.
7. Add retry/error response contract.
8. Add Docker verification.
9. Add live API verification.
10. Add official docs and closure verification.

---

## 8. Closure Criteria

HERMES-600 can close when:

1. Integration package exists.
2. Integration API contract exists.
3. Integration health endpoint works.
4. Event envelope contract exists.
5. Error/retry contract exists.
6. API fixtures exist.
7. Docker checks pass.
8. Live API checks pass.
9. Official docs are updated.
10. Final tag is created and pushed.

