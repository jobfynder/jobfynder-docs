# AI Standards

**Question this answers:** where is AI allowed to make decisions, and where must logic stay deterministic?

## The core boundary

Jobfynder's engineering philosophy (`ADR-0001`) draws one hard line: AI assists, it does not own, business-critical decisions. Concretely:

- Hermes generates recommendations, extracts structured information, and drafts content. Jobfynder Core (the NestJS backend) validates business rules and is the only thing that persists business data — Hermes never writes business records directly (`ADR-0006`).
- Only computed conclusions — rankings, scores — from the Network Relationship Module may reach LLM context. Raw relationship or interaction event rows must never reach an LLM call. This is enforced at the database function level, not application code, and applies to any future MCP or agent tooling without exception.
- Role-based agents (Founder, Recruiter, Bench Sales, Consultant, Engineering, Support — see `hermes/HERMES-700-multi-agent-foundation.md`) can analyze, summarize, recommend, and prepare drafts. They cannot submit candidates, message recruiters, change production data, or take any high-risk action automatically — those stay `needs_review`/blocked into human approval regardless of what's requested.

## Model routing and observability

- **LiteLLM** handles model routing across providers.
- **Langfuse** provides observability and tracing for every AI call, self-hosted on Elestio.
- **Sarvam AI** is the platform-wide STT/TTS provider, chosen specifically for Indian-accented English accuracy, since most users are from Asian countries (primarily India).

## Where this is enforced

- Database function level (the NRM boundary) — not application code, so it can't be bypassed by a new service that forgets to check.
- The Hermes Core/Edge split (`ADR-0002`, `ADR-0003`) — Edge never calls Core synchronously, limiting blast radius if a public-facing channel is compromised.

## Related

`ADR-0001` (Platform Engineering Philosophy), `ADR-0006` (Hermes is the Intelligence Layer), `hermes/HERMES-700-multi-agent-foundation.md`.
