# HERMES-700 — Multi-Agent Foundation

Status: Active  
Started From: HERMES-600 closed baseline  
Code Baseline: `/opt/hermes` tag `hermes-600-foundation-v1` at `7c23d1f`  
Docs Baseline: `/opt/jobfynder-docs` main at `27764d1`  

---

## 1. Purpose

HERMES-700 creates the first production-safe Multi-Agent Foundation for Hermes.

This module is the agent layer above the already closed Hermes foundations:

- HERMES-100 — Core Platform
- HERMES-200 — Understanding
- HERMES-300 — Matching & Decision Intelligence
- HERMES-400 — Taxonomy & Signal Intelligence
- HERMES-500 — Submission Intelligence & Workflow Foundation
- HERMES-600 — Integrations Foundation

HERMES-700 should allow Hermes to coordinate role-aware agents for Jobfynder without creating uncontrolled autonomous behavior.

---

## 2. Plain-English Definition

HERMES-700 is where Hermes starts acting like a controlled team of assistants.

Each agent should have a clear role, clear permissions, clear memory boundaries, and clear output rules.

Examples:

- Founder Agent
- Recruiter Agent
- Bench Sales Agent
- Consultant Agent
- Product Agent
- Engineering Agent
- Marketing Agent
- Operations Agent
- Support Agent

The goal is not to create random AI chatbots.

The goal is to create controlled, auditable, role-specific workers that can help Jobfynder users and internal systems make better decisions.

---

## 3. Core Principles

HERMES-700 must follow these rules:

1. Agents must be role-based.
2. Agents must be permission-aware.
3. Agents must use existing Hermes modules instead of duplicating logic.
4. Agents must produce structured, auditable outputs.
5. Agents must not silently take high-risk actions.
6. Agents must support human review where required.
7. Agents must work with n8n and future workflow orchestration.
8. Agents must remain simple enough for the Jobfynder team to understand and operate.

---

## 4. Safety Boundary

HERMES-700 must not allow uncontrolled autonomous actions.

Agents may:

- analyze
- summarize
- recommend
- prepare drafts
- prepare structured actions
- produce next-step suggestions
- call approved internal tools through controlled interfaces

Agents must not automatically:

- submit consultants to jobs
- message recruiters
- email external users
- change production data
- deploy code
- approve vendors
- verify users
- alter trust scores
- make billing decisions

unless a later approved workflow explicitly allows it with proper policy, logging, and human approval.

---

## 5. Initial Agent Scope

The initial HERMES-700 foundation should focus on agent definitions and routing, not complex autonomy.

Planned foundation pieces:

- Agent role registry
- Agent capability registry
- Agent policy and permission model
- Agent input/output schemas
- Agent router
- Agent execution envelope
- Agent audit log format
- Agent dry-run mode
- Agent handoff model
- Agent fixtures and tests
- Minimal API routes for agent execution

---

## 6. Suggested Initial Agents

### 6.1 Founder Agent

Purpose:

- summarize platform state
- explain risks
- prepare strategic decisions
- read system signals
- create executive summaries

### 6.2 Recruiter Agent

Purpose:

- review job requirements
- explain candidate fit
- prepare recruiter follow-ups
- summarize submissions
- suggest next actions

### 6.3 Bench Sales Agent

Purpose:

- match consultants to jobs
- prepare submission packets
- track recruiter follow-ups
- detect duplicate or risky submissions
- suggest best recruiter targets

### 6.4 Consultant Agent

Purpose:

- explain job fit
- suggest profile improvements
- summarize application status
- prepare consultant-facing updates

### 6.5 Engineering Agent

Purpose:

- summarize technical state
- prepare implementation steps
- explain module status
- read Engineering Memory
- support safe operational workflows

### 6.6 Support Agent

Purpose:

- explain user issues
- prepare support replies
- summarize account context
- route unresolved issues

---

## 7. Non-Goals

HERMES-700 should not build:

- a full chatbot product
- a public assistant UI
- uncontrolled autonomous agents
- browser automation
- direct LinkedIn automation
- direct WhatsApp automation
- production self-healing infrastructure
- billing automation
- trust-score auto-mutation
- replacement logic for HERMES-200 to HERMES-600

---

## 8. Expected Closure Criteria

HERMES-700 can close only when:

- Agent registry exists.
- Agent schemas exist.
- Agent router exists.
- At least 3 role agents are defined.
- Agents can run in dry-run mode.
- Agent actions are logged.
- Agent permissions are enforced.
- API routes are tested.
- Fixtures exist.
- Docker verification passes.
- Live health verification passes.
- Official docs are updated.
- Final branch is pushed.
- Final foundation tag is created and pushed.

---

## 9. Step Log

### Step 001 — Baseline Verification

Passed.

Confirmed HERMES-600 closed baseline:

- Code repo: `/opt/hermes`
- Branch: `feature/hermes-600-integrations`
- Commit: `7c23d1f`
- Tag: `hermes-600-foundation-v1`
- Docs repo: `/opt/jobfynder-docs`
- Docs branch: `main`
- Docs commit: `27764d1`

### Step 002 — Module Opening

Status: In progress.

Actions:

- Create code branch `feature/hermes-700-multi-agent`
- Create official HERMES-700 documentation
- Update Hermes documentation map

### Step 006 — Agent Registry and Dry-Run Router

Status: Passed.

Code commit:

- `/opt/hermes` branch `feature/hermes-700-multi-agent`
- Commit: `37ce96a`
- Message: `feat(hermes-700): add agent registry and dry-run router`

Implemented:

- `app/agents/__init__.py`
- `app/agents/models.py`
- `app/agents/service.py`
- `app/routers/agents.py`
- `scripts/hermes-700-agent-registry-check.py`
- Router wiring in `app/main.py`

Agents added:

- Founder Agent
- Recruiter Agent
- Bench Sales Agent
- Consultant Agent
- Engineering Agent
- Support Agent

Safety behavior:

- Dry-run first
- Human review required
- Execute mode blocked
- High-risk actions such as submit, send, email, approve, verify, deploy, delete, billing, WhatsApp, and LinkedIn are blocked into review-required prepared actions

Verification:

- Docker build passed
- Compile check passed
- Agent registry check passed

---

### Step 007 — Live RBAC-Protected Agents API Verification

Status: Passed.

Verified live routes:

- `GET /agents/health`
- `GET /agents/registry`
- `GET /agents/{agent_id}`
- `POST /agents/dry-run`

RBAC behavior:

- Protected routes correctly returned `Missing access token` without bearer token
- Live API passed with existing `pavan-admin` wildcard token
- RBAC remained enabled

Verified outcomes:

- Safe recruiter dry run returned `accepted`
- Bench Sales execute/send/submit request returned `needs_review`
- Blocked execute result returned `executed=false`
- Unknown agent returned `rejected`

---

### Step 008 — Repeatable Agents API Check and Fixtures

Status: Passed.

Code commit:

- Commit: `42eccb9`
- Message: `test(hermes-700): add agents API check and fixtures`

Implemented:

- `scripts/hermes-700-agent-api-check.py`

Fixtures added:

- `docs/hermes-700/api-fixtures/agents-health-response.json`
- `docs/hermes-700/api-fixtures/agents-registry-response.json`
- `docs/hermes-700/api-fixtures/bench-sales-agent-response.json`
- `docs/hermes-700/api-fixtures/blocked-execute-response.json`
- `docs/hermes-700/api-fixtures/safe-dry-run-response.json`
- `docs/hermes-700/api-fixtures/unknown-agent-response.json`

Verification:

- Live Agents API check passed
- Fixture validation passed
- Fixtures committed and pushed

---

### Step 009 — Agent Policy Enforcement Foundation

Status: Passed.

Code commits:

- `1ddf34c` — `feat(hermes-700): enforce agent policy decisions`
- `b62612f` — `test(hermes-700): refresh policy audit API fixtures`

Implemented:

- `capability_id` on `AgentRunRequest`
- `AgentPolicyDecision`
- `evaluate_agent_policy`
- Agent capability validation
- Actor permission validation
- Policy snapshot in response audit
- Router-level propagation of authenticated actor id, role, and permissions into agent context

Verified policy behavior:

- Valid recruiter `job_review` dry run is allowed
- Invalid capability is rejected
- Missing actor permissions return `needs_review`
- Execute mode for capability remains blocked
- Policy information appears in `audit.policy`

Verification:

- Compile passed
- Local registry check passed
- Docker rebuild passed
- Live API check passed after force-recreate
- Policy fixtures refreshed and validated

---

### Step 010 — Agent Handoff Envelope Foundation

Status: Passed.

Code commit:

- `2186580`
- Message: `feat(hermes-700): add agent handoff envelope`

Implemented:

- `AgentHandoffEnvelope`
- `AgentHandoffTarget`
- `AgentHandoffStatus`
- `build_agent_handoff`
- `handoff` field on `AgentRunResult`

Handoff targets:

- `human_review`
- `n8n`
- `jobfynder_api`
- `engineering_memory`
- `none`

Handoff statuses:

- `prepared`
- `blocked`
- `not_required`

Verified handoff behavior:

- Safe dry-run result creates `prepared` handoff
- Blocked execute result creates `blocked` handoff
- Handoff target is `human_review`
- Human approval remains required

Verification:

- Compile passed
- Local registry check passed
- Docker rebuild and force-recreate passed
- Live API check passed
- Handoff fixture validation passed

---

### Step 011 — Agent Execution Audit Event Foundation

Status: Passed.

Code commits:

- `6f90507` — `feat(hermes-700): add agent audit event`
- `301680a` — `test(hermes-700): fix agent audit registry assertions`

Implemented:

- `AgentAuditEvent`
- `audit_event` field on `AgentRunResult`
- `AGENT_AUDIT_VERSION`
- deterministic audit event id generation
- `build_agent_audit_event`

Audit event version:

- `hermes_agent_audit_event_v1`

Audit event behavior:

- Event type: `agent_run_completed`
- Includes agent id
- Includes role
- Includes capability id
- Includes requested and effective action mode
- Includes decision
- Includes `executed=false`
- Includes human review requirement
- Includes policy version
- Includes handoff version
- Includes actor context when available
- Includes risk and prepared-action counts

Verification:

- Compile passed
- Docker rebuild passed
- Registry check inside rebuilt container passed
- Live Agents API check passed
- Audit fixtures validated
- Registry-check assertion mistake was corrected in `301680a`

---

## Current HERMES-700 Code State

Latest code commit:

- `/opt/hermes`
- Branch: `feature/hermes-700-multi-agent`
- Commit: `301680a`
- Message: `test(hermes-700): fix agent audit registry assertions`

Current implemented foundation:

- Agent registry
- Role-aware agent definitions
- Capability registry
- Dry-run execution
- RBAC-protected API routes
- Agent policy decisions
- Controlled prepared actions
- Handoff envelope
- Audit event
- Repeatable local and live API verification scripts
- API fixtures


---

### Step 014 — Agents Snapshot Endpoint

Status: Passed.

Code commit:

- `c2fc718`
- Message: `feat(hermes-700): add agents snapshot endpoint`

Implemented:

- `AgentSnapshotResponse`
- `get_agent_snapshot()`
- `GET /agents/snapshot`
- Snapshot assertions in `scripts/hermes-700-agent-registry-check.py`
- Snapshot live API assertions in `scripts/hermes-700-agent-api-check.py`
- Snapshot fixture: `docs/hermes-700/api-fixtures/agents-snapshot-response.json`

Snapshot response includes:

- `snapshot_version`
- `status`
- `agent_version`
- `policy_version`
- `handoff_version`
- `audit_version`
- `agent_count`
- `supported_agents`
- `supported_action_modes`
- `safety_mode`
- `execution_mode`
- `api_routes`
- `closure_readiness`

Closure readiness flags:

- `agent_registry`
- `role_agents_defined`
- `dry_run_supported`
- `execute_blocked_by_policy`
- `policy_decisions`
- `handoff_envelope`
- `audit_event`
- `rbac_routes`
- `api_fixtures`

Verification:

- Compile passed
- Docker build passed
- Registry check inside Docker passed
- Live Agents API check passed
- Snapshot fixture validation passed

Updated current code state:

- `/opt/hermes`
- Branch: `feature/hermes-700-multi-agent`
- Commit: `c2fc718`
- Message: `feat(hermes-700): add agents snapshot endpoint`


---

### Step 016 — Full Current-State Verification

Status: Passed.

Code repository state:

- Repository: `/opt/hermes`
- Branch: `feature/hermes-700-multi-agent`
- Commit: `c2fc718`
- Origin branch: matched
- Working tree: clean

Code verification:

- Docker build passed
- `python -m compileall app scripts` passed inside Docker
- `scripts/hermes-700-agent-registry-check.py` passed inside Docker
- Live `scripts/hermes-700-agent-api-check.py` passed
- Direct `GET /agents/snapshot` returned healthy status
- Snapshot fixture exists at `docs/hermes-700/api-fixtures/agents-snapshot-response.json`

OpenAPI verification:

- `GET /agents/health` present
- `GET /agents/registry` present
- `GET /agents/snapshot` present
- `GET /agents/{agent_id}` present
- `POST /agents/dry-run` present

Snapshot closure readiness:

- `agent_registry`: true
- `role_agents_defined`: true
- `dry_run_supported`: true
- `execute_blocked_by_policy`: true
- `policy_decisions`: true
- `handoff_envelope`: true
- `audit_event`: true
- `rbac_routes`: true
- `api_fixtures`: true

Documentation repository state:

- Repository: `/opt/jobfynder-docs`
- Branch: `main`
- Commit: `f04525e`
- Origin branch: matched
- Working tree: clean
- Documentation map shows HERMES-700 as the active Hermes module


---

## Final Closure — HERMES-700 Multi-Agent Foundation

Status: Closed.

Closure date:

- 2026-07-07

Final code repository state:

- Repository: `/opt/hermes`
- Branch: `feature/hermes-700-multi-agent`
- Final commit: `c2fc718`
- Final tag: `hermes-700-foundation-v1`
- Tag target: `c2fc7188eed15208bb97103414006f4f9e086238`
- Origin branch: matched
- Working tree: clean

Final verification:

- Docker build passed
- `python -m compileall app scripts` passed inside Docker
- `scripts/hermes-700-agent-registry-check.py` passed inside Docker
- Live `scripts/hermes-700-agent-api-check.py` passed
- OpenAPI route verification passed
- `GET /agents/snapshot` returned healthy status
- All snapshot closure readiness flags were true

Final implemented foundation:

- Agent registry
- Role-aware agents
- Capability registry
- Dry-run execution
- RBAC-protected agent routes
- Agent policy decisions
- Controlled prepared actions
- Agent handoff envelope
- Agent audit event
- Agents snapshot endpoint
- API fixtures
- Repeatable local and live verification scripts

Final API routes:

- `GET /agents/health`
- `GET /agents/registry`
- `GET /agents/snapshot`
- `GET /agents/{agent_id}`
- `POST /agents/dry-run`

Final closure decision:

HERMES-700 is closed as the Multi-Agent Foundation v1 baseline.

Future Hermes multi-agent work must start from:

- Code tag: `hermes-700-foundation-v1`
- Code commit: `c2fc718`
- Official docs commit containing closure: pending this documentation commit

