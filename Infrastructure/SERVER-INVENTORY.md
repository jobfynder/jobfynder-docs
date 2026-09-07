# Server Inventory

**Status:** Verified by live probe (SSH/API) on 2026-09-07. This is the source of truth for what servers exist, where, and how to reach them. Update this file the same day any server is added, removed, moved, or re-keyed — do not let it drift from reality.

---

## Elest.io — `dash.elest.io/16075/default-project`

All on Netcup, Germany (Nuremberg), plan `MEDIUM-2C-4G` (2 vCPUs / 4 GB RAM / 60 GB disk) unless noted.

| Service (dashboard name) | Software | Public IPv4 | SSH alias | Notes |
|---|---|---|---|---|
| `ditto-jobfynder` | Dittofeed | 159.195.122.150 | `ditto-jobfynder` | |
| `litellm-gateway` | LiteLLM | 159.195.1.254 | `litellm-gateway` | AI gateway |
| `redis-ai-gateway` | Redis | 152.53.202.147 | `redis-ai-gateway` | Had pre-existing key `jonathan-support@elestio` (Elest.io support access) — left untouched |
| `langfuse-tnnaf` | Langfuse | 152.53.61.104 | `langfuse-tnnaf` | LLM observability |
| `centrifugo-rtms` | Centrifugo | 159.195.1.43 | `centrifugo-rtms` | Realtime messaging |
| `espocrm-wsnus` | EspoCRM | 159.195.122.45 | `espocrm-wsnus` | Had pre-existing keys `github-actions-benchteq-espocrm`, `my-laptop` — left untouched |
| `blog` | Ghost | 159.195.122.74 | `blog` | |
| `chatwoot-wnttb` | Chatwoot | 159.195.1.202 | `chatwoot-wnttb` | Support/chat |

Each service also has Elest.io's built-in per-service monitoring (uptime %, response time, CPU/disk/network metrics) under the **Monitoring** and **Metrics** tabs in the dashboard — check there before SSH-ing in for routine health checks.

## DigitalOcean — account `jobfynder.com@gmail.com`, project `first-project`, region `sgp1`

| Droplet | Role | Public IPv4 | Tailscale IP | SSH alias | Specs |
|---|---|---|---|---|---|
| `jobfynder-comm1` | COMM-1 — Communication Gateway | 152.42.219.165 | 100.85.146.124 | `jobfynder-comm1` | 2 vCPU / 4 GB / 80 GB |
| `jobfynder-intel-01` | INTEL-1 — Hermes | 167.71.217.230 | 100.84.69.124 (`intel`) | `jobfynder-intel-01` | 4 vCPU / 8 GB / 160 GB |

**Important:** `jobfynder-intel-01` only accepts SSH via **Tailscale SSH** (tailnet-identity auth, not a key in `authorized_keys`) — it has no key-based access on its public IP. `jobfynder-comm1` has normal key-based SSH on its public IP. See `SSH-STANDARDS.md` for why and how each was set up.

Both droplets are on the `pavan@` tailnet, reachable from any device already joined to it.

## Not yet inventoried

These local project folders are **not** documented here because their hosting/repo location wasn't confirmed as of 2026-09-07 — do not assume they don't exist, just that this file has no verified entry for them yet:
- `blog-automation`
- `jobfynder-demo-tool`
- `jobfynder-mcp`
- `n8n workflows`

Also referenced elsewhere in this repo (`DISASTER-RECOVERY/Rebuild Hostinger Server.md`) but not yet inventoried here: **Hostinger** servers. Add them here once confirmed.
