# HERMES-800 — Resume Builder Intelligence Foundation

Status: Open  
Server: INTEL-1 / jobfynder-intel-01  
Code Repository: /opt/hermes  
Code Branch: feature/hermes-800-resume-builder-intelligence  
Base Commit: 1869e82  
Documentation Repository: /opt/jobfynder-docs  
Documentation Branch: main  

## Goal

Build the Hermes backend intelligence foundation for the existing Jobfynder Resume Builder frontend.

HERMES-800 will build on:

- HERMES-200 — Understanding Foundation
- HERMES-400 — Taxonomy and Signal Intelligence
- HERMES-750 — Portkey Prompt Runtime Foundation
- Existing Jobfynder Resume Builder frontend

## Safety Rules

- Do not fabricate resume content
- Do not invent employers, dates, projects, skills, metrics, education, certifications, or responsibilities
- Human review is required before resume content is accepted or published
- Dry-run behavior remains the default
- Paid and external AI calls remain disabled by default
- Portkey live execution must not be activated during the foundation phase
- Every generated suggestion must preserve source traceability
- Missing information must be reported instead of inferred as fact

## Foundation Scope

HERMES-800 will establish:

- Resume Builder backend API contracts
- Structured resume document models
- Resume section analysis
- Summary improvement suggestions
- Experience bullet rewrite suggestions
- Skills normalization through Hermes taxonomy
- Resume completeness and quality checks
- Job-targeted tailoring contracts
- No-fabrication validation
- Human-review workflow metadata
- Dry-run-first prompt execution integration
- API fixtures and validation scripts
- Documentation and closure evidence

## Initial Non-Goals

The foundation will not:

- Automatically publish resume changes
- Replace the existing Resume Builder frontend
- Enable paid LLM calls
- Enable Portkey live calls
- Generate unsupported experience or achievements
- Store final user-approved resumes without an explicit downstream integration
- Introduce autonomous resume modification

## Initial Delivery Order

1. Existing contract and code inventory
2. Resume Builder domain models
3. Safety and provenance models
4. Analysis service contracts
5. Prompt runtime adapters
6. Resume intelligence APIs
7. Dry-run fixtures
8. Validation scripts
9. Documentation and closure checks

## Current State

The module has been formally opened.

No HERMES-800 implementation files have been created yet.

External AI execution remains disabled.
