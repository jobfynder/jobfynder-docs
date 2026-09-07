# Jobfynder Core — Product Modules

"Jobfynder Core" refers to the main product platform (backend + frontend), as distinct from the Hermes intelligence plane and the COMM communication plane. This file indexes the actual backend module structure so it's discoverable without browsing the codebase directly.

## Roles

Five user-registerable roles: **Consultant, Bench Sales Recruiter, Recruiter, Employer, Service Provider**. `CRM_ADMIN` is a sixth value in the schema but is the internal platform-admin role — not user-registerable, not part of the public role model. Source of truth: the `UserRole` enum in `jobFynder-BE-nestJS/prisma/schema.prisma` — trust the schema over any doc if they ever disagree.

## Backend module map (`src/`)

Descriptive, not a proposal to reorganize the code.

**Product / business modules:** `bench` (bench sales / marketing), `companies` (employer & vendor records), `jobs` / `job-templates`, `profile`, `resume` / `resume-intelligence`, `messenger` (feeds the NRM `relationship_event` log on first reply only — see `ADR-0006`), `connections` (Network Relationship Module), `verification`, `invites`, `org-access` / `org-team`, `crm-leads` / `crm-services`, `master-data`.

**Platform / infrastructure modules:** `auth` / `auth-core` / `oauth`, `linkedin` (OAuth only — name, email, photo; the LinkedIn API has been locked to more than that since 2018), `mail` / `sms`, `storage`, `typesense` (search), `cache`, `audit`, `health`, `cron`, `hermes` (Core's integration point with the Hermes intelligence layer), `ai` / `prompts` / `content-generation`.

## Related

`HERMES-COMM-CORE-INTEGRATION-GUIDE.md` for how to actually integrate with Core, `01-platform-architecture.md` for the broader service-oriented architecture, `ADR-0001` for the engineering defaults every module should follow.
