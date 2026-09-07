# Rebuild Cloudflare

## Confirmed

Cloudflare proxies at least `gateway.jobfynder.com` (LiteLLM) and `uat.jobfynder.com` (Hostinger core/UAT backend, confirmed via `nslookup` 2026-09-07 — resolves to the same Cloudflare anycast range as `gateway.jobfynder.com`, not the origin's real IP).

`redisgateway.jobfynder.com` is a known open item: it currently resolves to Cloudflare anycast rather than the actual Elestio Redis VM (see `Infrastructure/NETWORK-ARCHITECTURE.md`). **Re-checked via `nslookup` 2026-09-07: still unresolved** — same anycast IPs as the other two domains, still not pointed at the real Redis host. This has been broken across at least two verification passes now; worth actually fixing rather than re-confirming again next time.

## Unknown — needs someone with live access to fill in

Full DNS zone configuration, which other domains are Cloudflare-proxied (only the three above have been checked), WAF/firewall rules if any, and actual rebuild steps if the Cloudflare account or zone were lost. No Cloudflare dashboard access was available during this pass to check further — DNS was inferred from `nslookup` only.
