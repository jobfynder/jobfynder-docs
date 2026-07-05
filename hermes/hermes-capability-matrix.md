# Hermes Capability Matrix

Status: Active  
Owner: Jobfynder-Infra  
Purpose: Simple progress scoreboard for Hermes capabilities

---

## 1. Status Legend

| Status | Meaning |
|---|---|
| ✅ Production Baseline | Working and usable in production baseline |
| 🚧 In Progress | Started, but not complete |
| ⏳ Planned | Approved, not started |
| 🧪 Testing | Built, under validation |
| ❌ Blocked | Waiting on decision, access, or dependency |
| 🗑️ Deprecated | No longer used |

---

## 2. Current Capability Scoreboard

| Stream | Capability | Status | Notes |
|---|---|---|---|
| HERMES-000 | Architecture & Governance | ✅ | Production baseline docs created and pushed |
| HERMES-100 | Core Platform Review | 🚧 | Started with config, health, and RBAC baseline |
| HERMES-100 | Access Control & RBAC | ✅ | Token-based RBAC enabled and validated |
| HERMES-100 | API Version Consistency | ✅ | Central Hermes version used in health and parser responses |
| HERMES-100 | Docker Build Hygiene | ✅ | .dockerignore added and validated |
| HERMES-100 | RBAC User Management | ✅ | Server-side user add/list/disable script added |
| HERMES-200 | Parse Jobs | ⏳ | To be reviewed |
| HERMES-200 | Parse Resumes | ⏳ | To be built later |
| HERMES-200 | Parse Recruiter Emails | ⏳ | Future priority |
| HERMES-200 | Parse Telegram Messages | ⏳ | Future priority |
| HERMES-200 | Parse WhatsApp Messages | ⏳ | Future priority |
| HERMES-300 | Engineering Memory | ✅ | Production baseline complete |
| HERMES-300 | Product Memory | ⏳ | Planned |
| HERMES-300 | Recruiter Memory | ⏳ | Planned |
| HERMES-300 | Company Memory | ⏳ | Planned |
| HERMES-300 | Consultant Memory | ⏳ | Planned |
| HERMES-300 | Conversation Memory | ⏳ | Planned |
| HERMES-400 | Intent Understanding | ⏳ | To be reviewed |
| HERMES-400 | Duplicate Detection | ⏳ | Planned |
| HERMES-400 | Matching Engine | ⏳ | Planned |
| HERMES-400 | Trust Scoring | ⏳ | Planned |
| HERMES-400 | Relationship Intelligence | ⏳ | Planned |
| HERMES-500 | GitHub Webhook Automation | ✅ | Used by Engineering Memory |
| HERMES-500 | Failure Alerts | ✅ | Telegram and email alerts complete |
| HERMES-500 | Scheduled Jobs | ⏳ | Planned |
| HERMES-600 | GitHub Integration | ✅ | Production baseline for Engineering Memory |
| HERMES-600 | n8n Integration | ✅ | Production baseline for Engineering Memory |
| HERMES-600 | Portkey Integration | 🚧 | Already used, needs formal documentation |
| HERMES-700 | Multi-Agent Runtime | ⏳ | Future layer |

---

## 3. Rule

Every Hermes improvement should update this matrix.

If a capability changes status, update this file and commit it.

---

## 4. Next Target

Current focus:

HERMES-000 — Architecture & Governance

Next item:

Create Hermes Engineering Playbook.
