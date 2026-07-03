# Hermes Marketing Worker — Build Specification

**Companion to:** `jobfynder-ai-marketing-master.md`
**Purpose:** Everything needed to actually write the code, gathered before implementation starts — not a marketing plan, a build checklist.

---

## 0. Two things to verify before you build anything

Flagging these now because they change how much of this worker can be automated vs. handled manually — better to know before, not during, implementation.

1. **Confirmed: Radaar has no direct public developer API, but a working automation path exists via Pabbly Connect.** Pabbly's own integration listing for Radaar confirms two real primitives: a **"New Post Published" webhook trigger** (Radaar → out) and a **"Create Content in RADAAR" action** (already used by other Pabbly integrations, e.g. Google Forms → Radaar, Facebook Lead Ads → Radaar). So `marketing.content.publish` *can* be automated — Hermes calls Pabbly's webhook endpoint, Pabbly translates that into a "Create Content" call inside Radaar. It's an extra hop and an extra subscription (Pabbly Connect has a free tier, then task-based billing — check current limits before relying on it), not a simplification. **Recommendation: build the manual path first** (Hermes drafts in Notion, employee copy-pastes into Radaar — per the original RACI) and only add the Pabbly hop later if the manual step genuinely becomes a bottleneck. Don't add a third-party automation broker on day one for a task one person can do in two minutes.

2. **Obsidian has no API at all — this is by design, not a gap.** It's a local markdown-file app. "Hermes writes to Obsidian" concretely means: the worker writes `.md` files directly to a folder on disk that Obsidian Sync is watching (same machine as your droplet, or a synced path). There's no HTTP call to make — this is filesystem I/O, which changes how you architect that part of the worker (a file-writer utility, not an API client).

---

## 1. Credentials & Access to Gather

| Service | What you need | Where it's used |
|---|---|---|
| AI Ark | API key (Settings → API panel per their docs) | Prospect/company pull jobs |
| Bright Data | Existing API token (already have, per earlier decision) | User-sync jobs |
| Notion | Internal integration token + explicit share access to each database below | Read/write prospect tracker, content calendar |
| Portkey | Virtual key(s) already routing to Claude (existing) | Content drafting, reply classification |
| n8n | Webhook URL(s) for triggering sequences, + API key if calling n8n's REST API to check workflow status | Handoff for email sends |
| Radaar | Confirm API key availability per item 0.1 above | Auto-posting (if API exists) or N/A |
| SMTP/sending domain | SPF/DKIM/DMARC already configured (per Phase 1), sending credentials for n8n | Email sends |

**Security note, per your own Engineering OS principle 9 (Security by Default):** scope the Notion integration token to only the specific databases below — not full workspace access. Store all of these as environment variables on the droplet, never in code or committed config.

---

## 2. Data Schemas — design these before writing worker logic

### 2.1 Prospect record (person)
Fields the worker needs to read/write, wherever it's stored (Notion primarily, mirrored to Obsidian):

| Field | Type | Source | Notes |
|---|---|---|---|
| `linkedin_url` | string | AI Ark | Primary dedup key |
| `name`, `current_title`, `current_company` | string | AI Ark | |
| `role_segment` | enum: BSR / Corporate Recruiter / Employer / Service Provider | Founder-set targeting criteria | Drives which message template is used |
| `email` (verified) | string | AI Ark | Only populated if verification succeeded |
| `outreach_status` | enum: not_contacted / invited / opened / replied / claimed / unsubscribed | Worker-updated | Core pipeline state |
| `last_contacted_at` | datetime | Worker-updated | Drives follow-up sequence timing |
| `reply_classification` | enum: interested / not_interested / question / unsubscribe / spam_complaint | Claude classification job | See 2.3 |
| `ai_ark_credit_cost` | number | AI Ark response | For budget tracking |

### 2.2 Company record
| Field | Type | Notes |
|---|---|---|
| `company_name`, `domain` | string | Dedup key |
| `employee_count_estimate` | number | From AI Ark |
| `target_tier` | enum: Tier 1 (BSR-heavy) / Tier 2 / Tier 3 | Founder-set, drives prioritization |
| `recruiters_pulled` | number | How many people from this company are already in the pipeline |

