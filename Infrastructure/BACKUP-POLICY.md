# Backup Policy

**This is partial.** Confirmed that backup automation exists; the full schedule and retention policy is not recorded anywhere in this repo.

## Confirmed

- Volume backup automation was identified as missing during a 2026-08-21 inspection of COMM-1 and was fixed the same day (commit `0c33580`) — see `CHANGELOG.md`.
- Prior to that fix, COMM-1 had no backup automation at all. Treat anything older than 2026-08-21 as unrecoverable if it wasn't backed up some other way.

## Unknown — needs someone with live access to fill in

- Backup frequency and retention period
- What's actually included (database only? volumes? configuration?)
- Where backups are stored and whether that storage is itself tested for restore
- Whether INTEL-1 has the same backup coverage as COMM-1, or whether this fix was COMM-1-specific
