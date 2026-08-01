# Jobfynder Tools Registry

This is the canonical registry of external tools/software used across Jobfynder operations.

## File
- `jobfynder-tools.json` — the registry data (git-tracked, full history in this repo).

## Conventions
- **Adding a tool:** when Pulse references `tool: <url> : <description>`, add it to `jobfynder-tools.json` with an auto-incremented `tool-00X` id, the URL, category, and description, then update the `updated` timestamp and commit.
- **Listing tools:** when asked "jobfynder tools list" (or similar), output every tool currently in `jobfynder-tools.json`.

## Tools
See `jobfynder-tools.json`.
