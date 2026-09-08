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
- Name (deterministic, added 2026-09-07 — see below)
- Email
- Phone (now international-capable, added 2026-09-07 — see below)
- LinkedIn URL
- Location (deterministic, added 2026-09-07 — see below)
- Work authorization
- Summary (deterministic, added 2026-09-07 — see below)
- Structured experience entries: company/title/startDate/endDate/location/description (added 2026-09-07 — see below)
- Structured education entries: institution/degree/field/year (added 2026-09-07 — see below)
- Certifications (added 2026-09-07 — see below)

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

## 2026-09-07 update — deterministic resume-section extraction (no LLM)

Commit `8319c43f` on `jobfynder/hermes` `main` (`feat(understanding): extract resume sections and international phones without an LLM`) closes part of the "More resume fields" item under Future improvements below. Motivating bug quoted from the commit message: "Jake-style resumes were returning empty name, phone, experience, education, and certs because Understanding only kept email and keyword skills."

- New module `app/understanding/parsers/resume_sections.py` (`extract_resume_sections()`) splits resume text into sections by header (Education, Skills, Experience/Work Experience/Professional Experience, Projects, Achievements, Certifications/Certificates, Summary/Objective/Profile) and returns `name`, `location`, `phone`, `current_title`, `summary`, `experience` (list of `{company, title, jobTitle, startDate, endDate, location, description}`), `education` (list of `{institution, school, degree, field, year, startDate, endDate, location}`), and `certifications` (deduped, matched via a `certified|certification|certificate|<CODE>-<digits>` heuristic).
- `app/understanding/parsers/contact.py`'s `extract_phone()` was US-only (`PHONE_PATTERN`, 3-3-4 digits). It now first checks a labeled-line pattern (`mobile:`, `phone:`, `tel:`, `cell:`, `whatsapp:`), then an international pattern via the `phonenumbers` library (`PhoneNumberMatcher`), before falling back to the original US pattern.
- `ResumeStructuredData` (`app/understanding/structured.py`) gained `name`, `summary`, `experience: list[dict]`, `education: list[dict]`, `certifications: list[str]` fields. `parse_basic_structured_data()` (`app/understanding/parsers/basic.py`) now fills `current_title`/`phone` from `extract_resume_sections()` when the existing title-probe/regex extractors come back empty, rather than replacing them.
- `merge_llm_extracted()` (new, `app/understanding/llm_fallback.py`) fills only the fields the deterministic parser left empty from the LLM fallback's extraction (`name`, `current_title`, `phone`, `email`, `location`, `summary`, `experience`, `education`, `certifications`) — it never overwrites a value the deterministic parser already found, keeping "Local first" from the Goal section above intact even when the LLM fallback fires.
- Regression tests added: `tests/understanding/test_resume_sections.py` (Jake-style resume fixture — asserts name, location, phone, three parsed experience entries, one education entry with `year == "2023"`, and an `AZ-900` certification), `tests/understanding/test_basic_resume_parse.py`.

This is an extension of the Resume parser feature list above — it does not change HERMES-200's "Working foundation completed" status or close the foundation.

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
- More resume fields (partially addressed 2026-09-07 — see above: name, location, summary, structured experience/education, certifications)
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
