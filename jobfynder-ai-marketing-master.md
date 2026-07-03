# Jobfynder AI Marketing Master Document

**Owner:** Founder | **Team:** Founder + 1 Marketing Executive (remote) | **Status:** Living document — update as phases complete
**Product timeline:** Hermes/platform development ongoing, ~2-3 months to functional beta
**Public launch gate:** Minimum 500 real, active users with tested platform data — not a date-based launch

---

## 0. The One Rule Everything Else Follows

**We are not launching a product for the next 2-3 months. We are building a waitlist of the right 500 people**, so that the moment the platform can hold real usage, we already have a warm, qualified group ready to become Jobfynder's first real data. Every task in this document exists to serve that one goal until Phase 4.

Public, broad marketing (press, big content pushes, paid ads) is explicitly **out of scope** until the 500-user gate is cleared. Doing that now would burn credibility on a product that isn't ready to be judged.

---

## 1. Confirmed Tool Stack (verified pricing, no guessing)

| Tool | Role | Plan recommendation | Cost | Status |
|---|---|---|---|---|
| **Hermes Marketing Worker** | Orchestrates the pipeline: list pulls → sequencing → reply classification → content queue | N/A (your infra) | $0 (already built) | To be built out (Phase 1) |
| **AI Ark** | Finds new BSR/recruiter/company prospects | Starter tier (confirm current price at signup — was ~$49/mo for ~5,000 credits at time of research) | ~$49–99/mo | New |
| **Bright Data** | Keeps *existing platform users'* profiles fresh (not prospecting) | Existing PAYG | ~$1.50/1,000 records, low at current scale | Already decided |
| **n8n** | Runs scheduled/triggered sequences (email waves, follow-ups, content pipeline) | Self-hosted | $0 (existing droplet) | Already decided |
| **Claude / ChatGPT (existing subs)** | Drafts content, email copy, reply classification, SEO/GEO content structuring | Existing subscriptions | $0 incremental | Already have |
| **Notion** | Content calendar, prompt library, Draft→Live pipeline, prospect/task tracking | **Plus plan** ($10/user/month, billed annually) | ~$20/mo for 2 seats | **Recommended — see confirmation below** |
| **Obsidian** | Prospect & company memory (compiled-truth + evidence-trail pages), Hermes's long-term memory source. **Founder-only, single-editor vault** — see 1.1 | **Free core app + Sync add-on** ($4/user/month, billed annually) | ~$4/mo, 1 seat | **Recommended — see confirmation below** |
| **Radaar.io** | ALL social scheduling, publishing, inbox, monitoring, analytics, Kanban task board | Existing LTD | $0 incremental | **Already covers this need — no new SMM tool** |
| **Canva** | Visual assets for social/content | Existing subscription | $0 incremental | Already have |
| **Supademo** | Interactive clickable product demo, embedded on waitlist page + used in email/social | **Free tier first** (5 published demos, unlimited views) | $0 to start | New — see 1.2 |

**Total new monthly cash spend: roughly $70–125/month** (essentially just AI Ark + Notion Plus for 2 seats + 1 Obsidian Sync seat). Supademo starts free and only adds cost if you outgrow the 5-demo limit. Everything else is infrastructure, automation, or subscriptions you already have.

### 1.1 Confirmed: Notion Plus + Obsidian Sync — here's the reasoning

You asked for a direct confirmation. Here it is, with current verified pricing (checked directly against both vendors' pricing pages):

- **Notion: go with Plus ($10/user/month annual), not Business ($18-20/user/month annual).** Business's entire value-add over Plus is Notion's own AI Agents and SSO — but you're already paying for Claude and ChatGPT directly, so you don't need Notion to sell you AI a second time. Plus gives you everything that actually matters for this system: unlimited file uploads, unlimited guests (for any future collaborators), and 30-day version history. For 2 seats, that's about **$20/month total**.

- **Obsidian: keep the core app free, add Sync only ($4/user/month annual) — and keep it Founder-only, one seat.** You don't need Obsidian Publish (that's for turning notes into a public website — not your use case) or the commercial license (now optional/free as of 2025-2026 policy change). Sync is worth paying for since Obsidian is your locked-in "memory source" in the canonical architecture and needs to stay current across your own devices. Critically: **the employee should not get direct Obsidian access.** Obsidian's shared-vault sync is known to produce file conflicts with multiple simultaneous editors — it's fundamentally a single-player tool, not built for team collaboration the way Notion is. The employee's prospect/reply tracking happens in Notion (where he already works); Hermes reads that and writes the compiled-truth/evidence-trail pages into Obsidian automatically, no human hand-off required on his end. Founder keeps read/spot-check access only. For 1 seat, that's about **$4/month total**.

