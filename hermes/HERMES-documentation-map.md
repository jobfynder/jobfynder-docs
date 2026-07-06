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
- hermes/hermes-api-route-inventory.md
- hermes/hermes-capability-matrix.md
- hermes/hermes-deployment-runbook.md
- hermes/hermes-engineering-playbook.md
- hermes/hermes-platform-architecture.md
- hermes/hermes-rbac-access-control.md
- hermes/hermes-smoke-test.md

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

HERMES-100 Core Platform:

hermes/HERMES-100-core-platform-closure-checklist.md

HERMES-200 Understanding:

hermes/HERMES-200-understanding-foundation.md

Code tag:

hermes-200-foundation-v1

---

## Current Module

HERMES-300 Matching & Decision Intelligence:

hermes/HERMES-300-matching-decision-intelligence.md

Closure checklist:

hermes/HERMES-300-closure-checklist.md

Code branch:

feature/hermes-300-matching

Checkpoint tags:

- hermes-300-matching-policy-v1
- hermes-300-policy-guardrail-v1
- hermes-300-active-policy-endpoint-v1
- hermes-300-policy-snapshot-results-v1
- hermes-300-foundation-v1
