# Hermes Architecture — Frozen v1.0

Status: **FROZEN** — 2026-08-15
Owner: Jobfynder-Infra
Supersedes: `Jobfynder_Hermes_Integration_Blueprint_v1.md` + `Jobfynder_Hermes_Capability_Registry_v3.yaml` as the operative reference (those remain the historical design record; this document is the reconciled, as-built-plus-decided source of truth)
Change policy: this document changes only by deliberate amendment, not silently. If implementation diverges from what's written here, that's a bug or a decision to make — not something to quietly drift past.

---

## 1. What "frozen" means here

Everything in this document is one of two things:

- **Decided and built** — verified live against the running Hermes service on jobfynder-intel-01 as of this freeze date.
- **Decided, not yet built** — explicitly marked, with the reason it's deferred.

Nothing in this document is aspirational or unverified. Where the original blueprint described a capability that turned out not to exist, or existed but was broken, that's noted with what was actually found and what was done about it.

---

## 2. Core architecture decision (unchanged from blueprint, validated)

Hermes is the mandatory intelligence control plane between Jobfynder Core and LiteLLM. This decision stands as originally made:

```text
Frontend
  -> Jobfynder Core
  -> Hermes
      -> parse (deterministic first)
      -> normalize (taxonomy)
      -> entity resolve
      -> apply policies
      -> deduplicate
      -> score/match
      -> compress context (Context Cards)
      -> decide whether LLM is required (confidence threshold)
  -> LiteLLM only when required
  -> Hermes validates output
  -> Jobfynder Core persists or executes
  -> Langfuse traces the complete workflow
```

**Governing rule, unchanged:** raw resumes, job descriptions, recruiter messages, profiles, and conversations must not be sent directly to an LLM. Hermes parses first; only unresolved fields or genuinely generative work reaches LiteLLM.

**Access rules, unchanged and enforced:**
- `only_hermes_may_call_litellm: true` — Core and Frontend never hold a `LITELLM_API_KEY`.
- `raw_documents_may_reach_llm: false` — enforced in code as of this freeze via Context Cards (§5).
- `business_state_changes_require_core_authorization: true` — Hermes proposes, Core (with human confirmation where required) executes.

---

## 3. Execution classes (unchanged)

| Class | Meaning |
|---|---|
| **A. Core only** | CRUD, auth, RBAC, payments, notification delivery, file storage. No Hermes, no LLM. |
| **B. Hermes only** | Deterministic: normalization, duplicate detection, scoring, validation. Zero LLM cost. |
| **C. Hermes first, LLM fallback** | Hermes attempts deterministically; escalates to LiteLLM only below a confidence threshold. |
| **D. Hermes context + LLM** | Genuine generation/summarization/explanation. Hermes prepares compact context (Context Cards), LLM generates, Hermes validates output. |

---

## 4. Capability inventory — reconciled (built vs. blueprint)

This supersedes the capability registry YAML's aspirational list with what's actually true today.

### Built and verified live

| Capability | Class | Endpoint(s) |
|---|---|---|
| `understanding.parse_resume` | C | `POST /understanding/parse-text` (`document_kind: resume`) |
| `understanding.parse_job` | C | `POST /understanding/parse-text` (`document_kind: job_description`) |
| `understanding.parse_profile_import` | C | `POST /onboarding/profile/draft` |
| `taxonomy.normalize_skills` | B | `POST /understanding/taxonomy/normalize` |
| `taxonomy.normalize_title` | B | `POST /understanding/taxonomy/normalize` |
| `context.build_candidate_card` | B | `POST /context/candidate-card/build` |
| `context.build_job_card` | B | `POST /context/job-card/build` |
| `context.build_relationship_card` | B | `POST /context/relationship-card/build` |
| `context.compress_conversation` | B | `POST /context/conversation/compress` |
| `matching.evaluate_candidate_job` | B | `POST /matching/resume-to-job` |
| `matching.explain_candidate_job` | D | `POST /prompts/run` (`jf.jobs.fit.explain`) |
| `entity.detect_duplicate` (submission-scoped only) | B | Built into `POST /submissions/evaluate` |
| `workflow.validate_tracker_transition` | B | Built into `POST /submissions/evaluate` |
| `workflow.extract_tracker_update` | C | `POST /submissions/tracker-update/extract` |
| `workflow.extract_submission_status` | C | `POST /submissions/status/extract` |
| `messaging.classify_intent` | B | `POST /v1/messages/understand` |
| `messaging.extract_actions` | C | `POST /v1/messages/actions/extract` |
| `messaging.generate_reply` | D | `POST /prompts/run` (`jf.messaging.reply.draft`) |
| `broadcast.parse_requirement` | C | `POST /broadcast/requirement/extract` |
| `broadcast.parse_hotlist` | C | `POST /broadcast/hotlist/extract` |
| `validation.validate_llm_output` (partial) | B | Bracket-balanced JSON parsing inside every fallback call — schema/enum/hallucination checks not yet built |

### Decided, not yet built (deliberately deferred)

