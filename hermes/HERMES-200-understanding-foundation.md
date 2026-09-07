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
- Phone (deterministic international-number matching via `phonenumbers`, plus a labeled-field regex for `mobile:`/`phone:`/`tel:`/`cell:`/`whatsapp:` lines; falls back to the original US-shaped pattern)
- LinkedIn URL
- Location
- Summary
- Structured experience (company, title, start/end date, location, description bullets)
- Structured education (institution, degree, field, year)
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

## 2026-09-07 update — deterministic resume-section extraction (commit `8319c43f`)

`jobfynder/hermes` commit `8319c43f9fdd17b1f46937e64d458cc9a6dc3c13` ("feat(understanding): extract resume sections and international phones without an LLM") closes most of the "More resume fields" item under Next below. Evidence, from the diff itself:

- New `app/understanding/parsers/resume_sections.py` (316 lines) splits a resume into `header`/`education`/`skills`/`experience`/`projects`/`achievements`/`certifications`/`summary` sections by heading match, then parses name + location from the header line, structured experience entries (company/title/start-end date/location/description) from bullet+date-line pairs, structured education entries (institution/degree/field/year) the same way, and certifications by keyword hint (`certified`, `certification`, `certificate`, or an `XX-000`-shaped code).
- `app/understanding/parsers/contact.py`'s `extract_phone()` now tries a labeled-field regex first (`mobile:`/`phone:`/`tel:`/`cell:`/`whatsapp:`), then `phonenumbers.PhoneNumberMatcher` for international numbers, before falling back to the original US-shaped regex — this was the reported bug: Jake-style resumes with an Indian mobile number (`+91 89101 45846`) were returning no phone at all.
- `app/understanding/parsers/basic.py`'s `parse_basic_structured_data()` now calls `extract_resume_sections()` for `document_kind: resume` and fills `name`, `location`, `summary`, `experience`, `education`, `certifications` on `ResumeStructuredData` (all new fields on that model, `app/understanding/structured.py`) in addition to the fields already listed above.
- Regression tests added: `tests/understanding/test_resume_sections.py` (11 assertions against a real Jake-style resume fixture, including the Indian mobile number and a US number), `tests/understanding/test_basic_resume_parse.py` (asserts the full pipeline populates name/phone/title/email/experience count/education year/certification).
- The LLM fallback path (`app/understanding/llm_fallback.py`) gained a `merge_llm_extracted()` step that fills only the deterministic fields still empty after the parser above runs, from whichever alias the LLM extract used (`name`/`display_name`/`full_name`, `current_title`/`title`/`headline`, etc.) — it never overwrites a value the deterministic parser already found.

Live re-verification was not performed as part of this doc update — no SSH credentials for `jobfynder-intel-01` were available in the environment that made this edit. This entry is evidenced by the commit diff only; re-confirm against `POST /understanding/parse-text` with a real resume before treating the new fields as production-verified end to end.

---

## Next

Before closing HERMES-200 foundation:

1. Run final smoke test
2. Commit this checkpoint
3. Push to GitHub
4. Decide whether to close foundation or do one hardening pass

Future improvements:

- Better PDF testing
- ~~More resume fields~~ — largely done 2026-09-07, see the update above (name, location, summary, structured experience/education, certifications, international phone). JD-side field expansion is still open.
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
