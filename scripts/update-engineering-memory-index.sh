#!/usr/bin/env bash
set -euo pipefail

DOCS_REPO="${DOCS_REPO:-/opt/jobfynder-docs}"
DAILY_DIR="$DOCS_REPO/engineering-memory/daily"
README_FILE="$DOCS_REPO/engineering-memory/README.md"
INDEX_FILE="$DAILY_DIR/_index.json"
LATEST_MD="$DAILY_DIR/LATEST.md"
LATEST_JSON="$DAILY_DIR/LATEST.json"

echo "Repository: jobfynder-docs"
echo "File: scripts/update-engineering-memory-index.sh"
echo "Action: Update engineering memory index"

mkdir -p "$DAILY_DIR"

LATEST_DATE="$(
  find "$DAILY_DIR" -maxdepth 1 -type f -name '????-??-??.md' \
    | sed 's#.*/##' \
    | sed 's#\.md$##' \
    | sort \
    | tail -n 1
)"

if [ -z "$LATEST_DATE" ]; then
  echo "ERROR: No daily markdown memory files found"
  exit 1
fi

SOURCE_MD="$DAILY_DIR/$LATEST_DATE.md"
SOURCE_JSON="$DAILY_DIR/$LATEST_DATE.json"

if [ ! -f "$SOURCE_MD" ]; then
  echo "ERROR: Missing $SOURCE_MD"
  exit 1
fi

if [ ! -f "$SOURCE_JSON" ]; then
  echo "ERROR: Missing $SOURCE_JSON"
  exit 1
fi

cp "$SOURCE_MD" "$LATEST_MD"
cp "$SOURCE_JSON" "$LATEST_JSON"

python3 - "$DAILY_DIR" "$INDEX_FILE" "$README_FILE" "$LATEST_DATE" <<'PY'
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

daily_dir = Path(sys.argv[1])
index_file = Path(sys.argv[2])
readme_file = Path(sys.argv[3])
latest_date = sys.argv[4]

entries = []

for md_path in sorted(daily_dir.glob("????-??-??.md")):
    date = md_path.stem
    json_path = daily_dir / f"{date}.json"
    if json_path.exists():
        entries.append({
            "date": date,
            "markdown_path": f"engineering-memory/daily/{date}.md",
            "json_path": f"engineering-memory/daily/{date}.json"
        })

index = {
    "name": "Jobfynder Engineering Memory Index",
    "repository": "jobfynder-docs",
    "latest_date": latest_date,
    "latest_markdown_path": "engineering-memory/daily/LATEST.md",
    "latest_json_path": "engineering-memory/daily/LATEST.json",
    "daily_directory": "engineering-memory/daily",
    "entry_count": len(entries),
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "entries": entries
}

index_file.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

readme = f"""# Jobfynder Engineering Memory

This directory stores Hermes-generated engineering memory.

Latest date: {latest_date}

Latest Markdown: engineering-memory/daily/LATEST.md

Latest JSON: engineering-memory/daily/LATEST.json

Index: engineering-memory/daily/_index.json

Daily files are stored in: engineering-memory/daily/

Main script: scripts/generate-and-persist-engineering-memory.sh

Index script: scripts/update-engineering-memory-index.sh
"""

readme_file.write_text(readme, encoding="utf-8")
PY

echo "Verification: Updated LATEST.md"
echo "Verification: Updated LATEST.json"
echo "Verification: Updated _index.json"
echo "Verification: Updated README.md"
