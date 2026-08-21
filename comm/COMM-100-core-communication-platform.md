# COMM-100 — Core Communication Platform

Status: Foundation Complete (first documented 2026-08-21)
Server: COMM-1 (`152.42.219.165`, hostname `jobfynder-comm1`)
Code repo: `jobfynder/jobfynder-infra`, path `communication/`
Live-verified: 2026-08-21

---

## 1. What this is

The COMM Gateway is a small FastAPI service (`comm_gateway/`, 5 Python files, `title="Jobfynder COMM Gateway"`, `version="0.1.0"`) that receives provider webhooks (currently only Telegram), normalizes them into a canonical intake shape, and forwards them to Hermes over an HMAC-signed internal contract. It is deliberately thin — there is no database, no message queue usage, and no session store in the current code, despite Postgres-adjacent infrastructure (RabbitMQ, Redis) being provisioned alongside it.

## 2. Repository state

- Repo: `git@github-jobfynder-infra:jobfynder/jobfynder-infra.git`
- **Deployed branch on COMM-1: `main`, as of 2026-08-21.** `feature/comm-telegram-message-chunking` was merged into `main` (`git merge --no-ff`, merge commit on top of `814a8ed`) and the server's working directory was switched to `main` — no rebuild needed, `communication/` was byte-identical before and after the merge (confirmed via `git diff feature/comm-telegram-message-chunking main -- communication/`, only difference was `README.md`, which the Dockerfile doesn't copy into the image). Live health check post-merge: `{"status":"healthy",...}`.
- **Historical note (resolved):** this branch was 4 commits ahead of `main` and unmerged for weeks — same class of problem found on the Hermes docs side. It turned out to be a clean merge: `main`'s extra commits only touched `intelligence/`, this branch's only touched `communication/`, confirmed via `git merge-base` before merging — zero conflicts. The two stray SSH public keys (`jobfynder`, `jobfynder.pub`) and the separate `intelligence/docker-compose.yml` that were on `main` are preserved as-is; they were not part of what needed reconciling, just what made a naive fast-forward look risky at a glance.
- Other branches exist but are not deployed: `feature/comm-telegram-bridge`, `feature/comm-telegram-onboarding-integration`.
- `README.md` in the `communication/` folder now has real content (came in via the merge from `main`'s earlier "Document communication foundation stack" commit) — previously reported empty because the deployed branch predated that commit.

## 3. Source layout (complete — this is the entire application)

```
communication/
├── .env / .env.example
├── Dockerfile.comm-gateway
├── docker-compose.yml
├── requirements.txt
├── comm_gateway/
│   ├── main.py            — FastAPI app, 3 endpoints (see COMM-500), rate-limit middleware wired in 2026-08-21
│   ├── config.py           — env var loading, no validation/defaults beyond blank strings
│   ├── hermes_client.py     — HMAC-SHA256 signing + POST to Hermes /internal/comm/intake; timeout/error handling added 2026-08-21
│   ├── ratelimit.py         — per-IP, per-path in-memory rate limiter, added 2026-08-21
│   ├── telegram.py          — inbound normalization + raw sendMessage call
│   └── telegram_outbound.py — safe message chunking (3800-char Telegram limit) + reply delivery
└── scripts/
    ├── comm-telegram-message-chunking-check.py
    ├── comm-telegram-onboarding-check.py
    ├── comm-telegram-onboarding-route-check.py
    ├── comm-hermes-client-resilience-check.py  — added 2026-08-21, verifies the timeout/error-handling fix
    └── comm-1-backup-volumes.sh                 — added 2026-08-21, daily cron target for volume backups
```

## 4. Configuration (`comm_gateway/config.py`)

Five environment variables, all read with `os.getenv`, no startup validation — a missing value degrades a specific feature at request time rather than failing fast:

| Variable | Purpose | Behavior if unset |
|---|---|---|
| `COMM_ENV` | environment label | defaults to `"development"` string, purely cosmetic |
| `HERMES_BASE_URL` | Hermes API base | defaults to `https://hermes.jobfynder.com` |
| `HERMES_COMM_SHARED_SECRET` | HMAC key for signing requests to Hermes | if blank, `send_to_hermes()` short-circuits and returns `{"status": "blocked", "reason": "hermes_comm_shared_secret_missing"}` — no exception, no crash |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API auth | if blank, outbound sends return `{"status": "blocked", "reason": "telegram_bot_token_missing"}` |
| `TELEGRAM_WEBHOOK_SECRET` | validates inbound Telegram webhook calls | if blank, the webhook endpoint returns HTTP 503 |

**Live confirmed (2026-08-21, via `GET /providers/telegram/status`):** all three secrets are set in production — `has_bot_token: true`, `has_webhook_secret: true`, `has_hermes_secret: true`.

## 5. Deployment

- `docker-compose.yml` builds `comm-gateway` from `Dockerfile.comm-gateway` in the same directory, `restart: unless-stopped`, port `8080` (not published to the host directly — routed through `jobfynder-npm`).
- Public entry point: **`https://comm.jobfynder.com`**, confirmed from the live Nginx Proxy Manager database (`proxy_host` table, id 2, `forward_host: comm-gateway`, `forward_port: 8080`, `ssl_forced: 1`, `enabled: 1`, created 2026-07-10 23:02). A stale duplicate entry (id 1, same domain, `forward_host: jobfynder-comm-gateway`) is soft-deleted (`is_deleted: 1`) and can be ignored.
- Live health check (2026-08-21): `GET /health` → `{"status":"healthy","service":"jobfynder-comm-gateway","environment":"production"}`.

## 6. What is explicitly NOT built

- No database of any kind — the gateway is stateless per-request.
- No use of RabbitMQ or Redis for messaging/session state, despite both running alongside it (`grep -ril 'rabbitmq\|pika\|amqp' comm_gateway/` returns zero matches). They are provisioned capacity, not active infrastructure. See `COMM-300-900-1000-infrastructure-posture.md`. (The 2026-08-21 rate limiter is in-memory, not Redis-backed — see that file's COMM-900 section for why that's a stated limitation, not an oversight.)
- No identity/session layer (COMM-200) — the Telegram sender ID is passed straight through in the normalized payload with no persistent mapping to a Jobfynder user.
- No provider besides Telegram — no Email, WhatsApp, Slack, Teams, or Google Chat code exists on the COMM side (those are Hermes-side *contracts only*, per `HERMES-450-channel-intake.md`; there is nothing on COMM-1 to receive them yet).
- Request-level auth on `/health` or `/providers/telegram/status` — both remain open reads (rate-limited as of 2026-08-21, but not authenticated). Acceptable for health; the status endpoint still reveals which secrets are configured (booleans only, not values) and is worth eventually gating.

## 7. Production Ready assessment

**Closer, but still NO.** Foundation is real and live. Fixed 2026-08-21: the Hermes call no longer crashes on timeout (see COMM-500), the app is rate-limited, automated daily backups now run (see COMM-1000), and the deployed branch is now merged into `main` — repo/runtime parity restored. Still open: no restore test has been run against the new backups, and the public `/providers/telegram/status` endpoint is still unauthenticated (though now rate-limited).
