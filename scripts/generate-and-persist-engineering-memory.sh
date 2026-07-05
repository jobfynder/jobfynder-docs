#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="jobfynder-docs"
DOCS_REPO="${DOCS_REPO:-/opt/jobfynder-docs}"
BRANCH="${BRANCH:-main}"

HERMES_CONTAINER="${HERMES_CONTAINER:-hermes-api}"
HERMES_URL="${HERMES_URL:-http://localhost:8000/v1/engineering-memory/generate}"
HERMES_AUTH_TOKEN_FILE="${HERMES_AUTH_TOKEN_FILE:-/root/hermes-n8n-token.txt}"

SOURCE_DIR="${SOURCE_DIR:-/tmp/engineering-memory/daily}"
DEST_DIR="${DEST_DIR:-$DOCS_REPO/engineering-memory/daily}"

GITHUB_EVENT_FILE="${GITHUB_EVENT_FILE:-}"
GITHUB_EVENT_JSON="${GITHUB_EVENT_JSON:-}"
GITHUB_EVENT_B64="${GITHUB_EVENT_B64:-}"

PAYLOAD_FILE="/tmp/engineering-memory-github-event.json"
PROCESSED_EVENTS_FILE="$DOCS_REPO/engineering-memory/events/_processed-events.txt"
DEDUP_KEY=""

echo "Repository: $REPO_NAME"
echo "File: scripts/generate-and-persist-engineering-memory.sh"
echo "Action: Generate Hermes engineering memory, persist files into jobfynder-docs, commit, and push"
echo "Hermes container: $HERMES_CONTAINER"
echo "Hermes endpoint: $HERMES_URL"
echo "Source: ${HERMES_CONTAINER}:${SOURCE_DIR}"
echo "Destination: $DEST_DIR"
echo ""

if [ ! -d "$DOCS_REPO/.git" ]; then
  echo "ERROR: Git repository not found at $DOCS_REPO"
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -qx "$HERMES_CONTAINER"; then
  echo "ERROR: Docker container '$HERMES_CONTAINER' is not running."
  exit 1
fi

cd "$DOCS_REPO"

echo "Action: Pull latest Git state"
git pull --rebase origin "$BRANCH"

mkdir -p "$DOCS_REPO/engineering-memory/events"

if [ -n "$GITHUB_EVENT_FILE" ] && [ -f "$GITHUB_EVENT_FILE" ]; then
  echo "Input mode: GitHub event file"
  cp "$GITHUB_EVENT_FILE" "$PAYLOAD_FILE"
elif [ -n "$GITHUB_EVENT_B64" ]; then
  echo "Input mode: GitHub event base64"
  printf '%s' "$GITHUB_EVENT_B64" | base64 -d > "$PAYLOAD_FILE"
elif [ -n "$GITHUB_EVENT_JSON" ]; then
  echo "Input mode: GitHub event JSON"
  printf '%s' "$GITHUB_EVENT_JSON" > "$PAYLOAD_FILE"
else
  echo "Input mode: local repository scan"
  rm -f "$PAYLOAD_FILE"
fi

if [ -f "$PAYLOAD_FILE" ]; then
  python3 -m json.tool "$PAYLOAD_FILE" >/dev/null

  DEDUP_KEY="$(
    python3 - "$PAYLOAD_FILE" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    payload = json.load(f)

repo = payload.get("repository", {}).get("full_name", "unknown")
ref = payload.get("ref", "unknown")
after = payload.get("after") or payload.get("head_commit", {}).get("id") or "unknown"

print(f"{repo}|{ref}|{after}")
PY
  )"

  echo "Dedup key: $DEDUP_KEY"

  touch "$PROCESSED_EVENTS_FILE"

  if grep -Fxq "$DEDUP_KEY" "$PROCESSED_EVENTS_FILE"; then
    echo "Verification: Duplicate GitHub event already processed. Skipping memory generation."
    exit 0
  fi
fi

echo "Action: Generate daily engineering memory from Hermes"

if [ ! -f "$HERMES_AUTH_TOKEN_FILE" ]; then
  echo "ERROR: Hermes auth token file not found: $HERMES_AUTH_TOKEN_FILE"
  exit 1
fi

HERMES_AUTH_TOKEN="$(tr -d '\r\n' < "$HERMES_AUTH_TOKEN_FILE")"

if [ -z "$HERMES_AUTH_TOKEN" ]; then
  echo "ERROR: Hermes auth token is empty"
  exit 1
fi

if [ -f "$PAYLOAD_FILE" ]; then
  curl -fsS -X POST "$HERMES_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $HERMES_AUTH_TOKEN" \
    --data-binary @"$PAYLOAD_FILE" || {
      echo "ERROR: Hermes generation endpoint failed"
      exit 1
    }
else
  curl -fsS -X POST "$HERMES_URL" \
    -H "Authorization: Bearer $HERMES_AUTH_TOKEN" || {
    echo "ERROR: Hermes generation endpoint failed"
    exit 1
  }
fi

echo ""
echo "Verification: Hermes generation endpoint completed"
echo ""

if ! docker exec "$HERMES_CONTAINER" test -d "$SOURCE_DIR"; then
  echo "ERROR: Source directory does not exist inside container: $SOURCE_DIR"
  exit 1
fi

SOURCE_FILE_COUNT="$(
  docker exec "$HERMES_CONTAINER" sh -c "find '$SOURCE_DIR' -maxdepth 1 -type f \( -name '*.json' -o -name '*.md' \) | wc -l" | tr -d ' '
)"

if [ "$SOURCE_FILE_COUNT" = "0" ]; then
  echo "ERROR: No .json or .md files found in $SOURCE_DIR"
  exit 1
fi

echo "Verification: Found $SOURCE_FILE_COUNT generated files inside Hermes container"

echo "Action: Create destination directory"
mkdir -p "$DEST_DIR"

echo "Action: Copy generated files into jobfynder-docs"
docker cp "${HERMES_CONTAINER}:${SOURCE_DIR}/." "$DEST_DIR/"

echo "Action: Update engineering memory index"
"$DOCS_REPO/scripts/update-engineering-memory-index.sh"

DEST_FILE_COUNT="$(
  find "$DEST_DIR" -maxdepth 1 -type f \( -name '*.json' -o -name '*.md' \) | wc -l | tr -d ' '
)"

if [ "$DEST_FILE_COUNT" = "0" ]; then
  echo "ERROR: Copy failed. No .json or .md files found in $DEST_DIR"
  exit 1
fi

if [ -n "$DEDUP_KEY" ]; then
  echo "Action: Record processed GitHub event"
  touch "$PROCESSED_EVENTS_FILE"
  grep -Fxq "$DEDUP_KEY" "$PROCESSED_EVENTS_FILE" || echo "$DEDUP_KEY" >> "$PROCESSED_EVENTS_FILE"
fi

echo "Verification: Found $DEST_FILE_COUNT files in $DEST_DIR"
ls -la "$DEST_DIR"
echo ""

echo "Action: Stage engineering memory files"
git add engineering-memory scripts/generate-and-persist-engineering-memory.sh scripts/update-engineering-memory-index.sh

if git diff --cached --quiet; then
  echo "Verification: No new engineering memory changes detected. Nothing to commit."
  exit 0
fi

COMMIT_DATE="$(date +%F)"

echo "Action: Commit engineering memory update"
git commit -m "docs(memory): update engineering memory ${COMMIT_DATE}"

echo "Action: Push engineering memory update to GitHub"
git push origin "$BRANCH"

echo "Verification: Engineering memory committed and pushed successfully"
git log -1 --oneline
