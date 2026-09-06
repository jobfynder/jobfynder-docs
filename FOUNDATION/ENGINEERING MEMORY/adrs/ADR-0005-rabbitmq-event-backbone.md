---
id: ADR-0005
title: RabbitMQ as Event Backbone
status: accepted
date: 2026-08-21
repository: jobfynder-infra
authors: [Pavan]
context: >
  The COMM intake pipeline and other durable background work across the
  platform (notification dispatch, submission events, message intake)
  needed reliable delivery that survives a downstream consumer being
  temporarily unavailable — events must not simply be dropped.
decision: >
  RabbitMQ is the platform's durable, asynchronous event backbone,
  handling background tasks and intake queueing with exponential-backoff
  retry, dead-letter handling, and idempotency. Redis handles presence
  and short-lived state alongside it — not durable events. RabbitMQ
  credentials must never use defaults and must be externalized, never
  embedded in configuration committed to a repository.
alternatives_considered:
  - name: Redis as the durable queue
    reason: Rejected — Redis is well-suited to fast, short-lived state (presence, ephemeral data) but is not built for durable, retryable event delivery.
consequences:
  positive:
    - Events survive a downstream outage instead of being silently dropped.
    - Retry and dead-letter handling are consistent platform-wide instead of reimplemented per module.
    - Redis is freed to do what it's actually good at instead of being misused as a durable queue.
  negative:
    - Adds an operational component (RabbitMQ) that must be monitored, backed up, and patched.
    - Requires real credential discipline — a default RabbitMQ credential was found live in production and had to be fixed (see JOBFYNDER-HERMES-COMM-CANONICAL.md v1.5).
affected_components: [jobfynder-infra, comm]
related_adrs: [ADR-0007]
tags: [infrastructure, messaging, reliability]
confidence: proven
---

# ADR-0005: RabbitMQ as Event Backbone

Referenced by `Architecture/01-platform-architecture.md` §2.8.
