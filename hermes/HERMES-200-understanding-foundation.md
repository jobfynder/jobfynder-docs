# HERMES-200 Understanding — Consolidated Checkpoint

Status: Working foundation completed  
Branch: feature/hermes-200-understanding  
Server: jobfynder-intel-01

---

## Goal

Hermes Understanding converts resumes, job descriptions, and recruiter messages into structured data.

Rules:

- Parser first
- Local first
- Compress before LLM
- Cloud disabled by default
- LLM disabled by default
- Weak results go to manual review unless enabled later

---

## Completed

Core:

- Parse text endpoint
- Parse file endpoint
- Local extraction pipeline
- Quality scoring
- Document quality thresholds
- Token counting
- Compressed LLM context
- Fallback policy
- Parser validation
- Parser/schema version metadata
- Smoke test script

Extractors:

- Plain text
- MarkItDown
- pdfplumber fallback
- python-docx fallback
- Safe Unstructured.io placeholder

Resume parser:

- Skills
- Years of experience
- Current title (falls back to the most recent parsed experience entry's title when no probable-title match exists — commit `8319c43f`, `jobfynder/hermes`)
- Name — parsed from the resume header line, commit `8319c43f`
- Email
- Phone — US pattern; plus labeled values (`mobile:`/`phone:`/`tel:`/`cell:`/`whatsapp:`) and any number recognized by the `phonenumbers` library, formatted international-style, so non-US numbers (e.g. `+91 89101 45846`) are no longer dropped — commit `8319c43f`
- LinkedIn URL
- Location — parsed from the resume header line, commit `8319c43f`
- Summary — parsed from a "Summary"/"Objective"/"Profile" section, commit `8319c43f`
- Work authorization
- Structured experience (company, title, start/end date, location, description) — parsed from "Experience"/"Work Experience"/"Professional Experience" sections, commit `8319c43f`
- Structured education (institution, degree, field, year) — parsed from an "Education" section, commit `8319c43f`
- Certifications — parsed from "Certifications"/"Achievements" sections, commit `8319c43f`

When the LLM fallback fires, its extracted values now fill only the fields the deterministic parser left empty (`merge_llm_extracted`, `app/understanding/llm_fallback.py`) instead of only being stored in the raw `llm_fallback_extracted` side-channel — commit `8319c43f`.

Job description parser:

- Job title
- Skills
- Required skills
- Preferred skills
- Years of experience
- Location
- Employment type
- Work authorization
- Rate/salary

Taxonomy:

- Editable skills JSON
- Skill aliases
- Taxonomy version
- Taxonomy endpoint
- Short alias false-positive protection

---

## Current Endpoints

- GET /health
- POST /understanding/parse-text
- POST /understanding/parse-file
- GET /understanding/taxonomy/skills

---

## Validation

Run:

./scripts/hermes-200-smoke-test.sh

Expected:

HERMES-200 smoke test passed

Current smoke test checks:

- Health
- Good resume parsing
- Weak fallback
- File upload
- JD field extraction
- Required/preferred JD skills
- Resume contact extraction
- Skills taxonomy
- Parser version metadata
- Quality threshold metadata

---

## Current State

HERMES-200 is now a working local-first parser foundation.

It can return:

- Extracted text
- Quality score
- Validation warnings
- Fallback decision
- Compressed LLM-ready context
- Structured resume data
- Structured job description data
- Skills
- Required/preferred skills
- Version metadata

---

## Next

Before closing HERMES-200 foundation:

1. Run final smoke test
2. Commit this checkpoint
3. Push to GitHub
4. Decide whether to close foundation or do one hardening pass

Future improvements:

- Better PDF testing
- More resume fields
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
