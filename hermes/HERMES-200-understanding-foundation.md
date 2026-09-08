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
- Phone (now international-aware, see 2026-09-07 update below)
- LinkedIn URL
- Location
- Summary
- Work authorization
- Work experience (structured: company, title, start/end dates, location, description)
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

## 2026-09-07 update — deterministic resume-section extraction, international phones, local prompt fallback

Commit `8319c43` on `jobfynder/hermes` (`feat(understanding): extract resume sections and international phones without an LLM`).

**Problem.** Jake-style resumes (a common resume template) were coming back with empty `name`, `phone`, `experience`, `education`, and `certifications`. `app/understanding/parsers/basic.py` only ever populated `skills`, `years_experience`, `current_title`, `email`, `phone`, `linkedin_url`, and `work_authorization` on `ResumeStructuredData` — the other fields didn't exist on the schema at all, so "More resume fields" (listed under Next below since this file's original checkpoint) had never actually been done.

**Fix — all deterministic, no LLM call added:**

- New `app/understanding/parsers/resume_sections.py` splits a resume into header/summary/experience/education/certifications/etc. sections by recognized header lines, then extracts `name` and `location` from the header line, `current_title` from the first parsed job entry, and structured `experience` (company/title/startDate/endDate/location/description) and `education` (institution/degree/field/year) lists, plus deduplicated `certifications`.
- `app/understanding/parsers/contact.py`'s `extract_phone()` now tries the `phonenumbers` library first (formatted as `PhoneNumberFormat.INTERNATIONAL`) before falling back to the pre-existing regex — fixes extraction for non-US phone formats that the old regex-only approach missed.
- `app/understanding/structured.py`'s `ResumeStructuredData` gained `name`, `location`, `summary`, `experience`, `education`, `certifications` fields.
- `app/understanding/parsers/basic.py` now calls `extract_resume_sections()` for `document_kind == "resume"` and fills these new fields (falling back to the existing regex-based `current_title`/`phone` extractors when the section parser finds nothing).
- New unit tests: `tests/understanding/test_resume_sections.py`, `tests/understanding/test_basic_resume_parse.py`, `tests/prompt_runtime/test_local_resume_extract.py`. **No live/deployed verification is recorded in this commit** — treat this as unit-tested, not yet live-confirmed against a production Understanding deployment.

**Same commit — local prompt fallback for Langfuse outages.** `app/prompt_runtime/registry.json` gained two locally-defined prompts, `jf.resume.parse` and `jf.onboarding.profile-import.extract` (both tagged `metadata.source: "local"`). `app/prompt_runtime/langfuse_prompts.py`'s `_merged_prompts()` now merges these local prompts underneath whatever Langfuse returns, so `get_prompt()`/`list_prompts()` no longer come back empty for these two prompt IDs when Langfuse is unreachable or unconfigured — previously the LLM-fallback path for weak resume parses had no local backstop at all. `jf.jobs.jd.extract` (the job-description LLM-fallback prompt referenced by `FALLBACK_PROMPT_MAP`) has **no local counterpart yet** — the JD fallback path still depends on Langfuse being reachable. This local registry is separate from the 38-prompt Langfuse-hosted catalog in `hermes-parsing-and-prompts-api-guide.md`; it does not change that count.

**Still open, unaffected by this commit:** JD parser field coverage, bigger taxonomy, real Unstructured.io integration, and Langfuse/Promptfoo/Great Expectations evaluation — see Next below.

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

Note (2026-09-07): the smoke test script itself was not updated by commit `8319c43` — it still checks the original resume-contact fields. The new section-extraction fields (name/location/summary/experience/education/certifications) are covered only by the new unit tests listed above, not by this script.

---

## Current State

HERMES-200 is now a working local-first parser foundation.

It can return:

- Extracted text
- Quality score
- Validation warnings
- Fallback decision
- Compressed LLM-ready context
- Structured resume data (including deterministic section extraction as of 2026-09-07)
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
- ~~More resume fields~~ — done 2026-09-07, commit `8319c43` (name, location, summary, structured experience/education, certifications, international phone parsing)
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
