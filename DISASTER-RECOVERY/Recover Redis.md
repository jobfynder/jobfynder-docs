# Recover Redis

## The one fact that matters most here

**There are (at least) three separate Redis instances on this platform — do not conflate them during recovery:**

- **LiteLLM cache Redis** — `10.30.71.5:26379` (Elest.io service `redis-ai-gateway`, container `app-redis-1`). Cache only, never durable data. If lost, nothing is permanently lost — it can be recreated empty and will simply repopulate as cache misses occur.
- **Langfuse's own internal Redis** — `172.17.0.1:6379` (container `app-redis-1` inside Langfuse's own stack on `langfuse-tnnaf`, confirmed as `elestio/redis:7.0`). Used for Langfuse's event queue. Separate infrastructure, separate recovery path from LiteLLM's — despite the same container name, they are on different hosts.
- **COMM-1 Redis** — container `jobfynder-redis` (`redis:7`) on `jobfynder-comm1`. Not previously documented here. Backs the communication gateway/worker (`jobfynder-comm-gateway`/`jobfynder-comm-worker`) — exact usage (queue, session, cache) not yet confirmed by reading the gateway's actual code/config.

Recovering the wrong one, or pointing one service at the other's Redis, has already caused real incidents in this platform's history (see `Infrastructure/CHANGELOG.md`, 2026-08-02) — that incident predates the COMM-1 instance being documented, so re-confirm it isn't also affected.

## Unknown — needs someone with live access to fill in

The actual recovery/recreation steps for any of the three instances, whether any has its own backup or snapshot policy, and exactly what COMM-1's Redis is used for.
