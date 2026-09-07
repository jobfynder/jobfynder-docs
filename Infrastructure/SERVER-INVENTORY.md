# Server Inventory

**Status:** Live SSH/API probe of all three providers, 2026-09-07 (Elest.io + DigitalOcean same day as an independent doc-sync pass that first flagged Hostinger; Hostinger itself confirmed by direct SSH shortly after). This is the source of truth for what servers exist, where, and how to reach them. Update this file the same day any server is added, removed, moved, or re-keyed — do not let it drift from reality.

**Important:** the platform spans at least **three** hosting providers (DigitalOcean, Hostinger, Elest.io) — `ADR-0004` (two-server architecture) predates this fuller picture; see the note added to that ADR.

---

## DigitalOcean — account `jobfynder.com@gmail.com`, project `first-project`, region `sgp1`

| Droplet | Role | Public IPv4 | Tailscale IP | SSH alias | Specs |
|---|---|---|---|---|---|
| `jobfynder-comm1` (COMM-1) | Communication plane — `jobfynder-comm-gateway` | 152.42.219.165 | 100.85.146.124 | `jobfynder-comm1` | 2 vCPU / 4 GB / 80 GB |
| `jobfynder-intel-01` (INTEL-1) | Hermes — runs `hermes-gateway.service`, admin + sourcing gateways, dashboard, cron scheduler. **Confirmed by founder 2026-09-07.** | 167.71.217.230 | 100.84.69.124 (`intel`) | `jobfynder-intel-01` | 4 vCPU / 8 GB / 160 GB |

**Important:** `jobfynder-intel-01` only accepts SSH via **Tailscale SSH** (tailnet-identity auth, not a key in `authorized_keys`) — it has no key-based access on its public IP. `jobfynder-comm1` has normal key-based SSH on its public IP. See `SSH-STANDARDS.md` for why and how each was set up. Both are on the `pavan@` tailnet.

## Hostinger — confirmed by founder 2026-09-07 as a real, core hosting provider

Both confirmed live via SSH 2026-09-07. Server-level SSH keys (per-VPS in hPanel, not account-wide — see `SSH-STANDARDS.md`).

