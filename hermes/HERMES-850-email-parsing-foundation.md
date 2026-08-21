# HERMES-850 — Email Parsing Foundation

Status: Closed (foundation) — live provider wiring intentionally deferred, see §7
Code Repository: /opt/hermes
Final Code Branches:
- `feature/hermes-850-email-parsing` — deterministic parsing and routing (commits `5f08c22`, `fd2f088`)
- `feature/hermes-850-gmail-graph-providers` — Gmail and Microsoft Graph connectors (commit `0dce803`)
Documentation Repository: /opt/jobfynder-docs
Closed: 2026-08-21

---

## 1. Goal

Parse hotlist and job-requirement emails automatically, without an LLM, and route them into the same intake pipeline every other channel uses.

## 2. What's built and verified

### 2.1 Deterministic parsing (`app/email_parsing/`)

- `parsers.py` — `parse_hotlist_email()` parses table-formatted and freeform hotlist emails into consultant records (name, skills, experience, location, work authorization, rate), with per-record confidence scoring and review-flagging. `parse_requirement_email()` does the same for job-requirement emails, splitting multi-requirement emails into sections.
- `routing.py` — `classify_recipient_mailbox()` routes by recipient address (`hotlists@jobfynder.com` → hotlist, `requirements@jobfynder.com` → job_description), rejecting ambiguous or foreign-domain matches rather than guessing.
- No LLM in the parsing path itself — `PARSER_METADATA["uses_llm"] = False`.

### 2.2 Pipeline integration

Wired into the same intake pipeline every channel uses, not a side path:

```text
Inbound email
  -> normalize_*_payload() (provider-specific, see §2.3)
  -> classify_recipient_mailbox()
  -> ChannelIntakeRequest(channel="email", ...)
  -> process_channel_intake() (app/channels/service.py)
      -> detect_document_kind()
      -> understand_document() (HERMES-200)
      -> parse_email_business_records() (email-specific business parsing)
      -> confidence-gated ChannelIntakeResponse
```

### 2.3 Provider connectors

| Provider | Status | What exists |
|---|---|---|
| Generic webhook (`/providers/email/webhook`) | Contract, not live | `normalize_email_payload()` + HMAC signature verification (`require_comm_signature`) — works for any sender that can produce Jobfynder's own signed payload shape |
| Gmail | Contract, not live | `normalize_gmail_message()` (decodes real Gmail API `users.messages.get` resources, including base64url body extraction) + Pub/Sub push endpoint (`POST /providers/gmail/push`) that acknowledges mailbox-change notifications |
| Microsoft Graph (Office 365) | Contract, not live | `normalize_graph_message()` (handles HTML body stripping) + webhook endpoint implementing Graph's required subscription validation-token handshake |

All three normalize into the identical shape, so the deterministic parser and pipeline above don't know or care which provider the email came from.

## 3. API surface

| Method | Route | Purpose |
|---|---|---|
| POST | `/providers/email/webhook` | Generic signed email intake |
| GET | `/providers/gmail/status` | Gmail provider configuration status |
| POST | `/providers/gmail/push` | Cloud Pub/Sub push endpoint |
| GET | `/providers/microsoft-graph/status` | Graph provider configuration status |
| POST | `/providers/microsoft-graph/webhook` | Graph change-notification webhook (handles validation handshake) |
| POST | `/channels/intake` | Generic channel intake (email flows through here after provider normalization) |

## 4. Verification

Verified live, not just written — 13/13 checks pass across three scripts:

- `scripts/hermes-850-email-parsing-check.py` (10 checks) — mailbox routing, hotlist parsing (table + freeform), requirement parsing, confidence scoring, no-LLM guardrail.
- `scripts/hermes-850-email-integration-check.py` — full email-to-draft integration, including duplicate-intake protection.
- `scripts/hermes-850-gmail-graph-provider-check.py` (7 checks) — Gmail message normalization (base64url decoding, mailbox routing from headers), Pub/Sub envelope decoding, Graph message normalization (plain text and HTML), both providers' contract status.

Full regression confirmed 2026-08-21: all HERMES-400 and HERMES-850 checks pass together, 103 → 106 OpenAPI paths after adding the Gmail/Graph routes, app imports cleanly.

## 5. Bug found and fixed during this work

The uncommitted state that became this module's foundation (`feature/hermes-850-email-parsing`) was sitting on `jobfynder-intel-01` with **no git history or backup** until checkpointed 2026-08-20 (`checkpoint/2026-08-20-frozen-v1-uncommitted-state`). Not a code bug, but a real operational risk that's now closed.

## 6. What HERMES-850 does *not* do

- **Does not write to Jobfynder's production database.** Parsed output becomes a draft object inside Hermes's own storage (`/drafts/{draft_id}`, `app/drafts/`), not a live Candidate or Job record. Whether/how Core consumes these drafts is part of the separate, in-progress Core↔Hermes integration — not confirmed built as of this closure. Do not read "HERMES-850: closed" as "emails become database records automatically."
- **Does not auto-add unrecognized skills to the taxonomy.** Extracted skills go through HERMES-400 normalization; unrecognized terms follow the same suggestion-queue path as any other source (see `hermes-capability-matrix.md` HERMES-400 rows).

## 7. Deliberately deferred: live provider credentials

No real email flows through this yet. This was a product decision (2026-08-20), not an oversight: Jobfynder uses both Gmail and Office 365 mailboxes for hotlist/requirement email, and connecting either requires registering an OAuth application (Google Cloud Console for Gmail, Microsoft Entra/Azure AD for Graph) and granting it access to the actual receiving mailbox — steps that need a human with console access, not something to fabricate. The connector code (§2.3) is ready and tested against realistic sample payloads; only the authenticated fetch-from-provider-API step (calling Gmail's/Graph's API to retrieve a message after a push notification arrives) remains unimplemented, since it can't be tested without real credentials.

**To go live:** register the OAuth apps, set `HERMES_GMAIL_CLIENT_ID`/`HERMES_GMAIL_CLIENT_SECRET`/`HERMES_GMAIL_REFRESH_TOKEN` and `HERMES_MS_GRAPH_CLIENT_ID`/`HERMES_MS_GRAPH_CLIENT_SECRET`/`HERMES_MS_GRAPH_TENANT_ID` (all present as blank placeholders in `.env.example`), then implement the fetch call in `app/routers/gmail_provider.py`'s `/push` handler and `app/routers/microsoft_graph_provider.py`'s `/webhook` handler using those credentials.

## 8. Closure decision

HERMES-850 closes as a production-safe email parsing *foundation* — deterministic, verified, provider-agnostic. It is explicitly not closed as a live integration; §7 is the real remaining work, gated on a credential decision outside engineering's control.
