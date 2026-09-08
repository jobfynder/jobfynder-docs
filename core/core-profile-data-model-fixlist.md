Status: Active — live product/UX review findings, ready for development
Owner: Jobfynder-Infra
Companion document: `core-dashboards-rightpanel-settings-spec.md` (dashboards, right panel, and Settings — the other half of this same review pass)
Added to jobfynder-docs: 2026-09-07 (content from a live review conducted prior to that date; see dates cited within)

---

# Jobfynder Profile Data Model — Fix List for Development

All five roles (Consultant, Bench Sales Recruiter, Recruiter, Employer, Service Provider) were reviewed directly on `testing.jobfynder.com` — every field, every edit modal, every tab. This document is the complete fix list from that review, ready to hand to the dev team.

Companion document: `core-onboarding-redesign-spec.md` (registration field tiering — keep signup to 5 fields, everything else moves here, to profile completion). Added 2026-09-08.

---

## How to work through this with Cursor

This is written so each item can be handed to Cursor almost as-is. A few things that will make it go faster:

1. **One fix package per Cursor session, not one giant session.** Each numbered item below is scoped to be a single focused change. Open a new chat per item (or per small group of related items) so Cursor's context stays tight and the diff stays reviewable. Trying to do all of Priority 0 in one session will produce a diff too large to review properly.

2. **Before asking Cursor to build something new, ask it to find the existing correct pattern first.** Several of these components already exist and work correctly on one role — they just aren't reused on the others. Start every shared-component task with a prompt like:
   > "Search the codebase for how Recruiter's Specializations/Industries Served fields are implemented — I want to reuse that exact component and pattern for [X]." Don't let Cursor invent a second implementation of something that already exists.

3. **Give Cursor the acceptance criteria verbatim.** Each item below has a short "Done when" line — paste that directly into the prompt so Cursor can self-check its own output before you review it.

4. **For anything cross-cutting (touches multiple roles), ask Cursor to grep/search first, then list every file it will touch, before making changes.** For example: "Find every profile edit form that stores a taxonomy field as free text (comma or newline separated) and list the files" — review that list before saying go.

5. **Do the Priority 0 shared items first, in order.** They're ordered so that later items in this list either depend on or become trivial once the shared components exist. Skipping ahead to role-specific fixes means redoing work once the shared components land.

6. **After each session, verify against the field table it came from** (linked below) — not just the acceptance criteria, but the actual page in the running app, since that's how every one of these was originally found.

---

## Priority 0 — Shared fixes (do these first)

These four items resolve the majority of individual, role-specific bugs listed further down automatically. Build the shared component or fix the shared data problem once; role-specific sections then become "apply the fix here too," not new work.

### P0-1. Build `TaxonomyMultiSelect` and replace every free-text taxonomy field

**Problem:** Several fields that render as tags/chips on screen are actually raw comma-separated or one-item-per-line text boxes underneath, with no connection to master data. This means none of this data is searchable or filterable — it defeats the purpose of collecting it at all.

**Confirmed on:**
- Bench Sales Recruiter → Specialization Areas (Technologies, Roles, Industries, Visa Categories, Geography, Client Types, Contract Types)
- Recruiter → Submission Preferences (Accepts, Does Not Prefer, Required Info), Work Type
- Employer → Technology Specializations (Technologies, Languages, Databases, Tools/Frameworks)
- Consultant → Add Skill's Skill Name field (structured category/proficiency/experience, but the skill name itself is free text)

**Reference implementation (already correct, reuse this):** Recruiter's "Specializations" and "Industries Served" fields — tag chips with add/remove, backed by taxonomy. Consultant's "What I'm Looking For" → Contract Types and Industries also use this pattern correctly.

**Cursor prompt to start with:**
> "Find the component behind Recruiter's Specializations and Industries Served fields (tag multi-select backed by taxonomy). I want to extract this into a shared `TaxonomyMultiSelect` component and reuse it. First show me where it currently lives and what taxonomy/master-data source it reads from."

**Done when:** every field listed above uses the shared component, backed by the same taxonomy tables Consultant/Recruiter's correct fields already use — no comma-separated text boxes remain for any multi-value taxonomy field, on any role.

