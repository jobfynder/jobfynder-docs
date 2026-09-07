---
id: ADR-0003
title: Communication / Intelligence Separation
status: accepted
date: 2026-07-02
repository: all
authors: [Pavan]
context: >
  As Hermes and the communication layer both grew, the platform needed
  a permanent, non-overlapping way to assign architectural responsibility
  so that module numbers and ownership don't collide or get reused for
  unrelated things later.
decision: >
  The platform is organized into two first-class planes: HERMES/INTEL-1
  (Intelligence Plane — understanding, matching, taxonomy, workflow
  intelligence, AI runtime) and COMM/COMM-1 (Communication Plane —
  ingress, channel adapters, messaging transport, external communication
  integrations). Neither plane is secondary to the other. Their
  interaction happens through one documented contract
  (`POST /internal/comm/intake`, HMAC-signed) under a shared PLATFORM
  namespace. Module numbers are permanent architectural identifiers and
  are never reused for something unrelated, even if the original scope
  changes.
alternatives_considered: []
consequences:
  positive:
    - Clear ownership boundary prevents intelligence logic and communication/transport logic from becoming entangled.
    - Either plane can be rebuilt or replaced independently as long as the intake contract is honored.
    - Numbering discipline means historical identifiers are never lost or silently reassigned.
  negative:
    - Requires maintaining a stable cross-plane contract even as each plane evolves internally.
    - A change that seems to belong equally to both planes still requires deciding which one owns it.
affected_components: [hermes, comm, jobfynder-infra]
related_adrs: [ADR-0002, ADR-0006]
tags: [architecture, hermes, comm]
confidence: proven
---

# ADR-0003: Communication / Intelligence Separation

Referenced by `Architecture/01-platform-architecture.md` §2.8. This is the plane-level version of the same boundary ADR-0006 describes at the Core/AI level — read both together.
