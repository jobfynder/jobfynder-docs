# Restore Snapshot

## Two different kinds of "snapshot" exist — don't conflate them

**1. DigitalOcean droplet snapshots** (confirmed live via `doctl compute snapshot list`, 2026-09-07) — 13 full-droplet snapshots exist, spanning 2026-06-30 to 2026-09-01:

| Snapshot | Droplet | Date |
|---|---|---|
| `COMM1-GOLDEN-BASELINE-2026-06-30`, `INTEL1-GOLDEN-BASELINE-2026-06-30` | both | 2026-06-30 |
| `INTEL1-Hermes-v0.2-Baseline` | INTEL-1 | 2026-07-02 |
| `Jobfynder-Engineering-Memory-Module_Production-Baseline` | INTEL-1 | 2026-07-04 |
| `intel-hermes-public-admin-telegram-bots-working-2026-07-05` | INTEL-1 | 2026-07-05 |
| `HERMES-200` / `-300`(named `Hermes-300`) / `-500` / `-600` / `-700` | INTEL-1 | 2026-07-06 to 07-07 |
| `COMM-1-telegram-integration` (×2, one on each droplet) | both | 2026-07-11 |
| `jobfynder-intel-01-HERMES-CORE` | INTEL-1 | 2026-09-01 |

These are **manual milestone snapshots**, not an automated schedule — mostly tracking Hermes development milestones, two only for COMM-1. Restore via DigitalOcean dashboard/API (new droplet from snapshot, or in-place restore — the latter destroys current disk state). Not tested as an actual restore in this pass.

**2. The `hermes-hermes-api-snapshot:20260801` Docker image** described in `Restore Backup.md` — **checked 2026-09-07 and no longer present** on `jobfynder-intel-01` (`docker images` shows nothing matching). The backup's documented "fastest restore" path (run a container directly from this image) is **no longer available** — restoring `hermes-api` today would have to go through a normal image build/pull instead. See `Restore Backup.md` for the rest of that backup's contents, which are still present.

## Unknown — needs someone with live access to fill in
An actual tested droplet-snapshot restore, and whether Elest.io or Hostinger have their own snapshot/backup mechanisms beyond what's noted in `Infrastructure/SERVER-INVENTORY.md` (Hostinger hPanel shows "2 snapshots" per VPS and a weekly schedule — not yet inspected in detail).
