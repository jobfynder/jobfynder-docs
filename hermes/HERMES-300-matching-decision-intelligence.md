# HERMES-300 — Matching & Decision Intelligence

Status: In progress — first local matching endpoint built  
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

## First Endpoint Built

POST /matching/resume-to-job

Code branch:

`feature/hermes-300-matching`

Latest HERMES-300 code commits:

- `2b99ebc` — `feat(hermes-300): add basic resume to job scorer`
- `fe4532d` — `feat(hermes-300): expose resume to job matching endpoint`
- `7022cb6` — `test(hermes-300): add matching endpoint smoke coverage`

Live validation completed:

- Docker rebuild completed
- OpenAPI route verified
- Authenticated live endpoint smoke test passed
- Main Hermes smoke test now validates `/matching/resume-to-job`
- Current matcher version: `basic_local_matcher_v1`

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