### P0-2. Remove every editable input for a value that must be system-computed

**Problem:** Several numbers that are meant to be computed from real activity (submissions, interviews, responses) are directly editable text inputs in at least two roles, sitting next to a read-only display of the same number computed correctly.

**Confirmed on:**
- Recruiter → main profile modal: "Last Active / Current Activity", "Avg Response Time (hrs)", "Offer Acceptance Rate (%)" — all plain editable fields. A second, separate copy of "Avg Response Time" and "Response Rate (%)" also exists in the Response Behavior modal.
- Service Provider → "Years in Business" is a plain editable text field
- Consultant → Profile Completion reads 100% even when required fields are visibly empty (a calculation bug, not an editable-field bug, but same root issue: the number isn't trustworthy)

**Reference implementation (already correct):** Employer's "Years in Business" — read-only, computed from Founded Year. Bench Sales' Trust Score / Profile Completion / Submissions / Interviews / Offers — all read-only. Service Provider's Performance tab (Orders Completed, Bookings, Avg Response, Repeat Customers, Refund Rate) — all read-only.

**Cursor prompt to start with:**
> "Find every edit form field across all five profile roles where the field name matches a value that should be computed (response time, offer/acceptance rate, last active, years in business, trust score, profile completion). List each one with its file location before removing anything."

**Done when:** none of these values are accepted as raw input anywhere; each is derived server-side from Submission/Interview/Offer/Interaction/Review records and rendered through one shared read-only component (see P0-2b below). Consultant's Profile Completion calculation is fixed to actually check Professional Summary, Key Strengths, Value Proposition, Career Goals, and portfolio links before reporting 100%.

**P0-2b (small follow-up):** Build one shared `ComputedMetricBadge` component for displaying these values, so there's exactly one rendering pattern for "trust score / response time / offer rate" style numbers across all roles, instead of each role's Overview tab reimplementing its own version.

### P0-3. Build `StructuredLocationInput` and replace free-text location lists

**Problem:** Location fields that accept multiple values are stored as a single comma/newline-separated string. This actively produces wrong data, not just a design smell.

**Confirmed live, not theoretical:**
- Employer → "Other Locations" field stores `"Austin, TX, Remote — US"` as one string. The page renders it as three broken chips (`Austin`, `TX`, `Remote — US`) because the city/state comma collides with the list-separator comma.
- Consultant → "Also open to" (secondary preferred locations) has no validation constraining it to city/state level. On the reviewed account it contains a full landmark address — `"New Jersey Performing Arts Center (NJPAC), Center Street, Newark, NJ, USA"` — saved verbatim from an autocomplete suggestion and shown to recruiters exactly as typed.

**Cursor prompt to start with:**
> "Build a `StructuredLocationInput` component: a repeatable list of {city, state/region, country} entries, not a single text field. It should use a places-autocomplete API but constrain results to city/state-level granularity — reject or truncate landmark/address-level results. Then replace Employer's 'Other Locations' field and Consultant's 'Also open to' field with it."

**Done when:** both fields use the new component; a manual test of typing "Austin, TX" and a nearby landmark search confirms clean, correctly-separated city/state values are stored, not one merged string or a full address.

**Also needed:** a one-time data migration/cleanup script for existing records with garbled location strings (the Employer and Consultant accounts reviewed both already have bad data from this bug).

### P0-4. Fix the duplicate value in the engagement-type taxonomy

**Problem:** "C2C" and "Corp to Corp (C2C)" exist as two separate selectable values in the same taxonomy — this isn't a UI bug, it's a bad row in shared master data, and it surfaces identically on two different roles.

**Confirmed on:**
- Consultant → "What I'm Looking For" → Contract Types chip selector shows both "C2C" and "Corp to Corp(C2C)" as separate options
- Recruiter → Submission Preferences "Accepts" list has the same duplication (though currently free text, see P0-1)

**Cursor prompt to start with:**
> "Find the engagementTypes / contractTypes master data table or enum. Check for duplicate or near-duplicate values (e.g. 'C2C' and 'Corp to Corp (C2C)'). Consolidate to one canonical value per concept and update any seeded/existing records that reference the removed duplicate."

**Done when:** one canonical value exists per engagement type across the whole taxonomy; both Consultant's and Recruiter's selectors read from the same corrected table.

### P0-5. Seed-data / placeholder-content audit across all five roles

**Problem:** Placeholder and test content is visible on accounts that display a "Verified" badge — this is worse than an unfinished feature, because it actively misleads anyone evaluating the profile.

**Confirmed instances:**
- Employer → trust card shows `Vendor Access: test`
- Service Provider → About section contains literal Lorem Ipsum placeholder text
- Service Provider → "Category" displays the raw internal value `company` instead of a formatted label ("Company")
- Service Provider → header shows an unformatted raw ISO timestamp: `"Member since 2026-08-12T14:12:01.568Z"`
- Consultant → Documents tab shows raw storage filenames (`857437324-fsr-tegze-bonus-01.pdf`, and one containing a UUID and duplicated timestamp) instead of a clean display name

**Cursor prompt to start with:**
> "Search all seed/fixture data and any hardcoded placeholder strings across the five profile role templates for: Lorem Ipsum text, the literal string 'test' in badge/trust fields, unformatted ISO date strings rendered directly in JSX, and raw enum values rendered without a label map. List every instance found."

**Done when:** no placeholder or unformatted raw value renders on any profile page; add this check as a standing item in the pre-launch QA checklist, not just a one-time fix.

---

## Priority 1 — Role-specific fixes

Work through these after the Priority 0 items above are done — several of these become one-line changes once the shared components exist.

### Consultant

| Fix | Done when |
|---|---|
| Header "Status" field shows Work Authorization value instead of actual status | Header shows availability/submission status; Work Authorization is not duplicated into this label |
| "Visa," "Work Auth Detail," and "Current Status" in Submission Snapshot all show the identical value | Consolidated into one labeled field |
| Work Authorization "Expiry Date" is free text | Converted to a real date picker |
| Work Authorization "Sponsorship Required" is free text ("no") | Converted to a boolean toggle, matching its neighboring fields |
| "Notice Period" dropdown reuses Availability's option set | Given its own option set (Immediate, 2 weeks, 1 month, etc.) |
| "Willing to Relocate" (Work Authorization) and "Relocation" (Location Preferences) show conflicting values for the same person | Consolidated into one `relocationPreference` field |

**Cursor prompt for this batch:**
> "In the Consultant profile page, fix these five issues: [paste table above]. Each is in a different section of the same profile page — work section by section and show me the diff for each before moving to the next."

### Bench Sales Recruiter

| Fix | Done when |
|---|---|
| "Geographic Focus" (Overview tab) and "Geography" (Specialization tab) display the same percentages from two different sections | Consolidated to one field, shown once |
| "Operational Details" Edit button doesn't open anything | Fixed and covered by an integration test |
| Coverage & Rates "Rate Range (Typical)" is a single free-text string | Converted to structured min/max, consistent with Consultant's rate model |

### Recruiter

| Fix | Done when |
|---|---|
| Edit-form label "Recruiting Focus" vs. display label "Works With" for the same field | One label, used in both places |
| "Response Behavior" Edit button is unreliable (needed two clicks in testing) | Fixed and covered by an integration test |
| "Work Type" is free text | Converted to an enum |

### Employer

| Fix | Done when |
|---|---|
| Two separate Industry fields: single-select "Industry" (main modal) vs. multi-select "Industry Verticals" (Services tab), sharing a display label | **Recommendation: remove the single-select "Industry" field entirely.** A multi-select is a superset of what the single-select does — keep one canonical field (rename "Industry Verticals" to "Industries"), built on `TaxonomyMultiSelect`. If a "primary" industry is ever needed for a badge or headline, use the first entry in the list rather than maintaining a second field that can drift out of sync with the first |
| Engagement Models' "Rate Range" is a single free-text string | Converted to structured min/max |
| Onboarding wizard's Hiring Needs fields (rolesHired, preferredEmploymentType, workArrangementPreference, companyCulture, benefits) don't appear anywhere on the profile | **Recommendation: these are company-level defaults, not job-level fields.** Surface them on the Company Profile (a new "Hiring Preferences" section, using `TaxonomyMultiSelect` for each), and have the "post a job" flow pre-fill new job postings from these defaults, with per-job override allowed. This avoids re-asking the same preferences on every job post while still letting an individual posting diverge from the company's usual pattern |

**Cursor prompt for this batch:**
> "In the Employer profile page, fix these three issues: [paste table above]. For the Industry field: remove the single-select field and keep only the multi-select, renamed 'Industries'. For Hiring Preferences: add a new section to the Company Profile using the shared TaxonomyMultiSelect component for each multi-value field, then find the 'post a job' flow and wire it to pre-fill from these defaults, allowing override per posting."

### Service Provider

| Fix | Done when |
|---|---|
| Trust card asks "Can I submit this candidate?" — copied from the Bench Sales/Recruiter component, doesn't make sense for a service provider | Given role-appropriate copy |
| Service Offerings — not yet populated enough on any test account to confirm field type | Once a service is added, confirm it uses `TaxonomyMultiSelect`, not free text |

---

## Field additions and removals by role

Beyond fixing what's broken, here's what should be added or removed from the data model outright.

### Consultant
- **Add:** `noticePeriod` as its own enum (separate from availability); `documentDisplayName` per uploaded file (separate from the storage key); a single consolidated `relocationPreference` field
- **Remove/consolidate:** the header's mislabeled "Status" binding (fix the binding, don't add a field); the three duplicate visa-status displays in Submission Snapshot; the onboarding wizard's `snapshot`, `keyStrengths`, `valueProposition` fields — these sit empty on real accounts and feed directly into the broken Profile Completion calculation

