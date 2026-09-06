# Firewall Policy

**This is partial.** The specific fixes below are real and dated; a complete rule set is not recorded anywhere in this repo.

## Confirmed changes (2026-08-21, see `CHANGELOG.md` for full context)

- `ufw` enabled on COMM-1 (commit `33b6ec4`).
- `jobfynder-comm-gateway` port 8080 is no longer published directly — it was found exposed and closed the same day.
- Per-IP rate limiting added to the COMM intake path (commit `0c335804`).
- A real TLS-bypass was found and fixed during the same inspection pass (see `CHANGELOG.md`, v1.5) — the specific mechanism isn't detailed here; check the canonical doc's version history if you need it.
- A weak default RabbitMQ credential was found live in production and fixed the same pass.

## Unknown — needs someone with live access to fill in

- The actual current `ufw` rule set (which ports are open, to what)
- INTEL-1's firewall configuration — everything confirmed above is COMM-1-specific
- Any VPN, bastion, or SSH-allowlist configuration
