# jobfynder-docs
Engineering Operating System, Architecture, Standards, ADRs and Documentation for the Jobfynder Platform.

# Jobfynder Engineering OS

## Volume 0 — Start Here
- [HERMES + COMM Canonical Documentation](./JOBFYNDER-HERMES-COMM-CANONICAL.md) — the document of truth. Read this first.
- [HERMES + COMM Core Integration Guide](./HERMES-COMM-CORE-INTEGRATION-GUIDE.md) — developer-facing: auth, endpoints, samples, error codes, testing plan.

## Volume 1 — Engineering Philosophy
- `FOUNDATION/ENGINEERING MEMORY/adrs/ADR-0001-platform-engineering-philosophy.md`

## Volume 2 — Architecture
- [Architecture/](./Architecture/) — platform architecture, AI standards, Core module map

## Volume 3 — Infrastructure
- [Infrastructure/](./Infrastructure/)

## Volume 4 — Hermes & COMM
- [hermes/](./hermes/)
- [comm/](./comm/) — see `comm/COMM-documentation-map.md`

## Volume 5 — AI Standards
- [Architecture/02-ai-standards.md](./Architecture/02-ai-standards.md)

## Volume 6 — Jobfynder Core
- [Architecture/03-jobfynder-core-modules.md](./Architecture/03-jobfynder-core-modules.md)

## Volume 7 — Runbooks & Disaster Recovery
- [DISASTER-RECOVERY/](./DISASTER-RECOVERY/)

## Volume 8 — Architecture Decision Records
- [FOUNDATION/ENGINEERING MEMORY/adrs/](./FOUNDATION/ENGINEERING%20MEMORY/adrs/)

---

**Folded into existing docs rather than kept as separate empty volumes:**
- *Contracts* (API/service contracts) — covered by `HERMES-COMM-CORE-INTEGRATION-GUIDE.md` (endpoints, samples, error codes).
- *DevOps* — covered by `ADR-0004` (staged deployment plan) and `Infrastructure/`.
- *Security* — covered by `Infrastructure/FIREWALL-POLICY.md`, `SSH-STANDARDS.md`, `SSL-STANDARDS.md`, `BITWARDEN-STANDARDS.md`, and the AI/NRM boundary in `Architecture/02-ai-standards.md`.

**Removed, not folded — no known content anywhere in this repo to draw from:** *ERS*. If this meant something specific, bring it back with real content, not as another empty placeholder.

For the founder's own daily/weekly operating rhythm (not engineering documentation), see `FOUNDER-OS/`.
