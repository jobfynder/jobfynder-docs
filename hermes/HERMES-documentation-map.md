# Hermes Documentation Map

Status: Active rule
Owner: Jobfynder-Infra

---

## Main Rule

Final readable Hermes documentation must live in:

/opt/jobfynder-docs/hermes

GitHub repo:

jobfynder/jobfynder-docs

Branch:

main

---

## Code Repo Rule

Hermes code lives in:

/opt/hermes

Use this repo for:

- application code
- tests
- Docker files
- runtime logic
- temporary implementation notes

Do not treat /opt/hermes/docs as the final documentation source.

---

## Official Hermes Docs

Current official Hermes docs include:

- hermes/HERMES-000-architecture-governance.md
- hermes/HERMES-100-core-platform-closure-checklist.md
- hermes/HERMES-200-understanding-foundation.md
- hermes/HERMES-300-matching-decision-intelligence.md
- hermes/HERMES-400-taxonomy-signal-intelligence.md
- hermes/hermes-api-route-inventory.md
- hermes/hermes-capability-matrix.md
- hermes/hermes-deployment-runbook.md
- hermes/hermes-engineering-playbook.md
- hermes/hermes-platform-architecture.md
- hermes/hermes-rbac-access-control.md
- hermes/hermes-smoke-test.md
- hermes/HERMES-750-litellm-prompt-runtime-foundation.md — renamed and rewritten 2026-08-21, was HERMES-750-portkey-prompt-runtime-foundation.md
- hermes/HERMES-775-litellm-production-runtime-and-multi-model-routing.md — renamed and rewritten 2026-08-21, was HERMES-775-portkey-production-runtime-and-multi-model-routing.md; retired, see the doc for why
- hermes/HERMES-850-email-parsing-foundation.md — added 2026-08-21, closing HERMES-850
- hermes/hermes-architecture-frozen-v1.md — added 2026-08-20. Reconciled architecture reference (built vs. deferred capability inventory, response contract, cost discipline, RBAC gaps). Was previously living only inside the Core/Frontend repos' `docs/` folders, never in this repo — moved here to comply with the Main Rule above.
- hermes/hermes-complete-developer-guide.md — added 2026-08-20. Per-endpoint integration guide (99 endpoints), companion to the architecture doc above. Same prior-location issue.

---

## Module Documentation Pattern

For every Hermes module:

1. Build and test code in /opt/hermes
2. Keep temporary developer notes there only if needed
3. Write final readable documentation in /opt/jobfynder-docs/hermes
4. Commit and push docs to jobfynder/jobfynder-docs main
5. Take snapshot after major module closure

---

## Closed Modules

- HERMES-850 — Email Parsing Foundation
  - Final code branches: feature/hermes-850-email-parsing, feature/hermes-850-gmail-graph-providers
  - Official doc: hermes/HERMES-850-email-parsing-foundation.md
  - Status: Closed (foundation) — live provider credentials deliberately deferred, see the doc §7

- HERMES-800 — Resume Builder Intelligence Foundation
  - Final code branch: feature/hermes-800-resume-builder-intelligence
  - Final code commit: d9196b1
  - Final code tag: hermes-800-resume-builder-foundation-v1
  - Official doc: hermes/HERMES-800-resume-builder-intelligence-foundation.md
  - Status: Closed


- HERMES-750 — LiteLLM Prompt Runtime Foundation (originally Portkey, migrated and doc rewritten 2026-08-21)
  - Final code branch: feature/hermes-750-portkey-prompt-runtime (name is historical; runtime now runs on LiteLLM)
  - Final code commit: 1869e82
  - Final code tag: hermes-750-prompt-runtime-v1
  - Official doc: hermes/HERMES-750-litellm-prompt-runtime-foundation.md

- HERMES-700 — Multi-Agent Foundation
  - Final code branch: `feature/hermes-700-multi-agent`
  - Final code commit: `c2fc718`
  - Final code tag: `hermes-700-foundation-v1`
  - Official doc: `hermes/HERMES-700-multi-agent-foundation.md`


- [HERMES-600 — Integrations Foundation](./HERMES-600-integrations-foundation.md) — Closed

- [HERMES-500 — Submission Intelligence & Workflow Foundation](./HERMES-500-submission-intelligence-workflow-foundation.md) — Closed

HERMES-100 Core Platform:

hermes/HERMES-100-core-platform-closure-checklist.md

