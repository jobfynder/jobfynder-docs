# COMM-500 — Ingress & Intake

Status: Foundation Complete, live in production
Source: `comm_gateway/main.py`, `comm_gateway/hermes_client.py`
Live-verified: 2026-08-21 (re-verified after the 2026-08-21 resilience fix, commit `0c33580` on `jobfynder-infra`)

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

## 4. What is NOT built

- **No idempotency check on the COMM side.** `HERMES-450-channel-intake.md` documents idempotency as a *Hermes-side* feature (channel + source_message_id dedup). If Telegram retries a webhook delivery (which it does on timeout), COMM-1 will re-normalize and re-forward it — dedup, if it happens, happens only after the request reaches Hermes. Unaffected by the 2026-08-21 fix.
- **No queueing.** Every webhook is handled synchronously, inline, in the request/response cycle — including the outbound Telegram delivery. RabbitMQ is running on the same server and is still not used for this (see `COMM-100` §6 and `COMM-300-900-1000-infrastructure-posture.md`) — the 2026-08-21 fix makes failure visible and recoverable-by-retry-from-Telegram, it does not add COMM-side queueing or a dead-letter store.
- **No dead-letter path.** A failed `send_to_hermes()` call now returns a structured error instead of crashing, but nothing persists it for replay — if Hermes was down, that message's content isn't retried automatically once Hermes comes back (only if Telegram itself redelivers the webhook).

## 5. Production Ready assessment

**Closer, but still NO.** The signed contract is solid and live-verified. The 2026-08-21 fix (commit `0c33580`) closed the worst gap — a slow/unreachable Hermes call no longer crashes the request and the user now gets an explicit "could not process" reply instead of silence. What remains: no retry, no queueing, no idempotency on this side of the boundary. Given RabbitMQ is already running unused on the same box, the most direct next step is still to route inbound webhook processing through it rather than handling everything inline — that would address the queueing, retry, and dead-letter gaps in one move. Not attempted in this pass; it's a design change (new worker process, queue schema), not a bug fix.
