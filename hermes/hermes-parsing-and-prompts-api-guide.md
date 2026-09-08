# Hermes Parsing & Prompts API Guide

Status: Active — companion to `hermes-complete-developer-guide.md` (referenced from there and from `hermes-architecture-frozen-v1.md` §9 as the full prompt catalog; this file did not exist until 2026-09-07 despite being referenced by both since at least 2026-08-15 — created here to close that gap, sourced from the live running service rather than reconstructed from memory).

Server: jobfynder-intel-01, `GET /prompts/registry` (bearer token required — see `hermes-rbac-access-control.md`)
Source: live registry pull, 2026-09-07. At that time: `registry_version: hermes_langfuse_prompt_registry_v1`, `prompt_count: 38` — matched the count both companion docs and `JOBFYNDER-HERMES-COMM-CANONICAL.md` §7 had independently cited since 2026-08-21.

**Superseded the next day — re-verify before trusting "38" anywhere.** Re-checked live 2026-09-08: `registry_version` is now `hermes_prompt_registry_v1` (reused from the original 2026-07-10 static registry — see `hermes/HERMES-750-litellm-prompt-runtime-foundation.md` §11) and `prompt_count` is **42**, not 38. Cause: commit `8319c43` on `jobfynder/hermes` (2026-09-07, primarily a resume-parsing improvement — see `hermes/HERMES-200-understanding-foundation.md`) added a local fallback prompt registry for resilience against a Langfuse outage, but merges it into `list_prompts()` as a **union**, not a fallback used only when Langfuse is unreachable — so the 4 old, already-retired prompt IDs it contains resurface in the live registry unconditionally. **The 4 sections below are §§1-38, current as of 2026-09-07; the 4 resurrected legacy prompts (`resume_builder.summary_improve`, `resume_builder.bullet_rewrite`, `matching.fit_explanation`, `agents.support_reply_draft`) are listed separately in §3a — do not treat them as genuine new capability, each duplicates an existing jf.* prompt below.** Full analysis: PR #19 on `jobfynder/jobfynder-docs` (open as of 2026-09-08) and its update to `JOBFYNDER-HERMES-COMM-CANONICAL.md` §4 (HERMES-750/775 section).

**Note (2026-09-07, later same day; corrected 2026-09-08).** Commit `8319c43` on `jobfynder/hermes` `main` renamed `list_prompts()`'s `registry_version` field from `hermes_langfuse_prompt_registry_v1` to `hermes_prompt_registry_v1`, and made `list_prompts()`/`get_prompt()` merge a local fallback registry (`app/prompt_runtime/local_prompts.py`, `app/prompt_runtime/registry.json`) with the Langfuse-hosted one — see `HERMES-750-litellm-prompt-runtime-foundation.md` §11 for the full trail. **This note originally said the prompt count was unaffected — that turned out to be wrong.** `registry.json` carries six prompts, not two: the two new fallback copies (`jf.resume.parse`, `jf.onboarding.profile-import.extract`, both already in the 38 below) plus four prompt IDs left over from the original 2026-07-10 static registry that §7 of the HERMES-750 doc already documents as retired from Langfuse. Because `list_prompts()`'s merge is a union (local ∪ Langfuse-cache), those four are not overridden and can resurface in `GET /prompts/registry` whenever this code runs, including with Langfuse healthy — so `prompt_count` may read up to 42, not 38, once this deploys. Not re-pulled live for this note — no SSH/API credentials were available in this environment to re-verify against INTEL-1; re-pull `GET /prompts/registry` and update the header line above once it does.

---

## 1. How this catalog works

Every prompt here is fetched live by Hermes from Langfuse (project `jobfynder-ai`) — this file is a point-in-time snapshot for discoverability, not the runtime source. As of 2026-09-07, two of the fallback-extraction prompts below (`jf.resume.parse`, `jf.onboarding.profile-import.extract`) also have a hardcoded local copy, and `GET /prompts/registry` now also merges in four other, retired local-only prompt IDs not in this catalog — see the note above and `HERMES-750-litellm-prompt-runtime-foundation.md` §11. For the always-current version, call `GET /prompts/registry` yourself or `GET /prompts/{prompt_id}` for one prompt's full detail (includes the actual `system_template`/`user_template` text, omitted below for brevity — see `hermes-complete-developer-guide.md` §11 for the `/prompts/run` execution contract).

Each prompt's `metadata.execution_class` matches the classes defined in `hermes-architecture-frozen-v1.md` §3:
- **HERMES_FALLBACK_LLM** — Hermes attempts deterministic extraction first; this prompt only fires below a confidence threshold.
- **HERMES_LLM** — genuinely generative; no deterministic path exists for this task.

`litellm_router_alias` / `litellm_fallback_alias` map to the three abstract aliases in `hermes-architecture-frozen-v1.md` §9 (`extract-fast`, `generate-small`, `reasoning-small`), all currently backed by `anthropic/claude-haiku-4-5` per `JOBFYNDER-HERMES-COMM-CANONICAL.md` §4.

