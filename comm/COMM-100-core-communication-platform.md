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
- Deployed branch on COMM-1: `feature/comm-telegram-message-chunking`
- **This branch is 3 commits ahead of `main` and has never been merged** — `main` does not contain the working Telegram bridge. Commits: `b6ab4ca` "communication foundation stack", `26fc1c4` "feat(comm): add production Telegram bridge", `ca8cd0e` "feat(comm): deliver Telegram onboarding responses", `0d7616a` "fix(comm): split long Telegram responses safely". This mirrors the exact same problem found on the Hermes docs side (see canonical doc §9) — production code living ahead of `main` with no merge.
- Other branches exist but are not deployed: `feature/comm-telegram-bridge`, `feature/comm-telegram-onboarding-integration`.
- `README.md` in the `communication/` folder is empty.

## 3. Source layout (complete — this is the entire application)

```
communication/
├── .env / .env.example
├── Dockerfile.comm-gateway
├── docker-compose.yml
├── requirements.txt
├── comm_gateway/
│   ├── main.py            — FastAPI app, 3 endpoints (see COMM-500)
│   ├── config.py           — env var loading, no validation/defaults beyond blank strings
│   ├── hermes_client.py     — HMAC-SHA256 signing + POST to Hermes /internal/comm/intake
│   ├── telegram.py          — inbound normalization + raw sendMessage call
│   └── telegram_outbound.py — safe message chunking (3800-char Telegram limit) + reply delivery
└── scripts/
    ├── comm-telegram-message-chunking-check.py
    ├── comm-telegram-onboarding-check.py
    └── comm-telegram-onboarding-route-check.py
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
- No use of RabbitMQ or Redis, despite both running alongside it (`grep -ril 'rabbitmq\|pika\|redis\|amqp' comm_gateway/` returns zero matches). They are provisioned capacity, not active infrastructure. See `COMM-300-900-1000-infrastructure-posture.md`.
- No identity/session layer (COMM-200) — the Telegram sender ID is passed straight through in the normalized payload with no persistent mapping to a Jobfynder user.
- No provider besides Telegram — no Email, WhatsApp, Slack, Teams, or Google Chat code exists on the COMM side (those are Hermes-side *contracts only*, per `HERMES-450-channel-intake.md`; there is nothing on COMM-1 to receive them yet).
- No rate limiting, no request-level auth on `/health` or `/providers/telegram/status` (both are open reads — acceptable for health, worth reviewing for the status endpoint since it reveals which secrets are configured, even though it doesn't reveal values).

## 7. Production Ready assessment

**NO.** Foundation is real and live, but: the deployed branch was never merged to `main` (repo/runtime parity gap, same class of issue flagged for Hermes), there's no automated backup for the running containers beyond two manual snapshot folders (see COMM-1000), and the public `/providers/telegram/status` endpoint is unauthenticated. None of these are large fixes, but none are done either.
