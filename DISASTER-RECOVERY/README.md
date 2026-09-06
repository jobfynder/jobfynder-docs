# Disaster Recovery

Runbooks for recovering platform components after a failure. Every file here follows the same honesty rule as `Infrastructure/`: real, sourced facts are marked as such; everything else is a labeled template, not a guess dressed up as a procedure.

**Only one file has a real, tested procedure behind it right now: `Restore Backup.md`** — a 2026-08-01 backup with a passed restore dry-run. Everything else here needs someone with live server access to turn from a template into an actual runbook.

**One open question this pass surfaced:** `Rebuild Hostinger Server.md` references a hosting provider that appears nowhere else in this entire repo. Worth a direct answer before assuming it's stale.
