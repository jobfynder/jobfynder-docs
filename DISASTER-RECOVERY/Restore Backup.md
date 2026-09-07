# Restore Backup

## Confirmed real backup, still present (re-verified 2026-09-07)

`/root/jobfynder-backup` on `jobfynder-intel-01` (Hermes admin server), created 2026-08-01, still contains all originally documented files: `jobfynder-docs.bundle`, `patched-service.py`, `docker-compose.yml`, `env.bak` (chmod 600), `requirements.txt`, `RESTORE.md`.

**Staleness: this backup is now 5+ weeks old and covers only `jobfynder-docs` + the `hermes-api` container config for one server (`intel-01`).** It does not cover COMM-1, either Hostinger server, or any of the 8 Elest.io services. Given the pace of change seen in this repo's own git history (100+ commits since early August) and the Portkey→LiteLLM migration that happened after this backup was taken (`requirements.txt` still pins `portkey-ai` — see `Architecture/01-platform-architecture.md`), **treat the `jobfynder-docs.bundle` and `patched-service.py` contents as outdated, not current.** The restore *procedure* below is still structurally valid; the *artifacts* it restores are stale.

**Important — the fastest restore path in this doc no longer works:** step 4 restores from Docker image `hermes-hermes-api-snapshot:20260801`. That image **no longer exists** on `jobfynder-intel-01` as of 2026-09-07 (checked via `docker images`) — see `Restore Snapshot.md`. A restore today would need to rebuild the image from source instead of running it directly.

## The actual restore steps (pulled from `/root/jobfynder-backup/RESTORE.md` on `jobfynder-intel-01`, 2026-09-07 — no longer single-point-of-failure on the same server it recovers)

Backup dir: `/root/jobfynder-backup` · Created: 2026-08-01 · Snapshot image tag `hermes-hermes-api-snapshot:20260801` (**gone, see above**)

**What's backed up:**
| Artifact | Purpose |
|---|---|
| `jobfynder-docs.bundle` | Full git bundle of `/opt/jobfynder-docs` (tools, links, skills, patches, state) |
| `patched-service.py` | The Langfuse-instrumented `prompt_runtime/service.py` (bind-mounted into `hermes-api`) |
| `docker-compose.yml` | `hermes-api` compose config |
| `env.bak` | `.env` (chmod 600 — secrets, never commit) |
| `requirements.txt` | Pinned `langfuse` / `portkey-ai` versions — **stale, `portkey-ai` is superseded by LiteLLM** |
| Docker image `hermes-hermes-api-snapshot:20260801` | Full container snapshot with SDK + patch baked in — **no longer present** |

**Restore steps:**

1. **Restore the docs repo (bundle):**
   ```bash
   cd /opt/jobfynder-docs   # or a fresh dir
   git bundle verify /root/jobfynder-backup/jobfynder-docs.bundle
   git clone /root/jobfynder-backup/jobfynder-docs.bundle ./restored
   # or, into an existing repo:
   git bundle unbundle /root/jobfynder-backup/jobfynder-docs.bundle --all
   git reset --hard   # after unbundle into current repo
   ```
2. **Restore the patched service file:**
   ```bash
   cp /root/jobfynder-backup/patched-service.py /opt/jobfynder-docs/patches/service.py
   # bind-mounted read-only into the container at /app/app/prompt_runtime/service.py
   docker restart hermes-api
   ```
3. **Restore env (secrets):**
   ```bash
   cp /root/jobfynder-backup/env.bak /opt/jobfynder-infra/intelligence/.env
   chmod 600 /opt/jobfynder-infra/intelligence/.env
   ```
4. **Restore the container** — ~~fastest: from the snapshot image~~ **image no longer exists; rebuild from source instead**:
   ```bash
   docker run -d --name hermes-api --restart unless-stopped \
     --network intelligence_intelligence_net -p 8000:8000 \
     --env-file /opt/jobfynder-infra/intelligence/.env \
     -v /opt/jobfynder-docs:/jobfynder-docs \
     -v /opt/hermes-runtime:/hermes-runtime \
     -v /opt/jobfynder-docs/patches/service.py:/app/app/prompt_runtime/service.py:ro \
     hermes-hermes-api-snapshot:20260801   # <- this tag is gone, substitute a freshly built image
   ```
5. **Reinstall SDKs** (only if restoring into a fresh image): `docker exec hermes-api pip install langfuse portkey-ai -q` — **drop `portkey-ai`, it's no longer used.**

**Verify after restore:** `curl -s http://127.0.0.1:8000/health` → HTTP 200, and run one live prompt call to confirm a trace appears in Langfuse.

## Unknown
Whether a restore has actually been dry-run tested since 2026-08-01 (the original dry-run — bundle cloned to `/tmp`, tree matched — is real but that old), and whether any newer/broader backup exists for COMM-1, Hostinger, or the Elest.io services.
