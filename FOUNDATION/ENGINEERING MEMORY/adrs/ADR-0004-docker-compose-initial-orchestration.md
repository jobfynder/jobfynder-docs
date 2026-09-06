---
id: ADR-0004
title: Docker Compose as Initial Orchestration
status: accepted
date: 2026-07-02
repository: jobfynder-infra
authors: [Pavan]
context: >
  Jobfynder needed a deployment approach for its MVP stage matching the
  team's actual size (one non-technical founder, small dev team) without
  taking on infrastructure cost or complexity disproportionate to real
  traffic.
decision: >
  Deployment follows a staged plan. Stage 1 (MVP) uses Docker Compose
  across two DigitalOcean servers with manual deployments. Stage 2
  (Growth) introduces GitHub Actions, a container registry, and
  automated deployments, plus improved monitoring. Stage 3 (Scale)
  introduces multiple communication and intelligence nodes, managed
  databases if required, and high availability. Do not adopt a later
  stage's tooling before traffic or team size actually justifies it.
alternatives_considered:
  - name: Kubernetes from day one
    reason: Rejected — operational overhead disproportionate to MVP-stage traffic and team size; violates the no-infrastructure-without-measurable-value principle in ADR-0001.
consequences:
  positive:
    - Minimal operational overhead at MVP stage.
    - Easy to reason about and debug with a small team.
    - A pre-agreed staged path removes the temptation to over-engineer early.
  negative:
    - Manual deployments are slower and more error-prone than automated ones.
    - No built-in high availability at Stage 1 — a server failure is a real outage until Stage 3.
affected_components: [jobfynder-infra]
related_adrs: [ADR-0001, ADR-0002]
tags: [infrastructure, devops, staged-scaling]
confidence: proven
---

# ADR-0004: Docker Compose as Initial Orchestration

Referenced by `Architecture/01-platform-architecture.md` §2.8 (Scalability Strategy).
