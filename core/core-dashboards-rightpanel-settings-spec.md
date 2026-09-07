Status: Active — live product/UX review findings and engineering spec, ready for development
Owner: Jobfynder-Infra
Companion document: `core-profile-data-model-fixlist.md` (profile field-level fixes — the other half of this same review pass)
Added to jobfynder-docs: 2026-09-07 (content from a live review conducted prior to that date; see dates cited within)

This replaces `dashboard-rightpanel-review.md`, `dashboard-buildplan-and-rightpanel.md`, and `jobfynder-dashboards-final-spec.md` — none of those three predecessor files were ever added to this repo (checked before writing this note), so there is nothing to retire here; this is simply the first version of this content to land in `jobfynder-docs`.

---

# Jobfynder Dashboards, Right Panel & Settings — Final Consolidated Spec

This is the definitive version, replacing `dashboard-rightpanel-review.md`, `dashboard-buildplan-and-rightpanel.md`, and `jobfynder-dashboards-final-spec.md` — everything useful from all three is folded in here, plus a full Settings review (new) and a ready-to-paste Cursor prompt for every task in the build list. Companion document, still current and separate: `core-profile-data-model-fixlist.md` (profile field-level fixes).

All five roles were reviewed live on `testing.jobfynder.com` — dashboards, right panel, and now Settings. This is a development build on mock data, not production; findings about disconnected or inconsistent data are the reason a shared data model needs to exist before the unbuilt pieces go in, not evidence that something regressed.

## How to use this with Cursor

Same discipline as `core-profile-data-model-fixlist.md`: one numbered task (Section 8) per Cursor session, not the whole document at once. Each task below includes a ready-to-paste prompt. Start every shared-component or shared-data task by asking Cursor to find and reuse the existing correct pattern before building anything new — several of these already exist correctly on one role and just need extracting.

---

## 1. The shared data model — build this first

Every dashboard is a view onto one loop: a consultant gets matched to a job, gets submitted, gets interviewed, gets an offer. Consultant and Bench Sales Recruiter build the supply side. Recruiter is the demand side, receiving the exact submissions Bench Sales Recruiter sends. Employer sits above Recruiter, owning the requirements. Service Provider sits outside this loop, selling services to people in it.

| Shared source | Written by | Read by |
|---|---|---|
| `team_members` | Employer inviting a Bench Sales Recruiter or Recruiter | Employer's rollup views; a BSR/Recruiter's own dashboard header (already shows their employer — confirmed live) |
| `consultants` / Hotlist | Consultant's own profile; Bench Sales Recruiter adding to their Hotlist | Consultant profile, each BSR's Hotlist, Recruiter's Incoming Submissions, Employer's Hotlist rollup |
| `requirements` / Jobs | Recruiter posting a job | Recruiter's Open Roles, Employer's Open Positions (attributed per posting Recruiter), every "job match" surface on Consultant/Bench Sales dashboards |
| `submissions` | Bench Sales Recruiter or Consultant's "Submit" action | Recruiter's Incoming Submissions; every conversion metric on every role's Reports/Analytics/Track Record |
| `partnerships` | Either side accepting a partnership request (cross-company) | Bench Sales' Partnerships tab, Recruiter's Network tab, Employer's CRM Leads |
| `panel_dismissal` | User dismissing an alert-type Needs You item | `NeedsYouService` (Section 6.4) |
| `subscription_plans` (per role) | Admin/product config; user's plan selection | My Subscription settings page (Section 7) — currently broken, see below |
| Completeness/trust-score computation | Server-side, computed from the above | Every role's `ComputedMetricBadge` — never a raw editable input, never duplicated per-tab (see `core-profile-data-model-fixlist.md` P0-2) |

`team_members` is distinct from `partnerships`: team membership is internal to one Employer account; partnerships are cross-company relationships.

---

## 2. Shared UI components — build once, reuse everywhere