| Server (hPanel hostname) | Role | Public IPv4 | SSH alias | Plan | Location |
|---|---|---|---|---|---|
| `srv1250194.hstgr.cloud` | **Jobfynder Core** — confirmed by live probe: runs nginx, PostgreSQL 16, PM2 (Node process manager), and Typesense (search) — matches `jobFynder-BE-nestJS`'s stack exactly (Prisma/Postgres, Typesense integration, an `integration-studio-migration-temp` folder in `/root` matching that repo's `integration-studio` module) | 72.62.194.11 | `jobfynder-core` | KVM 2 (2 vCPU / 8 GB / 100 GB) | Malaysia, Kuala Lumpur |
| `srv1237404.hstgr.cloud` | n8n automation — confirmed live: `n8n-n8n-1` + `n8n-traefik-1` Docker containers running (Hostinger's n8n app catalog install, "+100 workflows") | 72.62.78.39 | `jobfynder-n8n` | KVM 1 (1 vCPU / 4 GB / 50 GB) | Malaysia, Kuala Lumpur |

See `DISASTER-RECOVERY/Rebuild Hostinger Server.md` for rebuild steps.

## Elest.io — `dash.elest.io/16075/default-project`

The **only** project on the Elest.io account is `default-project`, containing exactly these 8 services (verified: no other projects, no restorable/deleted services). All on Netcup, Germany (Nuremberg), plan `MEDIUM-2C-4G` (2 vCPUs / 4 GB RAM / 58 GB disk on `/`) unless noted. Confirmed live via SSH 2026-09-07 — all 8 accessible, all healthy, all ~1 day 2h uptime at check time (suggests a synchronized platform-level restart, not a per-service issue).

Each box runs `elestio-nginx` (SSL-terminating reverse proxy) and `elestio-postfix` (outbound mail) in addition to the app containers listed below — omitted from the table as boilerplate.

| Service (dashboard name) | Public IPv4 | SSH alias | App containers (docker ps) | Notes |
|---|---|---|---|---|
| `ditto-jobfynder` | 159.195.122.150 | `ditto-jobfynder` | Dittofeed (`dashboard`), Temporal, Postgres 15, pgAdmin, ClickHouse | |
| `litellm-gateway` | 159.195.1.254 | `litellm-gateway` | LiteLLM, Postgres 17, pgAdmin, MinIO | AI/model routing gateway |
| `redis-ai-gateway` | 152.53.202.147 (public) / 10.30.71.5 (private) | `redis-ai-gateway` | Redis, RedisInsight | Caching only for LiteLLM — never durable storage, never Langfuse-accessible. Had pre-existing key `jonathan-support@elestio` (Elest.io support access) — left untouched |
| `langfuse-tnnaf` | 152.53.61.104 | `langfuse-tnnaf` | Langfuse web + worker, Postgres 16, pgAdmin, ClickHouse, MinIO, Redis 7 | LLM observability — fully self-contained stack (own Postgres/ClickHouse/Redis, not shared with `redis-ai-gateway`). Described elsewhere as "self-hosted on INTEL" — **not confirmed** whether that means this instance or a separate one on `jobfynder-intel-01`; don't assume |
| `centrifugo-rtms` | 159.195.1.43 | `centrifugo-rtms` | Centrifugo | Realtime messaging |
| `espocrm-wsnus` | 159.195.122.45 | `espocrm-wsnus` | EspoCRM (app + daemon + websocket), **Metabase**, MySQL 8 | Also runs Metabase (BI/analytics) — not on the dashboard's headline label. Had pre-existing keys `github-actions-benchteq-espocrm`, `my-laptop` — left untouched |
| `blog` | 159.195.122.74 | `blog` | Ghost, MySQL 8 | |
| `chatwoot-wnttb` | 159.195.1.202 | `chatwoot-wnttb` | Chatwoot rails + sidekiq (`ghcr.io/jobfynder/chatwoot:v4.16.2-jobfynder.1` — **custom Jobfynder fork**, not stock Chatwoot), Postgres 16 w/ pgvector, Redis | Support/chat. Note the custom fork image — check `jobfynder` org's `chatwoot` repo (cloned to `C:\Dev\Jobfynder\chatwoot`) before assuming upstream behavior |

Each service also has Elest.io's built-in per-service monitoring (uptime %, response time, CPU/disk/network metrics) under the **Monitoring** and **Metrics** tabs in the dashboard — check there before SSH-ing in for routine health checks.

## Hermes-specific directory structure (from a 2026-08-08 runtime sweep, `RUNTIME-SWEEP-2026-08-08.md`)
- Active Hermes profile root: `/root/.hermes-admin`
- Older/secondary: `/root/.hermes`
- Canonical, git-tracked engineering memory: `/root/vault/work/meta/engineering-memory.md`

## Not a separate server
`blog-automation` (local folder name) is **not** a distinct server or service — **confirmed by founder 2026-09-07: it refers to the `blog` Ghost service on Elest.io above.** No separate automation infrastructure exists for it.

## Not yet inventoried
Checked against Elest.io (confirmed only one project, `default-project`, exactly the 8 services above — no other projects, no restorable/deleted services) and DigitalOcean/Hostinger (confirmed exhaustive lists above). These remaining local project folders are most likely local tooling/scripts rather than separately hosted servers, but that's not yet confirmed — treat as open:
- `jobfynder-demo-tool`
- `jobfynder-mcp`
- `n8n workflows` (local folder — likely a local export/backup of workflows from the Hostinger `jobfynder-n8n` server above; not yet confirmed as the same instance)

## Unknown — needs someone with live access to fill in
- Whether Langfuse runs on `jobfynder-intel-01` or a separate Elest.io instance
- Whether there's a third Hostinger server beyond the two confirmed above
