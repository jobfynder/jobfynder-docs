# Recover SSH

## Confirmed

Hermes WebUI access goes through Tailscale, not direct public SSH exposure — that's the one confirmed access pattern (see `Infrastructure/SSH-STANDARDS.md`).

## Unknown — needs someone with live access to fill in

What happens if SSH access itself is lost — whether Tailscale is the sole access path for every server, or a fallback exists, and where any recovery/emergency-access keys are actually kept.
