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
- Current title
- Name
- Email
- Phone (US and international — see 2026-09-07 update below)
- LinkedIn URL
- Location
- Summary
- Structured experience (company/title/dates/location/description)
- Structured education (institution/degree/field/year)
- Certifications
- Work authorization

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

## Update — 2026-09-07 (commit `8319c43f`)

`jobfynder/hermes` commit `8319c43f9fdd17b1f46937e64d458cc9a6dc3c13` ("feat(understanding): extract resume sections and international phones without an LLM") closed part of the "More resume fields" gap this checkpoint had listed under Next since its original write-up:

- New `app/understanding/parsers/resume_sections.py` deterministically splits a resume into header/education/skills/experience/projects/achievements/certifications/summary sections and parses name, location, structured experience entries (company, title, start/end date, location, description), structured education entries (institution, degree, field, year), and certifications — none of these were extracted before this commit; `ResumeStructuredData` (`app/understanding/structured.py`) previously had no `name`, `summary`, `experience`, `education`, or `certifications` fields at all.
- `app/understanding/parsers/contact.py`'s `extract_phone` now tries a labeled-field regex (`mobile:`/`phone:`/`tel:`/`cell:`/`whatsapp:`) and, failing that, the `phonenumbers` library (`PhoneNumberMatcher`) before falling back to the original US-shaped pattern — the original `PHONE_PATTERN` only matched US-style numbers (e.g. `+91 89101 45846` was previously not recognized as a phone number at all).
- `app/understanding/parsers/basic.py` wires `extract_resume_sections()` into `parse_basic_structured_data` for `document_kind == "resume"`, and `app/understanding/llm_fallback.py` gained `merge_llm_extracted()` so an LLM-fallback extraction only fills fields the deterministic pass left empty, never overwrites what the local parser already found.
- New tests: `tests/understanding/test_resume_sections.py`, `tests/understanding/test_basic_resume_parse.py` (both pass against a real Jake-style resume fixture in the diff).

No live re-verification was performed for this update — see the state-tracking note in this repo's sync automation; this entry is based on the commit diff only.

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
- Structured resume data (including name, location, summary, structured experience/education, certifications as of 2026-09-07 — see update above)
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
- More resume fields — partially addressed 2026-09-07 (name/location/summary/experience/education/certifications; see update above). Still open: JD field expansion is untouched by that commit.
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
