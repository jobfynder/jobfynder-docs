# Hermes Engineering Playbook

Status: Active  
Owner: Jobfynder-Infra  
Purpose: Simple working rules for building Hermes

---

## 1. Main Rule

Hermes must stay simple, clean, and production-ready.

Do not build messy features.

Do not create complicated documents.

Do not add tools unless they clearly make Hermes smarter, faster, more reliable, or easier to operate.

---

## 2. How We Work

We work one capability at a time.

For every capability:

1. Decide the Hermes stream.
2. Define the expected output.
3. Build the smallest production-safe version.
4. Test it.
5. Document it.
6. Update Engineering Memory.
7. Update the Capability Matrix.
8. Commit the change.

---

## 3. Hermes Streams

| Stream | Meaning |
|---|---|
| HERMES-000 | Architecture and governance |
| HERMES-100 | Core platform |
| HERMES-200 | Understanding and parsers |
| HERMES-300 | Memory |
| HERMES-400 | Intelligence |
| HERMES-500 | Automation |
| HERMES-600 | Integrations |
| HERMES-700 | Multi-agent runtime |

---

## 4. Definition of Done

A Hermes capability is complete only when the required items are done.

Basic checklist:

- [ ] API or workflow implemented
- [ ] Schema or input/output format defined
- [ ] Tests or manual validation completed
- [ ] Documentation updated
- [ ] Capability Matrix updated
- [ ] Engineering Memory updated
- [ ] Security reviewed if tokens, secrets, or webhooks are involved
- [ ] Alerts added if failure needs attention
- [ ] Commit created

---

## 5. Documentation Rule

Documentation should be short and useful.

Every document should answer:

- What is this?
- Why does it exist?
- How do we use it?
- What is the current status?
- What is the next action?

Avoid long theory.

Avoid duplicate documents.

Avoid confusing names.

---

## 6. Security Rule

Never expose secrets in documentation, commits, logs, Telegram, email alerts, or screenshots.

Secrets include:

- API keys
- Webhook tokens
- GitHub tokens
- SSH private keys
- Database passwords
- Email credentials
- n8n credentials

Use placeholders when needed.

---

## 7. Change Rule

Every meaningful Hermes change should be traceable.

Minimum trace:

- Git commit
- Engineering Memory entry
- Updated document if needed
- Updated Capability Matrix if status changed

---

## 8. COMM-1 Mission

COMM-1 exists to continuously improve Hermes.

Every change must answer:

Does this make Hermes smarter, faster, more reliable, or easier to operate?

If not, do not build it.

---

## 9. Current Focus

Current stream:

HERMES-000 — Architecture & Governance

Current goal:

Create the simple governance foundation before starting HERMES-100 Core Platform.
