# Hermes API Route Inventory

Status: Active
Owner: Jobfynder-Infra
Last updated: 2026-08-20 (reconciliation — previous version dated 2026-07-06 covered 18 of 99 live routes; see Reconciliation Note below)

---

## Rule

Only `/health` should remain public.

Every other route must have a clear target RBAC permission before external production exposure.

**Known gap, not yet resolved:** `/understanding/*` and `/submissions/evaluate*` currently have no RBAC check at all — no `require_permission` dependency on those routes. This was flagged in `hermes-architecture-frozen-v1.md` §11 (2026-08-15) and is still open. Not fixed as part of this reconciliation — it's the developer's item, tracked separately.

---

## Reconciliation note — 2026-08-20

The previous version of this file (last touched 2026-07-06) documented 18 routes. The live service — confirmed against the actual router registrations in `app/main.py` on the `checkpoint/2026-08-20-frozen-v1-uncommitted-state` branch — has 30 routers and 99 endpoints. The table below reflects what's actually running, sourced from `hermes-complete-developer-guide.md` §16 (point-in-time snapshot, 2026-08-15) and cross-checked against the live router list. For the always-current machine-readable version, use `GET /openapi.json` against the running service rather than this file.

---

## Full Route Table (99 endpoints, live as of 2026-08-15, cross-checked 2026-08-20)

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

---

## Official References

HERMES-200 official doc: `hermes/HERMES-200-understanding-foundation.md`
HERMES-300 official doc: `hermes/HERMES-300-matching-decision-intelligence.md`
HERMES-800 official doc: `hermes/HERMES-800-resume-builder-intelligence-foundation.md`
Architecture (superseding capability registry): `hermes/hermes-architecture-frozen-v1.md`
Full endpoint use-case guide: `hermes/hermes-complete-developer-guide.md`
Documentation map: `hermes/HERMES-documentation-map.md`

---

## Maintenance Rule

When a new Hermes route is added, update this file and the official module documentation in `/opt/jobfynder-docs/hermes`. This rule was not followed between 2026-07-06 and 2026-08-20 — 81 routes shipped without this file being updated. Do not let that gap repeat.
