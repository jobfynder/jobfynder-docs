# Firewall Policy

## Confirmed changes (2026-08-21, see `CHANGELOG.md`)

- `ufw` enabled on COMM-1 (commit `33b6ec4`).
- `jobfynder-comm-gateway` port 8080 is no longer published directly — found exposed, closed the same day.
- Per-IP rate limiting added to the COMM intake path (commit `0c335804`).
- A real TLS-bypass and a weak default RabbitMQ credential were found and fixed during the same inspection pass.

## Confirmed changes (2026-08-02, LiteLLM/Redis lockdown)

- The Redis instance used for LiteLLM caching (`10.30.71.5:26379`) is restricted to `159.195.1.254/32` only — the LiteLLM server itself, nothing else.
- **This required two layers, not one:** a UFW rule and the Docker `DOCKER-USER` chain. Elestio-hosted Redis defaults to public `0.0.0.0/0` exposure — removing only one of the two layers leaves it open.
- Default ports `22/80/443` are left open; additional ports `26380`, `18446`, `18374`, `4242` are explicitly left untouched (Elestio-managed, not to be firewalled without checking what they're for first).
- Verified closed from outside: public IP `152.53.202.147:26379` — confirmed filtered while caching stayed healthy from the permitted IP.

## Unknown — needs someone with live access to fill in

- The actual current full `ufw` rule set beyond the specific fixes above
- INTEL-1's firewall configuration specifically (everything confirmed above is COMM-1 or the LiteLLM/Redis Elestio VMs)
- Any VPN, bastion, or SSH-allowlist configuration
