---
id: ADR-0002
title: Use Centrifugo as the Realtime Layer
status: accepted
date: 2026-07-19
repository: centrifugo
authors: [Pavan]
context: >
  Jobfynder needs realtime communication across Messenger, Pulse feeds,
  submission updates, introductions, notifications, presence, typing
  indicators, read receipts, and tracker status changes. Managed realtime
  platforms such as Ably can simplify development, but usage-based pricing
  could become expensive and unpredictable as Jobfynder grows.
decision: >
  Jobfynder uses Centrifugo as the shared realtime event delivery layer,
  initially hosted as a managed service through Elestio. Jobfynder Core
  and the Messenger backend continue to own permissions, business rules,
  message persistence, and event authorization. Centrifugo only
  distributes realtime events to connected users and applications — it
  never becomes the system of record.
alternatives_considered:
  - name: Ably
    reason: Usage-based pricing could become expensive and unpredictable as Jobfynder grows.
consequences:
  positive:
    - Centrifugo becomes the common realtime layer across Jobfynder, avoiding usage-based pricing risk from managed alternatives like Ably.
    - Existing architecture stays intact — Postgres remains the source of truth, Redis handles presence and short-lived state, RabbitMQ handles durable background tasks; Centrifugo only adds fan-out, not a redesign.
    - Socket.IO may remain in the Messenger backend where useful, alongside Centrifugo as the shared platform-wide event layer.
  negative:
    - Realtime channels must implement secure, context-based authorization.
    - Business data must be persisted before or alongside realtime delivery — Centrifugo must never become the system of record.
    - The platform must handle reconnection, missed events, and event replay safely.
affected_components: [centrifugo, jobfynder-admin/jobFynder-BE-nestJS, messenger]
related_adrs: []
tags: [realtime, infrastructure, messenger]
confidence: proven
---

# ADR-0002: Use Centrifugo as the Realtime Layer

Migrated from `jobfynder/decision-ledger/decisions/002-centrifugo-realtime-layer.md` on 2026-09-07, as part of consolidating decision tracking into one system. Original reasoning preserved below.

## Reasoning

Centrifugo provides the realtime capabilities Jobfynder needs while keeping costs predictable and avoiding dependence on expensive usage-based messaging services. It works with the existing architecture rather than replacing it: Postgres stays the source of truth, Redis supports presence, RabbitMQ handles durable background tasks, the Messenger backend manages conversations, and Centrifugo handles realtime fan-out. This avoids building realtime infrastructure from scratch while preserving control over data and business logic.
