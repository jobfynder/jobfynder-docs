# Infrastructure

This folder documents Jobfynder's actual running infrastructure — servers, networking, backups, and operational standards. Unlike `Architecture/`, which describes durable structural decisions, this folder is closer to ground truth about what's actually deployed.

**Status of each file, as of this fill-in pass:**

| File | Status |
|---|---|
| `NETWORK-ARCHITECTURE.md` | Real content — servers, IPs, and services confirmed against `JOBFYNDER-HERMES-COMM-CANONICAL.md` and the ADRs |
| `SERVER-INVENTORY.md` | Partially filled — only what's independently confirmed; several fields marked unknown |
| `BACKUP-POLICY.md` | Partially filled — confirms backups exist, not the full schedule/retention |
| `FIREWALL-POLICY.md` | Partially filled — specific real fixes are documented; not a full rule set |
| `CHANGELOG.md` | Real content — transcribed from the canonical doc's own version history |
| `NAMING-STANDARDS.md`, `SSH-STANDARDS.md`, `SSL-STANDARDS.md`, `BITWARDEN-STANDARDS.md`, `PORTAINER-STANDARDS.md` | **Templates only.** No real content exists anywhere in this repo to fill these from. Writing plausible-sounding security standards without a real source would be actively misleading — these need someone with live access to the actual servers, firewall, and vault to fill in, not a git-repo read. |

If you have that access, or want to walk through it together, these five are the right next thing to close out.
