#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="jobfynder-docs"
DOCS_REPO="${DOCS_REPO:-/opt/jobfynder-docs}"
BRANCH="${BRANCH:-main}"

HERMES_CONTAINER="${HERMES_CONTAINER:-hermes-api}"
HERMES_URL="${HERMES_URL:-http://localhost:8000/v1/engineering-memory/generate}"

SOURCE_DIR="${SOURCE_DIR:-/tmp/engineering-memory/daily}"
DEST_DIR="${DEST_DIR:-$DOCS_REPO/engineering-memory/daily}"

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

echo "Action: Generate daily engineering memory from Hermes"
curl -fsS -X POST "$HERMES_URL" || {
  echo "ERROR: Hermes generation endpoint failed"
  exit 1
}

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
