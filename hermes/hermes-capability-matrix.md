# Hermes Capability Matrix

Status: Active
Owner: Jobfynder-Infra
Purpose: Simple progress scoreboard for Hermes capabilities

---

## Reconciliation note — 2026-08-20

This file was last substantively updated 2026-07-14 and had drifted badly from the running service — several capabilities marked "Planned" were actually live, and the previous version had rows appended at the bottom instead of the table being edited in place, creating direct contradictions (e.g. "Resume Parsing: Planned" near the top and "HERMES-800 Resume Builder: Closed" at the bottom, both about the same capability). This version reconciles the table against `hermes-architecture-frozen-v1.md` (2026-08-15, verified against the running service) and the actual router registrations checkpointed to git the same day. **Follow the Rule below from now on — edit rows in place, don't append.**

---

## 1. Status Legend

| Status | Meaning |
|---|---|
| ✅ Production Baseline | Working and usable in production baseline |
| 🚧 In Progress | Started, but not complete |
| ⏳ Planned | Approved, not started |
| 🧪 Testing | Built, under validation |
| ❌ Blocked | Waiting on decision, access, or dependency |
| 🗑️ Deprecated | No longer used |

---

## 2. Current Capability Scoreboard

| Stream | Capability | Status | Notes |
|---|---|---|---|
| HERMES-000 | Architecture & Governance | ✅ | Production baseline docs created and pushed |
| HERMES-100 | Access Control & RBAC | ✅ | Token-based RBAC enabled and validated |
| HERMES-100 | API Version Consistency | ✅ | Central Hermes version used in health and parser responses |
| HERMES-100 | Docker Build Hygiene | ✅ | .dockerignore added and validated |
| HERMES-100 | Smoke Test Script | ✅ | Deployment smoke test added and validated |
| HERMES-100 | Deployment Runbook | ✅ | Simple deployment and smoke-test runbook added |
| HERMES-100 | RBAC User Management | ✅ | Server-side user add/list/disable script added |
| HERMES-100 | Core Platform Review | ✅ | Production baseline complete after final smoke test, repo check, and Engineering Memory update |
| HERMES-200 | Parse Jobs | ✅ | `/understanding/parse-text`, `/v1/jobs/parse` — deterministic first, confidence-gated LLM fallback |
| HERMES-200 | Parse Resumes | ✅ | `/understanding/parse-text`, `/understanding/parse-file` — same pattern |
| HERMES-200 | Parse Recruiter Emails | ✅ | Closed 2026-08-21 — see HERMES-850 rows below and `hermes/HERMES-850-email-parsing-foundation.md` |
| HERMES-200 | Parse Telegram Messages | ✅ | Only channel with live credentials; webhook receiver live (`/channels/telegram/webhook`) |
| HERMES-200 | Parse WhatsApp Messages | ⏳ | Contract normalized and ready (`/providers/whatsapp/*`), credentials not yet provisioned |
| HERMES-300 | Engineering Memory | ✅ | Production baseline complete (this repo's own automation, separate from candidate/company memory below) |
| HERMES-300 | Product Memory | ⏳ | Planned |
| HERMES-300 | Recruiter Memory | ⏳ | Planned |
| HERMES-300 | Company Memory | ⏳ | Planned |
| HERMES-300 | Consultant Memory | ⏳ | Planned |
| HERMES-300 | Conversation Memory | ⏳ | Planned — note: conversation *compression* for prompt context is built (`/context/conversation/compress`), which is a different capability from durable conversation memory |
| HERMES-400 | Intent Understanding | ✅ | `/v1/messages/understand` — deterministic keyword/regex classifier, no LLM |
| HERMES-400 | Duplicate Detection | 🚧 | Submission-scoped duplicate detection built into `/submissions/evaluate`; general cross-entity `entity.resolve` (Users/Candidates/Jobs/Companies) not built |
| HERMES-400 | Taxonomy Suggestion Queue — persistence + fuzzy hints | ✅ | Added 2026-08-20 (branch `feature/hermes-400-taxonomy-suggestion-queue`). Was previously stateless — every unmatched term was re-suggested on every occurrence with nothing stored. Now deduped and persisted (`GET /understanding/taxonomy/suggestions/queue`, sorted by occurrence count), with a fuzzy "did you mean" hint (rapidfuzz) attached to likely formatting variants. Approve/reject endpoints added; approving writes to a runtime overlay that normalization picks up immediately, no restart. 5/5 checks pass, all 7 prior HERMES-400 checks still pass unmodified |
| HERMES-400 | Taxonomy near-duplicate auto-approval | ✅ | Added 2026-08-21, same branch. Product decision: a term scoring ≥92% similarity (`fuzz.ratio`) against something already in the taxonomy is auto-added as an alias with no human step — it's the same skill/title, just spelled differently. Anything below that still requires review. This is a deliberate, explicit narrowing of "never auto-approved" (not a removal of it) — every non-near-duplicate term still needs a human. Also fixed a real scoring bug found while calibrating: the original scorer (`fuzz.WRatio`) falsely scored "Prompt Engineer" as 85.5% similar to "Site Reliability Engineer" (shared only the word "Engineer") — switched to `fuzz.ratio`, verified empirically against several real and false-positive cases. Threshold is env-overridable (`HERMES_TAXONOMY_AUTO_APPROVE_THRESHOLD`), no redeploy needed to retune. 4/4 new checks pass, full regression (9 HERMES-400 + 3 HERMES-850 checks) still passes |
| HERMES-400 | Taxonomy version history | ⏳ | Still not built. The snapshot endpoint reports a static version *label* (e.g. `jobfynder_canonical_skills_v1`), not a changelog of what/when/why/who — the doc's original §4.6 ambition ("what changed, when, why, which source, approved or seeded") is unmet. Not addressed in the 2026-08-20 suggestion-queue work; the `approved` event does emit via `emit_event()` but nothing aggregates that into a browsable history yet |
| HERMES-400 | Taxonomy review UI | ⏳ | Still not built. The 2026-08-20 work added the API (queue/approve/reject endpoints) a UI could call, but no UI exists — review currently means calling the API directly |
| HERMES-400 | Matching Engine | ✅ | `/matching/resume-to-job` — deterministic weighted scorer (skills/experience/work-auth/location), no LLM |
| HERMES-400 | Trust Scoring | ⏳ | Planned — deliberately deferred; Trust/Network frontend is still mockup-only, backend intentionally not built against a mockup UI |
| HERMES-400 | Relationship Intelligence | ⏳ | Planned — same reason as Trust Scoring |
| HERMES-500 | GitHub Webhook Automation | ✅ | Used by Engineering Memory |
| HERMES-500 | Failure Alerts | ✅ | Telegram and email alerts complete |
| HERMES-500 | Scheduled Jobs | ⏳ | Planned |
| HERMES-600 | GitHub Integration | ✅ | Production baseline for Engineering Memory |
| HERMES-600 | n8n Integration | ✅ | Production baseline for Engineering Memory |
| HERMES-600 | Portkey Integration | 🗑️ | **Removed 2026-08-20.** Superseded by LiteLLM + Langfuse — see row below and `hermes-architecture-frozen-v1.md` Addendum §14 |
| HERMES-600 | LiteLLM + Langfuse Integration | ✅ | Sole LLM path as of this reconciliation. All 38 Langfuse-hosted prompts route through LiteLLM router aliases (`generate-small`, `extract-fast`, `reasoning-small`), currently backed by `anthropic/claude-haiku-4-5`. `only_hermes_may_call_litellm` enforced — Core and Frontend never hold a LiteLLM key |
| HERMES-700 | Multi-Agent Runtime | ✅ | Closed (`feature/hermes-700-multi-agent`, tag `hermes-700-foundation-v1`). Dry-run only by design — agents analyze/recommend/draft, never execute high-risk actions automatically |
| HERMES-750 | Prompt Runtime Foundation | ✅ | Closed foundation (tag `hermes-750-prompt-runtime-v1`), rewritten for LiteLLM 2026-08-21 — see `hermes/HERMES-750-litellm-prompt-runtime-foundation.md`. Dry-run-first, RBAC-protected (`agents:run`), safety-checked before every call. A wrong Langfuse API key and an N+1 performance issue (33s cold-cache prompt fetch) were found during that rewrite — both now fixed: key rotated, fetch made concurrent (33.59s → 7.55s, verified live) |
| HERMES-800 | Resume Builder Intelligence | ✅ | Closed foundation (tag `hermes-800-resume-builder-foundation-v1`): deterministic analysis, dry-run suggestions, taxonomy normalization, tailoring, quality checks, human review. Feedback analysis (`/resume-builder/feedback/analyze`) and ATS-specific rules added after this closure — not yet reflected in a doc revision |
| HERMES-850 | Email Parsing — deterministic parse + routing | ✅ | Verified: mailbox-based routing (`hotlists@`/`requirements@`), deterministic hotlist and job-requirement parsing with confidence scoring, full email-to-draft integration. 10/10 unit checks + full integration check pass (`scripts/hermes-850-email-parsing-check.py`, `scripts/hermes-850-email-integration-check.py`) |
| HERMES-850 | Email Parsing — Gmail connector | 🚧 | Normalizer built and tested (7/7 checks, `scripts/hermes-850-gmail-graph-provider-check.py`), registered as a contract provider (`GET /providers/gmail/status`, `POST /providers/gmail/push`). Not live: no Google Cloud OAuth app registered, no credentials, and the authenticated fetch-from-Gmail-API step is not implemented — only acknowledges Pub/Sub push notifications today. Branch `feature/hermes-850-gmail-graph-providers` |
| HERMES-850 | Email Parsing — Microsoft Graph connector | 🚧 | Same status as Gmail above, for Office 365. Includes the Graph subscription validation-token handshake. Not live: no Azure AD app registered, no credentials, fetch-from-Graph-API step not implemented. Branch `feature/hermes-850-gmail-graph-providers` |
| HERMES-850 | Email Parsing — generic inbound webhook | ✅ | `POST /providers/email/webhook` — works for any provider that can send Jobfynder's own HMAC-signed payload shape directly (e.g. a custom relay). `email_provider_status().configured` is `false` until a real sender is wired to it |

---

## 3. Built but not yet assigned an official module number

The following capabilities exist in the running service (verified live 2026-08-15, checkpointed to git 2026-08-20) but were never given a HERMES-8xx/9xx module number or a closure doc under the pattern this repo requires. Flagging so the team can assign numbers and write the missing docs rather than let this list grow silently:

| Capability | Routes | Notes |
|---|---|---|
| Context Cards | `/context/candidate-card/build`, `/context/job-card/build`, `/context/relationship-card/build`, `/context/conversation/compress` | The enforcement mechanism behind "raw documents never reach the LLM directly" — see `hermes-architecture-frozen-v1.md` §5 |
| Broadcast Extraction | `/broadcast/requirement/extract`, `/broadcast/hotlist/extract` | Upstream of Core's feed/broadcast delivery; Hermes does not call Centrifugo (§7) |
| Runtime Cache | `/runtime/cache/stats` | In-process TTL cache, 24h, resume/JD/profile-import parse results only. No dedicated Redis for Hermes yet — open follow-up decision |
| Submission Intelligence Extraction | `/submissions/tracker-update/extract`, `/submissions/status/extract` | Deterministic phrase-matching first, LLM fallback below 0.70 confidence |
| Messaging Actions Extraction | `/v1/messages/actions/extract` | Deterministic phrase-matching first, `jf.messaging.actions.extract` fallback |
| Understanding LLM Fallback | (internal to `/understanding/parse-text`, `/understanding/parse-file`) | Confidence-gated, single-attempt fallback — no retry loops |

**Recommendation:** assign these a module number (e.g. HERMES-825 or similar) and close them out properly, since `hermes-architecture-frozen-v1.md` already documents them in detail — the closure doc would mostly be a matter of extracting and formatting what's already written there.

---

## 3a. Reconciliation note — 2026-08-20 (later same day)

HERMES-850 rows above updated after building and verifying the Gmail and Microsoft Graph connectors. Parsing itself (the hard, judgment-heavy part — deciding what's a candidate record vs. a job requirement, extracting fields, scoring confidence) was already built, committed, and verified before this update; what was missing was getting real email *into* that parser. Two of three intake paths (Gmail, Graph) are now code-complete and tested but not live — they need OAuth credentials, which is a product/infra decision (which Google Cloud project, which Azure tenant) still pending, not an engineering gap.

**Important limit, not yet resolved:** parsed output currently lands as a draft object inside Hermes's own storage (`/drafts/{draft_id}`), not directly in Jobfynder's production database. Whether/how Core consumes these drafts and turns them into real Candidate/Job records is part of the in-progress Core↔Hermes integration (`feature/hermes-core-integration` on the Core repo) — not confirmed built as of this note. Don't read "HERMES-850 parsing: ✅" as "emails become database records automatically" — that last mile is a separate, currently-open question.

## 4. Rule

Every Hermes improvement should update this matrix.

If a capability changes status, **edit the existing row** and commit it. Do not append a new row for a capability that already has one — that's how this file went inconsistent between 2026-07-14 and 2026-08-20.

---

## 5. Next Target

Current focus: assign module numbers and closure docs to the unnumbered capabilities in §3 (Context Cards, Broadcast, Runtime Cache, Submission/Messaging extraction) — HERMES-850 closed 2026-08-21.
