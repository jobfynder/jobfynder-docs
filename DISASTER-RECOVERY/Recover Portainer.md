# Recover Portainer

## Confirmed (live probe, 2026-09-07)

Portainer runs on both DigitalOcean droplets only — not on any Hostinger or Elest.io box:
- **`jobfynder-comm1`**: `portainer` container (portainer-ce:lts).
- **`jobfynder-intel-01`**: `portainer` (portainer-ce:lts) **and** `portainer_agent` (agent:lts) — the agent suggests `intel-01` may be managed as a remote endpoint from a Portainer instance elsewhere (possibly `comm1`'s), or is set up for that but not yet connected. Not confirmed which.

Access: not exposed publicly by default on either box's Elest.io/DO firewall config as checked; likely reached via the Nginx Proxy Manager / Tailscale rather than a raw public port. Exact URL/port not yet confirmed.

## Unknown — needs someone with live access to fill in
Whether `intel-01`'s `portainer_agent` is actually connected to a controlling Portainer instance (and if so, which one), the actual access URL/port for either instance, admin credentials location, and recovery steps if the Portainer container itself is lost (data volume location, whether it's backed up).
