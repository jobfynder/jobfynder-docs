# HERMES-750 — Portkey Prompt Runtime Foundation

Status: Closed
Code Branch: feature/hermes-750-portkey-prompt-runtime
Code Commit: 1869e82
Code Tag: hermes-750-prompt-runtime-v1
Closed: 2026-07-10
Server: INTEL-1 / jobfynder-intel-01

## Purpose

HERMES-750 adds the Portkey-ready Prompt Runtime foundation for Hermes.

It gives Hermes a controlled prompt layer for Resume Builder, Matching explanations, Agents, and Support workflows while keeping external LLM calls disabled by default.

Default runtime mode: HERMES_PROMPT_RUNTIME_DRY_RUN=true

## Closure Facts

- runtime_version: hermes_prompt_runtime_v1
- registry_version: hermes_prompt_registry_v1
- prompt_count: 4
- dry_run_default: true
- portkey_configured: false
- external_llm_call: false

## Completed

- Prompt runtime package
- Versioned prompt registry
- Resume Builder summary improvement prompt
- Resume Builder bullet rewrite prompt
- Matching fit explanation prompt
- Support reply draft prompt
- Dry-run execution path
- Portkey-compatible live adapter
- Resume no-fabrication safety guardrail
- Required-variable validation
- Human-review-first policy
- JSONL prompt run logging
- RBAC-protected /prompts APIs
- Prompt runtime validation scripts
- API fixtures
- Portkey env markers in .env.example

## APIs

- GET /prompts/health requires agents:read
- GET /prompts/registry requires agents:read
- GET /prompts/{prompt_id} requires agents:read
- POST /prompts/run requires agents:run

## Resume Builder Safety

Hermes may improve wording and clarity.

Hermes must not invent employers, dates, degrees, certifications, projects, tools, clients, work authorization, metrics, years of experience, job titles, or achievements.

If evidence is missing, Hermes must ask a question or mark the field as missing.

## Closure

HERMES-750 is closed as a production-safe, dry-run-first, Portkey-ready Prompt Runtime foundation.
