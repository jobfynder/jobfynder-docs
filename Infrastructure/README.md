# Infrastructure

Source of truth for Jobfynder's servers, network, and access policy. Treat this folder as authoritative — when infrastructure changes, update the relevant file here in the same change, not as a follow-up.

- **[SERVER-INVENTORY.md](./SERVER-INVENTORY.md)** — every known server, provider, IP, role, and SSH alias.
- **[SSH-STANDARDS.md](./SSH-STANDARDS.md)** — key policy, `~/.ssh/config` convention, and the per-provider procedure for granting access to a new machine.
- `NAMING-STANDARDS.md`, `NETWORK-ARCHITECTURE.md`, `FIREWALL-POLICY.md`, `BACKUP-POLICY.md`, `SSL-STANDARDS.md`, `PORTAINER-STANDARDS.md`, `BITWARDEN-STANDARDS.md` — scaffolded, not yet written. Fill in as each area is actually established/verified rather than guessed.

See also **[DISASTER-RECOVERY/](../DISASTER-RECOVERY/)** for provider-specific rebuild/recovery runbooks.
