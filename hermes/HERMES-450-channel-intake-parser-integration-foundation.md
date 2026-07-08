# HERMES-450 — Channel Intake & Parser Integration Foundation

Status: Open  
Code Branch: feature/hermes-450-channel-intake  
Baseline: HERMES-400 closed foundation  
Baseline Code Commit: 1f21f8a  
Baseline Tag: hermes-400-foundation-v1  

## Purpose

HERMES-450 creates the Hermes ingress layer before Submission Intelligence.

It allows Hermes to receive real-world messages, files, identity intake, and onboarding inputs from external channels, normalize them into one internal intake contract, route them to Hermes Understanding, normalize results through HERMES-400 taxonomy intelligence, and return or store structured results safely.

## Final Scope

HERMES-450 includes:

1. Generic channel intake schema
2. Generic REST intake endpoint
3. Telegram intake endpoint
4. Email intake contract
5. WhatsApp adapter contract
6. Slack adapter contract
7. Microsoft Teams adapter contract
8. Google Chat adapter contract
9. Browser extension intake contract
10. Web upload intake contract
11. File attachment intake foundation
12. Text message intake foundation
13. Intake type detection
14. Parser routing contract
15. Taxonomy normalization handoff
16. Intake status lifecycle
17. Idempotency and duplicate protection
18. Intake audit logs
19. Draft object pattern
20. Onboarding and identity intake foundation
21. Channel health endpoint
22. Supported channels endpoint


## Supported Channel Bridges

Core implementation targets:

- Generic REST API
- Telegram webhook
- Email intake contract

Prepared adapter contracts:

- WhatsApp
- Slack
- Microsoft Teams
- Google Chat
- Browser extension
- Web application upload

## Canonical Intake Flow

```text
External Channel
        ↓
Channel Adapter
        ↓
Canonical Intake Schema
        ↓
Attachment Storage Contract
        ↓
Intake Type Detection
        ↓
Parser Routing
        ↓
Hermes Understanding
        ↓
HERMES-400 Taxonomy Normalization
        ↓
Draft-Ready Structured Output
        ↓
Intake Log + Response

```

## Canonical Intake Schema

```json
{
  "channel": "telegram",
  "source_message_id": "12345",
  "sender_id": "telegram_user_id",
  "sender_name": "Pavan",
  "workspace_id": null,
  "conversation_id": null,
  "content_type": "text",
  "text": "Java developer required with AWS and Kubernetes",
  "attachments": [],
  "received_at": "2026-07-08T00:00:00Z",
  "raw_payload_ref": null,
  "metadata": {}
}
```

## Intake Types

Hermes should detect and route:

- resume
- job_description
- hotlist
- recruiter_profile
- bench_sales_profile
- consultant_profile
- vendor_list
- plain_message
- unknown

## Intake Status Lifecycle

Every intake should move through safe lifecycle states:

```text
received
validated
stored
parsing
parsed
normalized
draft_created
needs_review
failed
duplicate
```

## Draft Object Pattern

HERMES-450 must not directly create final business records.

It should create draft-ready outputs:

```text
Resume → draft_consultant_profile
Job Description → draft_job_requirement
LinkedIn Profile → draft_recruiter_or_bench_sales_profile
Hotlist → draft_hotlist
Vendor List → draft_vendor_list
Plain Message → draft_channel_note
```

HERMES-500 will later convert reviewed drafts into submission workflows.

## Onboarding and Identity Intake

HERMES-450 includes onboarding foundation because onboarding is another form of intake.

Supported onboarding channels:

- Web app
- Telegram
- WhatsApp
- Email invite
- Slack
- Microsoft Teams
- Google Chat

Recommended onboarding flow:

```text
User selects role
        ↓
User authenticates
        ↓
LinkedIn OAuth verifies identity
        ↓
User confirms public LinkedIn profile URL
        ↓
Public profile data is parsed through compliant public-data provider
        ↓
Hermes normalizes profile data
        ↓
Draft Jobfynder profile is created
        ↓
User reviews and edits
        ↓
User publishes profile
```

Important rule:

LinkedIn OAuth is for identity verification and sign-in only. It must not be used for scraping LinkedIn pages.

