# Server Inventory

## Confirmed

| Server | IP | Role | Hosting |
|---|---|---|---|
| COMM-1 | `152.42.219.165` | Communication plane — `jobfynder-comm-gateway` | DigitalOcean |
| INTEL-1 | `167.71.217.230` | Hermes — runs `hermes-gateway.service`, admin + sourcing gateways, dashboard, cron scheduler. **Confirmed by founder 2026-09-07** (previously only inferred as likely). | DigitalOcean |
| Hostinger — "core" server | Unknown | **Confirmed by founder 2026-09-07: Hostinger is the platform's core server hosting provider.** This server very likely runs Jobfynder Core (`jobFynder-BE-nestJS` / `jobFynder-FE-vite`) — not confirmed which. | Hostinger |
| Hostinger — "n8n" server | Unknown | **Confirmed by founder 2026-09-07.** Runs n8n automation. | Hostinger |
| LiteLLM Gateway | `159.195.1.254` (public), `litellm-gateway-u14612.vm.elestio.app` | Model routing | Elestio |
| Redis (LiteLLM cache only) | `152.53.202.147` (public) / `10.30.71.5` (private) | Caching only — never durable storage, never Langfuse-accessible | Elestio |

Langfuse is described elsewhere as "self-hosted on INTEL" — if that's the same server as INTEL-1 above, it isn't stated explicitly as such anywhere; could still be a separate Elestio instance. Don't assume without checking.

**Important:** this means the platform spans at least three hosting providers (DigitalOcean, Hostinger, Elestio), not the "two DigitalOcean servers" that `ADR-0004` describes. `ADR-0004` predates this fuller picture — see the note added to that ADR.

## Hermes-specific directory structure (from a 2026-08-08 runtime sweep, `Infrastructure/RUNTIME-SWEEP-2026-08-08.md`)

- Active Hermes profile root: `/root/.hermes-admin`
- Older/secondary: `/root/.hermes`
- Canonical, git-tracked engineering memory: `/root/vault/work/meta/engineering-memory.md`

## Unknown — needs someone with live access to fill in

- Whether Langfuse runs on INTEL-1 or a separate instance
- The actual IPs of the two Hostinger servers
- Which of "core" vs "n8n" (or a third Hostinger server) actually hosts the production backend/frontend