### 2.3 Reply classification taxonomy
Lock this **before** building the classification job, since it determines what Claude is asked to output:
- `interested` → route to employee for personal reply
- `not_interested` → mark closed, no further sequence sends
- `question` → route to employee (needs a human answer, don't auto-respond)
- `unsubscribe` → **immediately** suppress from all future sends — this must be a hard rule, not just a status flag, given CAN-SPAM obligations
- `spam_complaint` → suppress + flag to Founder (deliverability risk signal)

### 2.4 Content draft record
| Field | Type | Notes |
|---|---|---|
| `pillar` | enum: Industry Insight / Building in Public / Waitlist Momentum | Per Section 6.4 of the marketing master doc |
| `channel` | enum: LinkedIn / X / Blog / Email | |
| `status` | enum: drafted / approved / published | Draft→Live, matching your existing Notion Prompt Workflow pattern |
| `geo_checklist_passed` | boolean | Definition-first opening, question-based heading, etc. — per Section 6.2 |

---

## 3. Job/Queue Definitions

Following your existing nine-worker BullMQ pattern — these are jobs within the Marketing worker, not new services:

| Job name | Trigger | Input | Output | Notes |
|---|---|---|---|---|
| `marketing.prospect.pull` | Manual/cron (Founder-triggered batch) | Target criteria (role, company tier, count) | New Prospect + Company records in Notion | Enforce a **weekly credit ceiling** here — hard stop, not a soft warning, to prevent runaway AI Ark spend |
| `marketing.sequence.trigger` | On new prospect batch ready | Prospect list | Handoff to n8n webhook | n8n owns actual send timing/pacing |
| `marketing.reply.classify` | Webhook from n8n on inbound reply | Email/reply text | `reply_classification` written back to Notion | Use Claude Haiku here (cheap, fast) — matches your existing three-tier routing strategy |
| `marketing.content.draft` | Weekly cron | Content pillar + channel | Draft written to Notion, `status: drafted` | Use Claude Sonnet (prose generation tier). Default: employee manually posts to Radaar after approval. **Optional future upgrade:** once `status: approved`, call Pabbly Connect's webhook to auto-create the post in Radaar via their confirmed "Create Content in RADAAR" action — adds a dependency, only worth it once manual posting is a proven bottleneck. |
| `marketing.memory.sync` | On any Prospect/Company record change in Notion | Changed record | Markdown file written/updated in Obsidian vault | Filesystem write, not API — see Section 0.2 |
| `marketing.scorecard.aggregate` | Weekly cron, Friday morning | All prospect/content records for the week | Populated scorecard (Section 8 of master doc) in Notion | Feeds the Friday review directly |

**Error handling, per your Engineering OS mandatory standards:** every job above needs a retry strategy and needs to fail loud (alert, not silent) — a failed `marketing.sequence.trigger` that nobody notices means a prospect batch silently never gets contacted.

---

## 4. Business Rules to Lock Before Build

These aren't code — they're decisions that determine what the code should do. Answer these first:

1. **AI Ark weekly credit budget ceiling** — a hard number, so `marketing.prospect.pull` has something concrete to enforce.
2. **ICP targeting criteria** — exact role/company-tier definitions for `role_segment` and `target_tier` (Section 2.1/2.2). Vague criteria here produces a vague enrichment job.
3. **Follow-up cadence** — exact day offsets (e.g., day 4, day 10, per the earlier plan) that `marketing.sequence.trigger` hands to n8n.
4. **Locked message templates per role_segment** — the "join the waitlist" framing from the master doc, one variant per segment.
5. **What counts as GEO-compliant content** — turn Section 6.2's checklist into literal boolean checks the `marketing.content.draft` job (or a review step) can verify before `status` moves to `approved`.

---

## 5. Notion Structure Needed

Two databases, minimum, with the integration token scoped to exactly these:

- **Prospect Tracker** — one row per Prospect record (Section 2.1 fields as properties)
- **Content Calendar** — one row per Content draft record (Section 2.4 fields as properties)

Both need a Notion API-readable schema (property types matching the field types above) before the worker can write to them reliably.

---

## 6. Non-Functional Requirements (per your own Engineering OS — already your standard, apply it here)

- `/health` and `/version` endpoints on the Marketing worker
- Structured JSON logging for every job run (success/failure, credit cost, record counts)
- All config (API keys, credit ceilings, cadence timings) via environment variables — nothing hardcoded
- Graceful shutdown (don't lose an in-flight AI Ark pull if the worker restarts)
- Automated tests, at minimum for the classification job (this is the one with real consequences if it misclassifies an unsubscribe)

---

## 7. Suggested Build Order

1. Notion databases + schema (no code yet — just structure)
2. `marketing.prospect.pull` (AI Ark integration, credit ceiling enforced) — this alone lets you resume manual list-building with less copy-paste
3. `marketing.memory.sync` (Obsidian file writer) — low complexity, high value for getting the memory layer running early
4. `marketing.reply.classify` — needed before any real outreach volume, since unsubscribe handling must work correctly from day one
5. `marketing.sequence.trigger` (n8n handoff) — the actual sending mechanism
6. `marketing.content.draft` and `marketing.scorecard.aggregate` — these can wait until 1-5 are stable, since they're not in the critical compliance/outreach path

---
*Last updated: 2026-07-02*
