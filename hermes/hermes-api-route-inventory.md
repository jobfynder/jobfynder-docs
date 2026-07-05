# Hermes API Route Inventory

Status: Active
Owner: Jobfynder-Infra
Stream: HERMES-100 Core Platform

---

## Purpose

This document tracks Hermes API routes, access level, and RBAC permission requirements.

---

## Routes

| Route | Method | Access | Permission | Purpose |
|---|---|---|---|---|
| /health | GET | Public | None | Health check |
| /security/rbac/status | GET | Protected | security:read | RBAC status |
| /v1/engineering-memory/generate | POST | Protected | engineering_memory:write | Generate Engineering Memory |
| /v1/messages/understand | POST | Protected | messages:understand | Understand incoming text |
| /v1/jobs/parse | POST | Protected | jobs:parse | Parse job text |
| /v1/consultants/parse | POST | Protected | consultants:parse | Parse consultant/resume text |
| /mission-control | GET | Protected | mission_control:read | Mission board |
| /session-brief | GET | Protected | session_brief:read | Next session brief |
| /workspace | GET | Protected | workspace:read | Hermes workspace |
| /actions | GET | Protected | actions:read | List actions |
| /actions/{action_id} | GET | Protected | actions:read | Get action |
| /actions | POST | Protected | actions:write | Create action |
| /actions/{action_id} | PUT | Protected | actions:write | Update action |
| /actions/{action_id} | DELETE | Protected | actions:write | Delete action |

---

## Rule

Only /health should remain public.

Every other Hermes route should have a clear RBAC permission.

When a new route is added, update this file.
