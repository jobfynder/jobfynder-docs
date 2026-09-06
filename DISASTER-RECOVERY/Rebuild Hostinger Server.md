# Rebuild Hostinger Server

## Confirmed

**Hostinger is the platform's core server hosting provider** (confirmed by the founder, 2026-09-07). Two servers:

- **"core"** — very likely runs Jobfynder Core (`jobFynder-BE-nestJS` / `jobFynder-FE-vite`), not yet confirmed which or whether both live on the same server.
- **"n8n"** — runs n8n automation.

This means `ADR-0004`'s "two DigitalOcean servers" description undersells the platform's actual hosting footprint — see the note added to that ADR and to `Infrastructure/NETWORK-ARCHITECTURE.md`.

## Unknown — needs someone with live access to fill in

Actual IPs, rebuild steps, backup/snapshot policy for either server, and whether "core" hosts both backend and frontend or just one.
