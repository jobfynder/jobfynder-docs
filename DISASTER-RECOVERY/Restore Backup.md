# Restore Backup

## Confirmed real backup, tested

A backup was created 2026-08-01 at `/root/jobfynder-backup` on the Hermes admin server, containing: `jobfynder-docs.bundle`, `patched-service.py`, `docker-compose.yml`, `env.bak` (chmod 600), `requirements.txt`, and a `RESTORE.md` with the actual restore steps.

**A restore dry-run already passed**: the bundle was cloned to `/tmp` and the resulting tree matched. That's real, verified evidence this backup is usable — not just that it exists.

## Where the real restore steps live

**Not in this repo.** They're in `/root/jobfynder-backup/RESTORE.md` on the server itself. If that file is ever lost, this doc becomes the only trace that a real, tested restore procedure once existed — worth pulling a copy of `RESTORE.md` into this repo so it isn't single-point-of-failure on the same server it's meant to help recover.

## Unknown

Whether this backup is still current (created 2026-08-01 — check how stale it is relative to today), whether it covers anything beyond `jobfynder-docs` and one server, and whether a restore has been dry-run tested since.
