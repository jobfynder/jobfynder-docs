# HERMES-400 — Taxonomy & Signal Intelligence Foundation

Status: Active  
Module Type: Foundation Module  
Started From: HERMES-300 closed baseline  
Code Baseline Tag: hermes-300-foundation-v1  
Code Baseline Commit: 2c5968f  
Docs Baseline Commit: f93c62d  

---

## 1. Purpose

HERMES-400 builds the Taxonomy & Signal Intelligence foundation for Jobfynder Hermes.

HERMES-300 created the matching foundation.

HERMES-400 makes matching smarter by giving Hermes a clean, versioned, self-improving understanding of:

- skills
- skill aliases
- job titles
- title aliases
- domains
- seniority levels
- employment signals
- recruiter signals
- resume signals
- job description signals
- submission outcome signals

Simple meaning:

Hermes should understand what recruitment terms mean, normalize them safely, and improve the matching system without creating confusion or unsafe automatic changes.

---

## 2. Why This Module Comes After HERMES-300

HERMES-300 can compare jobs and candidates.

But matching quality depends on whether Hermes understands that different words may mean the same or related things.

Examples:

- JavaScript, JS, ECMAScript
- React, React.js, ReactJS
- AWS, Amazon Web Services
- SRE, Site Reliability Engineer
- QA, Quality Analyst, Test Engineer
- US IT Recruiter, Technical Recruiter, Staffing Recruiter
- Bench Sales Recruiter, BDM, Marketing Recruiter

Without HERMES-400, matching can work but cannot continuously improve in a controlled way.

With HERMES-400, Hermes gets a living intelligence layer.

---

## 3. Primary Goal

Create a safe foundation for a live Jobfynder recruitment taxonomy.

The taxonomy should be:

- versioned
- explainable
- reviewable
- testable
- reusable by matching
- reusable by parsing
- reusable by recruiter workflows
- extensible for future outcome learning

---

## 4. What HERMES-400 Should Build

### 4.1 Canonical Skill Registry

A structured registry of normalized skills.

Example:

- canonical skill: React
- aliases: React.js, ReactJS
- category: Frontend
- type: framework
- related skills: JavaScript, TypeScript, Redux
- confidence: high
- source: seed/manual/observed

---

### 4.2 Skill Alias Registry

A controlled mapping of aliases to canonical skills.

Example:

- JS → JavaScript
- Node → Node.js
- Postgres → PostgreSQL
- K8s → Kubernetes

---

### 4.3 Job Title Normalization

Normalize noisy job titles into safer canonical titles.

Example:

- Sr Java Developer → Senior Java Developer
- React UI Engineer → Frontend React Developer
- US IT Recruiter → Technical Recruiter
- Bench Sales → Bench Sales Recruiter

---

### 4.4 Signal Extraction Layer

Extract useful signals from parsed resumes, job descriptions, and recruiter text.

Signals may include:

- required skills
- preferred skills
- years of experience
- domain
- seniority
- location
- work authorization
- rate
- availability
- client type
- recruiter intent
- submission readiness

---

### 4.5 Taxonomy Suggestion Queue

Hermes should not automatically accept every new skill or alias.

Unknown or uncertain terms should go into a reviewable queue.

Example:

- new observed term: GenAI Engineer
- suggested canonical title: AI Engineer
- confidence: medium
- action: review required

---

### 4.6 Versioned Taxonomy Snapshots

Every taxonomy change should be traceable.

Hermes should know:

- what changed
- when it changed
- why it changed
- which source created the suggestion
- whether it was manually approved or system seeded

---

### 4.7 Matching Integration Readiness

HERMES-400 should prepare normalized taxonomy output for HERMES-300 matching.

Matching should be able to use:

- canonical skills
- aliases
- related skills
- skill weights
- title normalization
- seniority hints
- domain hints

---

## 5. What HERMES-400 Should Not Build Yet

HERMES-400 should not become too large.

Do not build these yet:

- full outcome learning engine
- production admin UI
- marketplace intelligence
- messenger backend
- large-scale graph database
- automatic self-changing matching policy
- automatic recruiter trust score
- automatic skill approval without guardrails

Those belong to later modules.

---

## 6. Suggested Module Boundary

HERMES-400 should focus on the foundation only:

1. taxonomy schemas
2. seed taxonomy files
3. alias normalization service
4. title normalization service
5. signal extraction service
6. suggestion queue model
7. version snapshot model
8. tests and guardrails
9. lightweight API endpoints
10. documentation and handoff

---

## 7. Expected Code Areas

Expected Hermes code areas may include:

- app/schemas
- app/services
- app/api
- app/data
- app/tests
- docs or implementation notes inside code repo if needed

Official readable documentation must remain in:

- /opt/jobfynder-docs/hermes

---

## 8. Proposed HERMES-400 Milestones

### Milestone 1 — Module Opening

- Create branch
- Create official document
- Update documentation map
- Commit docs
- Push branch/docs baseline

### Milestone 2 — Taxonomy Data Foundation

- Create canonical taxonomy schema
- Create skill seed file
- Create title seed file
- Create alias seed file
- Add validation tests

### Milestone 3 — Normalization Services

- Build skill normalization service
- Build title normalization service
- Build alias resolution
- Add confidence scoring

### Milestone 4 — Signal Extraction

- Extract structured signals from text
- Support resume-like text
- Support job-description-like text
- Support recruiter-message-like text

### Milestone 5 — Suggestion Queue

- Detect unknown skills/titles
- Generate taxonomy suggestions
- Store review status
- Prevent unsafe auto-approval

### Milestone 6 — Versioning

- Create taxonomy snapshot mechanism
- Track taxonomy version
- Add change metadata

### Milestone 7 — Matching Integration

- Make normalized signals usable by HERMES-300 matching
- Add tests to prove matching can consume taxonomy output

### Milestone 8 — Closure

- Run full tests
- Create foundation tag
- Update official docs
- Move HERMES-400 to closed modules
- Confirm no active Hermes module remains open

---

## 9. Initial Acceptance Criteria

HERMES-400 is successful when:

- Hermes can normalize common skills and aliases
- Hermes can normalize common recruiting job titles
- Hermes can extract useful recruitment signals from text
- Unknown terms are routed to a suggestion queue
- Taxonomy changes are versioned
- HERMES-300 matching can consume normalized taxonomy output
- Tests protect against unsafe taxonomy behavior
- Official docs are updated and pushed

---

## 10. Current Status

HERMES-400 is now active.

Opened after HERMES-300 closure from:

- code tag: hermes-300-foundation-v1
- code commit: 2c5968f
- docs commit: f93c62d
