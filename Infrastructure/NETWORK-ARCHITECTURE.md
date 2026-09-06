# Network Architecture

## The two-server split

Per `ADR-0002` (Two-Server Architecture):

- **COMM-1** — `152.42.219.165` — runs the `jobfynder-comm-gateway` Docker container. Provider-facing ingress, HMAC-signed calls to Hermes, retries, attachments, outbound communication. Port 8080 is **not** exposed directly (fixed in commit `33b6ec4`).
- **INTEL-1** — `167.71.217.230` (DigitalOcean) — runs `hermes-gateway.service`, `hermes-admin-gateway`, `hermes-sourcing-gateway`, `hermes-dashboard`, and the cron scheduler. **Confirmed by the founder 2026-09-07** (previously only inferred as probable).

## AI infrastructure (Elestio, separate VMs from the two servers above)

- **LiteLLM Gateway** — `litellm-gateway-u14612.vm.elestio.app`, public `https://gateway.jobfynder.com` (Cloudflare-proxied), IP `159.195.1.254`. Routes model aliases (`jf-fast`, `jf-structured`, `jf-reasoning`, `jf-writing`, `jf-embedding`) to underlying providers.
- **Redis for LiteLLM caching** — `redis-ai-gateway-u14612.vm.elestio.app`, public `152.53.202.147`, private `10.30.71.5`, port `26379`. **This is strictly a cache — never a durable store, and never accessible to Langfuse.**
- **Langfuse** — self-hosted, `https://langfuse.jobfynder.com`, v4.1.0. Has its **own separate internal Redis** at `172.17.0.1:6379` for its own event queue — do not confuse this with the LiteLLM cache Redis above; they are two different instances on two different ports and must never be pointed at each other.
- **DeepInfra** — embedding provider (`deepinfra/BAAI/bge-m3`), accessed via API key, separate from the DeepInfra website login credentials.

## Self-hosted stack (Elestio, broader platform)

PostgreSQL (source of truth), Centrifugo (real-time transport), n8n (automation), Resend (email), Dittofeed (notification orchestration).

## Message backbone

RabbitMQ handles durable background tasks and the COMM intake pipeline (see `ADR-0005`). Redis is never used for durable events anywhere on this platform — see the LiteLLM/Langfuse Redis separation above for why that distinction is enforced strictly.

## Public domains

- `testing.jobfynder.com` — test environment
- `feedback.jobfynder.com` — feedback board
- `gateway.jobfynder.com` — LiteLLM Gateway (Cloudflare-proxied)
- `langfuse.jobfynder.com` — Langfuse
- `redisgateway.jobfynder.com` — **known issue:** currently resolves to Cloudflare anycast, not the actual Elestio Redis VM. Open item; fix if this friendly name is actually needed anywhere.

## Hosting providers, plural

The platform spans **three** hosting providers, not the two DigitalOcean servers `ADR-0004` describes:

- **DigitalOcean** — COMM-1 and INTEL-1 (above).
- **Hostinger** — confirmed by the founder 2026-09-07 as the platform's core server hosting provider. Two servers: **"core"** (very likely runs Jobfynder Core — `jobFynder-BE-nestJS` / `jobFynder-FE-vite` — not yet confirmed which) and **"n8n"** (runs n8n automation — note this means n8n may run on Hostinger, not Elestio as listed above; not yet reconciled). Actual IPs not yet documented anywhere in this repo.
- **Elestio** — LiteLLM Gateway, Redis cache, Langfuse, and the broader self-hosted stack.

## Deployment stage

Stage 1 (MVP) per `ADR-0004`: Docker Compose, manual deployments. `ADR-0004`'s "two DigitalOcean servers" description is now known to be incomplete — see the note added to that ADR.

## What's not documented here yet

Full server inventory beyond what's listed above, and actual DNS/registrar details beyond the one known DNS issue.
