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
- Phone (US and international — international pattern added 2026-09-07, see below)
- LinkedIn URL
- Work authorization
- Full name (added 2026-09-07)
- Location (added 2026-09-07)
- Structured experience entries: company, title, start/end date, location, description bullets (added 2026-09-07)
- Structured education entries: institution, degree, field, year, start/end date, location (added 2026-09-07)
- Certifications (added 2026-09-07)

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

## 2026-09-07 update — deterministic resume-section extraction

**Commit `8319c43f9fdd17b1f46937e64d458cc9a6dc3c13`** on `jobfynder/hermes` `main`: `feat(understanding): extract resume sections and international phones without an LLM`.

Jake-style resumes (a common single-column template) were returning empty name/phone/experience/education/certs because the basic parser only kept email and keyword skills. This commit adds:

- `app/understanding/parsers/resume_sections.py` (new, 316 lines) — splits a resume into sections (header/education/skills/experience/projects/achievements/certifications/summary) and parses structured experience and education entries out of bulleted, dated text.
- `app/understanding/parsers/contact.py` — added an international phone pattern (`+91 89101 45846`-style) ahead of the existing US-only 3-3-4 pattern, so international numbers are no longer sliced or dropped.
- `app/prompt_runtime/local_prompts.py` + `registry.json` (new) — a local, file-based prompt fallback (`jf.resume.parse`, `jf.onboarding.profile-import.extract`, plus four others) that `get_prompt()`/`list_prompts()` now fall back to when Langfuse is unconfigured or unreachable, so the LLM-fallback path for a weak deterministic parse still has a prompt to run.

**Verified in this sync (2026-09-08):** cloned `jobfynder/hermes` at this commit and ran the three new test files directly — `tests/understanding/test_resume_sections.py`, `tests/understanding/test_basic_resume_parse.py`, `tests/prompt_runtime/test_local_resume_extract.py` — 6/6 passed. Not re-verified against a live `/understanding/parse-file` call (no SSH credentials for INTEL-1 available in this environment).

JD-side field extraction is unchanged by this commit.

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
- Structured resume data (now including name, location, structured experience/education, certifications — see 2026-09-07 update above)
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
- More resume fields — partially done 2026-09-07 (name, location, structured experience/education, certifications, international phone); remaining: further field coverage as new resume templates surface gaps
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
