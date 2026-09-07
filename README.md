# jobfynder-docs
Engineering Operating System, Architecture, Standards, ADRs and Documentation for the Jobfynder Platform.

## Start here

**[JOBFYNDER-HERMES-COMM-CANONICAL.md](./JOBFYNDER-HERMES-COMM-CANONICAL.md)** is the document of truth for the entire HERMES + COMM platform — canonical module index, current status for every module (graded against real evidence, not historical claims), and the priority list for what's actually open. Read this before any other Hermes or COMM doc in this repo.

**[HERMES-COMM-CORE-INTEGRATION-GUIDE.md](./HERMES-COMM-CORE-INTEGRATION-GUIDE.md)** is the developer-facing integration guide — auth flows, endpoints, sample requests/responses, error codes, troubleshooting, and a testing plan for integrating Jobfynder CORE (backend and frontend) with both Hermes (INTEL-1) and the COMM Gateway (COMM-1). Use this when you're actually writing integration code; use the canonical doc above when you need to know what's production-ready.

**Looking for the Hermes API docs specifically?** → **[hermes/hermes-complete-developer-guide.md](./hermes/hermes-complete-developer-guide.md)** (per-endpoint reference, 99 endpoints) and **[hermes/hermes-parsing-and-prompts-api-guide.md](./hermes/hermes-parsing-and-prompts-api-guide.md)** (the 38-prompt catalog). Both live inside `hermes/` alongside the module-by-module build history (`HERMES-000` through `HERMES-850`) — see `hermes/hermes-architecture-frozen-v1.md` for the reasoning behind how the API is shaped.

## Folder map

- **`hermes/`** — the intelligence plane (INTEL-1). API docs, architecture, module build history.
- **`comm/`** — the communication plane (COMM-1). See `comm/COMM-documentation-map.md`.
- **`core/`** — Jobfynder Core (backend + frontend) product/engineering specs — dashboards, profiles, settings.
- **`Architecture/`** — durable platform-wide structural decisions (not day-to-day implementation detail).
- **`Infrastructure/`** — server inventory, SSH access, network architecture — the source of truth for what's actually deployed and how to reach it.
- **`DISASTER-RECOVERY/`** — per-component recovery runbooks.
- **`FOUNDATION/`** — engineering philosophy, ADRs, engineering memory.
- **`FOUNDER-OS/`** — the founder's daily/weekly operating rhythm and focus framework.