### Bench Sales Recruiter
- **Add:** a real percentage-allocation input for Geography if the percentage display is worth keeping (currently no field produces the percentages shown) — otherwise remove the percentage bars entirely; structured min/max for Coverage & Rates
- **Remove/consolidate:** duplicate Geography display across two tabs; free-text Specialization Areas fields (replace with `TaxonomyMultiSelect`, not a removal of the underlying concept)

### Recruiter
- **Add:** nothing — the field set is close to right; every issue here is implementation (free text, editable metrics), not a missing concept
- **Remove/consolidate:** duplicate response-time/offer-rate editable inputs (two modals, one concept); "Last Active" as an editable field; the "Recruiting Focus"/"Works With" label split

### Employer
- **Add:** a "Hiring Preferences" section on the Company Profile (rolesHired, preferredEmploymentType, workArrangementPreference, companyCulture, benefits) that serves as the default the "post a job" flow pre-fills from, with per-job override — resolves the current gap where these fields are collected once at onboarding and never used
- **Remove/consolidate:** the single-select "Industry" field (keep only the multi-select, renamed "Industries" — a single value is just a one-item list, no need for a second field); free-text "Other Locations"; the placeholder `Vendor Access: test` badge

### Service Provider
- **Add:** a real founding/start-date field to compute "Years in Business" from, matching the Employer pattern
- **Remove/consolidate:** free-text Technology Specializations fields; the raw `company` enum leak in "Category" display

---

## Suggested Cursor session plan

A reasonable way to split this into sessions so each stays reviewable:

1. **Session 1:** P0-1 — build `TaxonomyMultiSelect`, apply to Bench Sales' Specialization Areas only. Review, merge.
2. **Session 2:** Apply `TaxonomyMultiSelect` to Recruiter's Submission Preferences and Employer's Technology Specializations.
3. **Session 3:** P0-2 — audit and remove editable computed-metric fields across Recruiter and Service Provider; build `ComputedMetricBadge`.
4. **Session 4:** P0-3 — build `StructuredLocationInput`, apply to Employer's Other Locations and Consultant's Also-Open-To; write the data cleanup script for existing bad records.
5. **Session 5:** P0-4 — fix the engagement-type taxonomy duplicate; verify it updates both Consultant and Recruiter selectors.
6. **Session 6:** P0-5 — seed-data audit and QA checklist addition.
7. **Sessions 7+:** Role-specific Priority 1 tables, one role per session (Consultant has the most items — consider splitting it across two sessions: header/status fixes, then work-authorization/location fixes).

Do the field additions/removals for each role in the same session as that role's Priority 1 fixes, since they touch the same files.
