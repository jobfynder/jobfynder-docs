# HERMES-775 — Portkey Production Runtime and Multi-Model Routing

Status: Open
Server: INTEL-1 / jobfynder-intel-01
Code Repository: /opt/hermes
Code Branch: feature/hermes-775-prompt-runtime-production
Base Code Tag: hermes-800-resume-builder-foundation-v1
Base Code Commit: d9196b1
Proposed Final Code Tag: hermes-775-prompt-runtime-production-v1
Documentation Repository: /opt/jobfynder-docs
Documentation Branch: main

## Goal

Complete production Portkey integration and add capability-based multi-model routing while preserving parser-first, deterministic-first, safety-first behavior.

Parsers, taxonomy, matching, and deterministic rules must be used whenever they can solve the task. LLMs are limited to narrowly scoped generation and rewriting.

## Execution Policy

- Resume parsing: HERMES-200 deterministic parser
- Skill normalization: HERMES-400 taxonomy
- Matching, tailoring gap analysis, and quality analysis: deterministic
- Summary and bullet rewrite: small-model alias
- Failed eligible rewrite: medium-model alias once
- Strong-model execution: disabled by default
- Full-resume rewrite: disabled
- Missing evidence, failed safety, unavailable dependencies, or exceeded budgets: blocked or needs_review
- Human review required
- Automatic publishing disabled
- No uncontrolled retries or silent escalation

## Required Packages

```text
app/model_routing/
├── __init__.py
├── models.py
├── policy.py
├── router.py
├── budgets.py
├── telemetry.py
├── safety.py
└── portkey_adapter.py
```

Resume Builder output protection:

```text
app/resume_builder/
├── claim_extraction.py
├── evidence_validator.py
└── output_guard.py
```

## Model Aliases

- resume-small
- resume-medium
- resume-strong

Prompt definitions must not hardcode provider-specific model names.

## Required Controls

- Per-request, per-user daily, per-tenant monthly, capability, and global emergency budgets
- Input/output token limits
- Maximum LLM calls, retry counts, and escalation counts
- Capability allowlists, environment restrictions, and feature flags
- Portkey live-call gates
- Circuit breaker and provider failure handling
- Prompt-injection protection
- Claim-level evidence verification
- PII and secret redaction
- Sensitive-payload separation and configurable retention
- Provider-independent telemetry and audit metadata

## Live-Call Gates

Live execution requires:

- HERMES_EXTERNAL_LLM_CALLS_ENABLED=true
- HERMES_PORTKEY_ENABLED=true
- Prompt permits live execution
- Capability routing policy exists
- Environment permits live execution
- Budget permits the call
- Source evidence exists
- User explicitly requested generation
- Output safety validation is enabled

Otherwise execution remains dry_run or returns blocked / needs_review.

## Initial Runtime Defaults

```text
HERMES_EXTERNAL_LLM_CALLS_ENABLED=false
HERMES_PROMPT_RUNTIME_DRY_RUN=true
HERMES_PORTKEY_ENABLED=false
```

Staging must be activated before production. Production activation is a separate explicit step.

## HERMES-800 Integration

Migrate only:

- POST /resume-builder/summary/suggest
- POST /resume-builder/bullets/suggest

Keep deterministic behavior unchanged for:

- POST /resume-builder/analyze
- POST /resume-builder/skills/normalize
- POST /resume-builder/tailor
- POST /resume-builder/quality/analyze

Responses must retain human-review, source-traceability, prompt, routing, cost, unsupported-claim, mode, provider/model-alias, and fallback metadata.

## Safety Rules

- Parser-first and deterministic-first
- No fabricated resume content
- Human review required
- Dry-run and external-AI-off by default
- No hardcoded provider/model dependency
- No uncontrolled retries
- No silent escalation
- No raw resume content, secrets, access tokens, or Portkey keys in operational logs
- Strong-model execution disabled by default

## Current Module State

HERMES-775 is open. No application implementation changes, production Portkey calls, or external LLM execution have been enabled.