| Capability | Class | Why deferred |
|---|---|---|
| `entity.resolve` (general) | B | No cross-entity resolution against Users/Candidates/Jobs/Companies yet — only submission-key duplicate detection exists |
| `matching.rank_candidates` / `rank_jobs` (batch) | B | Only single-pair matching exists |
| `trust.*` (2 capabilities) | B | Trust/Network/Marketplace frontend is mockup-only; building backend against a mockup UI risks rework |
| `network.*` (2 capabilities) | B | Same reason |
| `marketplace.*` (3 capabilities) | mixed | Explicitly out of scope per 2026-08-15 direction |
| `search.*` (2 capabilities) | B | Typesense is currently called directly from CORE, not routed through Hermes |
| `dashboard.rank_actions` | B | Not built |
| `notifications.route` | B | **Directly relevant to the Centrifugo decision below — see §7** |
| `moderation.classify_content` | B | Not built |
| `understanding.parse_external_job` | B | Not built |
| `taxonomy.normalize_location` / `normalize_certification` | B | Not built |
| `search.nl_translate` | C/D | Needed for Core NL Search (Phase 8, spec 07). Not built yet — Phase 8 hasn't started. See Addendum, §14 |

---

## 5. Context Cards — the enforcement mechanism

`app/context/`: `CandidateCardV1`, `JobCardV1`, `RelationshipCardV1`, `ConversationContextV1`.

This is what makes `raw_documents_may_reach_llm: false` real rather than a policy statement. Any caller supplying only raw text to a card builder gets it routed through Hermes's deterministic parser first — the card, never the raw text, is what any downstream prompt receives. Endpoints: `POST /context/{candidate-card,job-card,relationship-card}/build`, `POST /context/conversation/compress`.

**Known gap, not yet closed**: established prompt-calling code (`resume_builder/adapters.py` was retrofitted; `jf.jobs.fit.explain`, `jf.messaging.reply.draft`, and other prompts called directly via `/prompts/run` are not yet forced through card builders — a caller could still paste raw text into `candidate_card`/`job_card` variables on those calls). Closing this fully means either validating card shape server-side on `/prompts/run`, or documenting it as a client-integration responsibility. **Not decided — flag for next review.**

---

## 6. Response contract

Canonical envelope (blueprint §7), applied to every capability built from 2026-08-15 onward:

```json
{
  "request_id": "req_...",
  "capability": "hermes.context.build_candidate_card",
  "execution_mode": "hermes_only",
  "confidence": 0.9,
  "llm_required": false,
  "llm_prompt_name": null,
  "structured_data": {},
  "unresolved_fields": [],
  "warnings": [],
  "proposed_actions": [],
  "trace_metadata": {}
}
```

**Decision**: established endpoints (`/understanding/*`, `/resume-builder/*`, `/matching/*`, `/v1/jobs/parse`, `/v1/consultants/parse`, `/v1/messages/understand`, `/submissions/evaluate`) **keep their existing response shapes**. Retrofitting them is a breaking change for any consumer already integrated against the documented shapes — deliberately not done without an explicit decision to accept that break. New capabilities use the envelope exclusively.

---

## 7. Real-time delivery — Centrifugo boundary (new decision, 2026-08-15)

Jobfynder runs a self-hosted Centrifugo instance (`https://centrifugo.jobfynder.com`) for real-time pub/sub delivery to connected clients.

**Decision: Hermes does not call Centrifugo.**

Reasoning:
- Centrifugo is a *delivery/transport* concern — connection lifecycle, channel auth (JWT), WebSocket fan-out. The blueprint already classifies "Notification delivery" as Core-only (§3.A). This is consistent, not a new exception.
- Hermes's broadcast capabilities (`broadcast.parse_requirement`, `broadcast.parse_hotlist`) are upstream of delivery — they turn a raw pasted message into structured data. What happens to that structured data next (persist as a feed post, publish to a Centrifugo channel for live subscribers) is Core's responsibility.
- The one legitimate Hermes touchpoint is the not-yet-built `notifications.route` capability: Hermes can deterministically decide event eligibility, channel selection, urgency, dedup, and quiet-hours suppression — i.e. *what* should be delivered and to *whom* — while Core executes the actual Centrifugo publish call using that decision. This keeps the same separation already established for every other capability: Hermes decides, Core executes.

**Action for Core team**: when building real-time feed/broadcast delivery, call Hermes's broadcast-extraction endpoints to get structured data, persist via Core's own logic, then publish to Centrifugo directly from Core (or a lightweight delivery service) — not through Hermes.

---

## 8. Caching

No dedicated Redis exists for Hermes. The only Redis instance in the infrastructure is policy-locked ("Redis is STRICTLY for LiteLLM caching only" — prior decision, 2026-08-02) and network-firewalled to a single IP that excludes Hermes's droplet.

**Interim decision (2026-08-15)**: in-process TTL cache (`app/runtime/cache.py`), matching the blueprint's `jf:hermes:*` key-pattern intent without Redis as the backend. Scope: resume/JD/profile-import parse results (including any LLM fallback outcome) cached 24h by content hash. Tracker/submission/messaging/broadcast extraction results are **not** cached (each input is a unique event — caching would never hit and isn't in the YAML's own `cache_ttl` scope for those capabilities anyway). Does not survive a container restart. `GET /runtime/cache/stats` for visibility.

