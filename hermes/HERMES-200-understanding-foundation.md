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
- Email
- Phone (now including international/non-US formats, e.g. `+91 89101 45846`)
- LinkedIn URL
- Work authorization
- Full name (2026-09-07, commit `8319c43` on `jobfynder/hermes`)
- Location (2026-09-07, commit `8319c43`)
- Structured work experience — company, title, start/end dates per entry (2026-09-07, commit `8319c43`)
- Structured education — institution, degree, year (2026-09-07, commit `8319c43`)
- Certifications (2026-09-07, commit `8319c43`)

**2026-09-07 addition.** `app/understanding/parsers/resume_sections.py` (new file, `extract_resume_sections()`) deterministically splits "Jake-style" resumes into sections (header/education/skills/experience/achievements) and parses name, location, phone, structured experience/education entries, and certifications without an LLM. `app/understanding/parsers/contact.py`'s `extract_phone()` was extended to accept international mobile formats. Commit message: "Jake-style resumes were returning empty name, phone, experience, education, and certs because Understanding only kept email and keyword skills." Evidence: 3 new test files (`tests/understanding/test_resume_sections.py`, `tests/understanding/test_basic_resume_parse.py`, `tests/prompt_runtime/test_local_resume_extract.py`), all passing (verified by this sync run: `pytest tests/understanding/ tests/prompt_runtime/` → 10 passed). No git tag, no live-endpoint re-verification on INTEL-1 (no SSH credentials configured in this environment) — this is code+test evidence only, not a closure claim.

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
- ~~More resume fields~~ — name/location/experience/education/certifications added 2026-09-07, commit `8319c43` (see Resume parser section above); JD fields still open
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
