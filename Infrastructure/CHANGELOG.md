# Infrastructure Changelog

Transcribed from the version history in `JOBFYNDER-HERMES-COMM-CANONICAL.md` — that document is the original source; this file exists so infrastructure changes aren't buried inside a doc primarily about module status.

## 2026-08-21

**v1.1** — COMM documentation added to `jobfynder-docs` after a direct SSH inspection of COMM-1 (`152.42.219.165`) and the `jobfynder-infra` repository. Produced `comm/COMM-000` through `comm/COMM-500` and the infrastructure-posture doc. Before this, no `comm/` folder, no `COMM-nnn` file, and no server inventory entry existed anywhere.

**v1.2** (same day) — Three gaps found during that inspection were fixed, deployed, and verified live: an unhandled-exception path in the COMM-500 intake call, missing HTTP rate limiting, and no backup automation (commit `0c33580`).

**v1.3** (same day) — Phase 0 completed: `jobfynder-infra` `main` reconciled with the deployed COMM branch (clean merge, zero conflicts). Four HERMES module docs (450/500/600/850) were corrected to record git tags that had existed for weeks but were never written down.

**v1.4** (same day) — Phase 1 completed: the Hermes RBAC gap was closed and deployed. The HERMES-1000 LiteLLM exit condition was fully resolved across CORE, including a real direct-OpenAI-client bypass found during the investigation that the original gap description hadn't anticipated.

**v1.5** (same day) — Further Phase 2/3 progress: COMM-1 was restore-tested, `ufw` was enabled, a real TLS-bypass and a weak default RabbitMQ credential were found and fixed, and three stale prompt-ID check scripts were repaired and verified against the live Hermes registry.

**v1.6** (same day) — RabbitMQ and Redis — previously flagged as "a design decision, not a bug fix" — were actually wired into COMM's intake pipeline: queueing, exponential-backoff retry, dead-letter handling, idempotency, live-verified end to end (commit `2622899`). A logging-configuration mistake that had briefly leaked the Telegram bot token into a log file was found and fixed in the same pass — if that token wasn't already rotated after this was caught, rotate it now.

## 2026-08-08

Hermes runtime sweep (`Infrastructure/RUNTIME-SWEEP-2026-08-08.md`): found the platform's self-learning memory tool was disabled at the config level (`memory` listed under `agent.disabled_toolsets`), fixed and verified. Documented the two parallel Hermes home directories (`/root/.hermes` vs `/root/.hermes-admin`) that had been causing silent script failures. Built a durable memory-write path (`memory-append.py`) that commits to the git-tracked vault. One stray 0-byte script (`daily-hermes-tips.sh`) was flagged but not yet repaired as of that sweep — check whether it still is.

## 2026-08-02

AI infrastructure build-out: LiteLLM Gateway, Redis caching, Langfuse, and DeepInfra embeddings stood up, replacing an earlier Portkey-based path (rolled back). Full detail in `docs/AI-INFRA-SUMMARY-2026-08-02.md`. Key real incidents from that pass, worth knowing even in summary:

- Redis passwords are case-sensitive in a way that isn't obvious from the dashboard — a screenshot showed uppercase, only lowercase actually authenticated. Verify with a live AUTH test, not the dashboard.
- LiteLLM's cache does not activate from environment variables alone — it requires a `config.yaml` block, and Elestio's plain "Restart" button doesn't reload it; "Update & Restart" (full recreate) does.
- A shared password was found reused across multiple services (LiteLLM admin, Postgres, AWS, Langfuse) — flagged as a real security priority, not yet confirmed rotated as of this writing.
- Elestio's Redis defaults to public exposure; locking it down requires both a UFW rule and the Docker `DOCKER-USER` chain — removing only one leaves it open.
