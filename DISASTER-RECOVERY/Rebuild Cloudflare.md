# Rebuild Cloudflare

## Confirmed

Cloudflare proxies at least `gateway.jobfynder.com` (LiteLLM) — confirmed edge TLS termination there. `redisgateway.jobfynder.com` is a known open item: it currently resolves to Cloudflare anycast rather than the actual Elestio Redis VM (see `Infrastructure/NETWORK-ARCHITECTURE.md`).

## Unknown — needs someone with live access to fill in

Full DNS zone configuration, which other domains are Cloudflare-proxied, WAF/firewall rules if any, and actual rebuild steps if the Cloudflare account or zone were lost.
