# Network Architecture

## The two-server split

Per `ADR-0002` (Two-Server Architecture):

- **COMM-1** — `152.42.219.165` — runs the `jobfynder-comm-gateway` Docker container. Provider-facing ingress, HMAC-signed calls to Hermes, retries, attachments, outbound communication. Port 8080 is **not** exposed directly (fixed in commit `33b6ec4`).
- **Hermes admin/sourcing gateway server** — `167.71.217.230` — runs `hermes-gateway.service`, `hermes-admin-gateway`, `hermes-sourcing-gateway`, `hermes-dashboard`, and the cron scheduler. This is very likely what `ADR-0002` calls INTEL-1, though nothing in this repo states that label-to-IP mapping explicitly — treat the mapping as probable, not confirmed.

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

## Deployment stage

Stage 1 (MVP) per `ADR-0004`: Docker Compose across two DigitalOcean servers, manual deployments.

## What's not documented here yet

Full server inventory beyond what's listed above, and actual DNS/registrar details beyond the one known DNS issue.
