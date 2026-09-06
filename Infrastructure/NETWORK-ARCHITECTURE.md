# Network Architecture

## The two-server split

Per `ADR-0002` (Two-Server Architecture):

- **COMM-1** — `152.42.219.165` — runs the `jobfynder-comm-gateway` Docker container. Owns provider-facing ingress, transport authentication (HMAC-signed calls to Hermes), retries, attachments, outbound communication. Port 8080 is **not** exposed directly (fixed in commit `33b6ec4`, see `CHANGELOG.md`).
- **INTEL-1** — runs Hermes Core: understanding, matching, taxonomy, workflow intelligence. Not directly internet-facing.

## Self-hosted stack (Elestio)

PostgreSQL (source of truth), Centrifugo (real-time transport), n8n (automation), LiteLLM (model routing), Langfuse (AI observability), Resend (email), Dittofeed (notification orchestration).

## Message backbone

RabbitMQ handles durable background tasks and the COMM intake pipeline (queueing, exponential-backoff retry, dead-letter, idempotency — see `ADR-0005`). Redis handles presence and short-lived state, not durable events.

## Public domains

- `testing.jobfynder.com` — test environment
- `feedback.jobfynder.com` — feedback board (ProductLift)

## Deployment stage

Currently Stage 1 (MVP) per `ADR-0004`: Docker Compose across two DigitalOcean servers, manual deployments. Stage 2 (GitHub Actions, container registry, automated deployments) and Stage 3 (multiple nodes, managed databases, high availability) are not yet reached — don't build for them ahead of actual need.

## What's not documented here yet

Full server inventory beyond COMM-1's IP, actual firewall rule set beyond the specific fixes in `CHANGELOG.md`, and DNS/domain registrar details. See `SERVER-INVENTORY.md` and `FIREWALL-POLICY.md` for what's confirmed there.
