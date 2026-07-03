cd /opt/jobfynder-docs

mkdir -p scripts

cat > scripts/generate-and-persist-engineering-memory.sh <<'EOF'
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
echo "Action: Generate Hermes engineering memory and persist into Git"
echo "Hermes endpoint: $HERMES_URL"
echo "Source: ${HERMES_CONTAINER}:${SOURCE_DIR}"
echo "Destination: $DEST_DIR"

if [ ! -d "$DOCS_REPO/.git" ]; then
  echo "ERROR: Git repository not found at $DOCS_REPO"
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -qx "$HERMES_CONTAINER"; then
  echo "ERROR: Docker container '$HERMES_CONTAINER' is not running."
  exit 1
fi

echo "Action: Generate daily engineering memory"
curl -fsS -X POST "$HERMES_URL"

echo ""
echo "Verification: Hermes generation endpoint completed"

if ! docker exec "$HERMES_CONTAINER" test -d "$SOURCE_DIR"; then
  echo "ERROR: Source directory does not exist inside container: $SOURCE_DIR"
  exit 1
fi

FILE_COUNT="$(
  docker exec "$HERMES_CONTAINER" sh -c "find '$SOURCE_DIR' -maxdepth 1 -type f \( -name '*.json' -o -name '*.md' \) | wc -l" | tr -d ' '
)"

if [ "$FILE_COUNT" = "0" ]; then
  echo "ERROR: No .json or .md files found in $SOURCE_DIR"
  exit 1
fi

echo "Verification: Found $FILE_COUNT generated engineering memory files"

mkdir -p "$DEST_DIR"

echo "Action: Copy generated files into jobfynder-docs"
docker cp "${HERMES_CONTAINER}:${SOURCE_DIR}/." "$DEST_DIR/"

cd "$DOCS_REPO"

echo "Action: Sync latest Git state"
git checkout "$BRANCH"
git pull --rebase origin "$BRANCH"

echo "Action: Stage engineering memory files"
git add engineering-memory/daily

if git diff --cached --quiet; then
  echo "Verification: No new changes detected. Nothing to commit."
  exit 0
fi

COMMIT_DATE="$(date +%F)"

echo "Action: Commit engineering memory update"
git commit -m "docs(memory): update engineering memory ${COMMIT_DATE}"

echo "Action: Push to GitHub"
git push origin "$BRANCH"

echo "Verification: Engineering memory committed and pushed successfully"
git log -1 --oneline
EOF

chmod +x scripts/generate-and-persist-engineering-memory.sh