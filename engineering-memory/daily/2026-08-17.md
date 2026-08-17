# Engineering Memory

Date: 2026-08-17

Status: green

---

# Executive Summary

GitHub push event processed for jobfynder-admin/jobFynder-FE-vite on branch feature/chatwoot-verified-identity-migration.

---

# Repositories

- jobfynder-admin/jobFynder-FE-vite

---

# Completed Today

- Source: GitHub webhook
- Repository: jobfynder-admin/jobFynder-FE-vite
- Branch: feature/chatwoot-verified-identity-migration
- Head SHA: 82e3277
- Commit count: 42
- Triggered by: jobfynder-admin
- Commits:
- 51c6b09 Load archived Messenger conversations — Pavan
- 9690d2f Add ImportProfileOnboarding component for unified profile import process — Nishant Arora
- 2ae174f Add backend specification for LinkedIn profile import during onboarding — Nishant Arora
- 462352b Merge branch 'dev' of https://github.com/jobfynder-admin/jobFynder-FE-vite into dev — Pavan
- 0a6a661 Improve archived conversation row layout — Pavan
- 8f97c7c Polish Messenger sidebar conversation rows — Pavan
- 375c68e Add Messenger delete chat UI — Pavan
- a68ddd7 Limit initial Direct Messages display — Pavan
- 4aa947b Replace Marketplace header link with Messenger — Pavan
- c0782c5 fix(messenger): show participant email in search — Pavan
- 35346b3 fix(messenger): normalize participant identity separator — Pavan
- 5c922d9 fix(messenger): archive conversations without sidebar reload — Pavan
- 99a64a2 feat(messenger): enable message edit and delete actions — Pavan
- 4b30bed fix(messenger): resolve replied message references — Pavan
- ae7fb51 fix(messenger): link replies to source messages — Pavan
- 423f962 fix(messenger): hide deleted messages from timeline — Pavan
- f7ae1ed fix(messenger): refresh reply references after message changes — Pavan
- 54aec11 debug(messenger): log realtime subscription lifecycle — Pavan
- 4011deb debug(messenger): trace typing realtime lifecycle — Pavan
- 5ea9372 debug(messenger): trace openConversation identity — Pavan
- 88da56f debug(messenger): trace typing identity handling — Pavan
- 823cb82 fix(messenger): keep typing indicator visible — Pavan
- 24e4a2d chore(messenger): remove realtime debug instrumentation — Pavan
- f9630c9 fix(messenger): derive capabilities from authenticated role — Pavan
- a1075a4 fix(messenger): keep workspace mounted when toggling sidebar — Pavan
- f194687 feat(messenger): integrate global navigation and toolbar search — Pavan
- 6e22e4c feat(network): wire My Network tab to real relationship API — Pavan
- 73ea67c Merge feature/network-module-dev: wire My Network tab to real relationship API — Pavan
- 595d607 feat(network): full spec redesign — My Network, Person Card, Find People, job-context panel, settings — Pavan
- 80f2319 Merge branch 'dev' of https://github.com/jobfynder-admin/jobFynder-FE-vite into dev — Pavan
- 3ff4f90 fix(messenger): consolidate search into toolbar — Pavan
- dc07c78 Fix authenticated Chatwoot support routing — JobFynder
- 71196ba Wait for Chatwoot frame before applying user identity — JobFynder
- b63b755 Switch Chatwoot inbox safely after login — JobFynder
- 0d866e5 Reset Chatwoot identity before switching inboxes — JobFynder
- 34161af Do not reload Jobfynder while logging out — JobFynder
- 96dd62d Keep Chatwoot reset from interrupting logout — JobFynder
- 768328f Prevent Chatwoot from blocking Jobfynder logout — JobFynder
- 787e2ca Navigate cleanly to login after logout — JobFynder
- fc12a54 Migrate legacy Chatwoot session after login — JobFynder
- 6cf1410 Run legacy Chatwoot migration once per browser — JobFynder
- 82e3277 Finalize verified Chatwoot identity migration (#12) — JobFynder
- Changed files:
- added: .github/workflows/chatwoot-integration-check.yml
- added: docs/onboarding-linkedin-import-backend-spec.md
- added: src/components/components/auth/onboarding/ImportProfileOnboarding.tsx
- added: src/components/components/auth/onboarding/LinkedInProfileImportDialog.tsx
- added: src/components/components/private/profile/helpers/benchOverviewHelpers.ts
- added: src/components/components/private/profile/helpers/employerOverviewHelpers.ts
- added: src/components/components/private/profile/helpers/recruiterOverviewHelpers.ts
- added: src/components/components/private/profile/helpers/serviceProviderOverviewEnrichment.ts
- added: src/components/components/private/settings/components/privacy-visibility/NetworkVisibilitySection.tsx
- added: src/components/components/public/job-details/JobContextNetworkPanel.tsx
- added: src/components/components/public/network/tabs/connections/PersonCardSheet.tsx
- added: src/features/network/networkApi.ts
- added: src/types/linkedin-brightdata.ts
- added: src/utils/completeAuthSession.ts
- added: src/utils/mapBrightDataLinkedInToResume.ts
- added: src/utils/onboardingOAuthContext.ts
- modified: src/api/apiClient.ts
- modified: src/components/ChatwootSupportWidget.tsx
- modified: src/components/components/auth/onboarding/ImportProfileOnboarding.tsx
- modified: src/components/components/auth/onboarding/bench-sales/bench-sales.tsx
- modified: src/components/components/auth/onboarding/bench-sales/index.tsx
- modified: src/components/components/auth/onboarding/checklist.tsx
- modified: src/components/components/auth/onboarding/consultant/consultant-form.tsx
- modified: src/components/components/auth/onboarding/consultant/index.tsx
- modified: src/components/components/auth/onboarding/employer/employer.tsx
- modified: src/components/components/auth/onboarding/employer/index.tsx
- modified: src/components/components/auth/onboarding/index.tsx
- modified: src/components/components/auth/onboarding/recruiter/index.tsx
- modified: src/components/components/auth/onboarding/recruiter/recruiter.tsx
- modified: src/components/components/auth/onboarding/service-provider/index.tsx
- modified: src/components/components/auth/onboarding/service-provider/service-provider.tsx
- modified: src/components/components/private/profile/components/BackgroundIdentityVerification.tsx
- modified: src/components/components/private/profile/components/EmployerCompanyDetailsSection.tsx
- modified: src/components/components/private/profile/components/EmployerCompanyStatsSection.tsx
- modified: src/components/components/private/profile/components/EmployerHiringMetricsStrip.tsx
- modified: src/components/components/private/profile/components/EmployerVerificationCredentialsSection.tsx
- modified: src/components/components/private/profile/components/InteractionTimeline.tsx
- modified: src/components/components/private/profile/components/InterviewAvailability.tsx
- modified: src/components/components/private/profile/components/ProfileStatusBar.tsx
- modified: src/components/components/private/profile/components/RecruiterClientRequirementContextCard.tsx
- modified: src/components/components/private/profile/components/RecruiterConversionMetricsCard.tsx
- modified: src/components/components/private/profile/components/RecruiterIndustryBenchmarkCard.tsx
- modified: src/components/components/private/profile/components/RecruiterOverviewMetricsStrip.tsx
- modified: src/components/components/private/profile/components/RecruiterPipelineYtdCard.tsx
- modified: src/components/components/private/profile/components/RecruiterPlacementTypeBreakdownCard.tsx
- modified: src/components/components/private/profile/components/RecruiterTrackRecordCard.tsx
- modified: src/components/components/private/profile/components/ServiceProviderCompanyDetailsCard.tsx
- modified: src/components/components/private/profile/components/ServiceProviderTeamTab.tsx
- modified: src/components/components/private/profile/components/ServiceProviderVerificationCard.tsx
- modified: src/components/components/private/profile/components/SubmissionSnapshot.tsx
- modified: src/components/components/private/profile/components/TopEndorsements.tsx
- modified: src/components/components/private/profile/components/TrustConversion.tsx
- modified: src/components/components/private/profile/components/bench/BenchPlacementMetricsCard.tsx
- modified: src/components/components/private/profile/components/bench/BenchProfileStrength.tsx
- modified: src/components/components/private/profile/components/bench/BenchVerificationStatusCard.tsx
- modified: src/components/components/private/profile/components/serviceProviderOverviewHelpers.ts
- modified: src/components/components/private/profile/helpers/benchOverviewForProfessionalSummary.ts
- modified: src/components/components/private/profile/helpers/clientRequirementContextHelpers.ts
- modified: src/components/components/private/profile/helpers/locationPreferencesHelpers.ts
- modified: src/components/components/private/profile/helpers/primarySkillsHelpers.ts
- modified: src/components/components/private/profile/helpers/professionalSummaryHelpers.ts
- modified: src/components/components/private/profile/helpers/profileHeaderHelpers.ts
- modified: src/components/components/private/profile/helpers/skillMatrixHelpers.ts
- modified: src/components/components/private/profile/helpers/submissionSnapshotHelpers.ts
- modified: src/components/components/private/profile/helpers/workAuthorizationDetailsHelpers.ts
- modified: src/components/components/private/profile/tabs/benchSalesTabItems.tsx
- modified: src/components/components/private/profile/tabs/employerTabItems.tsx
- modified: src/components/components/private/profile/tabs/recruiterTabItems.tsx
- modified: src/components/components/private/profile/tabs/serviceProviderTabItems.tsx
- modified: src/components/components/private/settings/sections/PrivacyVisibility.tsx
- modified: src/components/components/public/job-details/index.tsx
- modified: src/components/components/public/network/tabs/ConnectionsTab.tsx
- modified: src/components/components/public/network/tabs/FindPeopleTab.tsx
- modified: src/components/components/public/network/tabs/connections/ConnectionCard.tsx
- modified: src/components/components/public/network/tabs/find-people/PersonCard.tsx
- modified: src/components/messenger/ChatView.jsx
- modified: src/components/messenger/ConversationRow.jsx
- modified: src/components/messenger/ConversationSidebar.jsx
- modified: src/components/messenger/NavLeaf.jsx
- modified: src/components/messenger/NewConversationDialog.jsx
- modified: src/components/messenger/messages/MessageActions.jsx
- modified: src/components/messenger/messages/MessageItem.jsx
- modified: src/components/messenger/messages/MessageList.jsx
- modified: src/components/messenger/shell/ConversationListRegion.jsx
- modified: src/components/messenger/shell/ConversationWorkspaceRegion.jsx
- modified: src/components/messenger/shell/MessengerDesktopLayout.jsx
- modified: src/components/messenger/shell/MessengerHeader.jsx
- modified: src/components/messenger/shell/MessengerShell.jsx
- modified: src/constants/header/common-pages.ts
- modified: src/features/messenger/MessengerPage.tsx
- modified: src/features/messenger/MessengerRealtimeClient.ts
- modified: src/features/messenger/MessengerRealtimeProvider.tsx
- modified: src/features/messenger/messengerApi.ts
- modified: src/features/network/networkApi.ts
- modified: src/hooks/useThread.js
- modified: src/lib/contextCapabilities.js
- modified: src/lib/messengerApi.ts
- modified: src/lib/messengerCapabilities.js
- modified: src/lib/messengerFilters.js
- modified: src/lib/messengerRoles.js
- modified: src/lib/recruiterContent.js
- modified: src/pages/auth/RoleUpdate.tsx
- modified: src/pages/auth/callback.tsx
- modified: src/pages/auth/login.tsx
- modified: src/routes.ts
- modified: src/routes/index.tsx
- modified: src/services/authService.ts
- modified: src/services/chatwoot-support.ts
- modified: src/store/useAuthStore.ts
- modified: src/store/useOnboardingStore.ts
- modified: src/types/auth.ts

---

# Architecture Decisions

- ADR-EMI-002 - Engineering Memory accepts GitHub webhook input (accepted)
  - Hermes can generate engineering memory from GitHub webhook repository, branch, commit, author, and changed-file context.

---

# Incidents

- None

---

# Lessons Learned

- Repo-aware engineering memory is more useful than generic repository scanning.
- Webhook payloads provide reliable commit, author, branch, and changed-file context.

---

# Open Items

- Improve event archive to store full webhook payload.
- Add failure alerting for memory automation.
- Add deduplication guard for repeated memory commits.

---

# Tomorrow

Use repo-aware engineering memory as the default source for GitHub-triggered automation.

---

Generated by Hermes Engineering Memory Engine
