# Server Inventory

## Confirmed

| Server | IP | Role | Hosting |
|---|---|---|---|
| COMM-1 | `152.42.219.165` | Communication plane — `jobfynder-comm-gateway` | DigitalOcean |
| Hermes admin/sourcing gateway server | `167.71.217.230` | Runs `hermes-gateway.service`, admin + sourcing gateways, dashboard, cron scheduler. Very likely `ADR-0002`'s INTEL-1, but that exact label-to-IP mapping isn't stated anywhere in this repo | DigitalOcean |
| LiteLLM Gateway | `159.195.1.254` (public), `litellm-gateway-u14612.vm.elestio.app` | Model routing | Elestio |
| Redis (LiteLLM cache only) | `152.53.202.147` (public) / `10.30.71.5` (private) | Caching only — never durable storage, never Langfuse-accessible | Elestio |

Langfuse is described elsewhere as "self-hosted on INTEL" — if that means the same server as the Hermes admin/sourcing gateway above, it isn't stated explicitly; it may be a separate Elestio instance. Don't assume either way without checking.

## Hermes-specific directory structure (from a 2026-08-08 runtime sweep, `Infrastructure/RUNTIME-SWEEP-2026-08-08.md`)

- Active Hermes profile root: `/root/.hermes-admin`
- Older/secondary: `/root/.hermes`
- Canonical, git-tracked engineering memory: `/root/vault/work/meta/engineering-memory.md`

## Unknown — needs someone with live access to fill in

- Whether Langfuse runs on the Hermes admin server or a separate instance
- Any server beyond the four above, if one exists
- Which of the two DigitalOcean servers `ADR-0004` refers to as Stage 1 actually corresponds to which IP above
