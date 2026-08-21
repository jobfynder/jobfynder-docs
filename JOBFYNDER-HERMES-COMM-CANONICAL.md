# Jobfynder HERMES + COMM Canonical Documentation
## The Document of Truth

**Version:** 1.6
**Status:** ACTIVE — this is now the single reference for the entire Jobfynder HERMES + COMM platform
**Effective date:** 2026-08-21 (v1.1: COMM documentation added after direct inspection of COMM-1. v1.2, same day: three of the gaps that inspection found — the COMM-500 unhandled-exception bug, missing rate limiting, missing backups — were fixed, deployed, and verified live. v1.3, same day: Phase 0 completed — `jobfynder-infra` `main` reconciled with the deployed COMM branch (clean merge, zero conflicts), and four modules (HERMES-450/500/600/850) had their doc files corrected to record git tags that had existed for weeks but were never written down. v1.4, same day: Phase 1 completed — the Hermes RBAC gap closed and deployed, and the HERMES-1000 LiteLLM exit condition fully resolved across CORE, including a real direct-OpenAI-client bypass found during investigation that the original gap description hadn't anticipated. v1.5, same day: further Phase 2/3 progress — COMM-1 restore-tested, `ufw` enabled, a real TLS-bypass and a weak default RabbitMQ credential found and fixed during that pass, and three stale prompt-ID check scripts repaired and verified against the live Hermes registry. v1.6, same day: RabbitMQ and Redis — the one gap on the whole platform explicitly called "a design decision, not a bug fix" — actually wired into COMM's intake pipeline (queueing, exponential-backoff retry, dead-letter, idempotency), live-verified end to end; a logging-configuration mistake that briefly leaked the Telegram bot token into a log file was found and fixed in the same pass.)
**Owner:** Jobfynder-Infra
**Companion document:** [HERMES-COMM-CORE-INTEGRATION-GUIDE.md](./HERMES-COMM-CORE-INTEGRATION-GUIDE.md) is the developer-facing counterpart to this doc — auth flows, endpoint samples, error codes, and a testing plan for integrating Jobfynder CORE with both servers. This document (the canonical doc) answers "what's actually production-ready"; that one answers "how do I integrate with it."
**Supersedes:** `hermes/HERMES-documentation-map.md`, the "Closed Modules" status list inside `hermes/HERMES-000-architecture-governance.md` §4, and every prior informal status summary. Those files are moved to `archive/legacy-module-documentation/` and are historical reference only — see [§10](#10-what-was-retired-and-why).

---

# 0. How to use this document

This document has two halves:

- **Part A — Canonical Index.** The permanent module numbering for HERMES and COMM. Stable regardless of who builds what, when. (Adapted from the "Canonical Documentation Index v3.0" draft.)
- **Part B — Status Matrix.** What is actually true right now, module by module, verified against the live `jobfynder/jobfynder-docs` and `jobfynder/hermes` repositories, the running INTEL-1/COMM-1 infrastructure, and the project's own session records. Not a re-statement of old "completed" claims — every status below is graded against real evidence, and where no evidence exists, it says so.

**Rule going forward:** a module is never marked done because a chat thread said so. It is marked done because a file, a git tag, a live endpoint, or a running container proves it.

---

# 1. Documentation design principle

Module numbers describe **architectural responsibility**, not the order in which something happened to get built. HERMES numbers are intelligence-plane domains. COMM numbers are communication-plane domains. Cross-cutting infrastructure lives in a shared PLATFORM namespace. A module number is never reused for something unrelated, and historical identifiers (old doc names, old branch names) are preserved as a mapping table, never deleted.

```text
JOBFYNDER PLATFORM
│
├── HERMES / INTEL-1  (Intelligence Plane)
│   ├── HERMES-100  Core Intelligence Platform
│   ├── HERMES-200  Understanding Engine
│   ├── HERMES-300  Matching & Ranking Engine
│   ├── HERMES-400  Taxonomy & Signal Intelligence
│   ├── HERMES-500  Workflow Intelligence
│   ├── HERMES-600  Integration Intelligence
│   ├── HERMES-700  Orchestration & Agent Runtime
│   ├── HERMES-800  Domain Intelligence Applications
│   ├── HERMES-900  Role Intelligence Packages
│   └── HERMES-1000 AI Runtime & Production Intelligence
│
├── COMM / COMM-1  (Communication Plane)
│   ├── COMM-100  Core Communication Platform
│   ├── COMM-200  Identity & Session Layer
│   ├── COMM-300  Messaging & Event Transport
│   ├── COMM-400  Channel Adapters
│   ├── COMM-500  Ingress & Intake
│   ├── COMM-600  External Communication Integrations
│   ├── COMM-700  Realtime Communication
│   ├── COMM-800  Communication Workflows
│   ├── COMM-900  Reliability & Governance
│   └── COMM-1000 Production Operations
│
└── PLATFORM / Cross-Plane
    ├── PLATFORM-100  Network & Security
    ├── PLATFORM-200  Service Contracts
    ├── PLATFORM-300  Observability
    ├── PLATFORM-400  Deployment & Infrastructure
    ├── PLATFORM-500  Data Governance
    └── PLATFORM-600  Production Acceptance
```

Neither HERMES nor COMM is secondary. Both get first-class module documentation. Their interaction (the `POST /internal/comm/intake` HMAC-signed contract, the intake→understanding→matching pipeline) is documented under PLATFORM.

---

# 2. Terminology reconciliation — read this before anything else

Building this document surfaced two real naming collisions inside the existing documentation. Both are resolved here, permanently.

### 2.1 "COMM-1" has been used to mean two different things

- **Meaning A (the correct one, kept):** COMM-1 is the **communication-plane server** — IP `152.42.219.165`, running the `jobfynder-comm-gateway` Docker container. It owns provider-facing ingress, transport authentication (HMAC signing to Hermes), retries, attachments, and outbound communication. This is confirmed in both `hermes/HERMES-450-channel-intake.md` ("COMM-1 owns provider-facing ingress...") and the infra session-handoff record. **This is the definition used everywhere in this document and in the COMM index below.**
- **Meaning B (retired as a name, kept as a concept under a new name):** `hermes/HERMES-000-architecture-governance.md` §7 and `hermes/hermes-engineering-playbook.md` §8 define "COMM-1" as *"the autonomous engineering operator for Jobfynder-Infra"* — i.e. the automated bot that watches GitHub webhooks and writes `engineering-memory/daily/*.md` / `docs(memory): ...` commits. That is a real, distinct thing (evidence: the repeating `docs(memory): archive github event` / `docs(memory): update engineering memory` commits in `git log`), but it is **not a server and not the communication plane** — calling it "COMM-1" collided with the real COMM-1 server and must stop. **Going forward this is called the Engineering Memory Automation** (no module number — it is tooling, not a product module). `HERMES-000` §7 should be corrected to reflect this the next time that file is touched.

### 2.2 HERMES-300/400 have two different definitions on record

- `hermes/HERMES-000-architecture-governance.md` §4 (written 2026-07-05) defines HERMES-300 = "Memory" and HERMES-400 = "Intelligence" (reasoning/decision engines) — a governance sketch that was never built out under those definitions.
- What was **actually built and closed** under those numbers — confirmed by `hermes/HERMES-300-matching-decision-intelligence.md` (tag `hermes-300-foundation-v1`) and `hermes/HERMES-400-taxonomy-signal-intelligence.md` (tag `hermes-400-foundation-v1`) — is HERMES-300 = **Matching & Decision Intelligence** and HERMES-400 = **Taxonomy & Signal Intelligence**. This also matches the index in [§1](#1-documentation-design-principle).

**Canonical decision: the numbering in §1 of this document wins.** It matches what was actually shipped and tagged. `HERMES-000` §4's module list is superseded and should not be used to reason about module scope again.

### 2.3 What this repo documents vs. what actually runs

Every HERMES module below has a real documentation trail — closure checklists, git tags, commit SHAs, live-verified endpoints. **As of v1.0 of this document, COMM had none of this** — confirmed by exhaustive search: no `comm/` folder, no `COMM-nnn`-numbered file, no server inventory entry, anywhere in `jobfynder/jobfynder-docs`. That gap is now closed (v1.1, same day): a direct SSH inspection of COMM-1 (`152.42.219.165`) plus the `jobfynder/jobfynder-infra` repository produced `comm/COMM-000` through `comm/COMM-500` and the infrastructure-posture doc. See [§5](#5-part-b--comm--comm-1-master-status-matrix) for the resulting status matrix, and `comm/COMM-documentation-map.md` for the index. **COMM has now been brought into the same documentation discipline HERMES has had since HERMES-100** — the former P0 item in [§8](#8-priority-matrix) is done. Of the concrete gaps that inspection surfaced, all are now fixed across three 2026-08-21 passes: the unhandled-exception path in the intake call, missing HTTP rate limiting, and no backup automation (commit `0c33580`); a real TLS-bypass and a weak RabbitMQ credential found along the way, plus a host firewall (commit `33b6ec4`); and — the one item originally called "a design decision, not a bug fix, remains open on purpose" — RabbitMQ/Redis are now actually wired into the intake pipeline (commit `2622899`), live-verified end to end.

---

# 3. Status legend

Two layers are used together: a **maturity band** (the headline, one per module) and a **dimension grade** (the detail, eight per module). Do not use bare words like "Completed" or "Closed" without one of these — they are ambiguous and are exactly what this document replaces.

## 3.1 Maturity band (headline)

| Band | Meaning |
|---|---|
| ✅ **Foundation Complete** | Core architectural implementation exists, is committed, tagged, and was live-verified at closure time |
| 🟨 **Integration in Progress** | Foundation exists; end-to-end product/service integration is not yet proven |
| 🟦 **Designed** | Architecture/scope is written down; little or no implementation exists |
| 🟧 **Production Candidate** | Integrated and tested but final production acceptance (PLATFORM-600) is outstanding |
| 🟩 **Production Ready** | Full production acceptance checklist passed |
| 🟥 **Reconciliation Required** | Historical claims and current reality diverge enough that the module needs an audit before its status can be trusted |
| ⬜ **Not Started / No Documentation** | No material implementation evidence, or (for COMM) implementation may exist but has never been documented |

## 3.2 Dimension grade (detail, per module)

| Status | Meaning |
|---|---|
| 🟢 Complete | Strong, verifiable evidence exists (tag, commit, live-tested endpoint) |
| 🟡 Partial | Meaningful foundation exists, but gaps remain |
| 🔵 Designed | Architecture/design defined; implementation incomplete |
| ⚪ Not Started | No material implementation evidence |
| 🔴 Gap / Rework | Existing work requires replacement, reconciliation, or major correction |
| ❓ Verify | Historical evidence exists but runtime/repository verification is still required |

Eight dimensions are graded per module: **Architecture, Implementation, Deployment, Integration, Testing, Observability, Security, Production Ready (YES/NO)**.

**Hard rule carried over from the ChatGPT assessment and kept: a historical "Closed" or "Complete" label in an old doc is not, by itself, sufficient to mark a module Production Ready.** Every module below is capped by whichever dimension has the weakest verified evidence.

---

# 4. Part B — HERMES / INTEL-1 Master Status Matrix

Evidence for every row below was pulled directly from the live `hermes/*.md` files in `jobfynder/jobfynder-docs` (including the unmerged `docs/2026-08-21-retire-portkey-litellm-rewrite` branch, which is the most current state — see [§9](#9-branch-state-note)), cross-checked against git tags/commits quoted in those files.

| Module | Canonical Name | Maturity | Arch | Impl | Deploy | Integ | Test | Obs | Sec | Prod Ready |
|---|---|---|---|---|---|---|---|---|---|---|
| HERMES-100 | Core Intelligence Platform | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | **NO** |
| HERMES-200 | Understanding Engine | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | **NO** |
| HERMES-300 | Matching & Decision Intelligence | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | **NO** |
| HERMES-400 | Taxonomy & Signal Intelligence | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | **NO** |
| HERMES-450 | Channel Intake & Provider Integration | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | **NO** |
| HERMES-500 | Workflow Intelligence (Submission) | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🔵 | 🔵 | **NO** |
| HERMES-600 | Integration Intelligence | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🔵 | 🟡 | **NO** |
| HERMES-700 | Orchestration & Agent Runtime | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | **NO** |
| HERMES-750/775 | AI Execution Runtime (LiteLLM) | 🟨 Integration in Progress | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | 🟡 | 🟡 | **NO** |
| HERMES-800 | Domain Intelligence — Resume Builder | ✅ Foundation Complete | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🔵 | 🟡 | **NO** |
| HERMES-850 | Domain Intelligence — Email Parsing | ✅ Foundation Complete | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🔵 | 🟡 | **NO** |
| HERMES-900 | Role Intelligence Packages | ⬜ Not Started | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | **NO** |
| HERMES-1000 | AI Runtime & Production Intelligence (gateway-wide) | 🟨 Integration in Progress | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | **NO** |

## HERMES-100 — Core Intelligence Platform

**Evidence.** `hermes/HERMES-100-core-platform-closure-checklist.md` — status "Production Baseline Complete." Central config, health endpoint on central version, `.env.example`, RBAC foundation + enforcement, protected platform/parser routes, RBAC user-management script, API version consistency, `.dockerignore`, Docker build validated, smoke test added and passing, API route inventory created, deployment runbook created. `hermes/hermes-rbac-access-control.md` confirms baseline users (`pavan-admin` = admin, `n8n-engineering-memory` = automation) and token storage at `/root/hermes-admin-token.txt` / `/root/hermes-n8n-token.txt`.

**RBAC gap closed 2026-08-21.** `hermes-api-route-inventory.md`, `hermes-architecture-frozen-v1.md` §11, and `hermes-core-integration-guide.md` §9.1 had all independently flagged the same unresolved gap: `/understanding/*` and `/submissions/evaluate*` had no RBAC check at all. Fixed and deployed (commit `9dc69d5` on `jobfynder/hermes`), verified safe first (zero live traffic on either route group, confirmed via logs and a CORE-side grep before enabling), then live-tested (401/403/200 all behaving correctly, including a real end-to-end resume-parse call). A new `jobfynder-core` RBAC token was provisioned for future use. Security bumped to 🟢.

## HERMES-200 — Understanding Engine

**Evidence.** `hermes/HERMES-200-understanding-foundation.md` — "Working foundation completed." Local-first, parser-first pipeline (plain text, MarkItDown, pdfplumber, python-docx fallbacks); resume parser extracts skills/experience/title/contact/LinkedIn/work-authorization; JD parser extracts title/skills/required-preferred/experience/location/type/rate; taxonomy endpoint. Smoke test script covers 10 scenarios. Live endpoints: `/understanding/parse-text`, `/understanding/parse-file`, `/understanding/taxonomy/skills`.

**Gap.** File itself lists open "Next" items: bigger taxonomy, more resume/JD fields, real Unstructured.io integration, Langfuse/Promptfoo/Great Expectations evaluation — none confirmed done as of this document.

## HERMES-300 — Matching & Decision Intelligence

**Evidence.** `hermes/HERMES-300-matching-decision-intelligence.md` — "Closed — production-safe local deterministic matching foundation complete." Final tag `hermes-300-foundation-v1`, 13 commits on `feature/hermes-300-matching`. Deterministic (no LLM), explainable scoring across skill match, required/preferred coverage, experience, work-authorization, location. Live endpoints `GET /matching/policy`, `POST /matching/resume-to-job`, `POST /matching/resume-to-job/from-understanding`. Live validation: Docker rebuild, OpenAPI route check, authenticated smoke test, deterministic scenario coverage for submit/review/reject all passed.

**Gap.** This is a deterministic rules engine, not the benchmark-driven ranking system the original architecture intent implies (good/weak match sets, recruiter-judgment ground truth, false-positive/negative measurement) — that evaluation layer does not exist yet. Matches the priority-matrix item in [§8](#8-priority-matrix) (P2).

## HERMES-400 — Taxonomy & Signal Intelligence

**Evidence.** `hermes/HERMES-400-taxonomy-signal-intelligence.md` — "Closed" with tag `hermes-400-foundation-v1`, commit `1f21f8a`. Canonical skill/alias/job-title/title-alias registries (35 skills, 42 aliases, 14 titles, 37 title-aliases at closure), normalization service, signal extraction, suggestion queue (unknown terms are never auto-approved — explicit safety rule), versioned snapshots (`hermes-400-taxonomy-foundation-v1`). Integrated into both HERMES-200 output and the HERMES-300 matching adapter. 7 verification scripts, all passing inside Docker; live-verified endpoints.

**Governance match.** The suggestion-queue design ("Observed term → normalize → existing match → alias resolution → confidence → candidate proposal → governance → canonical taxonomy") matches exactly what the earlier assessment recommended — this is already built, not just planned.

## HERMES-450 — Channel Intake & Provider Integration

**Note on file duplication.** Two files exist for HERMES-450: `HERMES-450-channel-intake-parser-integration-foundation.md` (Status: Open — the original design doc, superseded) and `HERMES-450-channel-intake.md` (Status: Closed — the actual closure record, final commit `98b221c`). **The closure file is authoritative.** The design-doc file should be moved to archive; see [§10](#10-what-was-retired-and-why).

**Evidence.** Unified channel/file intake contracts, draft persistence, idempotency, role-action access control, conversation session engine, **Telegram production bridge configured and live**, Telegram webhook-secret verification, provider registry/health APIs, normalized contracts for Email/WhatsApp/Slack/Teams/Google Chat (contract-ready, not live), LinkedIn OAuth foundation, BrightData public-profile foundation, and — critically — the **signed COMM-1 → Hermes internal intake endpoint** (`POST /internal/comm/intake`, HMAC-SHA256 over `timestamp + "." + raw_body`, `X-Jobfynder-Timestamp` / `X-Jobfynder-Signature` headers). Five closure commits cited. Verification script `hermes-450-provider-verification.py` passed.

**Historical mapping note.** The v3.0 draft proposed retiring the "HERMES-450" number in favor of `COMM-500`. **This document does not adopt that move.** The real, closed HERMES-450 work is Hermes-side (parsing/draft-creation/RBAC on received intake) and is correctly HERMES-scoped; the provider-facing half (webhook receipt, retries, outbound delivery) belongs to COMM-500 once COMM gets documented, and the two sides meet at the `/internal/comm/intake` contract. HERMES-450 keeps its number.

## HERMES-500 — Workflow Intelligence (Submission)

**Resolved 2026-08-21 (Phase 0).** Earlier drafts of this document downgraded HERMES-500 to Integration in Progress because its own doc said "ready for closure" with no tag confirmed. **The tag existed all along.** Direct verification against `/opt/hermes` on INTEL-1: `hermes-500-foundation-v1` exists, tagged 2026-07-07 by Jobfynder Automation, pointing at commit `2d8c1ab` — the exact commit the doc already cited as final. The module doc's "Remaining closure actions" checklist was simply never updated to check its own boxes; this has been corrected in place.

**Evidence.** `hermes/HERMES-500-submission-intelligence-workflow-foundation.md` — extensive, 41-section build log. 14-stage submission lifecycle, three live endpoints (`GET /submissions/workflow-policy`, `POST /submissions/evaluate`, `POST /submissions/evaluate/from-handoff`), deterministic event/follow-up/outcome mapping, invalid-transition protection, handoff adapters from HERMES-200/300/400. All Docker + live-API verification steps recorded as "Passed." Final tag: `hermes-500-foundation-v1` @ `2d8c1ab`.

**What's still genuinely open (unaffected by the tag correction):** no persistence layer (Hermes returns structured recommendations only — Jobfynder API/Postgres, not Hermes, must persist), no authentication enforcement confirmed on these routes (this is the same RBAC gap tracked under HERMES-100/§9.1 of the companion integration guide), no webhook delivery.

## HERMES-600 — Integration Intelligence

**Resolved 2026-08-21 (Phase 0).** Same root cause as HERMES-500 above, found independently the same day. Direct verification against `/opt/hermes`: `hermes-600-foundation-v1` exists, tagged 2026-07-07 by Jobfynder Automation, pointing at commit `7c23d1f` — the exact commit the doc's "Final Closure Status" section already cited. The header-vs-closure-section contradiction flagged in earlier drafts of this document was a real, confusing bug in the source doc (fixed in place, 2026-08-21) — but it was a documentation bug, not evidence the module was actually incomplete.

**Evidence.** `hermes/HERMES-600-integrations-foundation.md`. 11 commits on `feature/hermes-600-integrations`. Endpoints: `/integrations/health`, `/integrations/events/normalize`, `/integrations/jobfynder/submission-handoff/evaluate`, `/integrations/retry-policy`, `/integrations/retry-decision`, `/integrations/events/identity`. Explicitly out of scope: production auth rollout, external SaaS integrations, paid connectors, background job queue, UI, DB-persistence redesign. Final tag: `hermes-600-foundation-v1` @ `7c23d1f`.

**Bonus finding from the same verification pass:** `hermes/HERMES-450-channel-intake.md` had the identical gap (said "Closed," never cited a tag) — checked and fixed the same way: `hermes-450-foundation-v1` exists, tagged 2026-07-10, matching its already-cited final commit `98b221c`. Three modules, one root cause: Jobfynder Automation tags modules on closure, but the human-readable doc isn't always updated to record the tag name. Worth building a lightweight check for this going forward (compare `git tag` output against what each module's doc cites) rather than relying on catching it by hand again.

## HERMES-700 — Orchestration & Agent Runtime

**Evidence.** `hermes/HERMES-700-multi-agent-foundation.md` — "Closed," 2026-07-07. Final tag `hermes-700-foundation-v1` @ commit `c2fc718`. Endpoints: `/agents/health`, `/agents/registry`, `/agents/snapshot`, `/agents/{agent_id}`, `/agents/dry-run`. Six confirmed agents: Founder, Recruiter, Bench Sales, Consultant, Engineering, Support. Explicit non-goals recorded: no public chatbot UI, no uncontrolled autonomous agents, no browser automation, no direct LinkedIn/WhatsApp automation, no production self-healing infra, no billing automation, no trust-score auto-mutation.

**Architectural correction carried forward.** The original name "Multi-Agent Intelligence" implied one independent agent per role. The corrected model (already reflected in how this was actually built) is: **one HERMES capability platform + role packages + orchestration policy**, not five duplicated agent stacks. HERMES-900 (Role Intelligence Packages) is where role-specific configuration belongs, not new agent code.

## HERMES-750 / HERMES-775 — AI Execution Runtime (LiteLLM)

**This is the most important reconciliation in this document — it resolves a P0 gap the pre-repo assessment flagged as unverified.**

**Evidence the migration is real and largely done.** As of the 2026-08-21 rewrite (`hermes/HERMES-750-litellm-prompt-runtime-foundation.md`, `hermes/HERMES-775-litellm-production-runtime-and-multi-model-routing.md`):
- Provider name in running code is `litellm` (`PROVIDER_NAME = "litellm"`, `app/prompt_runtime/service.py`).
- 38 Langfuse-hosted prompts route through LiteLLM router aliases (`generate-small`, `extract-fast`, `reasoning-small`), all currently backed by `anthropic/claude-haiku-4-5`, verified live 2026-08-21 against `https://gateway.jobfynder.com/ui/`.
- Per-key spend/budget enforcement confirmed live (example key: "$1.82 of $20," resets Aug 31).
- A wrong-Langfuse-key incident and an N+1 sequential prompt-fetch performance bug (33.59s cold-cache) were both found and fixed this cycle — key rotated to `hermes-production-2`, fetch parallelized to 8 concurrent workers, verified 33.59s → 7.55s.
- HERMES-775's original scope ("Portkey Production Runtime and Multi-Model Routing") is explicitly retired — "zero code was ever written" under it — and superseded in place by what LiteLLM already provides out of the box (per-key budgets, model access groups, router aliases, multi-provider backend).

**What is explicitly still open (quoted directly from HERMES-775 §3, this is the real gap list — not a guess):**
1. Claim-level evidence verification — stays Hermes's job (HERMES-800).
2. Prompt-injection protection — gateway rate limiting is not content-level injection defense; still unbuilt.
3. PII/secret redaction before Langfuse tracing — not automatic; still needs explicit handling in `send_langfuse_trace()`.
4. Circuit breaker beyond a single fallback attempt — adequate at current volume, would need real engineering if volume/provider instability grows.
5. Stale prompt-ID check scripts (`hermes-750-prompt-runtime-check.py`, parts of `hermes-800-foundation-check.py`) still reference retired prompt IDs (`resume_builder.summary_improve`, `resume_builder.bullet_rewrite`) that no longer exist in the live registry — confirmed failing as of 2026-08-21.

**Resolved 2026-08-21.** `hermes-architecture-frozen-v1.md` §14 (2026-08-20 addendum) had flagged that Jobfynder **CORE's** `src/resume/resume.controller.ts` and `src/ai/ai.service.ts` still called Portkey directly. Investigation found the scope was actually larger than "two files, repoint to LiteLLM": four call sites across three files (`ai.service.ts`, `resume.controller.ts`, `jobs.service.ts`, `content-generation.service.ts`), and `resume.controller.ts` additionally held a **second, entirely separate direct OpenAI client** bypassing even Portkey. Fixed in commit `50eeb30` on `jobFynder-BE-nestJS` `main` — both `OpenAI` client instantiations now point at `gateway.jobfynder.com` with a LiteLLM virtual key (LiteLLM exposes an OpenAI-compatible API, so the existing `openai` SDK needed no replacement, just re-pointing), and four hardcoded Portkey-style model-routing strings (`@chatgpt/...`, `@grok/...`) were replaced with the same router aliases (`generate-small`, `extract-fast`) Hermes itself uses. Verified: `npm run build` clean, live end-to-end call through the new config succeeded, repo-wide grep for `portkey`/direct-provider usage across `jobFynder-BE-nestJS` returns clean, and `jobFynder-FE-vite` was confirmed to have zero provider references at all (never a concern, browser apps shouldn't hold model keys).

**What this fix does NOT do — a real, deliberately-deferred gap:** CORE calling LiteLLM directly satisfies the platform's literal, already-adopted rule ("LiteLLM is the sole AI gateway"), but not the *stronger* architectural ideal stated in the companion integration guide ("CORE never talks to an LLM directly, always goes through Hermes"). Two of the four call sites (resume parsing, resume section generation) map closely onto Hermes capabilities that already exist, are tagged, and are now RBAC-protected (HERMES-200, HERMES-800) — routing CORE through Hermes for those would be the architecturally cleaner end-state, but it changes response shapes CORE's frontend contract currently depends on, so it was deliberately not attempted in this pass and is tracked separately (see [§8](#8-priority-matrix)).

**Two stale files remain in the repo and must not be read as current:** `hermes/HERMES-750-portkey-prompt-runtime-foundation.md` and `hermes/HERMES-775-portkey-production-runtime-and-multi-model-routing.md`. Both are moved to archive in this update — see [§10](#10-what-was-retired-and-why).

## HERMES-800 — Domain Intelligence — Resume Builder

**Evidence.** `hermes/HERMES-800-resume-builder-intelligence-foundation.md` — "Closed," final tag `hermes-800-resume-builder-foundation-v1` @ commit `d9196b1`. 8 endpoints (`/resume-builder/health`, `/policy`, `/analyze`, `/summary/suggest`, `/bullets/suggest`, `/skills/normalize`, `/tailor`, `/quality/analyze`). Runtime state at closure: prompt runtime available (now LiteLLM-backed), **live LiteLLM execution disabled by default, external AI calls disabled** — i.e. closed as a dry-run-safe foundation, not a live-firing production feature.

**2026-08-21 correction on record.** The original closure's two prompt IDs no longer exist under those names in the live Langfuse registry — two verification scripts currently fail because of this (confirmed, not hypothetical). Anyone re-verifying HERMES-800 must check `GET /prompts/registry` for current IDs, not the ones written in the original closure doc.

**What "Production Candidate" would require.** Full chain test: Resume Builder UI → Jobfynder Backend → HERMES → parser/AI → LiteLLM → response → persistence/UI, with authentication, error handling, tenant isolation, tracing, and failure handling all exercised together. Not done — this is why Integration stays 🟡 despite a clean closure tag.

## HERMES-850 — Domain Intelligence — Email Parsing

**Evidence.** `hermes/HERMES-850-email-parsing-foundation.md` — added 2026-08-21, "Closed (foundation) — live provider wiring intentionally deferred." Two branches (`feature/hermes-850-email-parsing`, `feature/hermes-850-gmail-graph-providers`), 3 commits. Final tag `hermes-850-foundation-v1` @ `0dce803` — existed since the module's own closure, confirmed live against `/opt/hermes` and added to the doc 2026-08-21 (same undocumented-tag pattern independently found on HERMES-450/500/600 the same day). 6 endpoints incl. generic webhook, Gmail status/push, Microsoft Graph status/webhook, `/channels/intake`. 13/13 verification checks pass across 3 scripts. 103 → 106 OpenAPI paths after this module.

**Explicit, intentional gap (a product decision, not an oversight).** "No real email flows through this yet." Gmail/Microsoft Graph connectors are contract-ready, not live — blocked on OAuth app registration and credentials (`HERMES_GMAIL_CLIENT_ID/SECRET/REFRESH_TOKEN`, `HERMES_MS_GRAPH_CLIENT_ID/SECRET/TENANT_ID`), which is explicitly called out as gated on a decision outside engineering's control, not a bug.

## HERMES-900 — Role Intelligence Packages

**Evidence.** None. No `HERMES-900*.md` file exists in the repo. The architecture (role-specific capability/permission/prompt/workflow packages sitting on top of the shared HERMES-700 orchestration layer, not standalone agents) is written down in the v3.0 index only — nothing has been implemented.

**Do not start this yet.** Per the design principle already agreed: role packages should not be built before HERMES-710-equivalent capability-registry cleanup, AI-gateway consolidation (HERMES-1000), and product-integration contracts (PLATFORM-200) are stable — otherwise role packages will just hide the inconsistencies those layers still have.

## HERMES-1000 — AI Runtime & Production Intelligence (gateway-wide)

**This module is graded separately from HERMES-750/775 because it means something broader: the platform-wide guarantee that *no Jobfynder service* — not just Hermes — calls a model provider directly.**

**What's proven:** Hermes's own runtime (HERMES-750/775) is fully on LiteLLM, with real spend controls, aliasing, and observability, verified live 2026-08-21.

**Resolved 2026-08-21 — the platform-wide "zero model calls bypass LiteLLM" guarantee is now true and verified, not assumed.** A repo-wide grep across `jobFynder-BE-nestJS` for `portkey`, direct `OpenAI(...)` instantiation, `anthropic`, `google.generativeai`, `groq`, and known provider endpoint URLs comes back clean (both `new OpenAI()` call sites confirmed pointed at LiteLLM, not the real OpenAI API); `jobFynder-FE-vite` had zero matches for any of the above, confirmed independently. See the HERMES-1000 section above for what the fix actually involved (it was bigger than "two files, repoint to LiteLLM" — four call sites, one of which bypassed even Portkey) and what it deliberately does not yet do (route CORE through Hermes's existing capabilities, a separate architectural follow-up).

---

# 5. Part B — COMM / COMM-1 Master Status Matrix

**Updated 2026-08-21 (v1.2).** The gap described below in earlier drafts of this document — zero COMM documentation anywhere — is now closed. `comm/COMM-000` through `comm/COMM-500` and `comm/COMM-300-900-1000-infrastructure-posture.md` were written directly against a live SSH inspection of COMM-1 (`152.42.219.165`) and the `jobfynder/jobfynder-infra` repository. See `comm/COMM-documentation-map.md` for the full index. **Same day, three of the gaps that inspection found were fixed and deployed** (commit `0c33580` on `jobfynder-infra`, rebuilt and restarted on COMM-1, live-verified) — see the COMM-500, COMM-900, and COMM-1000 rows below.

| Module | Canonical Name | Maturity | Evidence |
|---|---|---|---|
| COMM-100 | Core Communication Platform | 🟨 Integration in Progress | **Real, live, documented.** `comm/COMM-100-core-communication-platform.md`. FastAPI service (`comm_gateway/`, 5 files), Docker Compose, live `GET /health` → healthy/production. Deployed branch (`feature/comm-telegram-message-chunking`) is 3 commits ahead of `main` and never merged — same doc/runtime parity issue flagged on the Hermes side. |
| COMM-200 | Identity & Session Layer | ⬜ Not Started | Confirmed no dedicated code — Telegram sender ID passes through unmapped, no persistent user identity layer exists on COMM-1. |
| COMM-300 | Messaging & Event Transport | ✅ Foundation Complete | `comm/COMM-300-900-1000-infrastructure-posture.md`. **Fixed 2026-08-21 (commit `2622899`):** RabbitMQ, unused for 6+ weeks, now backs a real intake/retry/dead-letter pipeline with a delayed-requeue backoff pattern and a separate consumer process. Live end-to-end test passed (queued → consumed → Hermes call succeeded → reply attempted; a duplicate delivery correctly rejected). Open: the worker has no monitoring of its own. |
| COMM-400 | Channel Adapters | 🟨 Integration in Progress | `comm/COMM-410-telegram-channel-adapter.md`. Telegram is live, HMAC-secured, message-chunking-safe (fixed 2026-08-21 per commit `0d7616a`). No other channel has any COMM-side code — Email/WhatsApp/Slack/Teams/Google Chat exist only as Hermes-side contracts with nothing on COMM-1 to receive them. |
| COMM-500 | Ingress & Intake | ✅ Foundation Complete | `comm/COMM-500-ingress-intake.md`. The HMAC contract is cross-verified from both sides and matches byte-for-byte. **Fixed 2026-08-21 (two passes):** `hermes_client.py` catches timeout/connection errors (commit `0c33580`); queueing, retry, and idempotency wired via RabbitMQ/Redis (commit `2622899`) — all three gaps flagged since this module's first documentation pass are now closed and live-verified. Open: no monitoring on the new worker process. |
| COMM-600 | External Communication Integrations | ⬜ Not Started | No evidence found beyond Telegram (covered under COMM-400). |
| COMM-700 | Realtime Communication | ⬜ Not Started | A Centrifugo instance exists platform-wide (`centrifugo.jobfynder.com`) but nothing on COMM-1 calls or manages it — confirmed, not just absent from docs. |
| COMM-800 | Communication Workflows | ⬜ Not Started | No dedicated code beyond the reply-delivery logic already covered under COMM-410. |
| COMM-900 | Reliability & Governance | 🟨 Integration in Progress | `comm/COMM-300-900-1000-infrastructure-posture.md`. **Three passes, 2026-08-21:** (1) app-wide per-IP rate limiting, live-tested. (2) host firewall (`ufw`) enabled with an explicit allowlist, staged and verified carefully so SSH access wasn't lost; a real TLS-bypass (comm-gateway's port published directly, discovered mid-pass) closed; a weak/default RabbitMQ credential (a literal `CHANGE_THIS_STRONG_PASSWORD` placeholder, committed to git) rotated. (3) Redis now backs idempotency (previously unused). Still open: `fail2ban` still HTTP-blind (SSH-only jail), two admin ports (81, 9443) still open to the whole internet, no WAF, no alerting on the scanner traffic already observed or on the new worker's queue health. |
| COMM-1000 | Production Operations | 🟨 Integration in Progress | `comm/COMM-300-900-1000-infrastructure-posture.md`. Deployment real and stable. **Fixed 2026-08-21:** daily cron backup (3am, 14-day retention) — and, same day, a real restore test (extracted the NPM backup to a scratch dir, `PRAGMA integrity_check` passed, content matched the live database exactly). Deployed branch merged to `main` (clean, zero conflicts). Still open: no monitoring/alerting beyond Portainer's UI, no DigitalOcean-snapshot cross-check. |

**What changed the platform-level picture:** HERMES-450 (closed, tagged, verified on the Hermes side) genuinely does depend on COMM-1 behavior that is now, for the first time, actually documented and cross-checked — and that cross-check surfaced one concrete production risk (the unhandled-exception gap in COMM-500 §3) that no one had written down before. This is exactly the kind of gap that documentation-by-evidence is supposed to catch, and it worked on the first pass.

---

# 6. What "production ready" actually requires (carried forward, unchanged)

No module in either matrix is marked Production Ready, and none should be until it passes:

- **PLATFORM-600 acceptance**: end-to-end test, security review, disaster-recovery test, cross-server validation, documented rollback.
- Its **weakest** graded dimension is 🟢, not just its Implementation dimension.
- Historical "Closed"/"Complete" labels are evidence to check, never proof on their own.

---

# 7. Historical-to-canonical mapping

| Historical identifier | Canonical location | Real evidence (tag / commit / status as found) |
|---|---|---|
| HERMES Core Foundation | HERMES-100 | Production Baseline Complete (checklist, no tag quoted) |
| Original Understanding Engine | HERMES-200 | "Working foundation completed" (no closure tag quoted) |
| Original Matching Engine | HERMES-300 | Closed, tag `hermes-300-foundation-v1` |
| Original Taxonomy | HERMES-400 | Closed, tag `hermes-400-foundation-v1` @ `1f21f8a` |
| HERMES-450 Channel/Ingress (design doc) | HERMES-450 (superseded by closure doc, see §4) | Closed, tag `hermes-450-foundation-v1` @ `98b221c` (tag confirmed 2026-08-21) |
| Submission Intelligence | HERMES-500 | Closed, tag `hermes-500-foundation-v1` @ `2d8c1ab` (tag existed since 2026-07-07, confirmed 2026-08-21 — doc previously said "ready for closure," was actually already done) |
| External Intelligence Integrations | HERMES-600 | Closed, tag `hermes-600-foundation-v1` @ `7c23d1f` (tag existed since 2026-07-07, confirmed 2026-08-21 — resolves the header-vs-closure-section conflict flagged in earlier drafts of this document) |
| HERMES-700 Multi-Agent Foundation | HERMES-700 | Closed, tag `hermes-700-foundation-v1` @ `c2fc718` |
| HERMES-750 Portkey Prompt Runtime | HERMES-750 (rewritten) | Originally closed `hermes-750-prompt-runtime-v1` (2026-07-10); superseded in place by LiteLLM migration (2026-08-21), same file |
| HERMES-775 Portkey Production Runtime | HERMES-775 (rewritten) | Originally Open, zero code ever written; formally retired 2026-08-21, superseded by native LiteLLM capability |
| HERMES-800 Resume Builder | HERMES-800 | Closed, tag `hermes-800-resume-builder-foundation-v1` @ `d9196b1` |
| HERMES-850 Email Parsing | HERMES-850 | Closed (foundation), tag `hermes-850-foundation-v1` @ `0dce803` (tag confirmed 2026-08-21) |
| HERMES-900 Role Packages | HERMES-900 | Not started — no file exists |
| Telegram Integration | COMM-410 | Live/configured, now fully documented in `comm/COMM-410-telegram-channel-adapter.md`, cross-verified against HERMES-450 |
| COMM Gateway | COMM-100 | Documented in `comm/COMM-100-core-communication-platform.md` — FastAPI service, 5 source files, live-verified |
| RabbitMQ | COMM-300 | **Wired in 2026-08-21** — backs the intake/retry/dead-letter pipeline, live-verified (`comm/COMM-300-900-1000-infrastructure-posture.md`) |
| Redis (LiteLLM cache, Elestio) | HERMES-1000-adjacent infra, NOT COMM | Live, documented in `docs/AI-INFRA-SUMMARY-2026-08-02.md` |
| Redis (COMM-1) | COMM-900-adjacent infra | **Wired in 2026-08-21** — backs idempotency for the Telegram intake path; do not conflate with the Elestio/LiteLLM Redis above, they are two different instances on two different servers |
| Centrifugo | COMM-700 | Exists (`centrifugo.jobfynder.com`); Hermes explicitly does not call it; confirmed nothing on COMM-1 calls it either — still genuinely unowned |
| LiteLLM | HERMES-1010-equivalent | Live, gateway `https://gateway.jobfynder.com`, confirmed working for Hermes; **not yet confirmed for Jobfynder Core** |
| Langfuse | HERMES-1060-equivalent + PLATFORM-300 | Live, self-hosted on INTEL, v4.1.0, project `jobfynder-ai`, 38 prompts (current) — note the AI-infra summary doc (2026-08-02) cites 92 prompts, an earlier and now-stale count |
| "COMM-1" as autonomous engineering bot | Renamed: **Engineering Memory Automation** (no module number) | Real and running (auto-commits to `engineering-memory/`); name collision with the real COMM-1 server is retired as of this document — see [§2.1](#21-comm-1-has-been-used-to-mean-two-different-things) |

---

# 8. Priority matrix

| Priority | Item | Why |
|---|---|---|
| ~~P0~~ **Done (2026-08-21)** | ~~Document COMM-1 for real~~ | Closed same-day via direct COMM-1 inspection — see [§5](#5-part-b--comm--comm-1-master-status-matrix) and `comm/COMM-documentation-map.md`. |
| ~~P0~~ **Done (2026-08-21)** | ~~Fix the COMM-500 unhandled-exception gap~~ | Fixed and deployed, commit `0c33580` on `jobfynder-infra`. Verified with a mocked-failure check script, then live on COMM-1 post-redeploy. See `comm/COMM-500-ingress-intake.md`. |
| ~~P0~~ **Done (2026-08-21)** | ~~Finish the HERMES-1000 exit condition~~ | Fixed, commit `50eeb30` on `jobFynder-BE-nestJS`. Turned out to be 4 call sites across 3 files, not 2 — one bypassed even Portkey with a direct OpenAI client. Grep-clean verified across both CORE repos. See the HERMES-1000 section above. |
| ~~P0~~ **Done (2026-08-21)** | ~~Close the RBAC gap~~ | Fixed and deployed, commit `9dc69d5` on `jobfynder/hermes`. Verified safe before deploying (zero live traffic on the affected routes), then live-tested post-deploy (401/403/200 all correct). See the HERMES-100 section above. |
| **P1** | Route CORE's resume-parsing/generation through Hermes instead of LiteLLM directly | Deliberately deferred during the HERMES-1000 fix above — two of the four call sites map closely onto existing, tagged, RBAC-protected Hermes capabilities (HERMES-200, HERMES-800), but changing them risks CORE's frontend response-shape contract. Worth doing properly, not worth rushing. |
| ~~P0~~ **Done (2026-08-21)** | ~~Resolve the HERMES-600 status conflict~~ | Resolved — it was never actually unclear at the code level. `hermes-600-foundation-v1` tag has existed since 2026-07-07; the doc's header just never got updated. Fixed in place, see the HERMES-600 section above. Same root cause found and fixed on HERMES-450/500/850 the same pass. |
| ~~P1~~ **Done (2026-08-21)** | ~~Add HTTP-layer protection to COMM-1~~ | App-wide rate limiting added and live-verified (`comm_gateway/ratelimit.py`). `fail2ban`/`ufw`/WAF gaps remain — see COMM-900 in `comm/COMM-300-900-1000-infrastructure-posture.md`. |
| ~~P1~~ **Done (2026-08-21)** | ~~Set up automated backups for COMM-1~~ | Daily cron backup live, confirmed working, 14-day retention. Restore has not been tested yet — that's a new, smaller open item. See COMM-1000 in the same file. |
| ~~P1~~ **Done (2026-08-21)** | ~~Merge `feature/comm-telegram-message-chunking` to `main` on `jobfynder-infra`~~ | Merged (`git merge --no-ff`, merge commit on `814a8ed`, pushed). Turned out to be a clean, non-overlapping divergence — zero conflicts. Server working directory switched to `main`; no rebuild needed, `communication/` was byte-identical. |
| ~~P1~~ **Done (2026-08-21)** | ~~Run a restore test against a COMM-1 backup~~ | Extracted and integrity-checked, content matched live data exactly. See COMM-1000 above. |
| ~~P1~~ **Done (2026-08-21)** | ~~Add HTTP-layer hardening to COMM-1 (host firewall)~~ | `ufw` enabled with an explicit allowlist; a direct TLS-bypass and a weak default RabbitMQ credential were also found and fixed in the same pass. See COMM-900 above. |
| **P1** | IP-restrict COMM-1's admin ports (81 NPM, 9443 Portainer) | Left open to the whole internet deliberately — restricting them blind without knowing the real admin's source IP risked a lockout. Needs the admin to supply an IP/VPN range. |
| ~~P1~~ **Done (2026-08-21)** | ~~Close HERMES-500 for real~~ | It was already closed — `hermes-500-foundation-v1` tag has existed since 2026-07-07; the doc's closure checklist just never got its boxes checked. Fixed in place, see the HERMES-500 section above. |
| ~~P1~~ **Done (2026-08-21)** | ~~Fix the stale prompt-ID check scripts~~ | Turned out to be three scripts, not two (`hermes-800-resume-builder-suggestion-check.py` had the same issue). `hermes-750-prompt-runtime-check.py` needed more than a rename — the live registry had also moved to a Context-Card-based variable shape; rewrote the dry-run payloads and verified each assertion empirically against the live registry before committing. All three confirmed passing against the live container. |
| **P1** | HERMES-810 end-to-end chain test | Resume Builder UI → Backend → HERMES → LiteLLM → response → persistence/UI, with auth, tenant isolation, tracing, and failure handling all exercised together. |
| ~~P1~~ **Done (2026-08-21)** | ~~Wire COMM's RabbitMQ/Redis into the intake path~~ | Fixed and deployed, commit `2622899` on `jobfynder-infra`. Queueing, exponential-backoff retry, dead-letter, and idempotency all live-verified end to end (real webhook → queued → worker → Hermes 200 → reply attempted; a duplicate delivery correctly rejected). A logging-configuration mistake that briefly leaked the Telegram bot token into `docker logs` was found and fixed in the same pass. See the COMM-300/COMM-500 sections above. |
| **P1** | Add monitoring for the new `comm-worker` process | Queue depth, consumer lag, and dead-letter accumulation currently have no alerting — a stuck or crashed worker would only be noticed by manually checking. |
| **P2** | HERMES-300 evaluation benchmark | A deterministic matcher exists; a benchmark set of known good/weak matches with recruiter-judgment ground truth does not. |
| **P2** | COMM-700 (Centrifugo) product integration | The instance exists; nothing documents who calls it or how. |
| **P2** | Rotate the Telegram bot token | Not strictly required, but it briefly appeared in a `docker logs` file during this session's testing before the logging bug was fixed. Requires Telegram/BotFather access this session doesn't have. |
| **P2** | HERMES-900 Role Packages | Correctly sequenced *after* the P0/P1 items above — do not start early. |
| **P3** | HERMES-850 live provider wiring | Intentionally deferred pending an OAuth-credential decision outside engineering's control — not urgent, but should be tracked so it isn't forgotten. |

---

# 9. Branch state note

At the time this document was built, `main` on `jobfynder/jobfynder-docs` does **not** yet contain the most current HERMES documentation. Two unmerged branches exist:

- `docs/2026-08-20-hermes-reconciliation` — reconciles capability matrix, route inventory, and doc map against the running service; adds `hermes-architecture-frozen-v1.md` and `hermes-complete-developer-guide.md`.
- `docs/2026-08-21-retire-portkey-litellm-rewrite` — everything above, plus retires the Portkey docs, rewrites HERMES-750/775 for LiteLLM, closes HERMES-850, and adds `hermes-core-integration-guide.md`. **This is the most current state and is what this canonical document is built from.**

**This canonical document assumes `docs/2026-08-21-retire-portkey-litellm-rewrite` gets merged to `main` first** (or its content is carried in the same push as this document) — otherwise `main` will show older, contradicted information (the Portkey-named files, the pre-reconciliation capability matrix) sitting alongside this canonical index, which recreates the exact problem this document exists to fix.

---

# 10. What was retired, and why

Moved to `archive/legacy-module-documentation/` (files, not deleted — history is preserved):

| File | Reason |
|---|---|
| `hermes/HERMES-documentation-map.md` | Superseded in full by this document (Part A + Part B + §7 mapping table) |
| `hermes/HERMES-450-channel-intake-parser-integration-foundation.md` | Superseded by `hermes/HERMES-450-channel-intake.md`, the actual closure record — kept the two side by side was causing confusion about which is current |
| `hermes/HERMES-300-closure-checklist.md` | Content folded into `hermes/HERMES-300-matching-decision-intelligence.md`'s closure section in this document's evidence trail; kept as a separate file only duplicated information |
| `hermes/HERMES-750-portkey-prompt-runtime-foundation.md` | Fully superseded by `hermes/HERMES-750-litellm-prompt-runtime-foundation.md` |
| `hermes/HERMES-775-portkey-production-runtime-and-multi-model-routing.md` | Fully superseded by `hermes/HERMES-775-litellm-production-runtime-and-multi-model-routing.md` |

**Explicitly NOT retired** — these remain live, first-class reference documents that this canonical document's Evidence sections point to, and should keep being updated as the code changes:

- `hermes/HERMES-000-architecture-governance.md` (with the correction noted in [§2.2](#22-hermes-300400-have-two-different-definitions-on-record) — its §4 module list is superseded, the rest of the file is still valid governance)
- `hermes/hermes-capability-matrix.md`, `hermes/hermes-api-route-inventory.md`, `hermes/hermes-deployment-runbook.md`, `hermes/hermes-engineering-playbook.md`, `hermes/hermes-platform-architecture.md`, `hermes/hermes-rbac-access-control.md`, `hermes/hermes-smoke-test.md`
- `hermes/hermes-architecture-frozen-v1.md`, `hermes/hermes-complete-developer-guide.md`, `hermes/hermes-core-integration-guide.md`
- Every remaining `hermes/HERMES-nnn-*.md` closure/foundation file — these are the Work-Item-level detail this document's Evidence sections cite; this document is the index and status layer above them, not a replacement for them.

---

# 11. Documentation governance going forward

Carried forward from `HERMES-000` §5–6 and the v3.0 draft, unified into one rule set:

1. **Every module status claim needs a receipt** — a git tag, a commit SHA, a live-tested endpoint response, or a script that passed. A sentence in a chat is not a receipt.
2. **Definition of Done** for any Hermes/COMM capability: API implemented, schema finalized, prompt versioned (if applicable), unit + integration tests passing, fixtures included, this canonical document updated, metrics/alerting configured where applicable, security reviewed, performance baseline recorded where applicable.
3. **One canonical file per module number.** If a module gets a rewrite (like HERMES-750/775 did for LiteLLM), rewrite the file in place and note the supersession at the top — don't leave two files with the same number both claiming to be current.
4. **COMM gets the same discipline as HERMES starting now.** No more undocumented production servers.
5. Final readable documentation lives in `jobfynder/jobfynder-docs` on `main`. Code repos (`hermes`, `jobFynder-BE-nestJS`, `jobFynder-FE-vite`, comm-gateway) may carry temporary implementation notes, but those are never the source of truth.
6. This document is updated whenever a module's maturity band changes — not on a schedule, on the event.

---

# 12. Next actions

1. ~~Merge `docs/2026-08-21-retire-portkey-litellm-rewrite` to `main`~~ — **done, merged via [PR #3](https://github.com/jobfynder/jobfynder-docs/pull/3), 2026-08-21.**
2. ~~Start a COMM-1 documentation pass~~ — **done same day**, see `comm/COMM-documentation-map.md` and [§5](#5-part-b--comm--comm-1-master-status-matrix).
3. ~~Fix the COMM-500 unhandled-exception gap~~ — **done same day**, commit `0c33580` on `jobfynder-infra`, deployed and live-verified.
4. ~~Add HTTP-layer rate limiting and automated backups to COMM-1~~ — **done same day**, same commit. See COMM-900/COMM-1000 in `comm/COMM-300-900-1000-infrastructure-posture.md`.
5. Run a restore test against a COMM-1 backup — backups exist now, but none has ever been restored to confirm it works.
6. ~~Merge `feature/comm-telegram-message-chunking` to `main` on `jobfynder-infra`~~ — **done same day**, clean merge, zero conflicts, server switched to `main`.
7. ~~Resolve the HERMES-600 status conflict~~ / ~~Close HERMES-500 for real~~ — **done same day**: both modules were already tagged (`hermes-600-foundation-v1`, `hermes-500-foundation-v1`, both dated 2026-07-07); their doc files just never recorded it. Same pattern found and fixed on HERMES-450 and HERMES-850 too — four undocumented tags corrected in one pass. **Phase 0 (repo/doc hygiene) is now fully complete.**
8. Assign an owner and timeline to each remaining P0/P1 item in [§8](#8-priority-matrix) — this is now Phase 1 (the RBAC gap and the HERMES-1000 exit condition).
9. Run and record the HERMES-1000 exit-condition grep across both app repos.
10. Treat this document, not any chat thread or prior summary, as the reference for all future Jobfynder HERMES/COMM planning.
11. Keep this document current automatically — see [§13](#13-keeping-this-document-current-automatically) for the recurring update mechanism now in place.

---

# 13. Keeping this document current automatically

A scheduled cloud agent ("Jobfynder HERMES+COMM docs sync," routine id `trig_01WdMud3w2uv3c74rJN2BX7A`, set up 2026-08-21) now checks `jobfynder/hermes` and `jobfynder/jobfynder-infra` for new commits **every hour** and updates this document and the `hermes/`/`comm/` module docs when a commit actually changes something documented here — a closure, a tag, a new endpoint, a fix. It reads diffs, not commit messages, and is instructed to skip anything that doesn't move a documented claim rather than pad this document with noise.

**How it stays safe:**
- **Every real content change goes through a PR** against `main` in `jobfynder/jobfynder-docs`, not a direct commit — a human still approves before the document of truth changes. The one exception is its own bookkeeping file (`.doc-sync-state.json`, tracks the last commit SHA it synced from each repo) on a no-op run, which is not a documentation claim.
- It's instructed to follow the same evidentiary rules used to build this document in the first place: cite real commit SHAs/tags/endpoints, never mark something more done than the evidence supports, and never fabricate a check result.
- **Live server re-verification (SSH to COMM-1/INTEL-1) is best-effort, not assumed.** The cloud environment this agent runs in does not currently have SSH credentials configured for those servers — it will explicitly say so in its PR description ("Live verification skipped: no SSH credentials configured") rather than pretend to have re-checked live state. If you want it to also re-verify live endpoints the way this session did, that requires deliberately adding SSH credentials to the cloud environment's configuration (at `https://claude.ai/code`) — a real security decision (standing production credentials in an automated environment), not something done automatically here.
- **Cadence:** hourly (`37 * * * *` UTC), not fully event-driven. A GitHub push-triggered version was attempted first and is the better fit for "update the instant something changes," but registering it failed — the GitHub account connected for this automation doesn't have push access to `jobfynder/hermes`, `jobfynder/jobfynder-infra`, or `jobfynder/jobfynder-docs` (all three tested, all three rejected with the same permission error). To switch to real push-triggering, grant that GitHub App push access to the `jobfynder` org's repos, then attach a `push`-event webhook trigger to the same routine.

**To check on it:** the routine is visible and manageable at `https://claude.ai/code/routines` (or via the `/schedule` skill in a Claude Code session) — its run history shows every sync attempt, what it changed (if anything), and any PR it opened.