HERMES-200 Understanding:

hermes/HERMES-200-understanding-foundation.md

Code tag:

hermes-200-foundation-v1

---

HERMES-300 Matching & Decision Intelligence:

hermes/HERMES-300-matching-decision-intelligence.md

Closure checklist:

hermes/HERMES-300-closure-checklist.md

Code tag:

hermes-300-foundation-v1

Checkpoint tags:

- hermes-300-matching-policy-v1
- hermes-300-policy-guardrail-v1
- hermes-300-active-policy-endpoint-v1
- hermes-300-policy-snapshot-results-v1
- hermes-300-foundation-v1

---

## HERMES-400 Closed Module

HERMES-400 Taxonomy & Signal Intelligence:
- Status: Closed
- Started from HERMES-300 closed baseline
- Code branch: feature/hermes-400-taxonomy-intelligence
- Code tag: hermes-400-foundation-v1
- Official doc: hermes/HERMES-400-taxonomy-signal-intelligence.md

## HERMES-400 Taxonomy Routes


| HERMES-400 | `/understanding/taxonomy/skills` | GET | Internal/public depending deployment policy | understanding:read | Read legacy skills taxonomy |
| HERMES-400 | `/understanding/taxonomy/skills/canonical` | GET | Internal/public depending deployment policy | understanding:read | Read canonical skill taxonomy |
| HERMES-400 | `/understanding/taxonomy/skills/aliases` | GET | Internal/public depending deployment policy | understanding:read | Read skill alias taxonomy |
| HERMES-400 | `/understanding/taxonomy/job-titles` | GET | Internal/public depending deployment policy | understanding:read | Read canonical job title taxonomy |
| HERMES-400 | `/understanding/taxonomy/job-title-aliases` | GET | Internal/public depending deployment policy | understanding:read | Read job title alias taxonomy |
| HERMES-400 | `/understanding/taxonomy/snapshot` | GET | Internal/public depending deployment policy | understanding:read | Read taxonomy version snapshot |
| HERMES-400 | `/understanding/taxonomy/normalize` | POST | Internal/public depending deployment policy | understanding:parse | Normalize skills and job titles |
| HERMES-400 | `/understanding/taxonomy/extract-signals` | POST | Internal/public depending deployment policy | understanding:parse | Extract normalized taxonomy signals from text |
| HERMES-400 | `/understanding/taxonomy/suggestions` | POST | Internal protected recommended | understanding:parse | Create review-required taxonomy suggestions |

## Active Module

**Correction, 2026-08-20:** this section named HERMES-775 (Portkey Production Runtime) as active since 2026-07-14, five weeks with no update. In that time Portkey was removed from the project entirely — LiteLLM + Langfuse is now the sole LLM path (see `hermes-capability-matrix.md` HERMES-600 rows and `hermes-architecture-frozen-v1.md` Addendum §14). HERMES-775 as originally scoped (Portkey-specific multi-model routing) was superseded, not completed.

**Follow-up, 2026-08-21:** HERMES-775 has been formally retired and its doc rewritten — see `hermes/HERMES-775-litellm-production-runtime-and-multi-model-routing.md`. Most of its original scope (per-key budgets, model allowlists, provider routing) turned out to already be built into LiteLLM's own admin proxy, verified directly against the live dashboard. What's still genuinely open is narrower than the original plan — see that doc §3 before anyone picks this stream back up.

**Follow-up, 2026-08-21:** HERMES-850 is now closed as a foundation module — see `hermes/HERMES-850-email-parsing-foundation.md`. Parsing, routing, and both provider connectors (Gmail, Microsoft Graph) are built and verified (13/13 checks). Live provider credentials remain deliberately deferred (§7 of that doc) — a product decision, not an oversight.

No Hermes module is currently marked active. See `hermes-capability-matrix.md` §3 for capabilities (Context Cards, Broadcast, Runtime Cache, Submission/Messaging extraction) that are built and live but never got an official module number — a good candidate for the next module to formally open.


## HERMES-700 Closed Module

HERMES-700 Multi-Agent Foundation:

- Status: Closed
- Started from HERMES-600 closed baseline
- Code branch: `/opt/hermes` branch `feature/hermes-700-multi-agent`
- Official doc: `hermes/HERMES-700-multi-agent-foundation.md`
- Purpose: role-aware, permission-aware, auditable Hermes agent foundation