| Component | Purpose | Status |
|---|---|---|
| `DashboardStatRow` | Header stat-card row, config-driven per role | Needs extraction — built twice independently (Consultant, Bench Sales) |
| `NeedsYouService` + `<NeedsYouPanel />` | Ranked action list, powers both the center-column Action Queue and the right panel | Fully specified in Section 6, not yet built |
| `ActivityTimeline` | Chronological activity log | Needs extraction |
| `ReportsPage` | Analytics with role-scoped metric configs | Needs extraction — currently broken: Bench Sales Recruiter's Reports tab shows Consultant's content unchanged |
| `ComputedMetricBadge` | Read-only trust score / response time / completion % display | Referenced in the profile fix list; reuse for dashboard-level metrics too |
| `TaxonomyMultiSelect` / `StructuredLocationInput` | Structured multi-value and location fields | Already specified in `core-profile-data-model-fixlist.md`; the location bug is now confirmed on a third field (a job posting's location) |
| `RoleSettingsPanel` | Per-role settings section, scoped to the logged-in user's actual role only | New — needed to fix the Role Settings tab-visibility bug (Section 7) |
| `SubscriptionPlanCard` | Plan display/selection, config-driven per role's actual pricing tiers | New — needed to fix My Subscription (Section 7) |

---

## 3. Build sequence

1. **Data model** (Section 1).
2. **`NeedsYouService`** (Section 6) — backend service against existing tables; doesn't need the new dashboards built first, and every dashboard from this point on should consume it from day one.
3. **Remaining shared components** (Section 2), including `<NeedsYouPanel />`, `RoleSettingsPanel`, `SubscriptionPlanCard`.
4. **Settings fixes** (Section 7) — scope Role Settings to the user's actual role; fix My Subscription to show each role's real pricing tiers. This is independent of the dashboard builds below and can happen in parallel once Section 3's components exist.
5. **Recruiter dashboard** — direct receiving end of submissions Bench Sales Recruiter already generates.
6. **Employer dashboard** — depends on Recruiter (Open Positions/team rollup) and adds the Team invite-with-role-type flow.
7. **Service Provider dashboard** — most decoupled from the core loop; build last.
8. **Retrofit the right panel** on Consultant and Bench Sales Recruiter to consume `NeedsYouService`, replacing current static content.

---

## 4. Employer team structure — read before building Employer or Recruiter

Confirmed by the founder and confirmed live: **an Employer account has Bench Sales Recruiters and Recruiters working for it as team members.** Bench Sales Recruiters maintain Hotlists of consultants; Recruiters maintain Jobs. A BSR/Recruiter account already carries a reference to its Employer (confirmed live: "Apex Tech Solutions LLC · Your employer profile · Bench Sales Recruiter"). What's missing is the reverse direction — nothing on the Employer side rolls this up.

Live-checked on the Employer profile's Team tab: exactly one member exists (the account owner, tagged generically "admin"), with an "Invite a New Team Member" action that has no role-type selector.

- **"Hotlist" is the platform's own term** (appears in the site's footer nav: "Hotlist & Discovery") — use it consistently instead of "roster."
- **The Employer's existing "Bench" tab is a separate feature, not a Hotlist rollup.** Live review shows it's a talent-marketplace discovery view (Request Resume / Request Intro / Shortlist actions), not "my team's combined hotlists." Keep both: existing Bench tab for discovery, new rollup view for the team's actual hotlists.
- **The Employer's existing "Open Positions" tab needs a "Posted by [Recruiter name]" attribution** once more than one Recruiter is on the team.

### What to build
- **Team tab**: role selector in the invite flow (Bench Sales Recruiter / Recruiter / Admin). Accepted invite creates a `team_members` row; the person gets their own login landing on their own role-appropriate dashboard, Employer already attached as context.
- **Employer Dashboard (Overview)**: rolls up total Hotlist size, total active Jobs, team-wide pipeline, and a cross-team Action Queue.
- **New Hotlist rollup view**: every consultant on any team BSR's hotlist, owning BSR, status.
- **Analytics tab**: per-recruiter and per-BSR breakdown, not just company totals.

