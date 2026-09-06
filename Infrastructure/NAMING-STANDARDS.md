# Naming Standards

## Confirmed, real conventions in use

- **LiteLLM model aliases** use a `jf-` prefix: `jf-fast`, `jf-structured`, `jf-reasoning`, `jf-writing`, `jf-embedding`.
- **LiteLLM virtual keys** follow `jf-<purpose>-<environment>`: `jf-hermes-production`, `jf-core-production`, `jf-n8n-production`, `jf-evaluation-production`, `jf-development`.
- **Langfuse prompts** use dot notation for hierarchy: `jf.admin.ai-anomaly.explain`, `jf.screening.questions.generate`, `jf.job-tracker.interview.prep`. Folders within Langfuse's own UI are indicated with `/` in the name (e.g. `extraction/job-description`) — dot notation and slash notation serve different purposes here, don't conflate them.
- **Server naming**: `COMM-1` for the communication-plane server. No evidence of a numbered convention beyond that one instance (`INTEL-1` is referenced in architecture docs but its actual server hasn't been confirmed against a real IP — see `SERVER-INVENTORY.md`).

## Still unknown

Docker container/stack naming conventions, database/schema naming, environment variable naming beyond what's visible in the AI infra summary.
