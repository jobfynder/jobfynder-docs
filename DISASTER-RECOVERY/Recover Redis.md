# Recover Redis

## The one fact that matters most here

**There are two separate Redis instances on this platform — do not conflate them during recovery:**

- **LiteLLM cache Redis** — `10.30.71.5:26379` (Elestio-managed). Cache only, never durable data. If lost, nothing is permanently lost — it can be recreated empty and will simply repopulate as cache misses occur.
- **Langfuse's own internal Redis** — `172.17.0.1:6379`. Used for Langfuse's event queue. Separate infrastructure, separate recovery path.

Recovering the wrong one, or pointing one service at the other's Redis, has already caused real incidents in this platform's history (see `Infrastructure/CHANGELOG.md`, 2026-08-02).

## Unknown — needs someone with live access to fill in

The actual recovery/recreation steps for either instance, and whether either has its own backup or snapshot policy.
