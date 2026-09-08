Status: Active — ready for development
Owner: Jobfynder-Infra
Companion documents: `core-profile-data-model-fixlist.md` (profile field-level fixes — Tier 2 fields land there once collected), `core-dashboards-rightpanel-settings-spec.md` (dashboards/right panel/Settings)
Added to jobfynder-docs: 2026-09-08. Referenced by `core-profile-data-model-fixlist.md` since that file's own addition (2026-09-07) as a companion document; located and added the next day.

**Spot-verified against the live codebase before adding, not taken on faith:** the `canidateRetention` typo (Bug #3 below) is real — confirmed present in `jobFynder-BE-nestJS`'s `src/auth/dto/register.dto.ts`, `src/profile/dto/update-profile.dto.ts`, `src/profile/profile-process.service.ts`, and `src/profile/profile-transformers.service.ts` (stored inside a JSON blob, not a distinct Prisma column — the fix needs to touch the JSON key, not a schema migration). `privacyControl` (Bug #6) is also a real, live field name across several `jobFynder-FE-vite` files (`transformApiToFormData.ts`, `roleFormConfig.ts`, `onboardingTransform.ts`, `types/auth.ts`, `types/bench-sales-marketing-privacy.ts`). Not every field in this document was individually re-verified — treat the rest as reported, not independently confirmed.

---

# Onboarding Redesign — Field Tiering Spec

Goal: cut registration to one screen, 5 fields, for every role. Everything else moves to post-signup profile completion, collected through import prefill and feature-gated prompts instead of a second mandatory wizard.

---

## Tier 1 — Account Creation (blocks nothing, same shape for all 5 roles)

| Field | Required | Notes |
|---|---|---|
| `role` | Yes | Radio, unchanged |
| Name (`fullName` / `companyName` / `providerName`) | Yes | |
| `email` | Yes | Uniqueness check, unchanged |
| `password` | Yes | Hidden entirely if OAuth session exists, unchanged |
| `phoneExtension` + `phoneNumber` | Yes | Keep required — this is contact infrastructure the platform depends on, not registration friction |
| `profilePicture` | No | Keep optional, keep on this screen |

Everything below this line is removed from the registration gate for every role and re-classified as Tier 2.

Import-profile step (resume upload, Google/LinkedIn OAuth, `linkedinUrl`) stays exactly as-is — already correctly optional, already doing the prefill work.

---

## Tier 2 — Profile Completion, by role

Each group lists the fields, whether they can be auto-filled from resume/LinkedIn import, and the trigger point where the platform should actually ask for them (not at signup).

### Consultant

| Group | Fields | Auto-fillable from import? | Ask when |
|---|---|---|---|
| Discoverability | `jobTitle`, `yearsExperience`, `employmentType`, `currentAvailability`, `skills`, `tools`, `databases`, `operatingSystem` | Partial (title, years, skills) | Dashboard nudge on day 1; hard-gate before profile is included in recruiter search results |
| Compensation | `rateType`, `rateRange`, `customRateRange`, `openNegotiation` | No | Before consultant can apply to a job, or before a recruiter can view rate |
| Work authorization | `visaStatus`, `tnExpirationDate`, `h1bTransferable`, `otherVisaStatus` | No | Required before consultant can be submitted to a client (compliance gate) — not before account creation |
| Location & contact | `location`, `preferredCitiesStates`, `targetLocation`, `contactPreference`, contact hours | Partial (location) | Dashboard nudge, non-blocking |
| About & docs | `summary`, `portfolio`, `blog`, `publications`, `language`, `industries` | Partial (summary draft from resume) | Dashboard nudge |
| Experience records | `workExperience[]`, `education[]`, `certifications[]` | Yes, from resume parse | Already optional — keep optional forever, just prefill better |
| `openToWork` | Toggle | No | One-tap prompt post-signup, not a form field |
| `privacy` | Radio | — | Default to "Only to recruiters I apply to." Expose as a settings toggle, don't ask at all |
| `resume` (Step 4) | File | — | **Remove.** Already collected in import-profile. Don't ask twice. |
| `linkedin` (Step 4 URL field) | URL | — | **Remove.** Already collected via OAuth + `linkedinUrl` in import-profile. Don't ask a third time. |
| Verification block | email/phone/whatsapp/linkedin/KYC | — | Unchanged — always optional, self-serve |

### Bench Sales Recruiter

| Group | Fields | Auto-fillable? | Ask when |
|---|---|---|---|
| Discoverability | `jobTitle`, `company`, `yearsExperience`, `keySpecialization`, `jobRoles`, `visaTypes`, `contractTypes`, `industries` | Partial | Dashboard nudge; gate before appearing in Pulse Network matches |
| Metrics & vendors | `utilizationRate`, `successfulPlacements`, `preferredVendors`, `vendorTypes`, `engagementModels` | No | Prompt after first submission is logged, not at signup |
| Skills stack | `skills`, `technologies`, `tools`, `databases`, `operatingSystem` | Partial | Dashboard nudge |
| Location & contact | `location`, `preferredCitiesStates`, `contactPreferences`, contact hours | Partial | Dashboard nudge |
| `aboutMe` | Textarea | Partial (from resume) | Dashboard nudge |
| `privacyControl` / `privacy` | Radio (two separate fields currently — consolidate into one) | — | Default sensible value, expose in settings |
| `openToWork` | Toggle | No | One-tap post-signup prompt |
| Verification block | Same 5 items | — | Unchanged |

### Recruiter (Technical/Corporate)

| Group | Fields | Auto-fillable? | Ask when |
|---|---|---|---|
| Discoverability | `jobTitle`, `company`, `yearsExperience`, `keySpecialization`, `technologies`, `jobRoles`, `clientFocus`, `contractTypes` | Partial | Dashboard nudge; gate before appearing as a recruiter contact in search |
| Skills stack | `skills`, `tools`, `databases`, `operatingSystem` | Partial | Dashboard nudge |
| Location & contact | `location`, `language`, `contactPreferences`, contact hours | Partial | Dashboard nudge |
| `aboutMe` | Textarea | Partial | Dashboard nudge |
| Experience records | `workExperience[]`, `education[]`, `certifications[]` | Yes, from resume | Keep optional |
| `privacy` | Radio | — | Default, expose in settings |
| `openToWork` | Toggle | No | One-tap post-signup prompt |
| Verification block | Same 5 items | — | Unchanged |

### Employer

| Group | Fields | Auto-fillable? | Ask when |
|---|---|---|---|
| Company profile | `companySize`, `website`, `industries`, `availability` | No | Dashboard nudge on day 1 |
| Hiring contact | `hiringContactName`, `hiringContactTitle`, `hiringStatus`, `contactPreferences`, contact hours | No | Dashboard nudge |
| About | `aboutUs` | No | Dashboard nudge |
| Hiring needs | `rolesHired`, `hiringIndustry`, `technologies`, `preferredEmploymentType`, `workArrangementPreference`, `customWorkArrangement`, `companyCulture`, `benefits` | No | **Gate at "post your first job" flow**, not registration — this is exactly the information needed at that moment, so asking there removes friction and improves data quality |
| Recruiting partnerships | `recruitingAgencies`, `engagementModels`, `partnershipCriteria` | No | Gate before employer can invite/engage a recruiting partner through Marketplace |
| Verification block | Same items | — | Unchanged |

### Service Provider

| Group | Fields | Auto-fillable? | Ask when |
|---|---|---|---|
| Basic profile | `providerType`, `serviceCategory`, `location`, `website`, `contactPersonName`, `contactPersonTitle`, `contactMethod`, `availability` | No | Dashboard nudge |
| About & services | `aboutUs`, `services`, `targetUsers`, `benefits`, `technologyStack`, `skills` | No | **Gate before listing goes live in Marketplace** — a provider without this content shouldn't be publicly listed anyway, so this is a natural checkpoint, not an artificial one |
| Pricing & proof | `pricingModel`, `customPricing`, `caseStudies[]` | No | Same gate as above |
| Verification block | 7 items (incl. Company Documents, Credentials) | — | Unchanged |

---

## Bug fixes to ship in the same pass

| # | Issue | Fix | Acceptance criteria |
|---|---|---|---|
| 1 | Resume asked twice (optional in import-profile, required in Consultant Step 4) | Remove the Step 4 resume field entirely; if import-profile resume exists, reference it | A user who uploads a resume during import is never asked for it again |
| 2 | LinkedIn asked up to 3 times (OAuth, `linkedinUrl`, Step 4 `linkedin` URL, verification) | Keep only OAuth + `linkedinUrl` in import-profile; remove Step 4 `linkedin` field; verification block just confirms the same value | A user connects LinkedIn once and it's reflected everywhere it's used |
| 3 | `canidateRetention` misspelled in Recruiter metrics — **confirmed live in `jobFynder-BE-nestJS`, stored inside a JSON blob (not a distinct Prisma column) in `register.dto.ts`, `update-profile.dto.ts`, `profile-process.service.ts`, `profile-transformers.service.ts`** | Rename to `candidateRetention` in schema, form, and API before more code depends on the typo | Field key is `candidateRetention` end-to-end; migration script backfills existing records (JSON key rename, not a schema migration) |
| 4 | Resume upload label says "PDF" but picker accepts DOCX too | Update label to "PDF or DOCX, max 10MB" | Label matches actual accepted file types |
| 5 | Dead fields defined in types but never rendered (`timePreference`, `h1bExpirationDate`, `optExpirationDate`, `cptExpirationDate`, `eadCategory`, `eadExpirationDate`, `preferredHours`, `companyEmail`, `rateType` on Recruiter, `linkedinProfile` on Recruiter/Bench Sales, `openNegotiation` on Bench Sales, `skills` on Employer, `recommendations[]`, `endorsements[]`) | Delete from form types and default objects unless a near-term feature needs them | Schema contains no field without a rendered control or a named upcoming feature |
| 6 | Two separate privacy fields on Bench Sales (`privacyControl` and `privacy`) doing the same job — **`privacyControl` confirmed live in `jobFynder-FE-vite`** (`transformApiToFormData.ts`, `roleFormConfig.ts`, `onboardingTransform.ts`, `types/auth.ts`, `types/bench-sales-marketing-privacy.ts`) | Consolidate into one `privacy` field, migrate existing data | Only one privacy field exists per role |

---

## Migration notes

- Existing users who already completed the old wizard need no action — their data stays as-is.
- New signups get Tier 1 only. On first login, show a profile completion percentage on the dashboard, computed from Tier 2 fields actually filled.
- Run a one-time backfill job to compute the completion percentage for existing users so the meter isn't blank for them.
- Feature gates (search visibility, submission eligibility, job posting, Marketplace listing) need a single shared "profile completeness" check per role rather than being hardcoded per screen — build this once, reuse across Search, Submission Tracker, Job Tracker, and Marketplace. **This is the same `ComputedMetricBadge`/completeness-computation concept already specified in `core-profile-data-model-fixlist.md` P0-2b — implement once, shared by both specs.**

---

## Acceptance criteria for the redesign

1. Every role can create an account with exactly 5 fields (role, name, email, password/OAuth, phone) plus an optional photo.
2. No Tier 2 field blocks account creation for any role.
3. A consultant/recruiter/bench sales profile with 0% Tier 2 completion does not appear in search or matching results — this is the actual enforcement mechanism, not a required-field flag at signup.
4. An employer cannot post a job until the "hiring needs" group is filled — enforced at the post-a-job flow, not at registration.
5. A service provider listing is not publicly visible in Marketplace until the "about & services" and "pricing & proof" groups are filled.
6. Resume and LinkedIn are each collected exactly once per user, regardless of which screen they came from.
7. Dashboard shows a profile completion percentage that updates as Tier 2 fields are filled.