---

## 5. Per-role dashboard specs

### 5.1 Consultant — built, needs fixes

| Issue | Fix |
|---|---|
| Profile completeness shown as three different numbers across three tabs (82% Overview, 92/100 My Profiles, 80% Reports) | One `SYSTEM_COMPUTED` score via `ComputedMetricBadge`, everywhere |
| "Tech Staff Solutions" partner stats disagree between My Profiles (2/1/50%) and Overview/Reports (~4/3/1) | Trace My Profiles' source; point at the same aggregation the other two use |
| "Selected Consultant" placeholder text in Resume Credits usage history | Fix the save path if it's a default-value leak |
| Marketing Settings has overlapping duplicate toggles for one decision ("Require Submission Approval" vs. "Require My Approval Before Submission") | Consolidate to one control, one field |

**Open questions for the founder, not engineering:** does Resume Credits fit the locked pricing model? Are Reply/Message buttons wired to the Messenger module?

### 5.2 Bench Sales Recruiter — built, needs fixes (highest priority)

| Issue | Fix |
|---|---|
| **Three tabs show three different, non-overlapping consultant lists** — Overview (6 names), Partnerships (a 7th, David Kim), Live Jobs (two more, not appearing elsewhere) | All three must read the shared Hotlist table (Section 1) |
| Reports and Marketing Settings show Consultant's content unchanged | Build via the config-driven `ReportsPage` component |
| "Review Conflict" button does nothing | Wire to a real conflict-resolution view |
| "Submit" opens an edit form for an existing submission, not a new linked one; "Recruiter Contact Name" is filled while "Recruiter/Company" is empty | Fix Submit to create a properly-linked submission tied to the clicked match |

**Works correctly, don't change:** "Review Request" on the Overview header correctly navigates to a well-built Partnerships Inbox view — the reference example for every other action button.

### 5.3 Recruiter — not built, full spec

Tab shell confirmed live: `Dashboard`, `Open Roles`, `Network`, `Analytics` (all placeholder).

