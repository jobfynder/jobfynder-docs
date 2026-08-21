# COMM-410 — Telegram Channel Adapter

Status: Foundation Complete, live in production
Source: `comm_gateway/telegram.py`, `comm_gateway/telegram_outbound.py`, `comm_gateway/main.py`
Live-verified: 2026-08-21

---

## 1. Inbound path

`POST /providers/telegram/webhook` (see `COMM-500-ingress-intake.md` for the full request/response contract). Auth: Telegram's `X-Telegram-Bot-Api-Secret-Token` header is compared against `TELEGRAM_WEBHOOK_SECRET` — mismatch or missing secret returns 403/503 respectively.

`normalize_telegram_update()` converts a raw Telegram `Update` payload into the canonical COMM intake shape:

```json
{
  "channel": "telegram",
  "source_message_id": "<message_id or update_id>",
  "sender": {"sender_id": "...", "sender_name": "...", "username": "..."},
  "conversation_id": "<chat.id>",
  "content_type": "text | file | mixed",
  "text": "...",
  "attachments": [{"type": "document", "file_id": "...", "file_name": "...", "mime_type": "...", "file_size": "..."}],
  "metadata": {"telegram_update_id": ..., "telegram_chat_type": "...", "telegram_chat_id": ...}
}
```

**Gap:** only `document` attachments are extracted. Telegram photo, voice, video, and sticker message types are not handled — a message containing only a photo would normalize with `content_type: "text"` and empty `text`, silently losing the attachment. Not confirmed whether this has caused real data loss; worth a live test.

## 2. Outbound path

`deliver_hermes_telegram_response()` takes whatever Hermes returned (via `/internal/comm/intake`) and turns it into one or more Telegram messages back to the same chat:

- If Hermes's response includes structured `outbound_messages` (a list of `{text, reply_markup}` objects), each is sent as its own message.
- Otherwise, falls back to a generic templated success message: `"Jobfynder received your {document_kind}."` plus a `"Draft created: {draft_type}"` line if applicable.
- If Hermes returned a non-200 status, the user gets a fixed retry message instead of an error leak.

**Safety rule enforced in code (explicit comment):** *"The current webhook chat is always authoritative. COMM does not allow a downstream response to redirect to another chat."* — `chat_id` always comes from the inbound webhook, never from the Hermes response, closing an obvious spoofing/redirect vector.

## 3. Message chunking (`telegram_outbound.py`, added 2026-08-21 per commit `0d7616a`)

Telegram limits message text to ~4096 characters. `split_telegram_text()` splits on paragraph breaks first, then line breaks, then spaces, then a hard cutoff — in that preference order, to avoid breaking mid-word where avoidable. Safe limit used: 3800 chars (with another 100 reserved for the "Part X/Y" prefix on multi-part messages). Reply-markup buttons are attached only to the final chunk, so buttons don't repeat on every part of a long message.

This was a real, fixed bug — the commit message is literally "fix(comm): split long Telegram responses safely," implying long Hermes responses were previously either truncated or failed to send before this fix. No prior incident report exists in this repo to cite specifics; flagged here as evidence of an iterative fix, not a hypothetical.

## 4. Live verification (2026-08-21)

```
GET /providers/telegram/status
→ {"provider":"telegram","configured":true,"has_bot_token":true,"has_webhook_secret":true,"has_hermes_secret":true,"hermes_base_url":"https://hermes.jobfynder.com"}
```

Live container logs confirm real inbound traffic patterns consistent with a webhook under active internet scanning (unrelated scanner probes for `/.env`, `/.git/HEAD`, `/terraform.tfstate` — all correctly 404'd, no info disclosure) alongside legitimate internal health checks.

## 5. What is NOT built

- No onboarding-flow state machine visible in this adapter beyond generic reply delivery — session/conversation state, if it exists, lives entirely on the Hermes side (per HERMES-450's "conversation session engine"). COMM-410 itself is stateless.
- No retry/backoff on the outbound Telegram API call (`send_telegram_message` is a single `httpx` POST with a 20s timeout, no retry wrapper).
- No delivery confirmation tracking — if `send_telegram_message` fails, the result is returned to the caller but nothing persists or retries it.
