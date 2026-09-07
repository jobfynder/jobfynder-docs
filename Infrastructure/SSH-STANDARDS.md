# SSH Access Standards

**Status:** Established 2026-09-07 while setting up server access on a new laptop. Follow this for any new server or new machine going forward.

## Key policy

- One dedicated keypair per **machine**, not per service: `~/.ssh/elestio_jobfynder` (ed25519), comment `claude-code-monitoring@jobfynder`.
- Never reuse or extract another machine's private key. Never paste a private key into chat/logs if it can be avoided — if a key was pasted in a session by mistake, treat it as compromised and rotate it.
- Public key to distribute when granting access to a new server:
  ```
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH3TjqKpwTe+E8FFUyyWKFL6Ci3FdEUtiYcmB6MPVBK+ claude-code-monitoring@jobfynder
  ```
- Same public key is also registered on the `jobfynder-admin` GitHub account (`gh ssh-key list`) — this lets any server pull it via `ssh-import-id gh:jobfynder-admin` instead of pasting the raw key string into a console (avoids error-prone manual typing when clipboard paste isn't available).

## `~/.ssh/config` convention

Every server gets a short `Host` alias — never SSH by raw IP in day-to-day use. See the current file for the full list; pattern:
```
Host <service-or-droplet-name>
    HostName <ip>
    User root
    IdentityFile ~/.ssh/elestio_jobfynder
```

## How to add access, per provider

### Elest.io
Dashboard → service → **Security** tab → **Manage SSH Keys** → **Add key** (title + key body only, no comment suffix — the form rejects a trailing comment). Takes effect immediately, no reboot.

### DigitalOcean
DO does **not** support adding a key to an already-running droplet via the API/dashboard the way Elest.io does — a new account-level key (`doctl compute ssh-key create`) only auto-installs on droplets created *after* it's added. For an existing droplet with no working key/password:

1. **Do not** use `doctl compute droplet-action password-reset` + regular `ssh` — DigitalOcean images have `PasswordAuthentication no` in sshd by default, so a reset root password will not work over normal SSH (only via the Droplet Console, and it forces an immediate password change — avoid this if the box has other integrations that might assume the password stays fixed, though in practice nothing should depend on the literal OS root password).
2. **Working method:** Droplet → **Web Console** (not Recovery Console) → log in with the temp password from `password-reset` → when forced to set a new password, set anything → run `ssh-import-id gh:jobfynder-admin` → done, no reboot needed. The live system has real network access so this always works in one shot.
3. The **Recovery ISO** route (Settings → Recovery mode → Boot from Recovery ISO → power-cycle → Recovery Console → mount + chroot) was attempted first and technically avoids ever touching the root password, but the chroot environment has no working DNS/network, so `ssh-import-id` fails silently there. Not recommended unless the Web Console route is unavailable for some reason.
4. Always revert **Recovery mode** back to "Boot from Hard Drive" and power-cycle back if you used the Recovery ISO route, or the droplet will keep booting into rescue mode.

### Tailscale SSH (exception: `jobfynder-intel-01`)
`jobfynder-intel-01` already has Tailscale SSH enabled (`tailscale up --ssh` was run on it previously) and the tailnet ACL permits `root`. This means:
- `ssh root@intel` (or its Tailscale IP) works with **zero keys** — auth is via Tailscale's own identity, gated by tailnet policy, not `authorized_keys`.
- It does **not** currently permit the local Windows account name (e.g. `DELL`) — only `root` is allowed by policy.
- This is a *better* pattern than public-IP key auth where available (no public-facing SSH needed at all) — consider enabling Tailscale SSH on other droplets/servers instead of managing keys, once each one's tailnet ACL is reviewed.
- `jobfynder-comm1` is on the same tailnet but does **not** have Tailscale SSH enabled — it uses normal key-based auth on its public IP instead.

## Verifying access after any change
```
ssh <alias> "hostname && uptime"
```
Run this for every server touched in a session before considering the task done — do not report "access set up" without a live probe.
