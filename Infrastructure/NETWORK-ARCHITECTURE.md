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

Full list, confirmed via live `docker ps` 2026-09-07 (see `Infrastructure/SERVER-INVENTORY.md` for per-service container detail — the previous version of this list was incomplete):
- PostgreSQL (source of truth, run per-service — Dittofeed, LiteLLM, and Langfuse each have their own instance, not shared)
- Centrifugo (real-time transport)
- Dittofeed (notification orchestration, with its own Temporal + ClickHouse)
- EspoCRM (also runs Metabase for BI/analytics on the same box — not previously documented)
- Ghost (blog — this is the entirety of what "blog-automation" as a local folder name refers to; there is no separate automation server, just the Ghost service itself)
- Chatwoot (support/chat — runs a **custom Jobfynder fork**, `ghcr.io/jobfynder/chatwoot:v4.16.2-jobfynder.1`, not stock Chatwoot)
- Resend (email — application-level transactional email API; separate from the `elestio-postfix` container every Elest.io box also runs for system-level outbound mail)

(n8n runs on Hostinger, not here — see below.)

## Message backbone

RabbitMQ handles durable background tasks and the COMM intake pipeline (see `ADR-0005`). Redis is never used for durable events anywhere on this platform — see the LiteLLM/Langfuse Redis separation above for why that distinction is enforced strictly.

## Public domains

- `testing.jobfynder.com` — test environment
- `uat.jobfynder.com` — **confirmed 2026-09-07**, proxies to `jobfynder-core` (Hostinger, `72.62.194.11:3000`) via nginx + Certbot. This is `jobFynder-BE-nestJS`'s UAT deployment specifically.
- `feedback.jobfynder.com` — feedback board
- `gateway.jobfynder.com` — LiteLLM Gateway (Cloudflare-proxied)
- `langfuse.jobfynder.com` — Langfuse
- `redisgateway.jobfynder.com` — **known issue, re-confirmed still broken via `nslookup` 2026-09-07:** resolves to the same Cloudflare anycast range as the domains above, not the actual Elestio Redis VM. This has now failed two separate verification passes — worth actually fixing, not just re-noting.

`jobfynder-core` is confirmed by the founder (2026-09-07) to be a testing/UAT server, not production — `jobfynder.com`/`www.jobfynder.com` return `HTTP 200` behind Cloudflare with the real origin fully masked (no Cloudflare dashboard/API access during this pass to trace further); this is expected for the current stage rather than a discovered gap.

## Hosting providers, plural

The platform spans **three** hosting providers, not the two DigitalOcean servers `ADR-0004` describes:

- **DigitalOcean** — COMM-1 and INTEL-1 (above).
- **Hostinger** — confirmed by the founder 2026-09-07 as the platform's core server hosting provider. Two servers, both confirmed live via SSH: **`jobfynder-core`** (`srv1250194.hstgr.cloud`, `72.62.194.11`) — confirmed running `jobFynder-BE-nestJS` only (PM2 + nginx proxying `uat.jobfynder.com`, no frontend deployed there). **Confirmed by founder: this is a testing/UAT server.** And **`jobfynder-n8n`** (`srv1237404.hstgr.cloud`, `72.62.78.39`) — confirmed running n8n via Docker.
- **Elestio** — LiteLLM Gateway, Redis cache, Langfuse, and the broader self-hosted stack.

## Deployment stage

Stage 1 (MVP) per `ADR-0004`: Docker Compose, manual deployments. `ADR-0004`'s "two DigitalOcean servers" description is now known to be incomplete — see the note added to that ADR.

## What's not documented here yet

Full server inventory beyond what's listed above, and actual DNS/registrar details beyond the one known DNS issue.