- **Why not just use one tool for both jobs?** Notion is built for structured collaboration (calendars, kanban, shared docs) — it's your operational surface. Obsidian is built for freeform linked knowledge (markdown pages, backlinks) — it's your memory surface, and it's what Hermes/future AI agents will read from directly as plain files, which Notion's proprietary format doesn't offer. Using both, each for its actual strength, costs about **$28/month combined** and avoids forcing one tool to do a job it wasn't built for.

- **Radaar confirmed sufficient — do not add Buffer, Hootsuite, Later, or any other SMM tool.** Radaar's feature set (scheduler across FB/IG/X/LinkedIn/Pinterest/TikTok/Telegram/Google Business Profile, unified inbox, keyword/competitor monitoring, analytics, Kanban task manager, even a landing-page builder) already covers everything a 2-person team needs. Adding a second social tool would only fragment your data and add a subscription with zero new capability.

### 1.2 Confirmed: Supademo over Storylane, starting on the free tier

You asked to bring in interactive demos (Supademo and/or Storylane). Here's the call, based on independent comparisons, not vendor marketing:

- **Storylane is built for enterprise sales-led motions** — its Growth tier starts at $500/month with a 5-seat minimum, its Starter tier has a 2-seat minimum at $40/month, and reviewers report average customer spend around $11,500/year once add-ons (sandboxes, AI features) get layered on. That pricing shape assumes a sales team running dozens of live deal-specific demos — not where Jobfynder is.
- **Supademo fits a small/solo team's actual need.** Free tier gives 5 published demos with unlimited views — enough to cover a full product walkthrough plus a couple of role-specific cuts (e.g. one for BSRs, one for Corporate Recruiters) without paying anything. If you outgrow that, Pro/Scale runs roughly $27-38/creator/month, still far below Storylane's entry point. Multiple independent comparisons explicitly call out solo founders and 2-3 person teams as Supademo's better fit for exactly this reason.
- **Revisit Storylane later, not now** — specifically if Jobfynder moves toward enterprise-side selling (e.g. selling to large staffing agencies or corporate accounts that require SSO, Salesforce integration, or a dedicated CSM). That's a Phase 4+/post-launch consideration, not a prelaunch one.

**Where the demo actually plugs into the plan (not a new channel — it strengthens existing ones):**

1. **Waitlist landing page (Phase 1, Week 2):** embed the Supademo walkthrough directly on the page. Since your frontend is already largely built, this is real leverage — prospects get to *see* the actual product instead of reading a description of something that doesn't exist yet publicly. This is likely the single highest-conversion addition to the whole prelaunch funnel.
2. **Email nurture (Section 6.3):** "see how it works" as a demo link is a much stronger, lower-friction CTA in outreach and nurture sequences than asking someone to just join a waitlist blind.
3. **Social content (Section 6.4, "Building in Public" pillar):** short clips/exports from the demo are exactly the kind of specific, non-polished content that pillar calls for.
4. **Phase 3 onboarding:** once real users join, the same demo (or a role-specific variant) doubles as self-serve onboarding, directly supporting the "reduce manual data entry, increase adoption" goal from earlier in this plan.

