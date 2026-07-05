# HERMES-000 — Architecture & Governance

Status: Active  
Owner: Jobfynder-Infra  
Scope: Hermes Platform  
Created: 2026-07-05  

---

## 1. Purpose

HERMES-000 defines the architecture and governance layer for Hermes.

Hermes is no longer treated as only an application repository.

Hermes is the intelligence platform behind Jobfynder.

Every future Hermes module must follow this operating model so the platform grows in a stable, consistent, and production-ready way.

---

## 2. Hermes Platform Vision

Hermes exists to make Jobfynder smarter, faster, more reliable, and easier to operate.

Hermes should become the shared intelligence foundation for:

- Jobfynder Pulse
- Recruiter OS
- Bench Sales workflows
- Trust and Verification
- Job Tracker
- Talent Network
- Vendor Network
- Messaging
- Automation
- Multi-agent operations

Every improvement to Hermes should compound across the Jobfynder ecosystem.

---

## 3. Level 0 — Hermes Platform Kernel

The Hermes Platform kernel is the foundation every capability depends on.

It includes:

- API Gateway
- AI Gateway
- Memory Runtime
- Decision Runtime
- Action Runtime
- Event Bus
- Scheduler
- Plugin Framework
- Model Router
- Security
- Observability
- Workspace
- Mission Control
- Configuration

This layer is not a feature. It is the operating foundation.

---

## 4. Hermes Streams

Hermes work is organized into numbered streams.

### HERMES-000 — Architecture & Governance

Architecture, standards, roadmap, policies, decisions, and engineering rules.

### HERMES-100 — Core Platform

API, configuration, Docker, health checks, authentication, logging, deployment, versioning, plugin loading, and database foundation.

### HERMES-200 — Understanding

Parsers and structured knowledge extraction from unstructured data.

Examples:

- Job Parser
- Resume Parser
- Recruiter Parser
- Email Parser
- Telegram Parser
- WhatsApp Parser
- Hotlist Parser
- Company Parser
- PDF Parser
- Web Page Parser

### HERMES-300 — Memory

Everything Hermes remembers.

Memory domains include:

- Engineering Memory
- Product Memory
- Recruiter Memory
- Company Memory
- Consultant Memory
- Employer Memory
- Vendor Memory
- Conversation Memory
- Personal Memory
- System Memory

### HERMES-400 — Intelligence

Reasoning and decision engines.

Examples:

- Matching Engine
- Trust Engine
- Relationship Engine
- Recommendation Engine
- Priority Engine
- Duplicate Engine
- Risk Engine
- Intent Engine
- Quality Engine
- Reasoning Engine

### HERMES-500 — Automation

Event-driven workflows, scheduled jobs, background workers, n8n workflows, and orchestration.

### HERMES-600 — Integrations

External providers and systems.

Examples:

- GitHub
- Portkey
- PostgreSQL
- Typesense
- Crawl4AI
- Unstructured
- Cal.com
- Postmark
- Ably
- OpenRouter
- Telegram
- WhatsApp
- Slack
- Google Workspace

### HERMES-700 — Multi-Agent

Role-specific agents sharing the same memory, tools, intelligence, and action runtime.

Examples:

- Founder Agent
- Engineering Agent
- Recruiter Agent
- Bench Sales Agent
- Product Agent
- Marketing Agent
- Operations Agent
- Support Agent

---

## 5. Capability-Based Development

Hermes progress is measured by capabilities, not random features.

Each capability should move through clear statuses:

- Not Started
- Planned
- In Progress
- Testing
- Production Baseline
- Complete
- Deprecated

The Hermes Capability Matrix is the official scoreboard.

---

## 6. Definition of Done

A Hermes capability is not complete until it satisfies the Definition of Done.

Baseline checklist:

- API implemented
- Schema finalized
- Prompt versioned where applicable
- Unit tests passing
- Integration tests passing where applicable
- Sample fixtures included
- Engineering Memory updated
- Documentation written
- Metrics available where applicable
- Alerting configured where appropriate
- n8n workflow validated where applicable
- Security reviewed
- Performance baseline recorded where applicable

---

## 7. COMM-1 Mission

COMM-1 is the autonomous engineering operator for Jobfynder-Infra.

Its mission is:

Continuously improve Hermes so that every improvement compounds across the Jobfynder ecosystem.

Every automation, parser, workflow, and integration should answer:

Does this make Hermes smarter, faster, more reliable, or easier to operate?

If yes, it belongs in the Hermes roadmap.

---

## 8. Governance Rule

Before building new Hermes capabilities, we must confirm:

1. Which Hermes stream it belongs to.
2. Which capability it improves.
3. What Definition of Done applies.
4. Where documentation will be stored.
5. How Engineering Memory will record the change.

This prevents scattered implementation and keeps Hermes production-ready.

---

## 9. Current Status

Engineering Memory Module is production baseline complete.

Next official stream:

HERMES-000 — Architecture & Governance

Initial deliverables:

- Hermes Platform Architecture
- Hermes Capability Matrix
- Hermes Engineering Playbook

---

## 10. Implementation Backlog

- [ ] Create Hermes Platform Architecture document
- [ ] Create Hermes Capability Matrix document
- [ ] Create Hermes Engineering Playbook document
- [ ] Commit HERMES-000 baseline documents
- [ ] Update Engineering Memory after commit
- [ ] Begin HERMES-100 Core Platform review