---

## 2. Fallback-extraction prompts (HERMES_FALLBACK_LLM)

Hermes tries a deterministic parser first for every one of these; the LLM only runs below the confidence threshold documented in `hermes-architecture-frozen-v1.md` §4.

| Prompt ID | Domain | Router alias | Required variables |
|---|---|---|---|
| `jf.resume.parse` | resume | extract-fast | `clean_resume`, `resume_schema` |
| `jf.onboarding.profile-import.extract` | onboarding | extract-fast | `clean_text`, `profile_schema`, `source_type` |
| `jf.jobs.jd.extract` | jobs | extract-fast | `clean_jd`, `job_schema`, `taxonomy_subset` |
| `jf.job-tracker.update.extract` | job-tracker | extract-fast | `allowed_stages`, `message`, `tracker_context` |
| `jf.submissions.status.extract` | submissions | extract-fast | `message`, `statuses`, `submission_context` |
| `jf.messaging.actions.extract` | messaging | extract-fast | `allowed_actions`, `context`, `messages` |
| `jf.broadcast.requirement.extract` | broadcast | extract-fast | `broadcast_schema`, `message` |
| `jf.broadcast.hotlist.extract` | broadcast | extract-fast | `hotlist_schema`, `message` |

That's 8 — matches `Jobfynder_AI_Architecture_v3.md`'s original count of "8 conditional fallbacks" exactly, even though the total catalog has grown from that document's 35 to today's 38 (3 genuine-generation prompts were added since: `jf.resume.section.polish`, `jf.job-tracker.interview.prep`, `jf.job-tracker.offer.analyze` — see §3).

## 3. Genuine-generation prompts (HERMES_LLM)

No deterministic path exists for these — Hermes builds a Context Card (never raw text) and hands it to the model.

