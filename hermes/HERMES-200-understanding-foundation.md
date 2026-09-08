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
- Phone (US and international)
- LinkedIn URL
- Location
- Summary
- Work authorization
- Experience (structured: company, title, location, start/end date, description)
- Education (structured: institution, degree, field, year)
- Certifications

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

## 2026-09-07 update — deterministic resume-section extraction (commit `8319c43`)

**Evidence.** `jobfynder/hermes` commit `8319c43f9fdd17b1f46937e64d458cc9a6dc3c13` ("feat(understanding): extract resume sections and international phones without an LLM"). Commit message states the concrete bug this fixes: "Jake-style resumes were returning empty name, phone, experience, education, and certs because Understanding only kept email and keyword skills."

- New `app/understanding/parsers/resume_sections.py` (316 lines): splits a resume into sections (header/education/skills/experience/projects/achievements/certifications/summary) by header-line matching, then deterministically parses each — name/location from the header line, `experience[]` and `education[]` as structured objects (company/title/dates/location and institution/degree/field/year respectively), and certifications from a cert-keyword match over the certifications/achievements sections.
- `app/understanding/parsers/contact.py`'s `PHONE_PATTERN` was US-only (3-3-4 digit groups); now tries a labeled pattern (`Mobile:`/`Phone:`/etc.) first, then falls back to the `phonenumbers` library's `PhoneNumberMatcher` for international numbers, before the original US pattern.
- `app/understanding/parsers/basic.py`'s `parse_basic_structured_data` now calls `extract_resume_sections()` for `document_kind == "resume"` and fills `name`, `location`, `summary`, `experience`, `education`, `certifications` on `ResumeStructuredData` (new fields added in `app/understanding/structured.py`).
- New `app/understanding/llm_fallback.py::merge_llm_extracted()` backfills any of those fields that are still empty from the LLM-fallback extraction, without overwriting a deterministic value already found — the LLM fallback is additive, not primary.
- Regression tests added: `tests/understanding/test_resume_sections.py`, `tests/understanding/test_basic_resume_parse.py` — both assert against a real Jake-style resume fixture (name, phone `+91 89101 45846`, 3 experience entries, education year, and an `AZ-900` certification all extracted correctly).

This closes the "More resume fields" item that was listed under Future improvements below (for resumes; JD fields are unaffected and still open).

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
- ~~More resume fields~~ — done 2026-09-07, commit `8319c43` (see above)
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
