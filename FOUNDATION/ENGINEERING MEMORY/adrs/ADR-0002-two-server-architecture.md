---
id: ADR-0002
title: Two-Server Architecture
status: accepted
date: 2026-07-02
repository: jobfynder-infra
authors: [Pavan]
context: >
  Hermes (the intelligence/reasoning layer) and the platform's
  communication functions have different security and exposure
  requirements. Public-facing channels (Telegram, WhatsApp, email,
  Slack, Teams) must be reachable from the internet; the reasoning
  layer that acts on business data should not be.
decision: >
  Split the platform across two servers. INTEL-1 runs Hermes Core —
  understanding, matching, taxonomy, and workflow intelligence — and is
  not directly exposed to the internet. COMM-1 (152.42.219.165) runs the
  jobfynder-comm-gateway container and owns provider-facing ingress,
  transport authentication (HMAC-signed calls into Hermes), retries,
  attachments, and outbound communication. Hermes Edge — the component
  that actually touches public channels — lives at this boundary and
  must never call Core synchronously.
alternatives_considered:
  - name: Single combined server
    reason: Rejected — would expose the reasoning layer directly to public-facing traffic and public-channel outages/incidents.
consequences:
  positive:
    - Core's reasoning logic never has to defend directly against internet-facing traffic.
    - A compromise or outage on the communication side does not directly expose Core.
    - Each server scales independently based on its own load pattern.
  negative:
    - Cross-server calls require a signed contract (HMAC) instead of a simple in-process call, adding latency and a failure mode to handle.
    - Two servers to patch, monitor, and back up instead of one.
affected_components: [hermes, jobfynder-infra, centrifugo]
related_adrs: [ADR-0003]
tags: [architecture, infrastructure, security]
confidence: proven
---

# ADR-0002: Two-Server Architecture

Referenced by `Architecture/01-platform-architecture.md` §2.8. See `JOBFYNDER-HERMES-COMM-CANONICAL.md` §2.1 for the COMM-1 identity and role.
