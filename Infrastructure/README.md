# Infrastructure

This folder documents Jobfynder's actual running infrastructure — servers, networking, backups, access, and operational standards. Unlike `Architecture/`, which describes durable structural decisions, this folder is closer to ground truth about what's actually deployed. Treat it as authoritative — when infrastructure changes, update the relevant file here in the same change, not as a follow-up.

**Status of each file, as of the 2026-09-07 pass:**

| File | Status |
|---|---|
| `SERVER-INVENTORY.md` | Real content — all 8 Elest.io services + 2 DigitalOcean droplets confirmed live via SSH; Hostinger confirmed as a real provider by the founder but its server IPs/access are still unknown |
| `SSH-STANDARDS.md` | Real content — key policy, per-provider access procedure, and a flagged security item (public keys committed in `jobfynder-infra` under a confusing filename, worth double-checking) |
| `NETWORK-ARCHITECTURE.md` | Real content — servers, IPs, and services confirmed against `JOBFYNDER-HERMES-COMM-CANONICAL.md` and the ADRs |
| `BACKUP-POLICY.md` | Partially filled — confirms backups exist, not the full schedule/retention |
| `FIREWALL-POLICY.md` | Partially filled — specific real fixes are documented; not a full rule set |
| `CHANGELOG.md` | Real content — transcribed from the canonical doc's own version history |
| `NAMING-STANDARDS.md`, `SSL-STANDARDS.md`, `BITWARDEN-STANDARDS.md`, `PORTAINER-STANDARDS.md` | **Templates only.** No real content exists anywhere in this repo to fill these from. Writing plausible-sounding standards without a real source would be actively misleading — these need someone with live access to the actual firewall/vault/Portainer to fill in. |

See also **[DISASTER-RECOVERY/](../DISASTER-RECOVERY/)** for provider-specific rebuild/recovery runbooks.
