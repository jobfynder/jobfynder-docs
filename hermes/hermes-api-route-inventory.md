# Hermes API Route Inventory

Status: Active
Owner: Jobfynder-Infra
Last updated: 2026-07-06

---

## Rule

Only `/health` should remain public.

Every other route must have a clear target RBAC permission before external production exposure.

---

## Active Routes

| Stream | Route | Method | Access | Target Permission | Purpose |
|---|---|---:|---|---|---|
| HERMES-100 | `/health` | GET | Public | None | Health check |
| HERMES-100 | `/security/rbac/status` | GET | Protected | `security:read` | RBAC status |
| HERMES-100 | `/mission-control` | GET | Protected | `mission_control:read` | Mission board |
| HERMES-100 | `/session-brief` | GET | Protected | `session_brief:read` | Session brief |
| HERMES-100 | `/workspace` | GET | Protected | `workspace:read` | Workspace |
| HERMES-100 | `/actions` | GET | Protected | `actions:read` | List actions |
| HERMES-100 | `/actions/{action_id}` | GET | Protected | `actions:read` | Get action |
| HERMES-100 | `/actions` | POST | Protected | `actions:write` | Create action |
| HERMES-100 | `/actions/{action_id}` | PUT | Protected | `actions:write` | Update action |
| HERMES-100 | `/actions/{action_id}` | DELETE | Protected | `actions:write` | Delete action |
| HERMES-100 | `/v1/engineering-memory/generate` | POST | Protected | `engineering_memory:write` | Generate Engineering Memory |
| HERMES-100 | `/v1/messages/understand` | POST | Protected | `messages:understand` | Legacy text understanding |
| HERMES-100 | `/v1/jobs/parse` | POST | Protected | `jobs:parse` | Legacy job parser |
| HERMES-100 | `/v1/consultants/parse` | POST | Protected | `consultants:parse` | Legacy consultant parser |
| HERMES-200 | `/understanding/parse-text` | POST | Internal foundation | `understanding:parse` | Parse resume, JD, or message text |
| HERMES-200 | `/understanding/parse-file` | POST | Internal foundation | `understanding:parse` | Upload and parse resume/JD files |
| HERMES-200 | `/understanding/taxonomy/skills` | GET | Internal foundation | `understanding:read` | Read skills taxonomy |

---

## Active / Planned Routes

| Stream | Route | Method | Access | Target Permission | Purpose |
|---|---|---:|---|---|---|
| HERMES-300 | `/matching/policy` | GET | Internal protected | `matching:evaluate` | Read active matching policy weights, thresholds, and matcher version |
| HERMES-300 | `/matching/resume-to-job` | POST | Internal protected | `matching:evaluate` | Score resume-to-job match with deterministic local matcher |
| HERMES-300 | `/matching/resume-to-job/from-understanding` | POST | Internal protected | `matching:evaluate` | Score resume-to-job match from HERMES-200 parsed output |

---

## Official References

HERMES-200 official doc:

`hermes/HERMES-200-understanding-foundation.md`

HERMES-300 official doc:

`hermes/HERMES-300-matching-decision-intelligence.md`

Documentation map:

`hermes/HERMES-documentation-map.md`

---

## Maintenance Rule

When a new Hermes route is added, update this file and the official module documentation in `/opt/jobfynder-docs/hermes`.

## HERMES-750 Prompt Runtime Routes

| Module | Route | Method | Protection | Permission | Purpose |
|---|---|---:|---|---|---|
| HERMES-750 | /prompts/health | GET | RBAC | agents:read | Read prompt runtime health |
| HERMES-750 | /prompts/registry | GET | RBAC | agents:read | List prompt registry definitions |
| HERMES-750 | /prompts/{prompt_id} | GET | RBAC | agents:read | Read a single prompt definition |
| HERMES-750 | /prompts/run | POST | RBAC | agents:run | Render and run prompt through dry-run-first policy |
