# Rebuild Hostinger Server

## Confirmed (live SSH probe, 2026-09-07)

Two Hostinger VPS (hPanel), both Ubuntu 24.04, Malaysia/Kuala Lumpur:

- **`srv1250194.hstgr.cloud`** (72.62.194.11, KVM 2, 2 vCPU/8GB/100GB) — runs nginx, PostgreSQL 16, PM2, Typesense. PM2 runs exactly one process: `node /var/www/jobFynder-BE-nestJS/dist/main.js`. Nginx proxies `uat.jobfynder.com` (SSL via Certbot/Let's Encrypt) to it on port 3000. **`/var/www/` contains only `jobFynder-BE-nestJS` — no frontend deployed on this box. Confirmed by founder 2026-09-07: this server is for testing/UAT.**
- **`srv1237404.hstgr.cloud`** (72.62.78.39, KVM 1, 1 vCPU/4GB/50GB) — runs n8n via Docker (`n8n-n8n-1` + `n8n-traefik-1`), Hostinger's app-catalog n8n install ("+100 workflows").

SSH: `ssh jobfynder-core` / `ssh jobfynder-n8n` (see `Infrastructure/SSH-STANDARDS.md` for the per-VPS key-add procedure — hPanel → VPS → SSH key → Manage).

Rebuild path if either VPS is lost: Hostinger hPanel → VPS → **Manage → Snapshot & backups** (both boxes show 2 snapshots each in hPanel as of 2026-09-07, weekly backup schedule) → restore from snapshot, or provision a fresh KVM instance and redeploy from the `jobFynder-BE-nestJS`/`n8n` config respectively. Exact restore-from-snapshot steps not yet tested.


This means `ADR-0004`'s "two DigitalOcean servers" description undersells the platform's actual hosting footprint — see the note added to that ADR and to `Infrastructure/NETWORK-ARCHITECTURE.md`.
