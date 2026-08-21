# Hermes Complete Developer Guide

Status: Active — companion to `hermes-architecture-frozen-v1.md` (the "why"), this is the "how"
Server: jobfynder-intel-01 (`https://hermes.jobfynder.com` externally)
Audience: Jobfynder backend/frontend developers integrating Hermes

This is the single entry point for integrating with Hermes. For the prompt catalog in full detail, see `hermes-parsing-and-prompts-api-guide.md` §6. For the architectural decisions behind why Hermes is built this way, see `hermes-architecture-frozen-v1.md`.

---

## 1. What Hermes is, in one paragraph

Hermes is Jobfynder's intelligence layer, sitting between Core and any LLM. It parses documents, normalizes staffing terminology, matches candidates to jobs, and validates workflow transitions — almost all of it deterministic and free. It only calls an LLM when deterministic confidence is genuinely too low to trust, or when the task is inherently generative (writing a summary, drafting a message). Every LLM call is traced in Langfuse. Core never talks to an LLM directly — only Hermes does.

---

## 2. Getting started

**Base URL**: `https://hermes.jobfynder.com` (or `http://localhost:8000` on-box)

**Auth**: `Authorization: Bearer <token>` on every endpoint except `/health`. Ask Jobfynder-Infra for a token scoped to the permissions you need. Note: `/understanding/*` and `/submissions/evaluate*` currently have no RBAC check at all — this is a known inconsistency, not a feature to rely on (see frozen architecture §11).

**Two response shapes exist** (deliberate, not accidental — see frozen architecture §6):
- **Legacy shape**: endpoints built before 2026-08-15 keep their own typed response (e.g. `UnderstandingResult`, `ResumeTailoringResponse`). Documented per-endpoint below.
- **Canonical envelope**: everything built from 2026-08-15 onward returns this exact shape:
```json
{
  "request_id": "req_...", "capability": "hermes.context.build_candidate_card",
  "execution_mode": "hermes_only", "confidence": 0.9, "llm_required": false,
  "llm_prompt_name": null, "structured_data": {}, "unresolved_fields": [],
  "warnings": [], "proposed_actions": [], "trace_metadata": {}
}
```
Always check `execution_mode`/`llm_required` (envelope) or `decision`/`fallback.llm_fallback` (legacy) to know whether a call actually cost money — never assume from HTTP status alone.

**Errors**: business-logic outcomes (blocked, failed, needs_review) return HTTP 200 with the outcome in the body, not an HTTP error. Only auth failures (401/403) and genuine server errors (500) use non-200 status. Always check the decision/execution_mode field.

---

## 3. Resume Builder page

Powers: resume editing, "Tailor to Job," "Feedback & Suggestions," ATS targeting.

| Endpoint | Use case |
|---|---|
| `POST /understanding/parse-text` (`document_kind: resume`) | Parse raw resume text into structured fields. Auto-escalates to LLM if confidence < 0.70. |
| `POST /understanding/parse-file` | Same, for uploaded PDF/DOCX/TXT. |
| `POST /resume-builder/summary/suggest` | AI-drafted professional summary. Builds a Candidate Card internally first — never sends raw text straight to the LLM. `dry_run` by default. |
| `POST /resume-builder/bullets/suggest` | AI-rewritten experience bullets (`jf.resume.experience.rewrite`). |
| `POST /resume-builder/skills/normalize` | Taxonomy-normalize a skill list (JS → JavaScript, etc). Deterministic, free. |
| `POST /resume-builder/tailor` | Deterministic skill-gap analysis vs. a target job. Pass `target_ats` (`workday`, `oracle_taleo`, `kenexa_brassring`, `icims`, `lever`, `greenhouse`) for ATS-specific formatting guidance (static ruleset, not LLM-generated). |
| `POST /resume-builder/feedback/analyze` | Powers "Feedback & Suggestions" tab — missing sections, unquantified impact, weak language, incomplete work auth, missing keywords vs. a target job. **Fully deterministic, zero LLM cost.** Never fabricates a metric — asks the user to supply one if missing. |
| `POST /resume-builder/quality/analyze` | Completeness/provenance scoring for a structured resume document. |
| `POST /resume-builder/analyze` | General safety/fabrication analysis for a resume document. |
| `GET /resume-builder/policy` | Read the active safety policy (no-fabrication rules). |
| `GET /resume-builder/health` | Module health/config. |