Public LinkedIn profile parsing must use user-confirmed public profile URL only and must create a draft profile for user review before publishing.


## Role-Specific Onboarding

Bench Sales onboarding should prepare:

- name
- headline
- company
- location
- staffing specialization
- years of experience
- technologies handled
- consultants marketed per month
- work authorization focus
- preferred submission regions
- vendor/recruiter relationship preference
- hotlist visibility setting

Recruiter onboarding should prepare:

- name
- headline
- company
- location
- recruiting specialization
- client/domain focus
- hiring domains
- accepts vendor submissions
- preferred candidate format
- rate transparency preference
- submission rules
- preferred communication channels


## Recommended Endpoints

```text
POST /channels/intake
POST /channels/telegram/webhook
GET  /channels/health
GET  /channels/supported
POST /onboarding/session
GET  /onboarding/session/{session_id}
POST /onboarding/role
POST /onboarding/profile/draft
POST /onboarding/profile/publish
```

## Output Contract

```json
{
  "channel": "telegram",
  "intake_status": "parsed",
  "document_kind": "job_description",
  "understanding_result": {},
  "taxonomy_signals": {},
  "normalized_skills": [],
  "normalized_job_titles": [],
  "draft_object_type": "draft_job_requirement",
  "requires_review": false,
  "confidence": 0.86,
  "errors": []
}
```

## Idempotency Rule

Every channel intake must have a duplicate protection key:

```text
channel + source_message_id
```

If a channel retries the same webhook, Hermes must not create duplicate intake logs, parser runs, or draft objects.


## Attachment Rule

Files must follow this contract:

```text
Receive file metadata
        ↓
Validate file type and size
        ↓
Store safely or store reference
        ↓
Pass internal file reference to parser
        ↓
Never depend on temporary channel file URL
```

## Security Rules

Minimum HERMES-450 security requirements:

- Verify webhook secrets where applicable
- Validate content type
- Validate file size
- Validate file extensions
- Do not log raw secrets or OAuth tokens
- Do not expose provider tokens to frontend
- Store sensitive references safely
- Keep raw payload references separate from normalized output
- Use review-required drafts for uncertain data

## Adapter Registry

The channel registry should support:

```json
{
  "telegram": {"status": "enabled", "supports_text": true, "supports_files": true},
  "generic_api": {"status": "enabled", "supports_text": true, "supports_files": true},
  "email": {"status": "contract", "supports_text": true, "supports_files": true},
  "whatsapp": {"status": "contract", "supports_text": true, "supports_files": true},
  "slack": {"status": "contract", "supports_text": true, "supports_files": true},
  "teams": {"status": "contract", "supports_text": true, "supports_files": true},
  "google_chat": {"status": "contract", "supports_text": true, "supports_files": true}
}
```

## Out of Scope

HERMES-450 does not include:

- Full chat application
- Socket.IO messenger
- Recruiter-to-recruiter chat
- Submission workflow
- Approval workflow
- Production WhatsApp integration
- Production Slack integration
- Production Microsoft Teams integration
- Production Google Chat integration
- CRM workflows
- ATS workflows

## Success Criteria

HERMES-450 is complete when Hermes can:

1. Receive generic channel intake through REST
2. Receive Telegram webhook-shaped intake
3. Normalize channel input into a canonical schema
4. Accept text and attachment metadata
5. Detect intake type
6. Route content to Hermes Understanding
7. Normalize parser output through taxonomy intelligence
8. Return structured JSON
9. Store safe intake logs
10. Prevent duplicate source messages
11. Expose channel health endpoint
12. Expose supported channels endpoint
13. Provide onboarding and identity intake contracts
14. Create draft-ready output objects
15. Keep channel adapters separate from parsing logic

## Phase Alignment

HERMES-450 depends on:

- HERMES-100 Core Platform
- HERMES-200 Understanding
- HERMES-400 Taxonomy & Signal Intelligence

HERMES-500 must wait until HERMES-450 can reliably receive, normalize, parse, log, and return structured channel intake.

HERMES-600 will later convert prepared channel contracts into production external integrations.

HERMES-700 agents should consume clean intake events and structured outputs, not raw channel payloads.