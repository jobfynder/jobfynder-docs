# COMM-300 / COMM-900 / COMM-1000 — Infrastructure Posture

Status: Two hardening passes complete 2026-08-21 (rate limiting, backups, restore-tested, host firewall, TLS-bypass closed, weak RabbitMQ credential rotated) — RabbitMQ/Redis integration and admin-port IP-restriction still open
Server: COMM-1 (`152.42.219.165`)
Live-verified: 2026-08-21 (re-verified after both 2026-08-21 fix passes, commits `0c33580` and `33b6ec4` on `jobfynder-infra`)

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
- **`fail2ban` is active but scoped to SSH only** (`fail2ban-client status` → one jail, `sshd`). No HTTP-layer fail2ban jail added in this pass — the app-level rate limiter plus the new firewall (below) cover the immediate exposure; an nginx-log-based jail is still a reasonable future addition, not done.
- **`ufw` (host firewall): enabled 2026-08-21.** Was inactive; now active with an explicit allowlist (SSH 22, HTTP 80, HTTPS 443, NPM admin 81, Portainer 9443) and default-deny on everything else incoming. Staged and verified carefully given the risk of a firewall change locking out SSH permanently: rules confirmed via `ufw show added` *before* enabling, then `ufw --force enable`, then immediately re-verified SSH still connects and `https://comm.jobfynder.com/health` still returns 200. **Known residual risk, not addressed:** ports 81 (NPM admin) and 9443 (Portainer) are left open to the whole internet, same as before — genuinely restricting them to a known IP/VPN would be better, but doing that blind (without knowing the admin's actual source IP) risked locking out legitimate access, so it was left as an explicit follow-up decision rather than guessed at.
- **Direct bypass of TLS: closed 2026-08-21, found during this hardening pass, not part of the original plan.** `comm-gateway` was published as `8080:8080` in `docker-compose.yml` — reachable directly over plain HTTP, completely bypassing NPM's TLS termination and (before the fix above) the rate limiter's only real gate. Confirmed via `ss -tlnp` that port 8080 was listening on `0.0.0.0`. Fix: removed the port mapping entirely — `comm-gateway` and `npm` share the `communication_default` Docker bridge network, so NPM already resolves `comm-gateway:8080` internally without any host-level publish; the mapping was pure unnecessary exposure. Verified: `curl http://localhost:8080/health` now fails to connect, `https://comm.jobfynder.com/health` still returns 200.
- **Weak/default RabbitMQ credential: rotated 2026-08-21, also found during this pass.** `RABBITMQ_DEFAULT_PASS` was hardcoded directly in `docker-compose.yml` as the literal placeholder `CHANGE_THIS_STRONG_PASSWORD` — committed to git in plaintext across multiple prior commits. Not externally exploitable (the management port was never published to the host, confirmed via `docker port`), but a real weak/default credential regardless. Moved to `.env` (not committed) via `env_file` + variable substitution, and rotated to a random value via `rabbitmqctl change_password` against the live container — changing the env var alone would **not** have rotated the actual credential, since `RABBITMQ_DEFAULT_USER`/`PASS` only take effect on a fresh, uninitialized Mnesia database, and this container's had been running for 6+ weeks. Verified via `rabbitmqctl authenticate_user` (output suppressed to avoid a repeat of the mistake below). **Not addressed:** the old placeholder value remains visible in this repo's git history on earlier commits — rotating it makes that historical value inert, but a full history rewrite was not attempted (disruptive to other clones, out of scope for this pass).
- **Operational note, logged for honesty:** during the RabbitMQ credential verification, an `rabbitmqctl authenticate_user` call failed (the RabbitMQ app hadn't finished starting yet post-restart) and its error handler echoed the new password back into command output — briefly visible in this session's own transcript. Not a third-party exposure (the operator already has full server access), but sloppy handling of a secret. The password was rotated a second time immediately afterward using a method that suppresses all output, and the first (briefly-exposed) value is no longer the live credential.
- **Confirmed real-world exposure, not theoretical:** live `jobfynder-comm-gateway` logs (pre-fix) showed unsolicited scanner traffic already probing `/.env`, `/.git/HEAD`, `/terraform.tfstate`, `/login` — all correctly returned 404 (no secrets exposed). The rate limiter and firewall together now bound both the volume and the surface area of this traffic; there's still no automated alerting on the pattern itself.
- **`GET /providers/telegram/status` is unauthenticated** and reveals which secrets are configured (booleans only, not values) — unchanged, still low severity, still worth eventually gating.

**Net effect across both 2026-08-21 passes:** rate limiting, a host firewall, a real TLS-bypass path, and a weak default credential are all fixed. What's still missing — WAF-level content filtering, an HTTP-layer fail2ban jail, IP-restricting the two admin ports (81/9443), moving rate-limit state to Redis if the service ever scales, and automated alerting on the scanner traffic already observed — is real and left open deliberately, not hidden. A service that's had two hardening passes is meaningfully safer than one that's had none, but "hardened twice" is still not the same claim as "hardened comprehensively."

## COMM-1000 — Production Operations

**Status: 🟡 Partial — backups fixed 2026-08-21, other operational gaps remain.**

- **Deployment:** Docker Compose, `restart: unless-stopped` on every container, confirmed running continuously (comm-gateway up 4 weeks pre-redeploy, the rest up 6 weeks) — no evidence of unplanned downtime in that window, but no monitoring/alerting was found either, so this is an absence-of-evidence observation, not a clean bill of health. The 2026-08-21 redeploy (`docker compose up -d --force-recreate comm-gateway`) was clean — container came back healthy within seconds, verified via `/health`, `/providers/telegram/status`, and the public `https://comm.jobfynder.com/health` endpoint.
- **Backups: fixed 2026-08-21.** A daily cron (`0 3 * * *`) now runs `communication/scripts/comm-1-backup-volumes.sh`, tarring all four Docker named volumes (RabbitMQ, Redis, NPM data + letsencrypt certs) into `/opt/jobfynder-backups/comm-1/daily-<timestamp>/`, with 14-day automatic retention (older snapshots pruned by the script itself). Ran once manually to confirm it works before scheduling — produced a 2.1MB snapshot. The two pre-existing manual snapshots (`20260710-052714`, `telegram-reset-20260711-183728`) are untouched and still there for historical reference.
- **Disk/memory headroom:** 71G free of 77G disk, 2.9G available of 3.8G RAM at last check — healthy, no capacity pressure. The daily backup job's own footprint (~2MB/day at current volume sizes) is negligible against this.
- **Monitoring:** Unchanged — Portainer is installed and running (a Docker management UI) but there is no evidence of alerting, uptime checks, or log aggregation configured for COMM-1 specifically.
- **DR: restore test done 2026-08-21.** Extracted `communication_npm_data.tar.gz` from the one existing daily backup into a scratch directory (never touched the live volume), ran `PRAGMA integrity_check` against the restored `database.sqlite` (`ok`), and confirmed its `proxy_host` table contents exactly matched the live database (2 rows, same domain/forward-host/port values). Also confirmed the other three archives (`rabbitmq`, `redis`, `npm_letsencrypt`) are structurally valid via `tar -tzf` (not corrupt). Scratch directory deleted after. **This proves the backup mechanism produces genuinely restorable archives, not just files that exist** — the gap that remained after backups were first added.
- **Deployed-branch/`main` gap: closed 2026-08-21.** `feature/comm-telegram-message-chunking` (including the resilience/rate-limit/backup fix `0c33580`) merged into `main` on `jobfynder-infra` via `git merge --no-ff` (merge commit on `814a8ed`), pushed, and the server's working directory switched to `main`. It turned out to be a clean, non-overlapping divergence — `main`'s extra commits only touched `intelligence/`, this branch's only touched `communication/`, confirmed via `git merge-base` before merging. Zero conflicts. `communication/` was byte-identical before/after the merge (only `README.md` differed, which isn't copied into the Docker image), so no rebuild was needed — live health check confirmed the running container was unaffected.

### Remaining low-effort fixes worth flagging to whoever owns COMM-1 next

1. ~~Add a recurring backup cron for the Docker volumes~~ — **done 2026-08-21.**
2. ~~Add basic rate limiting to at least the Telegram webhook endpoint~~ — **done 2026-08-21** (applied app-wide, not just the webhook).
3. ~~Merge `feature/comm-telegram-message-chunking` to `main` on `jobfynder-infra`~~ — **done 2026-08-21**, clean merge, no conflicts (see above).
4. ~~Run a real restore test from one of the new daily backups~~ — **done 2026-08-21**, see DR note above.
5. ~~Enable a host firewall (`ufw`)~~ — **done 2026-08-21**, see COMM-900 above.
6. ~~Stop publishing comm-gateway's port directly (TLS bypass)~~ — **done 2026-08-21**, see COMM-900 above.
7. ~~Rotate the default RabbitMQ credential~~ — **done 2026-08-21**, see COMM-900 above.
8. Confirm whether DigitalOcean droplet-level snapshots also cover this box (a control-panel setting, not visible via SSH) — if not, consider it a second, independent backup layer.
9. IP-restrict the two admin ports (81 NPM, 9443 Portainer) instead of leaving them open to the whole internet — deliberately not done blind (Section COMM-900), needs the actual admin's source IP/VPN range.
10. Add an HTTP-layer fail2ban jail (nginx access-log-based) as a second line of defense behind the app-level rate limiter.
