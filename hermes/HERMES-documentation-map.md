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
- hermes/HERMES-750-portkey-prompt-runtime-foundation.md

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

- HERMES-750 — Portkey Prompt Runtime Foundation
  - Final code branch: feature/hermes-750-portkey-prompt-runtime
  - Final code commit: 1869e82
  - Final code tag: hermes-750-prompt-runtime-v1
  - Official doc: hermes/HERMES-750-portkey-prompt-runtime-foundation.md

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

Current active Hermes module: HERMES-800 — Resume Builder Intelligence Foundation.

- Code branch: feature/hermes-800-resume-builder-intelligence
- Official doc: hermes/HERMES-800-resume-builder-intelligence-foundation.md
- Status: Open


## HERMES-700 Closed Module

HERMES-700 Multi-Agent Foundation:

- Status: Closed
- Started from HERMES-600 closed baseline
- Code branch: `/opt/hermes` branch `feature/hermes-700-multi-agent`
- Official doc: `hermes/HERMES-700-multi-agent-foundation.md`
- Purpose: role-aware, permission-aware, auditable Hermes agent foundation
