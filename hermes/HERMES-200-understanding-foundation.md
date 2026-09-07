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
- Phone (international numbers, 2026-09-07 — see below)
- LinkedIn URL
- Work authorization
- Name, location, summary (2026-09-07 — see below)
- Structured experience entries: company, title, start/end date, location, description (2026-09-07 — see below)
- Structured education entries: institution, degree, field, year (2026-09-07 — see below)
- Certifications (2026-09-07 — see below)

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

**Resume-field extraction extended, 2026-09-07 (`jobfynder/hermes` commit `8319c43f9fdd17b1f46937e64d458cc9a6dc3c13` on `main`).** Closes part of the "More resume fields" item that had been open under [Next](#next) since this foundation's original checkpoint.

- New module `app/understanding/parsers/resume_sections.py`: splits resume text into sections (Education/Skills/Experience/Projects/Achievements/Certifications/Summary, header aliases handled) and deterministically parses a header name+location line, an `Experience` section into per-job entries (company, title, start/end date, location, bullet description), an `Education` section into per-entry records (institution, degree, field, year), and a `Certifications`/`Achievements` section into a certification list.
- `app/understanding/parsers/contact.py`: `extract_phone()` rewritten to try a labeled pattern (`mobile:`/`phone:`/`tel:`/`cell:`/`whatsapp:` followed by a number) first, then the `phonenumbers` library (`PhoneNumberMatcher`) for any valid international number, falling back to the original US-shaped regex only if neither matches — fixes international (e.g. Indian `+91`) mobile numbers that the old US-only `\d{3}-\d{3}-\d{4}`-style pattern could not recognize.
- `app/understanding/structured.py`: `ResumeStructuredData` gained `name`, `summary`, `experience: list[dict]`, `education: list[dict]`, `certifications: list[str]` fields.
- `app/understanding/parsers/basic.py`: `parse_basic_structured_data()` now calls `extract_resume_sections()` for `document_kind == "resume"` and fills the new fields (falling back to the existing title/phone extractors when a section parse comes up empty).
- `app/understanding/llm_fallback.py`: the LLM-fallback resume schema was extended to match (structured `experience`/`education` objects instead of bare string lists) and a new `merge_llm_extracted()` only fills fields the deterministic parser left empty, never overwriting a deterministic result.
- Root cause cited in the commit message: "Jake-style" resumes (a common single-column template) were returning empty name/phone/experience/education/certs because Understanding previously kept only email and keyword-matched skills for that document kind.
- New tests added in the same commit: `tests/understanding/test_resume_sections.py` (name/location/phone/experience/education/certification extraction against a full sample "Jake" resume, plus a direct international vs. US phone-number assertion) and `tests/understanding/test_basic_resume_parse.py` (same assertions through the `parse_basic_structured_data` entry point).

**Still open, unaffected by this change:** JD-field extraction was not touched by this commit (JD parser fields above are unchanged); bigger taxonomy, real Unstructured.io integration, and the Langfuse/Promptfoo/Great Expectations evaluation layer remain as listed under [Next](#next).

A related prompt-runtime change from the same commit (a local fallback definition for the `jf.resume.parse` prompt, used when the deterministic parser is weak and Langfuse is unreachable) is recorded in `hermes/HERMES-750-litellm-prompt-runtime-foundation.md` §11, not here — this file covers the deterministic parser only.

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
- Structured resume data (now including name, location, summary, structured experience/education, certifications — see 2026-09-07 note above)
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
- More resume fields — **partially done 2026-09-07**, see above (name, international phone, location, summary, structured experience/education, certifications); still no additional fields beyond these
- More JD fields
- Bigger taxonomy
- Real Unstructured.io integration
- Headroom integration
- Langfuse, Promptfoo, Great Expectations later
