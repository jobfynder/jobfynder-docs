# HERMES-300 — Matching & Decision Intelligence

Status: Started  
Base checkpoint: hermes-200-foundation-v1  
Official docs repo: jobfynder/jobfynder-docs

---

## Goal

HERMES-300 uses HERMES-200 parsed output to decide whether a resume matches a job.

It should answer:

- Does this resume match this job?
- Why does it match?
- What is missing?
- Should we submit, reject, or manually review?

---

## Simple Rule

Build a reliable local scoring engine first.

Do not start with a complex AI engine.

LLM can be added later only to improve explanations, not to replace deterministic matching.

---

## First Build Scope

HERMES-300 foundation will include:

- Skill match scoring
- Required skill coverage
- Preferred skill bonus
- Years experience comparison
- Work authorization comparison
- Location comparison
- Final decision:
  - submit
  - review
  - reject

---

## Input From HERMES-200

Resume fields:

- skills
- years_experience
- work_authorization
- location

Job description fields:

- required_skills
- preferred_skills
- years_experience
- work_authorization
- location

---

## Output

HERMES-300 should return:

- match_score
- decision
- matched_skills
- missing_required_skills
- matched_preferred_skills
- reasons
- risks
- recommendation

---

## First Endpoint Planned

POST /matching/resume-to-job

---

## Safety Rules

Initial version must be:

- local-first
- deterministic
- explainable
- testable
- no LLM required
- no cloud dependency

---

## Documentation Rule

This is the official HERMES-300 documentation file.

Final readable Hermes documentation must be stored in:

/opt/jobfynder-docs/hermes

Not in:

/opt/hermes/docs
