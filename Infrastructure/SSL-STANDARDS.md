# SSL Standards

## Confirmed

- `gateway.jobfynder.com` (LiteLLM) is Cloudflare-proxied — Cloudflare handles edge TLS termination for at least this domain. Likely true for other `*.jobfynder.com` public domains, but only confirmed for this one.
- A real TLS-bypass was found and fixed on COMM-1 during the 2026-08-21 inspection (see `CHANGELOG.md`) — confirms TLS was in active use there and had at least one real gap.

## Unknown — needs someone with live access to fill in

Certificate management approach (Let's Encrypt vs manual vs Cloudflare-issued), renewal process, and the complete list of domains/services covered.