**Follow-up decision needed**: whether to provision a dedicated Redis for Hermes. Not decided as of this freeze.

---

## 9. Prompt registry

38 prompts live in Langfuse (project `jobfynder-ai`), fetched dynamically by Hermes (5-minute in-memory cache), not hardcoded. Full catalog with use cases: `hermes-parsing-and-prompts-api-guide.md` §6.

**Known drift from the original blueprint**: roughly 20 prompt names referenced in blueprint §6 do not exist in Langfuse. Most correspond to `HERMES_ONLY` capabilities in §4 above marked "not yet built" — the absence of the prompt isn't the gap, the absence of the underlying deterministic capability is.

All prompts route through LiteLLM via router aliases (`generate-small`, `extract-fast`, `reasoning-small`), currently all backed by `anthropic/claude-haiku-4-5`. Automatic one-time fallback to a configured default model if a router alias has no healthy deployment.

---

## 10. Cost discipline — verified, not just designed

This isn't a principle on paper. Verified behaviors as of this freeze:

- Deterministic parsing is genuinely zero-cost: strong/well-formed input never reaches an LLM (confirmed across resume, JD, job-tracker, submission-status, messaging-actions, and broadcast extraction — each has a real deterministic first pass, not a stub).
- Weak/ambiguous input escalates automatically and only once (confidence-gated, single fallback attempt, no retry loops).
- Identical repeat input is cache-hit, not re-computed or re-billed (24h, resume/JD/profile-import scope).
- A cost bug was found and fixed during this work: onboarding profile-import was firing two separate paid LLM calls per request (the generic resume-fallback plus its own specialized fallback) — now exactly one.

---

## 11. RBAC

Bearer-token auth, permission strings checked against a wildcard-or-exact match (`app/security/rbac.py`). `HERMES_RBAC_ENFORCEMENT` env var gates whether it's enforced at all — currently `enabled`. New capabilities in this freeze use scoped permissions (`context:build`, `broadcast:extract`, `runtime:read`) that resolve automatically for wildcard (`*`) tokens without separate registration.

**Known inconsistency, not yet resolved**: `/understanding/*` and `/submissions/evaluate*` currently have **no RBAC check at all** (no `require_permission` dependency), while `/resume-builder/*`, `/prompts/*`, `/context/*` do. Not fixed as part of this work — flagged for a deliberate decision (is this intentional, since Understanding/Submissions are meant to be called by Core with implicit trust? Or an oversight?).

---

## 12. Bugs found and fixed during this build (for the record)

1. `/resume-builder/summary/suggest` and `/bullets/suggest` were silently failing (`prompt_not_found`) since the Langfuse prompt migration — still referenced old local-registry prompt IDs.
2. `/onboarding/profile/draft` was crashing with a 500 on every call — `document_kind="consultant_profile"` is not a valid `DocumentKind` literal.
3. Message intent classifier missed common bench/hotlist phrasing ("I have a Java developer available") — fixed with a regex pattern instead of exact-phrase matching.
4. `/v1/jobs/parse` and `/v1/consultants/parse` reported `confidence: 1.0` unconditionally, regardless of what was actually extracted — now computed from real field completeness.
5. Consultant location extraction falsely matched skill acronyms (e.g. "AWS" parsed as a location) due to an unanchored regex.
6. Onboarding profile-import fired two LLM calls per request instead of one (cost bug, §10).

---

## 13. What changes this document

Any of the following should trigger a deliberate update to this freeze, not a silent divergence:
- A new capability moves from "not yet built" to "built."
- A response contract decision changes (e.g. legacy endpoints get migrated to the envelope).
- Redis is provisioned for Hermes.
- The Centrifugo boundary decision changes (e.g. Hermes takes on `notifications.route`).
- Any RBAC gap in §11 gets resolved one way or the other.

---

## 14. Addendum — 2026-08-20

**NL Search reconciliation.** The Core master build plan's Phase 8 session table (`00-master-build-plan.md`, session 8.5) was worded ambiguously — "Haiku 4.5 via LiteLLM" read as a direct Core→LiteLLM call, which would violate `only_hermes_may_call_litellm` (§2). Checked against the detailed spec (`07-nl-search-spec.md` §2/§7), the actual design already routes NL Search through Hermes — the ambiguity was in the session-table wording only, not the underlying design. Session table corrected to say "via Hermes `search.nl_translate`" explicitly. `search.nl_translate` added to §4 as a needed-not-yet-built capability (Phase 8 hasn't started, so nothing to build yet — this just closes the documentation gap before that phase begins).

**Portkey removed.** The project has moved off Portkey entirely; LiteLLM + Langfuse is now the only LLM path, consistent with `only_hermes_may_call_litellm`. Core's `src/resume/resume.controller.ts` and `src/ai/ai.service.ts` still call Portkey directly as of this addendum — known, tracked separately as part of the in-progress Hermes↔Core integration (`feature/hermes-core-integration` branch), not a gap in this document.
