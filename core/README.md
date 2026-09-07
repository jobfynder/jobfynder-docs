# Core

Product/engineering specs for **Jobfynder Core** — the business-logic layer (`jobFynder-BE-nestJS` + `jobFynder-FE-vite`), as distinct from the intelligence plane (`hermes/`) and the communication plane (`comm/`). See `HERMES-COMM-CORE-INTEGRATION-GUIDE.md` §2 for how the three planes relate.

Unlike `hermes/` and `comm/`, this folder does not (yet) follow a numbered module scheme — Core isn't part of the HERMES-nnn/COMM-nnn/PLATFORM-nnn taxonomy in `JOBFYNDER-HERMES-COMM-CANONICAL.md` §1. These are living specs/fix-lists from active product review passes, not durable architecture decisions — see `Architecture/` for those.

## Contents

- **[core-dashboards-rightpanel-settings-spec.md](./core-dashboards-rightpanel-settings-spec.md)** — the shared data model, right-panel engineering spec, and per-role dashboard specs for all five roles (Consultant, Bench Sales Recruiter, Recruiter, Employer, Service Provider), plus a full Settings review. Includes a ready-to-paste Cursor prompt for every build task.
- **[core-profile-data-model-fixlist.md](./core-profile-data-model-fixlist.md)** — the companion field-level fix list from the same review pass: shared components to build (`TaxonomyMultiSelect`, `StructuredLocationInput`, `ComputedMetricBadge`) and role-specific profile bugs.

Both were reviewed live against `testing.jobfynder.com` — see `Infrastructure/SERVER-INVENTORY.md` and `DISASTER-RECOVERY/Rebuild Hostinger Server.md` for what that server actually is (confirmed testing/UAT, not production).

**Referenced but not yet added to this repo:** `onboarding-redesign-spec.md` (registration field tiering) — cited by the profile fix list as a companion document; not located as of 2026-09-07, don't assume its content.
