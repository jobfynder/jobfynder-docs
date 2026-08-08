# Hermes Runtime Sweep — 2026-08-08

**Why:** User reported lost confidence — "Hermes always having issues with tools, no consistency, self-learning not working."
**Method:** Every finding below was produced by my own live `hermes`/`ls`/`git` probes this session (ground truth, not relayed claims).

---

## 1. What is actually healthy
- **`hermes doctor`** — all core checks pass (Python 3.11.15, SSL, packages, config v33, no deprecated keys, no advisories).
- **Gateway(s):** `hermes-gateway.service` running; `hermes-admin-gateway`, `hermes-sourcing-gateway`, `hermes-dashboard` all active.
- **Cron scheduler:** running, heartbeat OK.
- **Daily AI-Infra cron:** repaired + verified (manual run `dd3b7c4e...` completed). Root cause was script path (see §4).

## 2. The "self-learning" gap — ROOT CAUSE
- `hermes doctor` reported: **"Memory tool: disabled ✗"** and "MEMORY.md not created yet."
- `config.yaml` line 25: `memory` was listed under **`agent.disabled_toolsets`** → the memory tool was disabled at the config level.
- **FIXED:** ran `hermes config set agent.disabled_toolsets '[...]'` **without** `memory`. Verified via python yaml load: `memory in disabled_toolsets: False`.
- Also confirmed `memory_enabled: true`, `user_profile_enabled: true`, provider `holographic`, and `memory_append` script (below) as the durable write path.

## 3. Directory confusion (why things silently break)
- **Two Hermes homes exist:** `/root/.hermes` and `/root/.hermes-admin`.
  - Active profile root: `/root/.hermes-admin` (doctor, status, config all use it).
  - `/root/.hermes` also has `.env`, `SOUL.md`, and a `/root/.hermes/memories/` with MEMORY.md + USER.md (older copy).
- **Cron scripts:** runner reads `/root/.hermes-admin/scripts/`. The daily status script now lives there (was mistakenly in `/root/.hermes/scripts/` → all 4 runs failed "Script not found").
- **Memory stores found:**
  - `/root/.hermes-admin/MEMORY.md` (active, 1950 bytes)
  - `/root/.hermes/memories/MEMORY.md`, `/root/.hermes/memories/USER.md` (older)
  - `/root/.hermes-admin/profiles/sourcing/memories/{MEMORY.md,USER.md}` (sourcing bot)
  - `/root/vault/work/meta/engineering-memory.md` (git-tracked, canonical — verified, committed)
- **Stray/empty artifact:** `/root/.hermes-admin/scripts/daily-hermes-tips.sh` is **0 bytes** — looks "configured but empty." Flagged for repair/removal.

## 4. Memory mechanism fix (permanent)
Created **`/root/.hermes-admin/scripts/memory-append.py`** — the durable self-learn write path:
- Appends a timestamped `## Learned (YYYY-MM-DD) - [kind] <text>` block to the canonical `/root/vault/work/meta/engineering-memory.md`.
- `git -C /root/vault add/commit`s automatically.
- Mirrors a short line into Hermes MEMORY.md (active + older) when writable.
- Usage: `memory-append.py --kind memory|user|lesson --text "..."`.
- **Tested:** appended a lesson, verified commit `528f9be` and file growth. Loop closes.

## 5. Reliability rule (fixes the "consistency" complaint)
Encode in MEMORY.md (inherited by every session):
> State "verified by my probe" or "per report, unverified" for every status. Never relay an unverified "ISSUE RESOLVED" to the user.

## 6. Context-corruption mitigation
Garbled/duplicated context blocks this session came from context bloat. Use `hermes sessions` deliberately; start a fresh session when a task stream ends.

---

## Actions taken this sweep (permanent)
1. ✅ Enabled memory tool (removed from `disabled_toolsets` via CLI).
2. ✅ Created + tested `memory-append.py` self-learning write path (commits to vault).
3. ✅ Documented the two-Hermes-home directory map.
4. ⏳ Daily-hermes-tips.sh is 0 bytes — needs repair or removal (noted).
5. ⏳ Memory-tool enable may require a gateway restart to show as enabled in a fresh session (config saved; runtime reads at startup).