| Prompt ID | Domain | Router alias | Required variables | Use case |
|---|---|---|---|---|
| `jf.assistant.response.generate` | assistant | generate-small | `persona`, `request`, `tool_results` | Settings/personal assistant replies, grounded only in supplied tool results |
| `jf.broadcast.rewrite` | broadcast | generate-small | `audience`, `broadcast`, `max_words` | Rewrite a live-feed broadcast for a target audience |
| `jf.jobs.fit.explain` | jobs | reasoning-small | `candidate_card`, `job_card`, `match_result` | Explain an *existing* deterministic match score — never generates its own score |
| `jf.jobs.jd.rewrite-inclusive` | jobs | generate-small | `job`, `max_words` | Bias-neutral JD rewrite |
| `jf.jobs.jd.quality-review` | jobs | generate-small | `job`, `job_policy` | JD quality feedback against policy |
| `jf.dashboard.daily-brief.generate` | dashboard | generate-small | `compressed_activity`, `deadlines`, `persona`, `timezone` | Daily brief on the user dashboard |
| `jf.job-tracker.followup.recommend` | job-tracker | reasoning-small | `allowed_actions`, `history_summary`, `tracker_item` | Suggest next action on a stale tracker item |
| `jf.job-tracker.interview.prep` | job-tracker | reasoning-small | `candidate_card`, `job_card` | Consultant-facing interview prep brief (distinct from `jf.screening.questions.generate`, the recruiter's question generator) — no LiteLLM fallback alias configured |
| `jf.job-tracker.offer.analyze` | job-tracker | reasoning-small | `offer_details`, `candidate_card`, `market_context` | Flags missing offer info, suggests negotiation points — never invents market-rate figures it wasn't given; no fallback alias configured |
| `jf.job-tracker.notes.summarize` | job-tracker | generate-small | `notes` | Summarize tracker notes |
| `jf.network.connection-request.draft` | network | generate-small | `recipient_card`, `sender_card`, `shared_context`, `tone` | "Connect Now" / re-engagement drafting (reuse for both) |
| `jf.network.relationship.summarize` | network | generate-small | `compressed_interactions`, `contact_card` | Relationship summary |
| `jf.network.relationship.next-action` | network | reasoning-small | `allowed_actions`, `relationship_summary`, `relevant_opportunities` | Next-action suggestion for a relationship |
| `jf.messaging.reply.draft` | messaging | generate-small | `compressed_conversation`, `entity_cards`, `max_words`, `tone` | Draft a message reply |
| `jf.messaging.conversation.summarize` | messaging | generate-small | `messages` | Summarize a message thread |
| `jf.introductions.request.draft` | introductions | generate-small | `candidate_card`, `job_card`, `recipient_card`, `sender_card`, `tone` | Request-introduction drafting |
| `jf.profile.about.generate` | profile | generate-small | `persona`, `profile_card`, `tone` | Profile "About" section |
| `jf.profile.headline.generate` | profile | generate-small | `persona`, `profile_card` | Profile headline |
| `jf.profile.achievement.rewrite` | profile | generate-small | `raw_notes`, `role` | Rewrite an achievement bullet |
| `jf.resume.gaps.analyze` | resume | reasoning-small | `candidate_card`, `job_card` | Resume/job gap analysis |
| `jf.resume.cover-letter.generate` | resume | generate-small | `candidate_card`, `job_card`, `tone`, `verified_company_context` | Cover letter generation |
| `jf.resume.section.polish` | resume | generate-small | `section_type`, `raw_content`, `role` | Polishes a resume section (e.g. Education, Certifications) — no fallback alias configured |
| `jf.resume.experience.rewrite` | resume | generate-small | `raw_bullets`, `role`, `target_skills` | Rewrite experience bullets |
| `jf.resume.tailor` | resume | generate-small | `job_card`, `structured_resume` | Tailor a resume to a target job |
| `jf.resume.summary.generate` | resume | generate-small | `candidate_card`, `job_card`, `tone` | Resume professional summary |
| `jf.screening.questions.generate` | screening | generate-small | `candidate_card`, `job_card`, `known_gaps`, `limit` | Recruiter's screening question generator |
| `jf.submissions.package.generate` | submissions | generate-small | `candidate_card`, `job_card`, `selected_evidence` | Submission package generation |
| `jf.marketplace.listing.rewrite` | marketplace | generate-small | `buyer_persona`, `listing`, `max_words` | Marketplace listing rewrite |
| `jf.support.reply.draft` | support | generate-small | `issue`, `safe_account_context`, `verified_steps` | Support reply drafting |
| `jf.support.ticket.summarize` | support | generate-small | `messages`, `safe_logs` | Support ticket summary |

That's 30 genuine-generation prompts, bringing the total to **38** (8 fallback + 30 generation) — the count as of 2026-09-07. See §3a for the 4 that have since resurfaced.

## 3a. Resurrected legacy prompts (live as of 2026-09-08 — not genuine new capability)

Re-verified live 2026-09-08: these 4 now appear in `GET /prompts/registry` alongside the 38 above, bringing the reported count to 42. Each is the original 2026-07-10 static-registry entry (`default_model` is a literal provider string, `anthropic/claude-haiku-4-5`, not a LiteLLM router alias — structurally different from every prompt in §2/§3, which carry `metadata.execution_class`/`litellm_router_alias`). They were retired from active use when Langfuse replaced the static registry (2026-08-21) but resurfaced as a side effect of commit `8319c43`'s local-fallback-registry merge (see the status note at the top of this file). **Each duplicates an existing `jf.*` prompt — treat the `jf.*` version as authoritative, not these:**

| Legacy prompt ID | Required variables | Duplicates |
|---|---|---|
| `resume_builder.summary_improve` | `source_text` | `jf.resume.summary.generate` |
| `resume_builder.bullet_rewrite` | `source_text` | `jf.resume.experience.rewrite` |
| `matching.fit_explanation` | `match_result` | `jf.jobs.fit.explain` |
| `agents.support_reply_draft` | `issue_summary` | `jf.support.reply.draft` |

**Not decided as of this writing:** whether `list_prompts()`'s merge behavior should change to fallback-only (only surface these when Langfuse is genuinely unreachable), or whether these 4 IDs should simply be deleted from `registry.json` now that the modern `jf.*` equivalents exist. Follow PR #19 on `jobfynder/jobfynder-docs` and `hermes/HERMES-750-litellm-prompt-runtime-foundation.md` §11 for resolution.

## 4. Prompts named in other docs but not present in the live registry

`hermes-architecture-frozen-v1.md` §9 notes "roughly 20 prompt names referenced in the original blueprint do not exist in Langfuse... the absence of the prompt isn't the gap, the absence of the underlying deterministic capability is." Consistent with that: `Jobfynder_AI_Architecture_v3.md`'s §7 catalog (35 prompts, 2026-08-04) lists several names not in the live 38 above — e.g. `jf.dashboard.next-actions.rank`, `jf.jobs.duplicate.assess`, `jf.matching.candidate-job.score` — all marked "REMOVE FROM LANGFUSE: Hermes/Core responsibility" in that same document's §21 disposition table. That disposition already explains the gap; don't treat their absence here as a regression.

## 5. Safety

Every prompt carries `safety_policy: hermes_prompt_safety_v1` and every `/prompts/run` response includes `safety.human_review_required: true` (per `hermes-complete-developer-guide.md` §11) — nothing in this catalog auto-publishes or auto-sends regardless of `execution_class`.

## 6. Related

- `hermes-complete-developer-guide.md` — per-endpoint integration guide; §11 covers the `/prompts/run` execution contract this catalog feeds into.
- `hermes-architecture-frozen-v1.md` — §9 is the architectural context for this catalog (why 38, not the original 35 or 92).
- `Jobfynder_AI_Architecture_v3.md` (2026-08-04, historical/superseded) — the original 35-prompt design intent and the full disposition table (§21) explaining what was cut and why. Superseded in full by `hermes-architecture-frozen-v1.md` (2026-08-15) as the operative reference; kept only as background for why specific prompts were deliberately not built.
