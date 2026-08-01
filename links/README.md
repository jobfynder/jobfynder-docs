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
`jobfynder links` output uses aligned **markdown tables**, grouped by logical infrastructure buckets (not raw category strings), in this order:

1. **🗄 Infrastructure** — every server (ID · name · IP · role)
2. **🌐 Services — Public** — public sites + API (ID · Service · URL · IP · Access)
3. **🛠 Services — Internal (INTEL · IP)** — services running on the INTEL server (ID · Service · URL/Port · Access · Notes)
4. **🛠 Services — Internal (Other hosts)** — internal services on other hosts (ID · Service · URL · IP · Access)
5. **🌍 External** — external tools/sources (ID · Service · URL · Status · Notes)

Within each table, services are sorted alphabetically. Purpose is embedded in the Service cell (e.g. `Feedback — ProductLift portal`); ports, container names and Cloudflare flags go in Notes. This collapses the old ~130-line bullet list into ~30 lines of dense, scannable output.

```
## 🛠 Services — Internal (INTEL · 167.71.217.230)
| ID       | Service          | URL / Port     | Access   | Notes |
|----------|------------------|----------------|----------|-------|
| link-007 | Hermes Dashboard | hermes.jobfynder.com | Login | NPM proxy → :9119 |
| link-014 | Hermes API       | 127.0.0.1:8000 | Internal | container jobfynder-hermes-api |
```

## Servers
Listed under `servers[]` in the JSON; shown in the Infrastructure table at the top of `list` output.
