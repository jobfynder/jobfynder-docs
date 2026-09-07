# Disaster Recovery

Runbooks for recovering platform components after a failure. Every file here follows the same honesty rule as `Infrastructure/`: real, sourced facts are marked as such; everything else is a labeled template, not a guess dressed up as a procedure.

**Status as of 2026-09-07** (live SSH/API probe of all 12 known servers — see `Infrastructure/SERVER-INVENTORY.md`): every file in this folder now has real, verified facts, though several still have genuinely unresolved unknowns (marked per-file) rather than a full tested procedure.

**The Hostinger open question from the previous pass is resolved:** Hostinger is confirmed real, with two servers now fully inventoried (`Rebuild Hostinger Server.md`). It surfaced a **new, more important open question**: the confirmed Hostinger "core" server only hosts `uat.jobfynder.com` (UAT/staging) — production's actual location is not yet confirmed anywhere in the 12 servers inventoried. See `Rebuild Hostinger Server.md` for detail; this needs a direct answer from the founder, not an assumption.

**Other things this pass found that need a decision, not just documentation:**
- `redisgateway.jobfynder.com` DNS misconfiguration (`Rebuild Cloudflare.md`) — confirmed still broken across two separate checks now.
- `comm1`'s `/opt/jobfynder-infra` checkout has uncommitted changes on a `fix/...` branch (`Recover Docker.md`) — should be committed or discarded so deployed state matches git.
- The `hermes-hermes-api-snapshot:20260801` Docker image referenced in `Restore Backup.md`'s fastest-restore path no longer exists — that restore path needs a real rebuild-from-source alternative written and tested.
