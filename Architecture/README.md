# Architecture

This folder documents Jobfynder's platform architecture at the level of durable structure and decisions — not day-to-day implementation detail, which lives in the code itself or in the `HERMES-nnn`/`COMM-nnn` docs for the AI and communication planes specifically.

## Files

- **`01-platform-architecture.md`** — the platform's service-oriented architecture, core principles, and staged scalability strategy (MVP → Growth → Scale).
- **`02-ai-standards.md`** — where AI is allowed to make decisions, where logic must stay deterministic, model routing, and observability.
- **`03-jobfynder-core-modules.md`** — the actual product modules in the backend, and how the five user-registerable roles map to the platform.

For the reasoning behind a specific architectural choice, see `FOUNDATION/ENGINEERING MEMORY/adrs/` — every ADR referenced in these files lives there.
