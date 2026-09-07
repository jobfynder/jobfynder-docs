# Server Inventory

**Status:** Merged from two independent same-day passes (2026-09-07): a live SSH/API probe of Elest.io + DigitalOcean, and a doc-sync pass that captured founder-confirmed facts about Hostinger. This is the source of truth for what servers exist, where, and how to reach them. Update this file the same day any server is added, removed, moved, or re-keyed — do not let it drift from reality.

**Important:** the platform spans at least **three** hosting providers (DigitalOcean, Hostinger, Elest.io) — `ADR-0004` (two-server architecture) predates this fuller picture; see the note added to that ADR.

---

## DigitalOcean — account `jobfynder.com@gmail.com`, project `first-project`, region `sgp1`

| Droplet | Role | Public IPv4 | Tailscale IP | SSH alias | Specs |
|---|---|---|---|---|---|
| `jobfynder-comm1` (COMM-1) | Communication plane — `jobfynder-comm-gateway` | 152.42.219.165 | 100.85.146.124 | `jobfynder-comm1` | 2 vCPU / 4 GB / 80 GB |
| `jobfynder-intel-01` (INTEL-1) | Hermes — runs `hermes-gateway.service`, admin + sourcing gateways, dashboard, cron scheduler. **Confirmed by founder 2026-09-07.** | 167.71.217.230 | 100.84.69.124 (`intel`) | `jobfynder-intel-01` | 4 vCPU / 8 GB / 160 GB |

**Important:** `jobfynder-intel-01` only accepts SSH via **Tailscale SSH** (tailnet-identity auth, not a key in `authorized_keys`) — it has no key-based access on its public IP. `jobfynder-comm1` has normal key-based SSH on its public IP. See `SSH-STANDARDS.md` for why and how each was set up. Both are on the `pavan@` tailnet.

## Hostinger — **confirmed by founder 2026-09-07 as a real, core hosting provider**

| Server | IP | Role |
|---|---|---|
| "core" server | Unknown — not yet probed | Very likely runs Jobfynder Core (`jobFynder-BE-nestJS` / `jobFynder-FE-vite`) — not confirmed which |
| "n8n" server | Unknown — not yet probed | Runs n8n automation |

SSH access to either has not been set up or documented yet. See `DISASTER-RECOVERY/Rebuild Hostinger Server.md`.

## Elest.io — `dash.elest.io/16075/default-project`

All on Netcup, Germany (Nuremberg), plan `MEDIUM-2C-4G` (2 vCPUs / 4 GB RAM / 60 GB disk) unless noted. Confirmed live via SSH 2026-09-07 (all 8 accessible, all healthy).

| Service (dashboard name) | Software | Public IPv4 | SSH alias | Notes |
|---|---|---|---|---|
| `ditto-jobfynder` | Dittofeed | 159.195.122.150 | `ditto-jobfynder` | |
| `litellm-gateway` | LiteLLM | 159.195.1.254 | `litellm-gateway` | AI/model routing gateway |
| `redis-ai-gateway` | Redis | 152.53.202.147 (public) / 10.30.71.5 (private) | `redis-ai-gateway` | Caching only for LiteLLM — never durable storage, never Langfuse-accessible. Had pre-existing key `jonathan-support@elestio` (Elest.io support access) — left untouched |
| `langfuse-tnnaf` | Langfuse | 152.53.61.104 | `langfuse-tnnaf` | LLM observability. Described elsewhere as "self-hosted on INTEL" — **not confirmed** whether that means this Elest.io instance or a separate one on `jobfynder-intel-01`; don't assume |
| `centrifugo-rtms` | Centrifugo | 159.195.1.43 | `centrifugo-rtms` | Realtime messaging |
| `espocrm-wsnus` | EspoCRM | 159.195.122.45 | `espocrm-wsnus` | Had pre-existing keys `github-actions-benchteq-espocrm`, `my-laptop` — left untouched |
| `blog` | Ghost | 159.195.122.74 | `blog` | |
| `chatwoot-wnttb` | Chatwoot | 159.195.1.202 | `chatwoot-wnttb` | Support/chat |

Each service also has Elest.io's built-in per-service monitoring (uptime %, response time, CPU/disk/network metrics) under the **Monitoring** and **Metrics** tabs in the dashboard — check there before SSH-ing in for routine health checks.

## Hermes-specific directory structure (from a 2026-08-08 runtime sweep, `RUNTIME-SWEEP-2026-08-08.md`)
- Active Hermes profile root: `/root/.hermes-admin`
- Older/secondary: `/root/.hermes`
- Canonical, git-tracked engineering memory: `/root/vault/work/meta/engineering-memory.md`

## Not yet inventoried
These local project folders are **not** documented here because their hosting/repo location wasn't confirmed as of 2026-09-07 — do not assume they don't exist, just that this file has no verified entry for them yet:
- `blog-automation`
- `jobfynder-demo-tool`
- `jobfynder-mcp`
- `n8n workflows` (local folder — likely relates to the Hostinger n8n server above, not yet confirmed as the same thing)

## Unknown — needs someone with live access to fill in
- Whether Langfuse runs on `jobfynder-intel-01` or a separate Elest.io instance
- The actual IPs of the two Hostinger servers, and SSH access to them
- Which of "core" vs "n8n" (or a third Hostinger server) actually hosts the production backend/frontend
