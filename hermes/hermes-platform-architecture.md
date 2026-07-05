# Hermes Platform Architecture

Status: Active
Owner: Jobfynder-Infra
Purpose: Simple architecture map for Hermes

---

## 1. What Hermes Is

Hermes is the intelligence platform behind Jobfynder.

Hermes helps Jobfynder read information, remember context, make decisions, and execute workflows.

Hermes supports Pulse, Recruiter OS, Bench Sales workflows, Job Tracker, Trust, Talent Network, Vendor Network, Messaging, and Automation.

---

## 2. Platform Kernel

The Hermes Platform kernel is the foundation.

| Kernel Part | Purpose |
|---|---|
| API Gateway | Receives requests |
| AI Gateway | Routes AI calls |
| Memory Runtime | Stores and retrieves knowledge |
| Decision Runtime | Makes decisions |
| Action Runtime | Executes actions |
| Event Bus | Moves events |
| Scheduler | Runs planned jobs |
| Plugin Framework | Adds capabilities cleanly |
| Model Router | Chooses the right model |
| Security | Protects access and secrets |
| Observability | Tracks logs, errors, metrics, and alerts |
| Workspace | Stores working context |
| Mission Control | Gives operator visibility |
| Configuration | Manages settings |

---

## 3. Main Architecture

Jobfynder Products -> Hermes API Gateway -> Hermes Platform Kernel -> Understanding, Memory, Intelligence, Automation, Integrations, Multi-Agent Runtime

---

## 4. Hermes Streams

- HERMES-000: Architecture and Governance
- HERMES-100: Core Platform
- HERMES-200: Understanding
- HERMES-300: Memory
- HERMES-400: Intelligence
- HERMES-500: Automation
- HERMES-600: Integrations
- HERMES-700: Multi-Agent

---

## 5. Simple Rule

Every new Hermes feature must clearly belong to one stream.

If it does not fit into a stream, we do not build it yet.

---

## 6. Current Production Baseline

Engineering Memory Module is production baseline complete.

---

## 7. Next Target

Next stream: HERMES-100 Core Platform.

Goal: Review the current Hermes codebase and make sure the core platform is clean, stable, secure, and easy to operate.
