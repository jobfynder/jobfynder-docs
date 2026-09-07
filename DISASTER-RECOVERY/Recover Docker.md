# Recover Docker

## Confirmed (live `docker ps` probe across all 12 servers, 2026-09-07)

Every server in `Infrastructure/SERVER-INVENTORY.md` runs Docker except the Hostinger core box (`jobfynder-core`, which runs the backend directly via PM2, not in a container). Container inventory per server:

- **`jobfynder-comm1`**: `jobfynder-comm-gateway`, `jobfynder-comm-worker`, `jobfynder-rabbitmq` (rabbitmq:3-management), `jobfynder-npm` (Nginx Proxy Manager), `jobfynder-redis` (redis:7), `portainer`
- **`jobfynder-intel-01`**: `hermes-api`, `hermes-graph-consumer`, `hermes-postgres` (postgres:16), `nginx-proxy-manager`, `jobfynder-typesense`, `portainer` + `portainer_agent`
- **`jobfynder-n8n`** (Hostinger): `n8n-n8n-1`, `n8n-traefik-1`
- Each Elest.io box: `elestio-nginx` + `elestio-postfix` boilerplate plus its app stack — see `Infrastructure/SERVER-INVENTORY.md` for the full per-service container list (Dittofeed+Temporal+ClickHouse, LiteLLM+MinIO, Redis+RedisInsight, Langfuse's full stack, Centrifugo, EspoCRM+Metabase+MySQL, Ghost+MySQL, and the custom Chatwoot fork).

No `docker-compose.yml`/`docker-compose down && up` recovery procedure has been tested for any of these. Elest.io services are managed through the dashboard's own **Update config / Restart / Change version** actions rather than raw Docker Compose. `jobfynder-comm1` and `jobfynder-intel-01` both run **Portainer** — see `Recover Portainer.md` for using it as the actual recovery interface instead of raw CLI.

## Compose files ARE version-controlled
`/opt/jobfynder-infra` on both `jobfynder-comm1` and `jobfynder-intel-01` is a live git checkout of `jobfynder/jobfynder-infra` (`communication/docker-compose.yml`, `intelligence/docker-compose.yml`), not a standalone copy. **As of 2026-09-07, `comm1`'s checkout is on branch `fix/comm-rabbitmq-tailscale-bind-reconciled` with uncommitted staged changes** (`communication/.env.example`, `communication/README.md`) — worth resolving (commit or discard) so the deployed state matches what's in git. `intel-01` also has `/opt/hermes/docker-compose.yml` and `/opt/nginx-proxy-manager/docker-compose.yml` outside the `jobfynder-infra` checkout — not confirmed whether those are tracked anywhere.

## Unknown — needs someone with live access to fill in
An actual tested container-recreation procedure (`docker compose up -d` from the `jobfynder-infra` checkout has not been verified to correctly rebuild a lost container), and whether `/opt/hermes` and `/opt/nginx-proxy-manager` on `intel-01` are backed up anywhere.
