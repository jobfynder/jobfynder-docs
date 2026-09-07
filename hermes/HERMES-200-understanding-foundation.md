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
- Name (added 2026-09-07, see Update below)
- Location (added 2026-09-07)
- Summary (added 2026-09-07)
- Email
- Phone, including non-US/international numbers (added 2026-09-07)
- Structured experience: company, title, start/end date, location, description (added 2026-09-07)
- Structured education: institution, degree, field, year (added 2026-09-07)
- Certifications (added 2026-09-07)
- LinkedIn URL
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

## Next

Before closing HERMES-200 foundation:

1. Run final smoke test
2. Commit this checkpoint
3. Push to GitHub
4. Decide whether to close foundation or do one hardening pass

Future improvements:

- Better PDF testing
- ~~More resume fields~~ — addressed 2026-09-07, see Update below (name/location/summary/experience/education/certifications added; JD fields still open)
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later

---

## Update 2026-09-07

Commit `8319c43` on `jobfynder/hermes` `main` (`feat(understanding): extract resume sections and international phones without an LLM`) — "Jake-style resumes were returning empty name, phone, experience, education, and certs because Understanding only kept email and keyword skills."

- New file `app/understanding/parsers/resume_sections.py` (316 lines): splits a resume into sections (header/education/skills/experience/achievements/etc.) by header line, then deterministically parses name+location from the header, structured experience entries (company/location, title, start/end date, bullet description) and structured education entries (institution/location, degree, field, year) from bulleted lines, and certifications from the certifications/achievements sections.
- `app/understanding/parsers/contact.py`: `extract_phone()` now checks a labeled pattern (`mobile:`/`phone:`/`tel:`/`cell:`/`whatsapp:` followed by digits) first, then the `phonenumbers` library's `PhoneNumberMatcher` (region hint `US`, formats to `INTERNATIONAL`) before falling back to the original US-only 3-3-4 regex — so a resume phone like `+91 89101 45846` is no longer mis-sliced by the US pattern.
- `app/understanding/parsers/basic.py` and `app/understanding/structured.py`: `ResumeStructuredData` gains `name`, `summary`, `experience`, `education`, `certifications` fields; `location` and `phone` now prefer the new section/labeled parsers over the older whole-text regexes.
- `app/understanding/llm_fallback.py`: adds `merge_llm_extracted()`, which fills only the deterministic fields that came back empty from an LLM fallback extraction, via a per-field alias map (e.g. `current_title` accepts `title`/`headline`) — it never overwrites a value the deterministic parser already found.
- Tests added: `tests/understanding/test_resume_sections.py` (13 assertions against a fixture "Jake-style" resume — confirms name, location, 3 structured experience entries in order, education institution/degree/year, and an Azure certification are all extracted correctly, plus the Indian mobile number `+91 89101 45846`), `tests/understanding/test_basic_resume_parse.py` (confirms the same fields surface through `parse_basic_structured_data()`), `tests/prompt_runtime/test_local_resume_extract.py` (confirms the new local fallback prompt renders correctly — see `HERMES-750-litellm-prompt-runtime-foundation.md` §11 for the prompt-runtime side of this same commit).
- Not verified live against INTEL-1 in this pass — no SSH credentials were configured in this environment; this entry is based on the commit diff and its own test suite only.
