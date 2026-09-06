---
id: ADR-0006
title: Hermes is the Intelligence Layer; Jobfynder Core is the System of Record
status: accepted
date: 2026-07-19
repository: hermes
authors: [Pavan]
context: >
  Jobfynder needs AI for parsing, matching, taxonomy, messaging assistance,
  recommendations, and workflow intelligence. AI must be able to evolve
  without compromising business data integrity.
decision: >
  Hermes is the Intelligence Layer. Jobfynder Core is the System of Record.
  Hermes analyzes data, generates recommendations, extracts structured
  information, and assists workflows. Jobfynder Core validates business
  rules and persists all business data. Hermes never writes business
  records directly.
alternatives_considered: []
consequences:
  positive:
    - AI providers can change without redesigning the platform.
    - Core remains stable even if AI behavior changes.
    - Every AI output is validated before persistence.
    - Hermes can expand into multiple AI agents without changing Core.
    - Business auditing and compliance remain centralized.
  negative: []
affected_components: [hermes, jobfynder-admin/jobFynder-BE-nestJS]
related_adrs: [ADR-0003]
tags: [hermes, architecture, ai-boundary]
confidence: proven
---

# ADR-0006: Hermes is the Intelligence Layer; Jobfynder Core is the System of Record

Migrated from `jobfynder/decision-ledger/decisions/001-hermes-intelligence-layer.md` on 2026-09-07, as part of consolidating decision tracking into one system. Original reasoning preserved below.

## Reasoning

Separating intelligence from business logic provides clear ownership, allows AI models to evolve independently, reduces operational risk, and keeps business operations deterministic and auditable.
