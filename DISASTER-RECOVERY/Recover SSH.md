# Recover SSH

## Confirmed — per-provider fallback if SSH/keys are lost (tested 2026-09-07)

Every provider hosting Jobfynder infrastructure has its own out-of-band console that doesn't depend on SSH keys at all:

- **Elest.io**: dashboard → service → **"Open terminal"** (AI DevOps panel) gives a browser-based shell without needing SSH access. Also: Security → Manage SSH Keys to add a new key directly, no existing access required.
- **DigitalOcean**: droplet → **Web Console** gives a real login prompt (needs the root password — trigger `doctl compute droplet-action password-reset` first if it's unknown, then log in and run `ssh-import-id gh:jobfynder-admin` to restore key-based access in one step, no reboot). A separate **Recovery Console** (boot from Recovery ISO) exists but its rescue/chroot environment has no working network, so `ssh-import-id` fails there — use the Web Console path instead. Full procedure in `Infrastructure/SSH-STANDARDS.md`.
- **Hostinger**: hPanel → VPS → **Web console** — same pattern, root password (resettable from the same VPS overview page) gets you in without SSH.

So: Tailscale SSH is the access pattern for `jobfynder-intel-01` specifically (and the Hermes WebUI per the original note), but it is **not** the sole access path for every server — every provider's own web console is the actual fallback of last resort, and doesn't depend on Tailscale, SSH keys, or `authorized_keys` being intact at all.

**Where keys are kept:** `~/.ssh/elestio_jobfynder` (ed25519) on the machine documented in `Infrastructure/SSH-STANDARDS.md`, and the matching public key registered on the `jobfynder-admin` GitHub account for `ssh-import-id` recovery. No separate "emergency" key exists beyond this — if this key and this machine are both lost, recovery goes through each provider's web console + password reset instead.

## Unknown — needs someone with live access to fill in
Whether any *other* machine/person also holds a working key to these servers (several pre-existing keys were found during this pass — `jobfynder-windows-hermes-DESKTOP-CAFG7FL`, `hermes-vault`, `jonathan-support@elestio`, `github-actions-benchteq-espocrm`, `my-laptop` — but their private-key holders and current validity aren't confirmed).