**For AI-polishing Education/Certifications sections** (UI has "AI" buttons for these, previously unwired): call `POST /prompts/run` with `prompt_id: "jf.resume.section.polish"`, `variables: {section_type, raw_content, role}`.

---

## 4. Job Board page

Powers: job listings, search, "why this matches you."

| Endpoint | Use case |
|---|---|
| `POST /v1/jobs/parse` | Parse a job posting into structured fields. Real confidence scoring (fixed from a prior hardcoded `1.0` bug), auto-escalates to `jf.jobs.jd.extract` below 0.6. |
| `POST /understanding/parse-text` (`document_kind: job_description`) | Same underlying capability via the more general endpoint — use this if you also need taxonomy signals/quality metrics in the response. |
| `POST /matching/resume-to-job` | Deterministic match score: required skills 55%, preferred 15%, experience 15%, work auth 10%, location 5%. Returns `submit`/`review`/`reject`. No LLM. |
| `POST /matching/resume-to-job/from-understanding` | Same, chained directly from `/understanding/parse-text` output. |
| `GET /matching/policy` | Read the active scoring weights/thresholds. |

**For "why does this job match me"**: `POST /prompts/run` with `jf.jobs.fit.explain` — explains an *existing* deterministic score, never generates its own.

---

## 5. Job Tracker page

Powers: submission pipeline, stage tracking, duplicate-risk warnings, follow-ups.

| Endpoint | Use case |
|---|---|
| `POST /submissions/evaluate` | Core workflow engine — given a current stage + event, returns recommended stage, follow-up requirement, conflicts (duplicate risk, invalid transitions — each with `resolution_steps`), and next actions. |
| `POST /submissions/evaluate/from-handoff` | Same, but accepts raw Understanding/Matching output directly — chains parse → match → workflow in one call. |
| `GET /submissions/workflow-policy` | The 14-stage lifecycle (`discovered` → ... → `placed`), allowed transitions, terminal stages. |
| `POST /submissions/tracker-update/extract` | Parse a freeform message ("client wants to interview next week") into a proposed stage update. Deterministic phrase-matching first, `jf.job-tracker.update.extract` fallback below 0.70 confidence. Returns the canonical envelope. |
| `POST /submissions/status/extract` | Same pattern for submission status specifically. |

