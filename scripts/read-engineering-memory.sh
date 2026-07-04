#!/usr/bin/env bash
set -euo pipefail

DOCS_REPO="${DOCS_REPO:-/opt/jobfynder-docs}"
MEMORY_DIR="$DOCS_REPO/engineering-memory/daily"

LATEST_MD="$MEMORY_DIR/LATEST.md"
LATEST_JSON="$MEMORY_DIR/LATEST.json"
INDEX_JSON="$MEMORY_DIR/_index.json"

echo "Repository: jobfynder-docs"
echo "File: scripts/read-engineering-memory.sh"
echo "Action: Read latest engineering memory"
echo ""

if [ ! -f "$LATEST_MD" ]; then
  echo "ERROR: Missing $LATEST_MD"
  exit 1
fi

if [ ! -f "$LATEST_JSON" ]; then
  echo "ERROR: Missing $LATEST_JSON"
  exit 1
fi

if [ ! -f "$INDEX_JSON" ]; then
  echo "ERROR: Missing $INDEX_JSON"
  exit 1
fi

echo "Latest Markdown:"
echo "$LATEST_MD"
echo ""

cat "$LATEST_MD"

echo ""
echo "Verification: Latest engineering memory read successfully"
