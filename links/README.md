# Jobfynder Links Registry

Canonical reference hub for all URLs, hosts, services and access details across the Jobfynder ecosystem.

## Files
- `links/jobfynder-links.json` — the link + server data (git-tracked, full history in this repo).
- `scripts/jobfynder-links.py` — management CLI (`list`, `add`, `check`, `reindex`).

## Data model

### Top-level sections
- `servers[]` — known servers (id, name, hostname, ip, role, region).
- `links[]` — every registered link.

### Link fields
| Field | Required | Description |
|-------|----------|-------------|
| `id` | ✅ | Auto-assigned `link-00X`, re-indexed on sort |
| `name` | ✅ | Short human-readable name |
| `url` | ✅ | Full URL (https://…) |
| `category` | ✅ | API / Public Site / External Source / External Tool / Internal |
| `purpose` | ✅ | What it is / why it exists |
| `status` | ✅ | active / configured / blocked / deprecated |
| `ip` | ⭐ | Resolved IP (when applicable, e.g. web hosts) |
| `subcategory` | ⭐ | Finer grouping (e.g. CRM, Search, DevOps) |
| `access` | ⭐ | How you get in (Public / Login / API key / Internal) |
| `server` | ⭐ | Server id (`srv-00X`) when the link runs on a known server |
| `note` | ⭐ | Extra context (Cloudflare, backends, container names) |

## Conventions
- **Adding a link:** when Pulse references `link: <url> - <description>` (or similar), add it to `jobfynder-links.json`, dedupe by URL, auto-assign id, re-sort by category/name, update the `updated` timestamp, then commit.
- **Listing links:** when asked "jobfynder links" / "list the links" / "listout the links", output every link using the Canonical display format below.

## Canonical display format
Group by category (heading first), links alphabetical within category, categories in this order: **🔌 API → 🌐 Public Site → 🌍 External Source → 🧩 External Tool → 🛠 Internal**. Include the optional lines (`IP`, `Server`, `Access`) only when present in the JSON.

```
🔌 API

link-005
• Name: Jobfynder Core API
• URL: api.jobfynder.com
• Category: API
• Purpose: Jobfynder core API (JOBFYNDER_CORE_API_URL)
• Status: configured
```

Example with optional fields:

```
🛠 Internal

link-007
• Name: Hermes Dashboard
• URL: hermes.jobfynder.com
• Category: Internal
• Purpose: Hermes Agent web dashboard (INTEL server)
• IP: 167.71.217.230
• Server: srv-001 (hermes.jobfynder.com)
• Access: Login required
• Status: active
```

## Servers
Listed under `servers[]` in the JSON; summarized at the top of `list` output.
