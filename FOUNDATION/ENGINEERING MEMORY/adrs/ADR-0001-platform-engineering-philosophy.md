---
id: ADR-0001
title: Platform Engineering Philosophy
status: accepted
date: 2026-07-02
repository: all
authors: [Pavan]
context: >
  Jobfynder is built by a small, non-technical-founder-led team relying
  heavily on AI coding tools (Claude Code, Cursor, Codex). Without a
  consistent set of engineering defaults, different modules built by
  different people (or different AI sessions) risk diverging in ways
  that are expensive to reconcile later.
decision: >
  Adopt these defaults platform-wide: deterministic business logic over
  AI-owned decisions (AI assists, never autonomously decides, anything
  business-critical); PostgreSQL as the single source of truth (no graph
  database or secondary store until real query volume justifies one);
  backend-authoritative operations (never trust client-supplied business
  logic); one shared access-control code path reused across all modules,
  not per-module branching; open-source and self-hosted tools preferred
  over paid SaaS; no infrastructure added without measurable value.
alternatives_considered: []
consequences:
  positive:
    - Consistent behavior across modules regardless of which developer or AI tool built them.
    - Lower infrastructure cost by defaulting to self-hosted, open-source tools.
    - Reduced risk of AI making unreviewed business-critical decisions.
    - Simpler onboarding for a new developer or AI agent — one set of rules applies everywhere.
  negative:
    - Some engineering convenience is traded for consistency — a trendy managed service needs justification before it's adopted.
    - Requires discipline to enforce, since nothing technical prevents violating it.
affected_components: [all]
related_adrs: []
tags: [engineering-philosophy, governance]
confidence: proven
---

# ADR-0001: Platform Engineering Philosophy

Referenced by `Architecture/01-platform-architecture.md` §2.8 and applied throughout `jobfynder-docs`.