**Owner:** Employee builds the demo (Supademo's Chrome extension makes this a same-day task per independent reviews, no engineering time needed), Founder approves before it goes live anywhere public.

---

## 2. Team & Responsibilities (RACI)

| Activity | Founder | Employee | AI (Hermes/Claude/n8n) |
|---|---|---|---|
| Set targeting criteria (who to enrich, ICP) | **R/A** | Consulted | Executes |
| Approve brand voice / what goes public | **R/A** | Drafts | Drafts |
| AI Ark list pulls | **R** | — | Executes via Hermes |
| Email sequence build (n8n) | **R** | Monitors | Executes |
| Social scheduling (Radaar) | Reviews | **R** | Drafts captions |
| Reply to prospects/users personally | — | **R/A** | Flags/classifies only |
| Prospect/reply status tracking | Spot-checks | **R** (in Notion) | Auto-syncs Notion → Obsidian |
| Weekly scorecard | **A** | **R** | Feeds data |
| SEO/GEO content structuring | Reviews | **R** | Drafts |
| Community engagement (Reddit, LinkedIn groups) | Occasional | **R** | — |
| Build/update Supademo interactive demo | Approves | **R** | — |

**R = Responsible (does the work), A = Accountable (owns the outcome).** Note the employee is Responsible for most execution — the founder's job is targeting, approval, and weekly accountability, not daily doing.

---

## 3. Timeline Overview

```
Month 1          Month 2          Month 3          Gate: 500 users     Public Launch
├─ Foundation    ├─ Waitlist      ├─ Waitlist      ├─ Private beta      ├─ Continuous
│  + Waitlist    │  Growth        │  Growth +      │  activation        │  branding
│  Page Live     │  (SEO/GEO      │  Beta Prep     │  (once dev ready)  │  (ongoing)
│                │  content       │                │                    │
│  Phase 1       │  Phase 2       │  Phase 2 cont. │  Phase 3            │  Phase 5
```

Phase 3 (Private Beta / 500-user activation) starts **whenever Hermes/platform is functionally ready** — not on a fixed calendar date. If development takes 4 months instead of 3, Phase 2 simply runs longer. The waitlist only grows stronger the longer it has to compound.

---

## 4. Phase 1 — Foundation (Weeks 1–4)

**Goal:** Infrastructure, brand presence, and the waitlist mechanism live — before any real outreach volume.

### Week 1: Infrastructure
| Task | Owner | Done when |
|---|---|---|
| Set up Notion Plus (2 seats) — content calendar, prompt library migrated | Founder | Live, employee has access |
| Set up Obsidian + Sync (2 seats) — Prospect/Company vault schema created | Founder | Vault syncing across both devices |
| Domain email auth (SPF/DKIM/DMARC) + warmup started | Founder | Test email lands in inbox |
| Confirm Radaar channels connected (LinkedIn Company Page priority, X, Instagram) | Employee | All channels connected, test post published |
| AI Ark free-tier pilot (100 credits) on staffing niche | Founder | Match quality confirmed for BSR/staffing vertical |

### Week 2: Waitlist Mechanism
| Task | Owner | Done when |
|---|---|---|
| Build waitlist landing page (on your own domain, NOT Radaar's landing builder — domain authority matters for SEO/GEO from day one) | Founder (or delegate to dev time) | Live, capturing emails |
| Landing page copy: "Connect with Clarity" tagline, one-liner, clear value prop, waitlist CTA | Employee drafts, Founder approves | Copy locked |
| Basic technical SEO/GEO pass on landing page (see Section 6.1) | Employee, using Claude | Checklist complete |
| Build initial Supademo interactive demo (full product walkthrough via Chrome extension) using existing frontend | Employee, Founder approves | Published, embedded on landing page |
| n8n: waitlist confirmation + welcome sequence | Founder | Test signup flows end-to-end |

### Week 3: Content Engine Setup
| Task | Owner | Done when |
|---|---|---|
| Notion content calendar populated for Weeks 4-8 | Employee | 4 weeks scheduled |
| Content pillars locked (see Section 6.4) | Founder + Employee | Documented in Notion |
| First 10 pieces of GEO/SEO-structured content drafted (definition-first, question-based headings — see Section 6.2) | Employee via Claude | Drafted, awaiting approval |
| Obsidian "claim-ready" schema for prospect pages (compiled truth + evidence trail, per GBrain-style pattern) | Founder | Template page created |

### Week 4: First Wave
| Task | Owner | Done when |
|---|---|---|
| Pull first real batch via AI Ark (~500 BSRs across ~100 target companies) | Founder | List enriched, in Obsidian |
| Send Wave 1 "join the waitlist" invites (small batches, NOT "your profile has been updated" — see Section 5 caution) | Automated via n8n, monitored by Employee | 500 sent across the week |
| Daily reply handling | Employee | 0 replies sitting >24hrs |
| First week of scheduled social content live via Radaar | Employee | 5 posts published |
| **End of Phase 1 review** | Founder + Employee | Scorecard baseline established |

---

## 5. The Outreach Message — Locked Framing

**This is the single most important paragraph in this document.** As covered previously: do not imply a profile already exists and was "updated" — that crosses from prospecting into publishing personal data without consent, which is both a legal risk and a trust-destroying first impression.

**Locked message pattern for all waitlist invites:**
> "We're building [Jobfynder — one-liner]. Based on your public work in [X], we think you'd be a strong fit for early access. Join the waitlist to be one of the first 500 recruiters shaping the platform."

This is honest, creates the same "we see you" effect, and sets accurate expectations: they're joining a **waitlist for something not yet live**, not claiming an existing profile. Given your gate is literally "500 users," lean into this directly — "one of the first 500" is a genuine, honest scarcity hook you don't have to manufacture.

---

## 6. Channel Playbooks

### 6.1 SEO (Search Engine Optimization) — foundation for everything else

Technical SEO is the base layer GEO/AEO build on top of. One-time setup + quarterly refresh, not daily work.

**One-time technical checklist (Week 2):**
- [ ] Clean URL structure, one clear H1 per page, logical H2/H3 hierarchy
- [ ] Meta titles/descriptions on every page (Claude can draft these from page content)
- [ ] Fast load time — check via PageSpeed Insights, fix anything under 90
- [ ] Sitemap.xml submitted to Google Search Console
- [ ] Mobile responsive (should already be true given your Vite frontend)

**Ongoing (weekly):**
- 1 SEO-structured blog post/week targeting real staffing-industry search terms (bench sales, C2C, hotlist management, W2 vs C2C, etc.) — use Google Search Console + Reddit staffing communities to find actual phrasing recruiters search, not guessed keywords.

### 6.2 AEO/GEO (Answer & Generative Engine Optimization) — being cited by ChatGPT, Perplexity, Google AI Overviews

This is no longer optional in 2026 — a large and growing share of searches now resolve inside AI answers with zero click-through to any website, so being the source an AI cites matters as much as ranking on a results page.

**One-time technical setup (Week 2, do alongside SEO):**
- [ ] Ensure `robots.txt` explicitly **allows** AI crawlers: GPTBot (OpenAI), ClaudeBot (Anthropic), PerplexityBot, Google-Extended
- [ ] Publish an `llms.txt` file at your site root — a curated, plain-text index of your most important pages, written for AI systems rather than humans (AI Ark itself does this, at docs.ai-ark.com/llms.txt, if you want a live example)
- [ ] Add FAQ schema markup to key pages (landing page, any "what is Jobfynder" content)
- [ ] Confirm no important content is hidden behind JavaScript-only rendering or logins

**Content-writing rules for every piece of content (train the employee on this explicitly):**
- **Definition-first sentences** — open each section with a direct, quotable answer, then explain. ("Bench sales recruiting is the process of marketing available consultants to vendors and clients." — not built up to over three paragraphs.)
- **Question-based headings** — phrase H2s as the actual question a recruiter would type into ChatGPT ("How do bench sales recruiters find C2C opportunities?" not "C2C Opportunities Overview")
- **Include real numbers/stats where possible** — cited statistics measurably increase AI citation rates
- **Self-contained passages** — each paragraph should make sense pulled out of context, since that's literally how RAG systems extract and cite it
- **Keep a visible "last updated" date and refresh core pages quarterly** — AI systems weigh content recency

**Where to seed presence beyond your own site (this matters as much as your own content):** Reddit threads in r/recruiting or staffing-adjacent communities, Quora answers, and any staffing-industry forums — LLMs draw heavily on these when answering staffing-related questions. A few genuinely helpful, non-promotional answers from your team's real accounts compounds over months.

### 6.3 Email — your highest-leverage channel at this stage

Covered operationally in Section 4 and Section 5. Two additions:

- **Segment from day one in Obsidian**, not just a flat list: BSRs, Corporate Recruiters, Employers, Service Providers each get slightly different messaging — same waitlist mechanic, different value prop line.
- **Weekly nurture, not just the initial invite.** Waitlist members who don't convert to "claimed/confirmed" in week 1 get a short, valuable nurture sequence (industry insight, not "please sign up again") over the following weeks — this is what keeps the waitlist warm for 2-3 months instead of going cold.

### 6.4 Social (via Radaar — no new tool needed)

**Content pillars (lock these in Week 3, keep to 3 so it's sustainable for one employee):**
1. **Industry insight** — bench sales/staffing market observations, positioned as genuinely useful even to someone who never signs up (this is what earns GEO citations and organic follows)
2. **Building in public** — Hermes/product development updates, honest and specific (recruiters trust specificity over polish)
3. **Waitlist momentum** — "X/500 spots" style updates as the count grows (again, honest scarcity, not manufactured)

**Cadence:** 3 posts/week minimum (LinkedIn priority — that's where your ICP lives), using Radaar's scheduler + Canva for visuals. Use Radaar's Social Inbox to guarantee same-day reply handling — this is the single habit that most affects whether someone converts from "saw a post" to "joined the waitlist."

### 6.5 Community

Not a separate task — it's the "who" behind Section 6.2's Reddit/Quora presence and any staffing-industry LinkedIn groups. Employee spends a fixed 30 min/week here, tracked as its own scorecard line so it doesn't silently get skipped in favor of easier tasks.

---

## 7. Weekly SOP (unchanged core, now tool-specific)

**Monday**
- [ ] Check weekend replies (email + Radaar inbox), respond to all
- [ ] Confirm week's content calendar in Notion is fully drafted and approved
- [ ] Check n8n dashboard for failed sends/bounces

**Tuesday–Thursday**
- [ ] Publish scheduled content via Radaar (1/day minimum)
- [ ] Respond to every comment/DM same-day (Radaar inbox)
- [ ] 30 min community engagement (Reddit/Quora/LinkedIn groups)
- [ ] Update prospect status in Notion as replies come in (Hermes syncs this into Obsidian automatically — employee never opens Obsidian directly)

**Friday**
- [ ] Update weekly scorecard (Section 8)
- [ ] 30-min review call with Founder
- [ ] Next week's content batch loaded into Notion

---

## 8. Weekly Scorecard

| Metric | Target trend | This week | Last week |
|---|---|---|---|
| New prospects enriched (AI Ark) | Steady, matched to list-building phase | | |
| Waitlist invites sent | Steady weekly batches, never one huge spike | | |
| Open rate % | >35% (cold B2B benchmark; investigate if lower) | | |
| Reply rate % | Track trend, not absolute — flag 2-week drops | | |
| **Waitlist signups** | The core number — should compound weekly | | |
| Waitlist → "confirmed interest" (opened nurture, replied, or engaged) | Rising | | |
| LinkedIn posts published | 3/week minimum | | |
| LinkedIn engagement (likes+comments+shares) | Rising | | |
| Bounce rate % | <2%, hard stop and fix if higher | | |
| GEO: AI citation spot-checks (ask ChatGPT/Perplexity a staffing question monthly, see if Jobfynder appears) | Monthly, not weekly | | |

**Rule, unchanged from before:** two consecutive weeks of falling signup or reply rate is the Friday agenda item — fix the message before adding more volume.

---

## 9. Phase 2 — Sustained Waitlist Growth (Months 2–3, while development continues)

This phase runs as long as development takes. The work doesn't change in kind, only in scale:

- AI Ark list-building expands toward the full target (companies + recruiters across the BSR-first ICP)
- Weekly outreach batches continue at a sustainable pace — bounce rate and reply-rate health matter more than raw speed
- SEO/GEO content compounds weekly (aim for a real content library by the time you hit the 500-user gate — this becomes your onboarding/education material too)
- Monthly milestone content: "waitlist crossed X" posts, which double as both social proof and GEO-citable data points
- **No public launch messaging yet.** Everything still frames Jobfynder as "coming, join the list" — resist the temptation to soft-launch early just because momentum feels good.

**Phase 2 exit criteria (tell the employee this explicitly, so he knows what "done" looks like):** Hermes/platform reaches functional beta readiness (Founder's call, tied to engineering milestones, not marketing pressure) **and** the waitlist has meaningfully more than 500 people (aim for 2-3x buffer, since not every waitlist signup converts to an active user).

---

## 10. Phase 3 — Private Beta: The Path to 500 Real Users

**Goal:** Convert waitlist into actual logged-in, active users, and validate the platform with real usage — this is the actual gate, not just 500 email addresses.

| Task | Owner | Notes |
|---|---|---|
| Invite waitlist in controlled waves (not all at once) | Founder decides pace | Lets you catch platform issues on a small group before wider exposure |
| Personal onboarding touch for each wave (employee, not automated) | Employee | This is where "digital proof of work" trust gets built — high-touch matters here specifically |
| Track real activation, not just signup (did they actually build a profile, log a placement, etc.) | Hermes/Analytics | Define "active" concretely before this phase starts |
| Weekly bug/feedback loop back to Founder | Employee logs, Founder triages | Feeds directly into product, not just marketing |
| Identify first Charter Members (most active early users) | Founder | Named cohort, per existing Charter Member program |
| Collect 5+ real testimonials once usage is genuine | Employee, personal outreach | Do not ask before someone has real experience to speak to |

**Exit criteria:** 500+ active users, real usage data collected, product validated by actual behavior — not projected. This is when Phase 4 begins.

---

## 11. Phase 4 — Public Launch

Only triggered once Phase 3's gate is met. At that point:

- Convert the content library built in Phase 1-2 into launch-day assets (you'll have months of GEO/SEO content already live and indexed — this is the compounding payoff of not waiting to start content)
- Charter Member testimonials become the core social proof
- Press/broader outreach becomes appropriate for the first time — the product now has real users and real data behind every claim
- Radaar monitoring (competitor/keyword tracking) becomes more active here, watching for market reaction

*(Full Phase 4 launch-week playbook to be detailed as a follow-up once Phase 3 is underway — building it now would be planning against assumptions about a product that's still 2-3+ months from ready.)*

---

## 12. Phase 5 — Continuous Branding (Ongoing, Post-Launch)

The Weekly SOP (Section 7) and Scorecard (Section 8) continue unchanged — this system is designed to run indefinitely, not just through launch. The only shifts:

- Content pillars expand to include real user stories/outcomes (the actual moat — see prior conversation on self-reported data as canonical truth)
- GEO monitoring becomes monthly-tracked, not just spot-checked
- AI Ark shifts from pure prospecting toward the ongoing-sync use case discussed previously (job-change tracking on active users, cheap incremental credits)
- Consider Crustdata-style real-time monitoring **only once revenue justifies it** — not before

---

## 13. Governance

This document is the master reference — if a decision here conflicts with something decided verbally in a meeting, **this document loses until it's explicitly updated**, the same rule your Engineering OS already applies to code decisions. Log any material change to this plan (not routine execution details) as a dated entry at the bottom of this section.

**Recommend formalizing the tool decisions in Section 1 as entries in `DECISIONS.md`** in the jobfynder-docs repo, so "why did we pick Notion Plus over Business" doesn't get re-litigated in three months.

### Change Log
- **2026-07-02** — Master document created. Tool stack confirmed: AI Ark (prospecting), Bright Data (existing-user sync), Notion Plus, Obsidian + Sync, Radaar (existing LTD, no new SMM tool), Canva + Claude/ChatGPT (existing). Phase 1 begins.
- **2026-07-02** — Corrected: Obsidian access restricted to Founder only, single-editor vault (1 seat, ~$4/mo). Reason: shared-vault sync conflicts are a known Obsidian limitation, and the employee's tracking work already lives in Notion — no need for a second tool. Hermes syncs Notion status into Obsidian automatically instead of requiring manual employee entry.
- **2026-07-02** — Added: Supademo (free tier) for interactive product demos, embedded on the waitlist landing page and used across email/social. Storylane evaluated and rejected for now — its pricing (2-5 seat minimums, $40-500/mo) targets enterprise sales-led teams, not a 2-person bootstrap. Revisit Storylane only if/when Jobfynder moves toward enterprise-side selling post-launch.

---
*Last updated: 2026-07-02*
