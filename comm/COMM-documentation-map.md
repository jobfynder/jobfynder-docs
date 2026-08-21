# COMM Documentation Map

Status: Active rule
Owner: Jobfynder-Infra
Mirrors: `hermes/HERMES-documentation-map.md`'s role for the Hermes side.

---

## Main rule

Final readable COMM documentation lives in `jobfynder/jobfynder-docs`, folder `comm/`, on branch `main`. Code lives in `jobfynder/jobfynder-infra`, folder `communication/` — implementation notes may live there temporarily, but it is never the source of truth.

## Official COMM docs

- `comm/COMM-000-architecture-governance.md` — governance, module index, the COMM-1 naming correction
- `comm/COMM-100-core-communication-platform.md` — the comm-gateway service, deployment, config
- `comm/COMM-410-telegram-channel-adapter.md` — the Telegram inbound/outbound adapter (currently the only live channel)
- `comm/COMM-500-ingress-intake.md` — the full webhook → HMAC → Hermes → reply pipeline, cross-checked against the Hermes-side contract
- `comm/COMM-300-900-1000-infrastructure-posture.md` — RabbitMQ/Redis (provisioned, unused), reliability gaps, and operations posture

## Origin

**This entire folder was created 2026-08-21, in one pass, directly against the live COMM-1 server and the `jobfynder-infra` repository.** No COMM documentation existed anywhere before this. See [JOBFYNDER-HERMES-COMM-CANONICAL.md](../JOBFYNDER-HERMES-COMM-CANONICAL.md) for the status matrix these docs feed into, and its §2.3/§5 for why this gap mattered.

## What's covered vs. not

Covered with real evidence: COMM-100 (core platform), COMM-410 (Telegram), COMM-500 (ingress/intake), and the infrastructure posture of COMM-300/900/1000.

**Not covered — no evidence exists, do not write speculative docs for these:** COMM-200 (Identity & Session Layer — no dedicated code found), COMM-600 (external integrations beyond Telegram), COMM-700 (Realtime/Centrifugo — instance exists platform-wide, nothing on COMM-1 touches it), COMM-800 (Communication Workflows beyond what COMM-410 already does). If work starts on any of these, open a new `comm/COMM-nnn-*.md` file the same way HERMES modules are opened — a document at start, closure evidence at the end, no undocumented gap in between.
