# COMM-300 / COMM-900 / COMM-1000 — Infrastructure Posture

Status: Provisioned, largely unused / undocumented until now
Server: COMM-1 (`152.42.219.165`)
Live-verified: 2026-08-21

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

**Recommendation** (also noted in `COMM-500-ingress-intake.md` §5): the most direct way to close COMM-500's resilience gaps (no retry, no dead-letter, no queueing) is to actually start using this RabbitMQ instance for inbound webhook processing, rather than standing up something new.

## COMM-900 — Reliability & Governance

**Status: 🔴 Real gaps found, not previously documented anywhere.**

- **Redis** (`jobfynder-redis`, `redis:7`, `--appendonly yes`) — running 6+ weeks, `DBSIZE` = 0 live. Same story as RabbitMQ: provisioned, never used by `comm_gateway/`.
- **No rate limiting** anywhere in `comm_gateway/` — every endpoint, including the public webhook, accepts unlimited requests. There is no WAF-style protection at the application layer.
- **`fail2ban` is active but scoped to SSH only** (`fail2ban-client status` → one jail, `sshd`). There is no HTTP-layer abuse protection — Nginx Proxy Manager is not configured with any access lists or rate limits on the `comm.jobfynder.com` proxy host (checked directly in the NPM sqlite database: `access_list_id` is unset on the active proxy host row).
- **`ufw` (host firewall) is inactive.** All host-level traffic control is currently just "whatever Docker's `iptables` rules do by default" plus `fail2ban` on SSH.
- **Confirmed real-world exposure, not theoretical:** live `jobfynder-comm-gateway` logs show unsolicited scanner traffic already probing `/.env`, `/.git/HEAD`, `/terraform.tfstate`, `/login` — all correctly returned 404 (no secrets exposed), but this is a public, internet-facing, unauthenticated-by-default endpoint receiving that traffic today, with no rate limiting or WAF between it and the internet beyond what NPM/FastAPI do by default.
- **`GET /providers/telegram/status` is unauthenticated** and reveals which secrets are configured (booleans only, not values) — low severity, but avoidable information disclosure for an endpoint with no clear reason to be public.

**None of this is catastrophic** — no secret values are exposed, and 404 responses are correct — but it is a real, previously-undocumented gap between "runs in production" and "production ready," consistent with the caution this whole documentation effort is built around: a service running for 6 weeks is not the same claim as a service that's been hardened.

## COMM-1000 — Production Operations

**Status: 🟡 Partial — deployment is real, operational discipline is thin.**

- **Deployment:** Docker Compose, `restart: unless-stopped` on every container, confirmed running continuously (comm-gateway up 4 weeks, the rest up 6 weeks) — no evidence of unplanned downtime in that window, but no monitoring/alerting was found either, so this is an absence-of-evidence observation, not a clean bill of health.
- **Backups:** `/opt/jobfynder-backups/comm-1/` contains exactly two snapshot folders — `20260710-052714` (initial) and `telegram-reset-20260711-183728` (a manual, one-off snapshot named after what looks like an incident response, not a schedule). **No cron job exists on the host** (`crontab -l` for root returns empty) — there is no automated, recurring backup for COMM-1's data (RabbitMQ/Redis/NPM volumes are all Docker named volumes with no external backup target found).
- **Disk/memory headroom:** 71G free of 77G disk, 2.9G available of 3.8G RAM at last check — healthy, no capacity pressure.
- **Monitoring:** Portainer is installed and running (a Docker management UI) but there is no evidence of alerting, uptime checks, or log aggregation configured for COMM-1 specifically.
- **DR:** No disaster-recovery plan or restore test found. This mirrors the "Restore testing: ⚪/❓" gap already flagged for HERMES/COMM-1000 in the canonical doc before this investigation — now confirmed concretely rather than inferred.

### Immediate, low-effort fixes worth flagging to whoever owns COMM-1 next

1. Add a recurring backup cron for the Docker volumes (or confirm DigitalOcean droplet-level snapshots cover this — `droplet-agent` is installed but no droplet snapshot schedule was checked from inside the host, since that's a DO control-panel setting, not something visible via SSH).
2. Merge `feature/comm-telegram-message-chunking` to `main` on `jobfynder-infra` so the deployed code and the default branch match (see `COMM-100` §2).
3. Add basic rate limiting to at least the Telegram webhook endpoint, given it's already visibly targeted by scanners.
