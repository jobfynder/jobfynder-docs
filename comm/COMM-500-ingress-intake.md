# COMM-500 — Ingress & Intake

Status: Foundation Complete, live in production — now with queueing, retry, and idempotency (2026-08-21)
Source: `comm_gateway/main.py`, `comm_gateway/hermes_client.py`, `comm_gateway/queue.py`, `comm_gateway/worker.py`, `comm_gateway/idempotency.py`
Live-verified: 2026-08-21 (re-verified after the resilience fix `0c33580`, and again after the RabbitMQ/Redis wiring `2622899`, both on `jobfynder-infra`)

---

## 1. The contract, from both sides

This is the one piece of COMM that was already partially documented — from the *Hermes* side, in `hermes/HERMES-450-channel-intake.md` and `hermes/hermes-core-integration-guide.md` §4.5. Reading the actual `comm_gateway/hermes_client.py` source confirms the two sides agree byte-for-byte:

```python
# comm_gateway/hermes_client.py
def build_signature(timestamp: str, body: bytes) -> str:
    return hmac.new(
        HERMES_COMM_SHARED_SECRET.encode("utf-8"),
        timestamp.encode("utf-8") + b"." + body,
        hashlib.sha256,
    ).hexdigest()
```

Headers sent: `X-Jobfynder-Timestamp`, `X-Jobfynder-Signature`. Target: `POST {HERMES_BASE_URL}/internal/comm/intake` (`https://hermes.jobfynder.com/internal/comm/intake` in production). This matches exactly what `HERMES-450-channel-intake.md` documents as the signature contract Hermes expects: `HMAC-SHA256(shared_secret, timestamp + "." + raw_body)`. **This is the one part of the platform where COMM and HERMES documentation were independently verified to agree — first cross-checked here, 2026-08-21.**

## 2. Full request lifecycle

```text
Telegram
   │  webhook POST, X-Telegram-Bot-Api-Secret-Token header
   ▼
POST /providers/telegram/webhook  (comm-gateway, COMM-1)
   │  1. verify webhook secret (403 if wrong, 503 if unconfigured)
   │  2. normalize_telegram_update() → canonical intake shape
   ▼
send_to_hermes()  (comm-gateway, COMM-1)
   │  3. HMAC-sign the normalized payload
   │  4. POST to https://hermes.jobfynder.com/internal/comm/intake
   ▼
POST /internal/comm/intake  (hermes-api, INTEL-1)
   │  5. verify HMAC signature + timestamp freshness
   │  6. parse / taxonomy-extract / draft-create (HERMES-200/400/450)
   ▼
response flows back to comm-gateway
   │  7. deliver_hermes_telegram_response() → Telegram sendMessage (COMM-410)
   ▼
Telegram user sees the reply
```

Every hop in this chain now has documentation on at least one side; this file is the first place the whole chain is written down end to end.

## 3. Failure behavior (from source, not speculation)

| Failure point | What happens | Where |
|---|---|---|
| `HERMES_COMM_SHARED_SECRET` unset on COMM-1 | Request to Hermes never sent; returns `{"status": "blocked", "reason": "hermes_comm_shared_secret_missing"}` | `hermes_client.py` |
| Telegram webhook secret mismatch | HTTP 403 `invalid_telegram_webhook_secret`, request rejected before reaching Hermes | `main.py` |
| Hermes returns non-200 | User gets a fixed "could not process this message" reply, no error detail leaked | `telegram_outbound.py` |
| Hermes unreachable / timeout | **Fixed 2026-08-21, commit `0c33580`.** `send_to_hermes()` now catches `httpx.TimeoutException` and `httpx.RequestError` and returns `{"status": "error", "reason": "hermes_request_timeout"}` or `{"status": "error", "reason": "hermes_request_failed", "detail": ...}`. `deliver_hermes_telegram_response()` already treats any result without a `200` `status_code` as a failure and sends the user the existing "could not process this message" reply — so the fix required no change on the outbound side, only closing the hole upstream. Verified with `scripts/comm-hermes-client-resilience-check.py` (mocked timeout, connection error, and missing-secret cases), then re-verified live against the rebuilt container on COMM-1 (`docker compose up -d --force-recreate comm-gateway`, health + Telegram-status endpoints both 200 after restart). |

## 4. What was NOT built — closed 2026-08-21 (commit `2622899`)

All three gaps below are now fixed by wiring in the RabbitMQ and Redis instances that had been running unused on COMM-1 since the service's first deployment. Full detail in `COMM-300-900-1000-infrastructure-posture.md` (COMM-300) and `COMM-410-telegram-channel-adapter.md`; summarized here since they were originally documented as gaps in this file:

- **Idempotency: fixed.** `comm_gateway/idempotency.py` claims `(channel, source_message_id)` in Redis (atomic `SETNX`+`EX`, 24h TTL) before anything else happens in the webhook handler. A Telegram-redelivered webhook is now acknowledged (`{"status": "duplicate"}`) without being re-normalized, re-queued, or re-forwarded. Live-verified: sending the identical webhook payload twice returns `queued` then `duplicate`.
- **Queueing: fixed.** The webhook handler now claims idempotency, normalizes, publishes to `comm.intake.telegram`, and returns `{"status": "queued"}` immediately — it no longer waits on the Hermes round-trip inline. A new `comm-worker` process (same image, `python -m comm_gateway.worker`) consumes the queue and does the actual Hermes call + Telegram reply delivery.
- **Dead-letter path: fixed.** Retry uses a delayed-requeue pattern (`comm.intake.retry` → per-message `expiration` → dead-lettered back to the main queue), exponential backoff (5s/15s/60s/300s/900s), up to 5 attempts. The retry policy distinguishes definitive failures (`401`/`403`/`404`/`422` — retrying the identical payload will never succeed differently) from transient ones (5xx, timeout, connection error) — only transient failures are retried; definitive ones go straight to `comm.intake.dead` with the user still notified immediately, not silently dropped.

**Incident during this work, fixed in the same pass:** the worker's initial logging setup (`logging.basicConfig(level=INFO)`) caused `httpx`'s own request logger to emit full request URLs — and Telegram's Bot API embeds the live bot token directly in the URL (`.../bot<TOKEN>/sendMessage`), so this leaked the token into `docker logs jobfynder-comm-worker` once during testing. Fixed by setting `httpx`/`httpcore`'s loggers to `WARNING` specifically. Checked disk directly for the one container-log file that had the leaked token — gone after the container recreate, no external log shipping configured on this host to have copied it elsewhere. Not otherwise remediated (rotating the bot token requires Telegram/BotFather access this session doesn't have) — flagged as a recommendation for whoever owns the bot, not forced through, since the practical exposure was bounded to whoever already has SSH+docker access to COMM-1, the same trust boundary `.env` itself already has.

## 5. Production Ready assessment

**Closer still, but not yet fully there.** The signed contract, resilience (§3), and now queueing/retry/idempotency are all fixed and live-verified. What remains: the worker process itself has no monitoring (if it silently stops consuming, nothing alerts anyone — Portainer shows the container status but nothing watches queue depth or consumer lag), and the dead-letter queue has no automated inspection or alerting — a message that exhausts retries sits there until a human happens to look. Both are real, smaller gaps than what existed before this pass, not new ones introduced by it.
