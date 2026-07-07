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


---

## Step 004 — Integrations Core and API Foundation

Status: Passed

Code branch:

`feature/hermes-600-integrations`

Code commits:

- `a15a665 feat(hermes-600): add integrations core foundation`
- `ab2fb2e feat(hermes-600): expose integrations API router`
- `90e9567 test(hermes-600): make integrations API check docker-aware`

Files added:

- `/opt/hermes/app/integrations/__init__.py`
- `/opt/hermes/app/integrations/models.py`
- `/opt/hermes/app/integrations/service.py`
- `/opt/hermes/app/routers/integrations.py`
- `/opt/hermes/scripts/hermes-600-integrations-core-check.py`
- `/opt/hermes/scripts/hermes-600-integrations-api-check.py`

Files updated:

- `/opt/hermes/app/main.py`

API routes added:

- `GET /integrations/health`
- `POST /integrations/events/normalize`

Foundation contracts added:

- `IntegrationProvider`
- `IntegrationEventType`
- `IntegrationSource`
- `IntegrationEnvelope`
- `IntegrationNormalizedEvent`
- `IntegrationHealthResponse`

Supported providers:

- `jobfynder_api`
- `n8n`
- `webhook`
- `email`
- `telegram`
- `whatsapp`
- `slack`
- `unknown`

Supported event types:

- `document_received`
- `job_received`
- `resume_received`
- `match_requested`
- `submission_event`
- `workflow_handoff`
- `notification_requested`
- `unknown`

Verification completed:

- Docker build passed
- Python compile passed
- Integrations core check passed
- Live host API check passed
- Docker service URL API check passed
- OpenAPI route validation passed

Notes:

The integrations API check was updated to support `HERMES_API_BASE_URL` so the same verification script works from both the host and Docker network context.

---

## Step 006 — Jobfynder Submission Handoff Integration

Status: Passed

Code branch:

`feature/hermes-600-integrations`

Code commits:

- `7d26acf feat(hermes-600): add Jobfynder submission handoff adapter`
- `7ba2584 feat(hermes-600): expose Jobfynder submission handoff API`

Files added:

- `/opt/hermes/app/integrations/jobfynder.py`
- `/opt/hermes/scripts/hermes-600-jobfynder-adapter-check.py`
- `/opt/hermes/scripts/hermes-600-jobfynder-api-check.py`

Files updated:

- `/opt/hermes/app/integrations/models.py`
- `/opt/hermes/app/routers/integrations.py`

API route added:

- `POST /integrations/jobfynder/submission-handoff/evaluate`

Purpose:

This endpoint accepts a Jobfynder integration envelope and produces two outputs:

1. A normalized Hermes integration event
2. A HERMES-500 submission intelligence evaluation

The adapter converts Jobfynder payloads into `SubmissionIntelligenceRequest` so Jobfynder can call Hermes using an integration-safe handoff contract.

Supported handoff behavior:

- Accept Jobfynder workflow handoff events
- Convert requirement snapshot
- Convert consultant snapshot
- Convert recruiter/vendor/employer relationship snapshot
- Convert event snapshot
- Pass match result into submission intelligence
- Pass taxonomy context into submission intelligence
- Detect duplicate submission risk through existing submission keys
- Return recommended submission workflow stage
- Return correlation ID for traceability

Verification completed:

- Python syntax check passed
- Docker build passed
- Docker compile passed
- Integrations core check passed
- Jobfynder adapter check passed
- Host live API check passed
- Docker service URL API check passed
- OpenAPI route validation passed

Notes:

The long Step 006-B command was split into smaller safe steps after the console disconnected. Final verification passed before committing the endpoint.
