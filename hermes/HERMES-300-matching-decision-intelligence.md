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

Checkpoint tags:

- `hermes-300-matching-policy-v1`
- `hermes-300-policy-guardrail-v1`
- `hermes-300-active-policy-endpoint-v1`

Latest HERMES-300 code commits:

- `2b99ebc` — `feat(hermes-300): add basic resume to job scorer`
- `fe4532d` — `feat(hermes-300): expose resume to job matching endpoint`
- `7022cb6` — `test(hermes-300): add matching endpoint smoke coverage`
- `c318567` — `test(hermes-300): add matching decision scenario coverage`
- `7d3c399` — `feat(hermes-300): add understanding to matching adapter`
- `ad685d6` — `test(hermes-300): add understanding adapter scenario coverage`
- `7a44cfc` — `feat(hermes-300): add matching endpoint for understanding output`
- `4032baf` — `test(hermes-300): add understanding output endpoint smoke coverage`
- `10da47f` — `fix(hermes-300): improve matching explanation formatting`
- `54da152` — `refactor(hermes-300): extract matching scoring policy`
- `2ed2fbc` — `test(hermes-300): add matching policy validation guardrail`
- `bde627d` — `feat(hermes-300): expose active matching policy endpoint`
- `2c5968f` — `feat(hermes-300): include policy snapshot in match results`

Live validation completed:

- Docker rebuild completed
- OpenAPI route verified
- Authenticated live endpoint smoke test passed
- Main Hermes smoke test now validates `/matching/resume-to-job`
- Deterministic decision scenarios now validate `submit`, `review`, and `reject` outcomes
- HERMES-200 structured output can now be adapted into HERMES-300 match requests
- Dedicated adapter scenario validates HERMES-200-style structured data into HERMES-300 scoring
- Live `/matching/resume-to-job/from-understanding` endpoint validates HERMES-200 parsed output directly
- Main Hermes smoke test now covers both matching endpoints
- Live matcher explanation formatting now uses readable comma spacing
- Matching scoring weights, thresholds, and matcher version are now centralized in `app/matching/policy.py`
- Safe checkpoint tag created and pushed: `hermes-300-matching-policy-v1`
- Main smoke test now validates HERMES-300 scoring policy weights and thresholds
- Safe guardrail checkpoint tag created and pushed: `hermes-300-policy-guardrail-v1`
- Protected `/matching/policy` endpoint exposes the active matcher version, weights, and thresholds
- Match results now include `policy_snapshot` showing the exact matcher version, weights, and thresholds used to produce the score
- Safe active policy endpoint checkpoint tag created and pushed: `hermes-300-active-policy-endpoint-v1`
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