- **Dashboard**: Header stat row (Active Requirements, New Submissions to Review, Interviews Scheduled, Offers Pending, Avg Time to Fill — from the profile's existing `SYSTEM_COMPUTED` Track Record fields). Action Queue via `NeedsYouService`. **Incoming Submissions** — candidates submitted against this recruiter's requirements, rendering from the same `submissions` table Bench Sales writes to. Partner Performance from the shared `partnerships` table. Activity Timeline.
- **Open Roles**: requirement management (role, client, urgency, status, submissions received, days open, Client & Requirement Context fields already on the profile). Writes to the same `requirements` table Employer's Open Positions reads.
- **Network**: BSR/Consultant directory, shared `partnerships` table.
- **Analytics**: Recruiter-specific only (Submission→Interview, Interview→Offer, time-to-fill, ranked partners, fill rate). Must not reuse another role's Reports content.

### 5.4 Employer — not built, full spec

Tab shell confirmed live: `Dashboard`, `Team`, `Bench`, `Analytics` (Team and Bench already exist on the profile and were reviewed). Read Section 4 first.

- **Dashboard**: Header stat row (Active Job Postings rolled up across Recruiter team members, New Applicants This Week, Interviews Scheduled, Offers Pending, Avg Time to Fill). Action Queue. Open Positions summary. Recruiting Partner Activity. Activity Timeline.
- **Team**: role-type invite flow (Section 4).
- **Open Positions** (exists): wire to shared `requirements` table; fix the two confirmed live issues — location saved as a full landmark address (`"Citi Field, Seaver Way, Flushing, NY, USA"`) instead of city/state, and two tags reading the literal placeholder "test."
- **Bench** (exists): keep as market-wide discovery, separate from the new Hotlist rollup.
- **New Hotlist rollup view** (Section 4).
- **Analytics**: per-recruiter/per-BSR breakdown.
- **Services, CRM Leads, Hiring** (exist, reviewed in the profile fix list): field-level fixes only (two-Industry-fields conflict, Hiring Preferences section, `Vendor Access: test` placeholder).

### 5.5 Service Provider — not built, full spec

Tab shell confirmed live: `Dashboard`, `Services`, `Projects`, `Analytics` (all placeholder). Sits outside the core placement loop — closer to small-business order management.

- **Dashboard**: Header stat row (Active Projects, New Inquiries, Pending Responses, Revenue This Month — from the profile's existing correct Performance-tab metrics). Action Queue. Client Activity feed.
- **Services**: management/editing view for the service catalog — same underlying data as the profile's public "Service Offerings" (currently "0 services"), one record two views. Use `TaxonomyMultiSelect` from day one, not free text.
- **Projects**: the real order pipeline (Inquiry → Quoted → Booked → In Progress → Delivered, per client/service/value) — the operational detail behind the profile's aggregate Performance numbers.
- **Analytics**: conversion by service type, repeat-customer rate, average deal size, response-time trend. Must not reuse another role's content.

---

## 6. Right panel — full engineering spec

Currently: identical, static, vendor-styled content on every page across every role. Replace entirely.

### 6.1 What we're building
- **Needs You** — single ranked list, merging "Action Queue" and "Alerts." Every item has a deadline, staleness signal, or explicit priority behind it, and one CTA.
- **Activity** — plain unranked log, no CTA, collapsed below the fold.
- **Quick Actions is removed from this panel** and moves to the persistent top bar — flag as a separate small task if not already supported there.

### 6.2 One engine, not five
One backend service, `NeedsYouService`, computes ranked items for any user filtered by role and `user_id`. One frontend component, `<NeedsYouPanel />`, renders it from a per-role config object — role differences live in data, not code. The center-column Action Queue on every dashboard in Section 5 is a fuller, uncapped view over this same service, not a second implementation.

### 6.3 Deterministic, not AI-generated
Ranking is pure scoring, no LLM — consistent with the platform's existing rule that AI assists decisions but doesn't own them (see `hermes-architecture-frozen-v1.md` §2 in `hermes/`). AI-generated explanations of ranking are a separate, later, clearly-labeled enhancement (6.10) if wanted at all.

### 6.4 Data model

`needs_you_item` — computed live at request time, not stored:

```json
{
  "id": "string (composite: source_table + source_id + rule_id)",
  "role": "consultant | bench_sales_recruiter | recruiter | employer | service_provider | admin",
  "type": "action | alert",
  "title": "string, plain language, max 60 chars",
  "subtitle": "string, optional",
  "cta_label": "string",
  "cta_action": "string, deep link or action key",
  "urgency_score": "float, 0-100",
  "source_table": "string",
  "source_id": "string",
  "created_at": "timestamp",
  "dismissible": "boolean",
  "dismissed_at": "timestamp | null"
}
```

`panel_dismissal` (new table):

```sql
CREATE TABLE panel_dismissal (
  user_id UUID NOT NULL,
  item_id TEXT NOT NULL,
  dismissed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, item_id)
);
```

No new table for Activity — reads existing audit/event tables.

### 6.5 Urgency scoring

```
urgency_score = deadline_weight + staleness_weight + explicit_priority_weight
```
- **deadline_weight** (0–50) — scales as a real deadline approaches; 0 if none.
- **staleness_weight** (0–30) — reuses the existing NRM decay function; don't rebuild it.
- **explicit_priority_weight** (0–20) — flat bump for explicitly flagged items.

Sort descending, **cap at 7**, "View all (N)" link to the fuller Action Queue view. Items auto-drop off when their condition resolves, computed live.

### 6.6 API contract

```
GET /api/dashboard/needs-you
GET /api/dashboard/needs-you/all
GET /api/dashboard/activity?limit=20&before=<timestamp>
POST /api/dashboard/needs-you/:item_id/dismiss
```

Real-time: reuse existing Centrifugo + Redis, publish `dashboard:refresh` to `user:{userId}`, client re-fetches on receipt.

### 6.7 Per-role item catalog

**Consultant**: interview within 48h → Prepare (Job Tracker) · unread recruiter message >4h → Reply (Messenger) · resume unedited >30 days → Update (Resume Builder) · new job match above threshold → View (Pulse/Hermes).

**Bench Sales Recruiter**: consultant ready, unsubmitted 24h+ → Submit (Submission Tracker) · no vendor reply >3 days → Follow up (NRM decay score) · duplicate submission risk → Review (anti-noise rule engine) · onboarding request pending → Review (Submission Tracker).

**Recruiter**: new submissions unreviewed → Review (shared `submissions` table) · role open >14 days no shortlist → View pipeline (Job Tracker/`requirements`) · interview needs scheduling → Schedule (Job Tracker) · employer feedback overdue >48h → Follow up (Placement).

**Employer**: shortlist ready unreviewed → Review (Job Tracker) · interview needs approval → Approve (Job Tracker) · role open, 0 candidates in 5 days → View (Job Tracker) · offer pending sign-off → Approve (Placement).

**Service Provider**: delivery due within 48h → View (Projects tab, 5.5) · inquiry unanswered >24h → Reply (Messenger) · payment received, delivery unconfirmed → Confirm (Marketplace).

**Admin** (forward-compatible catalog; no Admin dashboard reviewed or in scope otherwise): verification request pending → Review · content flagged → Moderate · support ticket past SLA → View.

### 6.8 Activity section
Last 20 events per role from existing audit/event tables, newest first, no CTA. If an item seems to need a button, it belongs in Needs You instead.

### 6.9 Enhancements
7-item cap with overflow · auto-resolve on state change (no cleanup job) · dismiss (alerts) vs. complete-only (actions) · reuse NRM decay for staleness · reuse Centrifugo/Redis for real-time · empty state reads "You're caught up" · no push notification tied 1:1 to every item — batch low-urgency into a daily digest, immediate push only above a high urgency threshold, per the platform's existing Hook Model principle.

### 6.10 Out of scope this phase
Per-user customizable ranking weights · AI-generated ranking explanations · cross-role Needs You for users with more than one role.

### 6.11 Acceptance criteria
`NeedsYouService` returns correctly ranked/capped/role-filtered results · items auto-resolve without a background job · dismissed alerts don't reappear · `<NeedsYouPanel />` is one component driven by config · real-time refresh uses existing Centrifugo, no new socket layer · empty state renders "You're caught up" · staleness scoring calls the existing NRM decay function · no LLM in the ranking path · Quick Actions relocated to the top bar.

---

## 7. Settings — reviewed live, currently one shared page for all roles

Confirmed live, logged in as Service Provider: the Settings page has one sidebar shared by every role — Communication, My Subscription, Payment & Billing, Block & Mute, Smart Privacy, Safety & Moderation, Privacy & Visibility, Platform Settings, Role Settings. Some of this is genuinely fine to share; two sections are seriously broken.

### 7.1 What's already correct as a shared page — don't change the architecture here

- **Platform Settings** (theme, language, date/time format, accessibility, 2FA, session timeout, data export/delete) — correctly universal. No role-specific version needed.
- **Payment & Billing** (payment methods, payout settings, billing history) — correctly universal in structure; it even self-aware notes "For users who receive earnings from the platform (service providers, referral commissions)." The only problem here is downstream of the My Subscription bug below (billing history shows charges for a plan that shouldn't exist for this role).
- **Block & Mute, Smart Privacy, Safety & Moderation, Privacy & Visibility** — not reviewed in full detail this pass, but conceptually these are trust/safety controls that reasonably apply to every role. Worth a quick confirmation pass, not a redesign.

### 7.2 What's broken

**"My Subscription" shows the wrong role's pricing tiers entirely.** Confirmed live: logged in as a **Service Provider**, this page displays "Starter / Pro / Elite" plans with features like "Up to 5 applications/month," "Basic Pulse matches," "Unlimited applications," "AI resume optimization," "Direct recruiter introductions" — this is Consultant job-seeker pricing, shown as the Service Provider's active plan ("Pro Plan, $19/mo, current"). This doesn't match the platform's own locked pricing model (Consultants are free at the core tier; Bench Sales Recruiters follow a separate SaaS ladder; Service Provider and Employer monetization are different again). Whatever a Service Provider's actual plan should be — likely a commission or Marketplace-listing-fee model, not an applications/Pulse-matches plan — it isn't this.

**"Role Settings" shows all five roles' settings panels to every user, not just their own.** Confirmed live: the page has a role tab switcher — Consultant / Bench Sales Recruiter / Recruiter / Employer / Service Provider — fully visible and clickable to a logged-in Service Provider account, defaulting to the **Consultant** tab (Rate Preferences, Visa/relocation settings, Pulse matching — none of which apply to a Service Provider). Clicking through to "Service Provider" does show correct, well-built content (Booking Mode, Instant Book, Max bookings per day, Cancellation policy, Service Visibility, calendar sync) — so the per-role content itself is fine. **The bug is scope, not content:** a user should only ever see their own role's settings panel here, with no tab switcher to other roles' settings at all.

### 7.3 Recommended settings architecture per role

- **Universal, unchanged**: Platform Settings, Payment & Billing (once My Subscription is fixed), and — pending the quick confirmation above — Block & Mute, Smart Privacy, Safety & Moderation, Privacy & Visibility.
- **Communication**: keep the shared page, but filter the notification-category list to what's relevant per role. Confirmed live: a Service Provider currently sees "Job Board Notifications" (new matching job posted, job saved alert, recruiter viewed profile) and "Job Tracker Notifications" (application submitted, interview scheduled, offer received) — pure Consultant job-search concepts that don't apply. "Marketplace Notifications" (new service inquiry, booking confirmed/cancelled, review received, payout processed) is the section that's actually relevant and correctly present. Each role should see only its relevant notification categories, via the same config-driven pattern as `ReportsPage`.
- **Role Settings**: remove the cross-role tab switcher entirely; render only the logged-in user's own role panel. The content already built per role (confirmed: Consultant's Rate/Visa/Pulse settings, Service Provider's Booking/Visibility settings) can stay as-is — this is a scoping fix, not a content rebuild.
- **My Subscription**: rebuild against each role's actual locked pricing model instead of showing Consultant plans to everyone. Needs a `subscription_plans` config per role (Section 1) and a `SubscriptionPlanCard` component (Section 2) that renders whichever plan structure matches the logged-in user's role.

### 7.4 What's needed from the founder before this can be built correctly

The Consultant, Bench Sales Recruiter pricing tiers are already locked (Consultant free core / ~$9–15 paid tier; Bench Sales Free → ~$15–19 → ~$39–49 → ~$79–99). **Recruiter, Employer, and Service Provider pricing models weren't part of the locked pricing decisions covered in prior work** — before `SubscriptionPlanCard` can be built for those three roles, their actual plan tiers and pricing need to be defined. Flag this as a product decision, not something to guess at in code.

---

## 8. Consolidated Cursor task list — every task, with a ready-to-paste prompt

Work top to bottom. Items 1–4 are the foundation; don't start the per-role dashboard builds (10, 11, 13) until they're done.

**1. Shared data model**
> "Create the following tables/schemas: `team_members` (links a Bench Sales Recruiter or Recruiter account to an Employer, with a role type), `panel_dismissal` (per Section 6.4), and a `subscription_plans` config table keyed by role. Confirm the existing `consultants`, `requirements`, `submissions`, and `partnerships` tables/models — if they don't already exist as single shared tables, consolidate them; every role-specific view in this codebase should read from one of these, not a per-role copy."

**2. `NeedsYouService` backend**
> "Build a `NeedsYouService` implementing the scoring formula and data model in Section 6.4–6.6 of this document: `urgency_score = deadline_weight + staleness_weight + explicit_priority_weight`, capped at 7 items per request, sorted descending. Staleness must call the existing NRM decay function — find it in the codebase first and reuse it, don't reimplement. Wire the four API endpoints in 6.6. Start with the Consultant and Bench Sales Recruiter item catalogs from 6.7 since those roles already exist."

**3. `<NeedsYouPanel />` frontend + retrofit**
> "Build `<NeedsYouPanel />` per Section 6.1 (Needs You + Activity sections, 7-item cap, 'You're caught up' empty state, dismiss-vs-complete-only behavior). Replace the current static right panel content on the Consultant and Bench Sales Recruiter dashboards with this component, consuming the `NeedsYouService` API from task 2. Move the existing Quick Actions buttons out of the panel into the top bar."

**4. Remaining shared components**
> "Extract `DashboardStatRow`, `ActivityTimeline`, and a config-driven `ReportsPage` from the existing Consultant and Bench Sales Recruiter dashboard code — find both implementations first, since they currently duplicate this logic slightly differently, and build one shared version each takes a role config rather than reusing either implementation as-is."

**5. Fix Bench Sales Recruiter's three-way consultant list mismatch**
> "The Bench Sales Recruiter dashboard's Overview, Partnerships, and Live Jobs tabs each currently show a different, non-overlapping list of consultants for the same logged-in user. Point all three at the shared `consultants`/Hotlist table from task 1. Report back on where each tab's data currently comes from before changing anything — this may be three separate mock sources, not a simple query fix."

**6. Fix Bench Sales Recruiter's Reports and Marketing Settings tabs**
> "Bench Sales Recruiter's Reports tab currently shows Consultant's content unchanged (a personal resume completeness score, 'your profile is not complete'). Rebuild it using the config-driven `ReportsPage` from task 4 with bench-wide metrics instead: per-consultant submission/interview/offer breakdown, not one profile's completeness. Do the same for Marketing Settings — it should control what each consultant/partner can see about the recruiter's operations, not show visa/rate/availability toggles that describe an individual job-seeker."

**7. Fix Bench Sales Recruiter's Review Conflict and Submit actions**
> "The 'Review Conflict' button in the Duplicate/Conflict Alerts section currently does nothing when clicked — wire it to a real conflict-resolution view. The 'Submit' button on a consultant row opens an edit form for an existing submission instead of creating a new one tied to the clicked job match, and that form has 'Recruiter Contact Name' filled while the 'Recruiter/Company' field it should derive from is empty — fix Submit to create a properly-linked new submission record."

**8. Fix Consultant's completeness score mismatch**
> "Consultant's profile completeness is shown as three different numbers on three tabs (Overview header, My Profiles, Reports) for the same profile. Compute one `SYSTEM_COMPUTED` score server-side and render it via a shared `ComputedMetricBadge` component in all three places — no independent per-tab calculation."

**9. Fix Settings: Role Settings scoping and My Subscription**
> "Two fixes to the Settings page: (1) 'Role Settings' currently shows a tab switcher for all five roles to every user — remove the switcher and render only the logged-in user's own role panel, using the existing per-role content already built (it's correct, just not scoped). (2) 'My Subscription' currently shows Consultant job-seeker pricing plans (Starter/Pro/Elite with job applications and Pulse matches) to every role regardless of their actual role. Build a `SubscriptionPlanCard` component driven by the `subscription_plans` config from task 1, and confirm with product/founder what Recruiter, Employer, and Service Provider's actual pricing tiers should be before wiring those three — Consultant and Bench Sales Recruiter's tiers are already defined and can be built now."

**10. Add role-type selector to Employer's Team invite flow**
> "Add a role field (Bench Sales Recruiter / Recruiter / Admin) to the Team invite flow on the Employer profile. On acceptance, create a `team_members` row. Confirm that a Bench Sales Recruiter or Recruiter account created this way shows the inviting Employer as its affiliated company on its own dashboard, the way the existing test account already does."

**11. Build Recruiter dashboard**
> "Build out the Recruiter dashboard's four existing tabs (Dashboard, Open Roles, Network, Analytics — currently placeholder) per Section 5.3 of this document. Use `NeedsYouService` and `<NeedsYouPanel />` from tasks 2–3 for the Action Queue and right panel from the start, not a new bespoke query. 'Incoming Submissions' on the Dashboard tab must read from the same `submissions` table Bench Sales Recruiter's Submit action writes to."

**12. Fix Employer's existing Open Positions data issues**
> "On the Employer profile's Open Positions tab, fix two confirmed issues on the existing job posting: the location field saved a full landmark address instead of city/state — replace with the shared `StructuredLocationInput` component from `core-profile-data-model-fixlist.md`. Also remove the two tags showing the literal placeholder text 'test.'"

**13. Build Employer dashboard**
> "Build out the Employer dashboard's Dashboard and Analytics tabs (currently placeholder) per Section 5.4, plus the new Hotlist rollup view described in Section 4. Wire Open Positions to the shared `requirements` table with per-posting Recruiter attribution. Use `NeedsYouService`/`<NeedsYouPanel />` for the Action Queue and right panel."

**14. Extend NeedsYouService to Recruiter and Employer**
> "Add the Recruiter and Employer item catalogs from Section 6.7 to `NeedsYouService`."

**15. Build Service Provider dashboard**
> "Build out the Service Provider dashboard's four tabs (Dashboard, Services, Projects, Analytics — currently placeholder) per Section 5.5. The Services tab should be the management/editing view for the same service-offerings data already shown publicly (but empty) on the profile's Services tab — one record, two views. Use `TaxonomyMultiSelect` for service categories from the start."

**16. Extend NeedsYouService to Service Provider**
> "Add the Service Provider item catalog from Section 6.7 to `NeedsYouService`."

**17. Filter Communication settings notification categories per role**
> "On the Communication settings page, filter the notification-category sections (Job Board, Job Tracker, Marketplace, Trust & Network, etc.) to only show categories relevant to the logged-in user's role, using the same config-driven pattern as `ReportsPage`. A Service Provider should not see Job Board/Job Tracker notification toggles; a Consultant should not see Marketplace booking notifications."

**18. Consultant's remaining minor fixes**
> "Fix the 'Selected Consultant' placeholder-looking text in the Resume Credits usage history table (confirm whether it's a default-value leak). Consolidate the duplicate Marketing Settings toggles that control the same submission-approval decision worded two different ways in two sections of the same page."

**19. Confirm the four untested Settings sections**
> "Review Block & Mute, Smart Privacy, Safety & Moderation, and Privacy & Visibility for all five roles — confirm whether any role-specific content is missing or incorrectly shared, following the same pattern used to review Communication and Role Settings in this document."

**20. Founder decisions needed — not engineering tasks**
- Does Resume Credits fit the locked pricing model, or predate it?
- Are the dashboard's Reply/Message buttons wired to the real-time Messenger module?
- What are Recruiter, Employer, and Service Provider's actual subscription pricing tiers (needed to complete task 9)?

---

## 9. Status

All five roles reviewed live: dashboards (including button/flow testing), right panel, and now Settings. Consultant and Bench Sales Recruiter dashboards are built and reviewed in full. Recruiter, Employer, and Service Provider dashboards are specified from their confirmed-live placeholder tab shells and existing profile pages. The right panel has a complete engineering spec ready to build directly. Settings review found two clearly broken areas (My Subscription showing the wrong role's pricing, Role Settings showing every role's panel to every user) and confirmed several areas are already correctly built as shared pages. This document is ready to hand to the development team, with a Cursor prompt for every task in Section 8.
