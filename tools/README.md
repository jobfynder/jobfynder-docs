# Jobfynder Tools Registry

This is the canonical registry of external tools/software used across Jobfynder operations.

## File
- `jobfynder-tools.json` — the registry data (git-tracked, full history in this repo).

## Conventions
- **Adding a tool:** when Pulse references `tool: <url> : <description>`, add it to `jobfynder-tools.json` with the URL, category, and description, then update the `updated` timestamp and commit. IDs are auto-assigned (`tool-001`, `tool-002`, …) and re-indexed when the list is sorted.
- **Listing tools:** when asked "jobfynder tools list" (or similar), list every tool currently in `jobfynder-tools.json` using the canonical format below.

## Canonical display format
When listing tools, use this exact format per tool (URL without `https://` or trailing slash):

```
tool-002
• Tool: BrightData
• URL: brightdata.com
• Category: Web Scraping

Description: Anti-bot scraping, proxies & data collection
```

Group tools by category (category heading first, e.g. `## Web Scraping`), tools sorted alphabetically within each category, categories sorted alphabetically.

## Tools
See `jobfynder-tools.json`.