**For "Prepare Interview"**: `POST /prompts/run` with `jf.job-tracker.interview.prep` — consultant-facing prep brief (distinct from `jf.screening.questions.generate`, which is the *recruiter's* question generator).

**For "Review Offer"**: `POST /prompts/run` with `jf.job-tracker.offer.analyze` — flags missing info, suggests negotiation points, never invents market-rate figures it wasn't given.

---

## 6. Messenger

Powers: inbound message routing, reply drafting, action extraction.

| Endpoint | Use case |
|---|---|
| `POST /v1/messages/understand` | Classify a message's intent (`JOB`/`RESUME`/`HOTLIST`/`QUESTION`/`UNKNOWN`) and auto-route to the matching parser. Deterministic keyword+regex classifier, no LLM. Recognizes `"<role> available"` phrasing (fixed from an earlier gap). |
| `POST /v1/messages/actions/extract` | Extract actionable items ("send the resume," "schedule a call") from a message list. Deterministic phrase-matching first, `jf.messaging.actions.extract` fallback. Returns the canonical envelope. |
| `POST /context/conversation/compress` | Token-budget-compress a message history into a bounded context object — use before passing conversation history to any generative prompt. |

**For drafting a reply**: `POST /prompts/run` with `jf.messaging.reply.draft`. **For summarizing a thread**: `jf.messaging.conversation.summarize`.

---

## 7. Network & Broadcasting

Powers: the live feed, hotlist/requirement broadcasts, connection requests, relationship tracking. **Frontend is currently mockup-only** — these endpoints are ready for backend wiring.

| Endpoint | Use case |
|---|---|
| `POST /broadcast/requirement/extract` | Parse a job-requirement broadcast. Deterministic key:value line parser (`Title: ...`, `Rate: ...`) first; `jf.broadcast.requirement.extract` fallback for unstructured text. Canonical envelope. |
| `POST /broadcast/hotlist/extract` | Parse a bench/hotlist broadcast (numbered/bulleted consultant list). Deterministic per-line rate/experience/skill detection first; `jf.broadcast.hotlist.extract` fallback. |
| `POST /context/relationship-card/build` | Pack pre-summarized interaction history into a bounded card for relationship prompts — does not itself summarize raw messages. |

**For "Request Introduction"**: `jf.introductions.request.draft`. **For "Connect Now" / re-engaging a dormant contact**: `jf.network.connection-request.draft` (reuse for both — pass prior interaction summary as `shared_context` for re-engagement). **For relationship summaries / next-action suggestions**: `jf.network.relationship.summarize` / `jf.network.relationship.next-action`.

**Recommended, not yet built**: "People You May Know" should be a deterministic recommender (mutual-connection count + taxonomy overlap), not an LLM call — no prompt needed.

**Real-time delivery**: Hermes does not call Centrifugo. See frozen architecture §7 — Core owns publishing structured broadcast output to Centrifugo channels.

---

## 8. Onboarding

Powers: signup flow, profile import (LinkedIn/resume paste), identity verification.

| Endpoint | Use case |
|---|---|
| `POST /onboarding/session` | Start an onboarding session (role, channel). |
| `POST /onboarding/profile/draft` | Parse imported profile text into a draft profile. **Was crashing with a 500 on every call prior to 2026-08-15 — fixed.** Deterministic resume-shaped parsing first, `jf.onboarding.profile-import.extract` fallback below 0.70 confidence, cached 24h. |
| `GET /onboarding/profile/draft/{session_id}` | Retrieve a draft. |
| `POST /onboarding/profile/publish/{session_id}` | Publish (requires role + headline present). |
| `POST /onboarding/verification/draft` | Identity/company verification draft — deterministic trust-signal scoring (public email domain check, missing fields), no LLM. |

---

## 9. Taxonomy (cross-cutting)

Used by nearly every other module. Deterministic, in-process cached (effectively free after first load).

| Endpoint | Use case |
|---|---|
| `GET /understanding/taxonomy/skills` | Full skill list + aliases. |
| `GET /understanding/taxonomy/skills/canonical` / `/aliases` | Canonical registry / alias mapping. |
| `GET /understanding/taxonomy/job-titles` / `/job-title-aliases` | Same for job titles. |
| `GET /understanding/taxonomy/snapshot` | Full versioned snapshot. |
| `POST /understanding/taxonomy/normalize` | Normalize a list of skills/titles to canonical form. |
| `POST /understanding/taxonomy/extract-signals` | Pull skills/titles out of freeform text. |
| `POST /understanding/taxonomy/suggestions` | Queue an unrecognized term for human review — **never auto-approved**. |

---

## 10. Context Cards (cross-cutting)

The enforcement layer — see frozen architecture §5 for why this exists. Use these instead of passing raw text/records directly into any generative prompt call.

| Endpoint | Use case |
|---|---|
| `POST /context/candidate-card/build` | From raw `source_text` (auto-parsed via Hermes first) or already-structured resume data → `CandidateCardV1`. |
| `POST /context/job-card/build` | Same for jobs → `JobCardV1`. |
| `POST /context/relationship-card/build` | Bounded relationship summary card. |
| `POST /context/conversation/compress` | Token-budget-compressed conversation context. |

All four return the canonical envelope with `execution_mode: "hermes_only"` — card building never itself calls an LLM.

---

## 11. Prompt Runtime — generative capabilities

38 prompts, all sourced live from Langfuse. Full catalog with every prompt's use case and variables: `hermes-parsing-and-prompts-api-guide.md` §6.

| Endpoint | Use case |
|---|---|
| `GET /prompts/registry` | List all prompts + required variables — discover programmatically instead of hardcoding. |
| `GET /prompts/{prompt_id}` | Full detail for one prompt. |
| `POST /prompts/run` | Execute. `mode: "dry_run"` (default) validates rendering with zero cost/call. `mode: "live"` executes for real if the server-wide dry-run default allows it. |
| `GET /prompts/health` | Runtime status, LiteLLM/Langfuse connectivity. |

Every response includes `safety.human_review_required: true` — nothing here should auto-publish or auto-send.

---

## 12. Agents (dry-run only, by design)

Role-based agents (Founder, Recruiter, Bench Sales, Consultant, Engineering, Support) — see frozen architecture / HERMES-700 for the safety model. Agents can analyze, summarize, recommend, and prepare drafts. They cannot submit candidates, message recruiters, change production data, or take any high-risk action automatically — those stay `needs_review`/blocked into human approval regardless of what's requested.

| Endpoint | Use case |
|---|---|
| `GET /agents/registry` / `/snapshot` | List agents and capabilities. |
| `GET /agents/{agent_id}` | One agent's detail. |
| `POST /agents/dry-run` | Run an agent in dry-run (the only supported mode). |
| `GET /agents/health` | Module health. |

---

## 13. Channels & Providers (inbound integration layer)

Normalizes inbound messages from Telegram, Email, WhatsApp, Slack, Teams, Google Chat, LinkedIn into a common contract before they reach Understanding/Messaging. **Only Telegram is actually configured with live credentials** — the rest are normalized contracts ready for credentials.

| Endpoint | Use case |
|---|---|
| `POST /channels/intake` / `/intake/file` | Unified inbound message/file intake. |
| `GET /channels/supported` / `/health` | What's wired, health status. |
| `POST /channels/telegram/webhook` | Live Telegram webhook receiver. |
| `GET /providers/status` / `/{provider}` | Per-provider configuration status. |
| `POST /providers/{provider}/webhook` | Per-provider inbound webhook (email, WhatsApp, Slack, Teams, Google Chat). |
| `GET /providers/linkedin/authorize` / `/callback` | LinkedIn OAuth flow (foundation ready, credentials pending). |
| `POST /internal/comm/intake` | Signed intake from the COMM-1 server (HMAC-authenticated). |

---

## 14. Integrations (Core handoff layer)

For Jobfynder Core/n8n to call Hermes as a black box without knowing internal capability names.

| Endpoint | Use case |
|---|---|
| `GET /integrations/health` | Health. |
| `POST /integrations/events/normalize` | Normalize an arbitrary integration event envelope. |
| `POST /integrations/events/identity` | Generate idempotency key + payload fingerprint — prevents duplicate processing of replayed webhooks. |
| `POST /integrations/jobfynder/submission-handoff/evaluate` | One-call bridge: Jobfynder integration envelope → normalized event + full submission intelligence evaluation. |
| `GET /integrations/retry-policy` / `POST /integrations/retry-decision` | Deterministic retry/no-retry/needs-review decision for a failed integration call. |

---

## 15. Security & operations

| Endpoint | Use case |
|---|---|
| `GET /security/rbac/status` | RBAC enforcement status, configured user count. |
| `GET /runtime/cache/stats` | In-process cache entry counts (see frozen architecture §8). |
| `GET /health` | Public, no auth. Service liveness. |
| `GET /mission-control`, `/session-brief`, `/workspace` | Internal operational dashboards. |
| `GET/POST /actions`, `/drafts` | Generic action/draft persistence used by several modules internally. |

---

## 16. Full endpoint index

99 endpoints total, live as of 2026-08-15. Grouped by tag — see `GET /openapi.json` for the always-current machine-readable version; this table is a point-in-time snapshot for quick reference.

<details>
<summary>Expand full list</summary>

| Method | Path | Module |
|---|---|---|
| GET | `/access/actions` | Access |
| POST | `/access/authorize` | Access |
| GET,POST | `/actions` | Actions |
| GET,PUT,DELETE | `/actions/{action_id}` | Actions |
| POST | `/agents/dry-run` | Agents |
| GET | `/agents/health` | Agents |
| GET | `/agents/registry` | Agents |
| GET | `/agents/snapshot` | Agents |
| GET | `/agents/{agent_id}` | Agents |
| POST | `/broadcast/hotlist/extract` | Broadcast |
| POST | `/broadcast/requirement/extract` | Broadcast |
| GET | `/channels/health` | Channels |
| POST | `/channels/intake` | Channels |
| POST | `/channels/intake/file` | Channels |
| GET | `/channels/supported` | Channels |
| POST | `/channels/telegram/webhook` | Channels |
| POST | `/context/candidate-card/build` | Context |
| POST | `/context/conversation/compress` | Context |
| POST | `/context/job-card/build` | Context |
| POST | `/context/relationship-card/build` | Context |
| GET | `/drafts` | Drafts |
| GET | `/drafts/{draft_id}` | Drafts |
| POST | `/drafts/{draft_id}/publish` | Drafts |
| GET | `/health` | Core |
| POST | `/integrations/events/identity` | Integrations |
| POST | `/integrations/events/normalize` | Integrations |
| GET | `/integrations/health` | Integrations |
| POST | `/integrations/jobfynder/submission-handoff/evaluate` | Integrations |
| POST | `/integrations/retry-decision` | Integrations |
| GET | `/integrations/retry-policy` | Integrations |
| POST | `/internal/comm/intake` | COMM Internal |
| GET | `/matching/policy` | Matching |
| POST | `/matching/resume-to-job` | Matching |
| POST | `/matching/resume-to-job/from-understanding` | Matching |
| GET | `/mission-control` | Mission Control |
| POST | `/onboarding/profile/draft` | Onboarding |
| GET | `/onboarding/profile/draft/{session_id}` | Onboarding |
| POST | `/onboarding/profile/publish/{session_id}` | Onboarding |
| POST | `/onboarding/session` | Onboarding |
| GET | `/onboarding/session/{session_id}` | Onboarding |
| POST | `/onboarding/verification/draft` | Onboarding |
| GET | `/prompts/health` | Prompt Runtime |
| GET | `/prompts/registry` | Prompt Runtime |
| POST | `/prompts/run` | Prompt Runtime |
| GET | `/prompts/{prompt_id}` | Prompt Runtime |
| GET | `/providers` | Providers |
| POST | `/providers/brightdata/linkedin-profile` | BrightData |
| GET | `/providers/brightdata/status` | BrightData |
| GET | `/providers/email/status` | Email Provider |
| POST | `/providers/email/webhook` | Email Provider |
| GET,POST | `/providers/google-chat/{status,webhook}` | Provider Contracts |
| GET | `/providers/linkedin/authorize` | LinkedIn Provider |
| GET | `/providers/linkedin/callback` | LinkedIn Provider |
| GET | `/providers/linkedin/status` | LinkedIn Provider |
| GET,POST | `/providers/slack/{status,webhook}` | Provider Contracts |
| GET | `/providers/status` | Providers |
| GET,POST | `/providers/teams/{status,webhook}` | Provider Contracts |
| POST | `/providers/telegram/register-webhook` | Telegram Provider |
| GET | `/providers/telegram/status` | Telegram Provider |
| GET,POST | `/providers/whatsapp/{status,webhook}` | Provider Contracts |
| GET | `/providers/{provider}` | Providers |
| POST | `/resume-builder/analyze` | Resume Builder |
| POST | `/resume-builder/bullets/suggest` | Resume Builder |
| POST | `/resume-builder/feedback/analyze` | Resume Builder |
| GET | `/resume-builder/health` | Resume Builder |
| GET | `/resume-builder/policy` | Resume Builder |
| POST | `/resume-builder/quality/analyze` | Resume Builder |
| POST | `/resume-builder/skills/normalize` | Resume Builder |
| POST | `/resume-builder/summary/suggest` | Resume Builder |
| POST | `/resume-builder/tailor` | Resume Builder |
| GET | `/runtime/cache/stats` | Runtime |
| GET | `/security/rbac/status` | Security |
| GET | `/session-brief` | Session Brief |
| POST | `/submissions/evaluate` | Submission Intelligence |
| POST | `/submissions/evaluate/from-handoff` | Submission Intelligence |
| POST | `/submissions/status/extract` | Submission Intelligence |
| POST | `/submissions/tracker-update/extract` | Submission Intelligence |
| GET | `/submissions/workflow-policy` | Submission Intelligence |
| POST | `/understanding/parse-file` | Understanding |
| POST | `/understanding/parse-text` | Understanding |
| POST | `/understanding/taxonomy/extract-signals` | Understanding |
| GET | `/understanding/taxonomy/job-title-aliases` | Understanding |
| GET | `/understanding/taxonomy/job-titles` | Understanding |
| POST | `/understanding/taxonomy/normalize` | Understanding |
| GET | `/understanding/taxonomy/skills` | Understanding |
| GET | `/understanding/taxonomy/skills/aliases` | Understanding |
| GET | `/understanding/taxonomy/skills/canonical` | Understanding |
| GET | `/understanding/taxonomy/snapshot` | Understanding |
| POST | `/understanding/taxonomy/suggestions` | Understanding |
| POST | `/v1/consultants/parse` | Core |
| POST | `/v1/engineering-memory/generate` | Core |
| POST | `/v1/jobs/parse` | Core |
| POST | `/v1/messages/actions/extract` | Core |
| POST | `/v1/messages/understand` | Core |
| GET | `/workspace` | Workspace |

</details>

---

## 17. Related documents

- `hermes-architecture-frozen-v1.md` — the architectural decisions and reasoning behind this guide
- `hermes-parsing-and-prompts-api-guide.md` — full 38-prompt catalog with use cases and variables
- `hermes-blueprint-alignment-review.md` — the original gap analysis that drove this work
- `HERMES-000` through `HERMES-800` — the historical build-log documents for each foundation module
