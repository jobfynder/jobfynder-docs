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
