# Server Inventory

**This is partial.** Only what's independently confirmed is listed as fact — everything else is marked unknown rather than guessed.

## Confirmed

| Server | IP | Role | Hosting |
|---|---|---|---|
| COMM-1 | `152.42.219.165` | Communication plane — `jobfynder-comm-gateway` container, provider-facing ingress | DigitalOcean (Stage 1) |
| INTEL-1 | Unknown | Hermes Core — intelligence plane | DigitalOcean (Stage 1) |

Stage 1 deployment (`ADR-0004`) confirms exactly two DigitalOcean servers exist — COMM-1 and INTEL-1 are presumably those two, but INTEL-1's actual IP is not recorded anywhere in this repo.

## Hermes-specific directory structure (from a 2026-08-08 runtime sweep, `Infrastructure/RUNTIME-SWEEP-2026-08-08.md`)

- Active Hermes profile root: `/root/.hermes-admin` (config, status, `hermes doctor` all read from here)
- Older/secondary: `/root/.hermes` — still has `.env`, `SOUL.md`, an older memory copy
- Canonical, git-tracked engineering memory: `/root/vault/work/meta/engineering-memory.md`
- Running services confirmed on this server: `hermes-gateway.service`, `hermes-admin-gateway`, `hermes-sourcing-gateway`, `hermes-dashboard`, cron scheduler

## Unknown — needs someone with live access to fill in

- INTEL-1's actual IP/hostname
- Elestio-hosted service inventory (which services run on which Elestio instance)
- Any server beyond these two, if one exists
