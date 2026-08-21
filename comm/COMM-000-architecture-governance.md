# COMM-000 — Architecture & Governance

Status: Active
Owner: Jobfynder-Infra
Scope: COMM Platform (COMM-1)
Created: 2026-08-21
Corresponding intelligence-side doc: `hermes/HERMES-000-architecture-governance.md`

---

## 1. Purpose

COMM-000 defines the architecture and governance layer for COMM — the communication plane of Jobfynder, symmetric to how `HERMES-000` governs the intelligence plane.

**This is the first documentation COMM has ever had.** Every fact in this `comm/` folder was collected directly from the live COMM-1 server (`152.42.219.165`) and the `jobfynder/jobfynder-infra` repository on 2026-08-21 — not carried forward from an earlier doc, because none existed. See [JOBFYNDER-HERMES-COMM-CANONICAL.md](../JOBFYNDER-HERMES-COMM-CANONICAL.md) §2.3 and §5 for why this gap mattered and how it was closed.

## 2. COMM-1 — what it actually is

COMM-1 is the communication-plane server. IP `152.42.219.165`, hostname `jobfynder-comm1`, a DigitalOcean droplet (77G disk, 3.8G RAM). It owns provider-facing ingress, transport authentication (HMAC signing to Hermes), retries, attachments, and outbound communication — confirmed independently from both sides of the integration: `hermes/HERMES-450-channel-intake.md` on the Hermes side, and the `comm_gateway/hermes_client.py` source code on the COMM side, which implement the same HMAC-SHA256 contract.

**Naming note:** an earlier doc (`hermes/HERMES-000-architecture-governance.md` §7, before its 2026-08-21 correction) used "COMM-1" to mean an unrelated internal engineering-automation bot. That collision is resolved — COMM-1 means this server, full stop. See the canonical doc §2.1.

## 3. What runs on COMM-1

Everything is Docker Compose, no systemd services beyond the OS baseline (unlike INTEL-1, which runs Hermes's Telegram gateways as systemd services). Source: `/opt/jobfynder-infra/communication/docker-compose.yml`, a real git repo (`git@github-jobfynder-infra:jobfynder/jobfynder-infra.git`).

| Container | Image | Purpose | Live status (2026-08-21) |
|---|---|---|---|
| `jobfynder-comm-gateway` | built from `Dockerfile.comm-gateway` (FastAPI, Python) | The COMM application itself | Up 4 weeks, healthy |
| `jobfynder-npm` | `jc21/nginx-proxy-manager:latest` | Public TLS termination and reverse proxy | Up 6 weeks |
| `jobfynder-rabbitmq` | `rabbitmq:3-management` | Provisioned for async messaging | Up 6 weeks — **0 queues, default vhost only, not wired into any code path** |
| `jobfynder-redis` | `redis:7` | Provisioned for caching/session state | Up 6 weeks — **0 keys, not wired into any code path** |
| `portainer` | `portainer/portainer-ce:lts` | Docker management UI | Up 6 weeks |

## 4. COMM Streams (module index)

Mirrors the numbering in the canonical doc §1. Status per stream is graded in the canonical doc's Part B COMM matrix, not repeated here.

- **COMM-100** — Core Communication Platform (this doc + `COMM-100-core-communication-platform.md`)
- **COMM-200** — Identity & Session Layer — no dedicated implementation found; Telegram sender identity is passed through unmapped (see `COMM-410`)
- **COMM-300** — Messaging & Event Transport — RabbitMQ is running but unused; see `COMM-300-900-1000-infrastructure-posture.md`
- **COMM-400** — Channel Adapters — Telegram only; see `COMM-410-telegram-channel-adapter.md`
- **COMM-500** — Ingress & Intake — the webhook → normalize → HMAC-sign → forward-to-Hermes pipeline; see `COMM-500-ingress-intake.md`
- **COMM-600** — External Communication Integrations — no evidence beyond Telegram
- **COMM-700** — Realtime Communication — a Centrifugo instance exists platform-wide (`centrifugo.jobfynder.com`, confirmed from the Hermes side) but nothing on COMM-1 calls or manages it
- **COMM-800** — Communication Workflows — no dedicated implementation found beyond the Telegram outbound delivery logic in `COMM-410`
- **COMM-900** — Reliability & Governance — Redis provisioned unused; `fail2ban` guards SSH only, not HTTP; see `COMM-300-900-1000-infrastructure-posture.md`
- **COMM-1000** — Production Operations — see `COMM-300-900-1000-infrastructure-posture.md`

## 5. Governance rule (same as HERMES-000 §8)

Before adding a new COMM capability, confirm: which COMM stream it belongs to, what evidence will prove it's done (a live endpoint, a passing check, a git tag — never a chat message), where documentation will live (`jobfynder/jobfynder-docs` `comm/`, same rule as Hermes), and how it gets recorded here or in the canonical doc.
