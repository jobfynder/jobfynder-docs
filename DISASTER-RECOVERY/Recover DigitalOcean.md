# Recover DigitalOcean

## Confirmed (live probe via `doctl`, 2026-09-07)

Two droplets, account `jobfynder.com@gmail.com`, project `first-project`, region `sgp1`:
- **`jobfynder-comm1`** (152.42.219.165) — COMM-1. Confirmed running: `jobfynder-comm-gateway`, `jobfynder-comm-worker`, RabbitMQ (management), Redis 7, Nginx Proxy Manager, Portainer.
- **`jobfynder-intel-01`** (167.71.217.230) — INTEL-1/Hermes. **Confirmed by founder 2026-09-07**, not just probable. Confirmed running: `hermes-api`, `hermes-graph-consumer`, Postgres 16, Typesense, Nginx Proxy Manager, Portainer + agent.

SSH: `ssh jobfynder-comm1` (key-based) / `ssh jobfynder-intel-01` (Tailscale SSH only — see `Infrastructure/SSH-STANDARDS.md`).

## Snapshots — yes, taken, but manually and irregularly

`doctl compute snapshot list --resource droplet` shows 13 snapshots across both droplets, spanning 2026-06-30 to 2026-09-01, mostly named after Hermes milestones (`HERMES-200` through `HERMES-700`, `jobfynder-intel-01-HERMES-CORE`) plus two `COMM1`/`INTEL1-GOLDEN-BASELINE` snapshots from the same day. These are **manual milestone snapshots, not an automated schedule** — no evidence of a recurring backup policy. Restore via DigitalOcean dashboard/API: create a new droplet from snapshot, or restore in place (destroys current disk state — confirm before running).

## Unknown — needs someone with live access to fill in
Actual tested restore-from-snapshot steps (untested as of this pass) and target recovery time.
