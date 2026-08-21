# COMM-300 / COMM-900 / COMM-1000 — Infrastructure Posture

Status: Provisioned, largely unused / undocumented until now — rate limiting and backups fixed 2026-08-21, RabbitMQ/Redis integration still open
Server: COMM-1 (`152.42.219.165`)
Live-verified: 2026-08-21 (re-verified after the 2026-08-21 fixes, commit `0c33580` on `jobfynder-infra`)

These three modules are combined into one file because the evidence for all three comes from the same infrastructure inspection, and — unlike COMM-100/410/500 — none of them has real application code to document yet. This file records what's *provisioned* honestly, rather than writing separate stub files that would imply more progress than exists.

---

## COMM-300 — Messaging & Event Transport

**Status: ⚪ Provisioned, not integrated.**

`jobfynder-rabbitmq` (`rabbitmq:3-management`) has been running for 6+ weeks. Live inspection (2026-08-21):

```
rabbitmqctl list_vhosts  → only "/" (default vhost)
rabbitmqctl list_queues  → empty (zero queues)
```

`grep -ril 'rabbitmq\|pika\|amqp' comm_gateway/` against the entire COMM Gateway source returns **zero matches**. RabbitMQ is running, has a management UI, has a persistent volume (`communication_rabbitmq_data`), and has never been called by any code in this repo. It is capacity, not infrastructure-in-use.

**Recommendation** (also noted in `COMM-500-ingress-intake.md` §5): the most direct way to close COMM-500's remaining resilience gaps (no retry, no dead-letter, no queueing — the 2026-08-21 fix addressed the crash-on-timeout bug, not these) is to actually start using this RabbitMQ instance for inbound webhook processing, rather than standing up something new. Still not attempted — it's a design change (new worker process, queue schema), not a bug fix.

## COMM-900 — Reliability & Governance

**Status: 🟡 Partial — rate limiting fixed 2026-08-21, other gaps remain.**

- **Rate limiting: fixed 2026-08-21, commit `0c33580`.** `comm_gateway/ratelimit.py` adds an in-memory, per-IP, per-path sliding-window limiter (120 requests/60s default), applied to the whole app via `app.add_middleware(RateLimitMiddleware, ...)` in `main.py`. Live-tested on COMM-1 after redeploy: 125 rapid requests to `/health` produced 114×`200` + 11×`429` at the threshold, exactly as designed, and the service stayed healthy afterward. **Known limitation, stated in the code's own docstring:** this is in-memory and per-instance — fine for the current single-container deployment, but if COMM Gateway is ever scaled to multiple replicas, the counters need to move to the Redis instance already running alongside it (see below) rather than staying in-process.
- **Redis** (`jobfynder-redis`, `redis:7`, `--appendonly yes`) — running 6+ weeks, `DBSIZE` = 0 live, still not used by any code (the new rate limiter is in-memory, not Redis-backed — see limitation above). Same story otherwise: provisioned, unused.
- **`fail2ban` is active but scoped to SSH only** (`fail2ban-client status` → one jail, `sshd`). The new application-level rate limiter (above) is the first line of HTTP-layer defense; Nginx Proxy Manager itself still has no access lists or rate limits configured on the `comm.jobfynder.com` proxy host.
- **`ufw` (host firewall) is inactive.** Unchanged by this pass — host-level traffic control is still just Docker's default `iptables` rules plus `fail2ban` on SSH.
- **Confirmed real-world exposure, not theoretical:** live `jobfynder-comm-gateway` logs (pre-fix) showed unsolicited scanner traffic already probing `/.env`, `/.git/HEAD`, `/terraform.tfstate`, `/login` — all correctly returned 404 (no secrets exposed). The rate limiter now caps how much of that traffic can hit the app in a burst; it does not stop it from being logged, and there's still no automated alerting on the pattern.
- **`GET /providers/telegram/status` is unauthenticated** and reveals which secrets are configured (booleans only, not values) — unchanged, still low severity, still worth eventually gating.

**Net effect of the 2026-08-21 pass:** the burst-traffic exposure is now bounded instead of unlimited. What's still missing — WAF-level filtering, HTTP-layer fail2ban rules, an active host firewall, and moving rate-limit state to Redis if the service ever scales — is real, previously-undocumented gap, consistent with the caution this whole documentation effort is built around: a service running for 6 weeks is not the same claim as a service that's been hardened, and one fix pass doesn't change that verdict, just moves the line.

## COMM-1000 — Production Operations

**Status: 🟡 Partial — backups fixed 2026-08-21, other operational gaps remain.**

- **Deployment:** Docker Compose, `restart: unless-stopped` on every container, confirmed running continuously (comm-gateway up 4 weeks pre-redeploy, the rest up 6 weeks) — no evidence of unplanned downtime in that window, but no monitoring/alerting was found either, so this is an absence-of-evidence observation, not a clean bill of health. The 2026-08-21 redeploy (`docker compose up -d --force-recreate comm-gateway`) was clean — container came back healthy within seconds, verified via `/health`, `/providers/telegram/status`, and the public `https://comm.jobfynder.com/health` endpoint.
- **Backups: fixed 2026-08-21.** A daily cron (`0 3 * * *`) now runs `communication/scripts/comm-1-backup-volumes.sh`, tarring all four Docker named volumes (RabbitMQ, Redis, NPM data + letsencrypt certs) into `/opt/jobfynder-backups/comm-1/daily-<timestamp>/`, with 14-day automatic retention (older snapshots pruned by the script itself). Ran once manually to confirm it works before scheduling — produced a 2.1MB snapshot. The two pre-existing manual snapshots (`20260710-052714`, `telegram-reset-20260711-183728`) are untouched and still there for historical reference.
- **Disk/memory headroom:** 71G free of 77G disk, 2.9G available of 3.8G RAM at last check — healthy, no capacity pressure. The daily backup job's own footprint (~2MB/day at current volume sizes) is negligible against this.
- **Monitoring:** Unchanged — Portainer is installed and running (a Docker management UI) but there is no evidence of alerting, uptime checks, or log aggregation configured for COMM-1 specifically.
- **DR:** Backups now exist, but **no restore has been tested.** A backup that has never been restored is a hypothesis, not a guarantee — this is still an open gap, just a smaller one than "no backups at all."
- **Deployed-branch/`main` gap:** Confirmed still open. `feature/comm-telegram-message-chunking` (including the 2026-08-21 fix commit `0c33580`) has not been merged to `main` on `jobfynder-infra` — attempted during this pass and deliberately not forced through, because `main` has diverged with unrelated infra restructuring (a different `intelligence/docker-compose.yml`, and two stray SSH public keys committed at the repo root) that needs a deliberate look, not an automatic merge.

### Remaining low-effort fixes worth flagging to whoever owns COMM-1 next

1. ~~Add a recurring backup cron for the Docker volumes~~ — **done 2026-08-21.**
2. ~~Add basic rate limiting to at least the Telegram webhook endpoint~~ — **done 2026-08-21** (applied app-wide, not just the webhook).
3. Merge `feature/comm-telegram-message-chunking` to `main` on `jobfynder-infra` — still open, needs a deliberate reconciliation pass (see above), not a next-pass automatic merge.
4. Run a real restore test from one of the new daily backups, at least once, to confirm the backup is actually usable and not just present.
5. Confirm whether DigitalOcean droplet-level snapshots also cover this box (a control-panel setting, not visible via SSH) — if not, consider it a second, independent backup layer.
