# Engineering Memory

Date: 2026-10-13

Status: green

---

# Executive Summary

GitHub push event processed for jobfynder-admin/jobFynder-FE-vite on branch dev-duplicate.

---

# Repositories

- jobfynder-admin/jobFynder-FE-vite

---

# Completed Today

- Source: GitHub webhook
- Repository: jobfynder-admin/jobFynder-FE-vite
- Branch: dev-duplicate
- Head SHA: bd433c6
- Commit count: 9
- Triggered by: jobfynder-admin
- Commits:
- 1fd00ca Merge pull request #19 from jobfynder-admin/dev-duplicate — JobFynder
- 5baae80 Merge pull request #25 from jobfynder-admin/dev-duplicate — JobFynder
- 102bac5 refactor(onboarding): simplify onboarding role selection and update signup flow — Nishant Arora
- 2ca79eb feat(profile): implement LinkedIn profile autofill and completion widget — Nishant Arora
- 703b140 feat(profile): add EmployerVendorNetworkSection and enhance profile components — Nishant Arora
- 23610ce refactor(profile): remove react-select and enhance profile modals — Nishant Arora
- 2b47bd5 feat(profile): add placeholders for rate input fields in EditRatesEngagementModal — Nishant Arora
- 5234519 feat(profile): enhance profile completion features and UI components — Nishant Arora
- bd433c6 Merge pull request #26 from jobfynder-admin/dev — JobFynder
- Changed files:
- added: .env.example
- added: AGENTS.md
- added: CLAUDE.md
- added: docs/messenger/UI-INTEGRATION-v1.md
- added: src/components/components/private/profile/components/AnalyzeJd.tsx
- added: src/components/components/private/profile/components/CompanySearchSelect.tsx
- added: src/components/components/private/profile/components/EmployerVendorNetworkSection.tsx
- added: src/components/components/private/profile/components/LinkedInProfileAutofill.tsx
- added: src/components/components/private/profile/components/ProfileCompletionAutofill.tsx
- added: src/components/components/private/profile/components/ProfileCompletionWidget.tsx
- added: src/components/components/private/profile/components/ServiceProviderCaseStudyModal.tsx
- added: src/components/components/private/profile/components/ServiceProviderContactBookingTab.tsx
- added: src/components/components/private/profile/helpers/recruiterOverviewMetrics.ts
- added: src/components/components/private/profile/modals/AddBenchHotlistConsultantModal.tsx
- added: src/components/ui/formFieldStyles.ts
- added: src/components/ui/list-wysiwyg-field.tsx
- added: src/components/ui/simple-multi-select.tsx
- added: src/features/messenger/MessengerPage.test.tsx
- added: src/features/messenger/MessengerPage.tsx
- added: src/features/messenger/MessengerRealtimeClient.test.ts
- added: src/features/messenger/MessengerRealtimeClient.ts
- added: src/features/messenger/MessengerRealtimeProvider.tsx
- added: src/features/messenger/messengerApi.test.ts
- added: src/features/messenger/messengerApi.ts
- added: src/features/messenger/realtimeEvents.ts
- added: src/pages/private/HermesDraftsReview.tsx
- added: src/services/bench-submissions.ts
- added: src/services/hermes-drafts.ts
- added: src/services/resume-intelligence.ts
- added: src/services/resume.ts
- added: src/store/useOrganisationStore.ts
- added: src/test/setup.ts
- added: src/utils/applyLinkedInProfile.ts
- added: src/utils/profileCompletion.ts
- added: src/utils/resume-builder-bench-sales-review.ts
- added: src/utils/resume-builder-document.ts
- added: vitest.config.ts
- modified: docs/profile-data-model-backend-changes.md
- modified: package-lock.json
- modified: package.json
- modified: src/api/apiClient.ts
- modified: src/components/ChatwootSupportWidget.tsx
- modified: src/components/ImportProfileGate.tsx
- modified: src/components/ProtectedRoute.tsx
- modified: src/components/components/auth/onboarding/OnboardingRoleForm.tsx
- modified: src/components/components/auth/onboarding/checklist.tsx
- modified: src/components/components/private/profile/ProfileContent.tsx
- modified: src/components/components/private/profile/components/BackgroundIdentityVerification.tsx
- modified: src/components/components/private/profile/components/BenchSalesEditProfileModal.tsx
- modified: src/components/components/private/profile/components/ConsultantEditProfileModal.tsx
- modified: src/components/components/private/profile/components/DocumentsTab.tsx
- modified: src/components/components/private/profile/components/EducationSection.tsx
- modified: src/components/components/private/profile/components/EmployerTechnologySpecializationsSection.tsx
- modified: src/components/components/private/profile/components/InteractionTimeline.tsx
- modified: src/components/components/private/profile/components/LookingFor.tsx
- modified: src/components/components/private/profile/components/PrimarySkills.tsx
- modified: src/components/components/private/profile/components/ProfileCompletionWidget.tsx
- modified: src/components/components/private/profile/components/ProfileHeader.tsx
- modified: src/components/components/private/profile/components/ProfileStatusBar.tsx
- modified: src/components/components/private/profile/components/ProfileTabPanel.tsx
- modified: src/components/components/private/profile/components/RecruiterActiveRequirementsCard.tsx
- modified: src/components/components/private/profile/components/RecruiterConversionMetricsCard.tsx
- modified: src/components/components/private/profile/components/RecruiterEditProfileModal.tsx
- modified: src/components/components/private/profile/components/RecruiterFeaturedPlacementsCard.tsx
- modified: src/components/components/private/profile/components/RecruiterIndustryBenchmarkCard.tsx
- modified: src/components/components/private/profile/components/RecruiterOverviewMetricsStrip.tsx
- modified: src/components/components/private/profile/components/RecruiterPeerReviewsCard.tsx
- modified: src/components/components/private/profile/components/RecruiterPipelineYtdCard.tsx
- modified: src/components/components/private/profile/components/RecruiterPlacementTypeBreakdownCard.tsx
- modified: src/components/components/private/profile/components/RecruiterSubmissionPreferencesCard.tsx
- modified: src/components/components/private/profile/components/RecruiterTrackRecordCard.tsx
- modified: src/components/components/private/profile/components/RecruiterTrustVerificationCard.tsx
- modified: src/components/components/private/profile/components/SecondarySkills.tsx
- modified: src/components/components/private/profile/components/ServiceProviderEditCompanyProfileModal.tsx
- modified: src/components/components/private/profile/components/ServiceProviderInviteTeamMemberModal.tsx
- modified: src/components/components/private/profile/components/ServiceProviderSuccessStoriesCard.tsx
- modified: src/components/components/private/profile/components/ServiceProviderTeamTab.tsx
- modified: src/components/components/private/profile/components/SkillMatrix.tsx
- modified: src/components/components/private/profile/components/SubmissionSnapshot.tsx
- modified: src/components/components/private/profile/components/ToolsAndFrameworks.tsx
- modified: src/components/components/private/profile/components/TrustConversion.tsx
- modified: src/components/components/private/profile/components/WorkAuthorization.tsx
- modified: src/components/components/private/profile/components/bench/BenchCoverageRates.tsx
- modified: src/components/components/private/profile/components/bench/BenchHotlistFilterBar.tsx
- modified: src/components/components/private/profile/components/bench/BenchHotlistPanel.tsx
- modified: src/components/components/private/profile/components/bench/BenchOperationalDetails.tsx
- modified: src/components/components/private/profile/components/bench/BenchPrimaryTechnologyStacks.tsx
- modified: src/components/components/private/profile/components/bench/BenchSpecializationAreas.tsx
- modified: src/components/components/private/profile/components/bench/BenchTopPlacementTechnologiesCard.tsx
- modified: src/components/components/private/profile/components/serviceProviderOverviewHelpers.ts
- modified: src/components/components/private/profile/helpers/activeRequirementsHelpers.ts
- modified: src/components/components/private/profile/helpers/certificationsHelpers.ts
- modified: src/components/components/private/profile/helpers/clientRequirementContextHelpers.ts
- modified: src/components/components/private/profile/helpers/educationHelpers.ts
- modified: src/components/components/private/profile/helpers/employerHiringPreferencesHelpers.ts
- modified: src/components/components/private/profile/helpers/lookingForHelpers.ts
- modified: src/components/components/private/profile/helpers/operationalDetailsHelpers.ts
- modified: src/components/components/private/profile/helpers/primarySkillsHelpers.ts
- modified: src/components/components/private/profile/helpers/primaryTechnologyStacksHelpers.ts
- modified: src/components/components/private/profile/helpers/profileHeaderHelpers.ts
- modified: src/components/components/private/profile/helpers/skillMatrixHelpers.ts
- modified: src/components/components/private/profile/helpers/submissionSnapshotHelpers.ts
- modified: src/components/components/private/profile/helpers/workAuthorizationDetailsHelpers.ts
- modified: src/components/components/private/profile/modals/AddBenchHotlistConsultantModal.tsx
- modified: src/components/components/private/profile/modals/AddCertificationModal.tsx
- modified: src/components/components/private/profile/modals/AddSkillModal.tsx
- modified: src/components/components/private/profile/modals/EditAboutModal.tsx
- modified: src/components/components/private/profile/modals/EditActiveRequirementModal.tsx
- modified: src/components/components/private/profile/modals/EditClientRequirementContextModal.tsx
- modified: src/components/components/private/profile/modals/EditCoverageRatesModal.tsx
- modified: src/components/components/private/profile/modals/EditEmployerTechnologySpecializationsModal.tsx
- modified: src/components/components/private/profile/modals/EditLocationPreferencesModal.tsx
- modified: src/components/components/private/profile/modals/EditLookingForModal.tsx
- modified: src/components/components/private/profile/modals/EditOperationalDetailsModal.tsx
- modified: src/components/components/private/profile/modals/EditPrimaryTechnologyStacksModal.tsx
- modified: src/components/components/private/profile/modals/EditProfessionalSummaryModal.tsx
- modified: src/components/components/private/profile/modals/EditRatesEngagementModal.tsx
- modified: src/components/components/private/profile/modals/EditSubmissionSnapshotModal.tsx
- modified: src/components/components/private/profile/modals/EditWorkAuthorizationModal.tsx
- modified: src/components/components/private/profile/modals/EducationModal.tsx
- modified: src/components/components/private/profile/modals/RecruiterSubmitConsultantModal.tsx
- modified: src/components/components/private/profile/modals/WorkExperienceModal.tsx
- modified: src/components/components/private/profile/tabs/benchSalesTabItems.tsx
- modified: src/components/components/private/profile/tabs/consultantTabItems.tsx
- modified: src/components/components/private/profile/tabs/employerTabItems.tsx
- modified: src/components/components/private/profile/tabs/recruiterTabItems.tsx
- modified: src/components/components/private/profile/tabs/serviceProviderTabItems.tsx
- modified: src/components/components/private/resume-builder/ConsultantResumeBuilder.tsx
- modified: src/components/components/private/resume-builder/ResumeATSCheckPanel.tsx
- modified: src/components/components/private/resume-builder/ResumeBuilderPreviewPane.tsx
- modified: src/components/components/private/resume-builder/ResumeGenerateWithAi.tsx
- modified: src/components/components/private/resume-builder/ResumeJobMatchPanel.tsx
- modified: src/components/components/private/resume-builder/bench-sales/BenchSalesCreateBaseResumeAlignRole.tsx
- modified: src/components/components/private/resume-builder/bench-sales/BenchSalesCreateBaseResumeModal.tsx
- modified: src/components/components/private/resume-builder/bench-sales/BenchSalesTailorResumeToJobModal.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantCreateResumeVariantModal.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantFeedbackView.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantMyResumesView.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantPerformanceView.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantResumeBuilderNav.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantResumeVariantsView.tsx
- modified: src/components/components/private/resume-builder/consultant/ConsultantTailorToJobView.tsx
- modified: src/components/components/private/resume-builder/consultant/performance/PerformanceVariantCard.tsx
- modified: src/components/components/private/resume-builder/consultant/performance/PerformanceWeeklyTrendChart.tsx
- modified: src/components/components/private/resume-builder/consultant/tailor-to-job/ConsultantTailorToJobSession.tsx
- modified: src/components/components/private/resume-builder/editors/ExperienceSectionEditor.tsx
- modified: src/components/components/private/resume-builder/editors/SkillsSectionEditor.tsx
- modified: src/components/components/private/resume-builder/editors/SummarySectionEditor.tsx
- modified: src/components/components/private/userInfoDropdown.tsx
- modified: src/components/components/public/job-board/create-job-modal-tabs/PreScreeningTab.tsx
- modified: src/components/ui/TaxonomyMultiSelect.tsx
- modified: src/components/ui/dialog.tsx
- modified: src/components/ui/input.tsx
- modified: src/components/ui/places-autocomplete.tsx
- modified: src/components/ui/select.tsx
- modified: src/components/ui/simple-multi-select.tsx
- modified: src/components/ui/simple-select.tsx
- modified: src/components/ui/textarea.tsx
- modified: src/components/ui/time-range-picker.tsx
- modified: src/components/ui/timezone-select.tsx
- modified: src/constants/auth/role.ts
- modified: src/constants/navigation.ts
- modified: src/hooks/useApiMutation.ts
- modified: src/hooks/useApiQuery.ts
- modified: src/hooks/useProfileMutations.ts
- modified: src/pages/auth/RoleUpdate.tsx
- modified: src/pages/auth/callback.tsx
- modified: src/pages/auth/onboarding.tsx
- modified: src/pages/private/Profile.tsx
- modified: src/pages/private/ResumeBuilder.tsx
- modified: src/pages/private/layout.tsx
- modified: src/root.tsx
- modified: src/routes.ts
- modified: src/routes/index.tsx
- modified: src/seo/route-registry.ts
- modified: src/services/authService.ts
- modified: src/services/profileApi.ts
- modified: src/store/useAuthStore.ts
- modified: src/types/auth.ts
- modified: src/types/linkedin-brightdata.ts
- modified: src/types/onboarding.ts
- modified: src/utils/applyLinkedInProfile.ts
- modified: src/utils/auth.ts
- modified: src/utils/completeAuthSession.ts
- modified: src/utils/importProfileGate.ts
- modified: src/utils/mapBrightDataLinkedInToResume.ts
- modified: src/utils/onboardingOAuthContext.ts
- modified: src/utils/onboardingTransform.ts
- modified: src/utils/profileCompletion.ts
- modified: src/utils/transformApiToFormData.ts
- modified: vite.config.ts
- removed: src/components/components/private/profile/components/WorkAuthorizationDetails.tsx

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
