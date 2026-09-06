# SSH Standards

## Confirmed

- `jobfynder/jobfynder-infra` has ed25519 public keys committed under `pavan@jobfynder.com` — confirms a key exists, says nothing about rotation policy or who else has access.
- Hermes WebUI is accessed via **Tailscale**, not direct public SSH/HTTP exposure — this is the one confirmed access-control pattern in this repo.

## Unknown — needs someone with live access to fill in

Key rotation policy, who has access to which servers, whether a bastion host is used beyond the Tailscale pattern above, and where private keys are actually stored (should never be in a git repo — worth double-checking `jobfynder-infra` doesn't have one, since it did have public keys sitting in it under a confusing filename).
