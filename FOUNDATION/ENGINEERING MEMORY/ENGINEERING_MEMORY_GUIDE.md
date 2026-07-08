# Engineering Memory Module Guide

Status: Production-ready baseline  
Audience: Jobfynder team, developers, operations, and future maintainers

---

## 1. What Is Engineering Memory?

Engineering Memory is a simple system that remembers important engineering activity automatically.

Think of it like a daily engineering diary for Jobfynder.

Whenever code changes are pushed to GitHub, the system records:

- Which repository changed
- Which branch changed
- Which commit was pushed
- Who triggered the change
- What files changed
- What Engineering Memory was generated
- Whether the automation succeeded or failed

This helps us avoid losing technical context as Jobfynder grows.

---

## 2. Why We Built It

Before Engineering Memory, important infrastructure work could easily be forgotten inside chats, terminals, n8n executions, or GitHub commits.

Engineering Memory solves this by creating a permanent reference trail.

It helps us answer:

- What changed today?
- Which repository triggered the automation?
- What was the latest engineering update?
- Did the automation run successfully?
- What GitHub event caused a memory entry?
- If something failed, did we get alerted?

The goal is simple:

> Jobfynder should remember its own engineering progress.

---

## 3. The Main Idea

```text
GitHub push happens
→ n8n receives it
→ Hermes understands it
→ jobfynder-docs stores it
→ Telegram and Email alert us if something fails
```

---

## 4. Main Components

### GitHub

GitHub stores our code.

When code is pushed to a connected repository, GitHub sends a webhook event to n8n.

Connected repositories:

- `jobfynder/hermes`
- `jobfynder/jobfynder-infra`
- `jobfynder-admin/jobFynder-BE-nest.JS`
- `jobfynder-admin/jobFynder-FE-vite`
- `jobfynder/jobfynder-docs`

### n8n

n8n is the automation runner.

Main workflow:

```text
Engineering Memory GitHub Webhook
```

It does four things:

1. Checks the webhook token.
2. Prevents infinite loops from `jobfynder-docs`.
3. Archives the full GitHub event.
4. Runs the Engineering Memory generation script.

### Hermes

Hermes is the intelligence service.

Hermes receives the GitHub event and creates Engineering Memory from:

- Repository name
- Branch
- Commit SHA
- Commit message
- Author
- Changed files

Hermes creates:

- A JSON memory file
- A Markdown memory file

### jobfynder-docs

`jobfynder-docs` is the permanent storage place for Engineering Memory.

Important folders and files:

```text
engineering-memory/daily/
engineering-memory/events/
engineering-memory/MODULE_CLOSURE.md
engineering-memory/ENGINEERING_MEMORY_GUIDE.md
```

---

## 5. Workflow Explained Simply

### Step 1: A developer pushes code

Example:

```bash
git push origin main
```

GitHub sees the new code push.

### Step 2: GitHub sends a webhook to n8n

GitHub sends the push details to:

```text
Engineering Memory GitHub Webhook
```

The webhook includes:

- Repository name
- Branch
- Commit ID
- Commit message
- Changed files
- Sender

### Step 3: n8n checks the token

The webhook URL includes a security token.

If the token is wrong, the workflow stops.

This prevents random outside requests from triggering Engineering Memory.

### Step 4: n8n prevents loops

The system ignores direct memory commits from:

```text
jobfynder/jobfynder-docs
```

This is important because Engineering Memory itself commits files into `jobfynder-docs`.

Without loop prevention, this could happen forever:

```text
Memory commit → webhook → memory commit → webhook → memory commit
```

Loop prevention stops that.

### Step 5: n8n archives the GitHub event

The full GitHub event is saved into:

```text
engineering-memory/events/
```

Example:

```text
engineering-memory/events/20260704T075303Z-github-event.json
```

This helps us debug later because we can see exactly what GitHub sent.

### Step 6: n8n sends the GitHub payload to Hermes

n8n sends the webhook payload to Hermes.

Hermes creates repo-aware Engineering Memory.

Repo-aware means Hermes knows which repository triggered the memory.

Example:

```text
Source: GitHub webhook
Repository: jobfynder/hermes
Branch: main
Head SHA: 2a9c370
Commit count: 1
```

### Step 7: Hermes generates memory files

Hermes creates files inside the Hermes container:

```text
/tmp/engineering-memory/daily/
```

The files look like:

```text
YYYY-MM-DD.json
YYYY-MM-DD.md
```

The JSON file is structured data.  
The Markdown file is easy for humans to read.

### Step 8: The script copies files into jobfynder-docs

The persistence script copies the generated files into:

```text
/opt/jobfynder-docs/engineering-memory/daily/
```

Then it updates:

```text
engineering-memory/daily/LATEST.md
engineering-memory/daily/LATEST.json
engineering-memory/daily/_index.json
```

### Step 9: jobfynder-docs commits and pushes the update

The system commits the memory update to GitHub.

Example commit:

```text
docs(memory): update engineering memory 2026-07-04
```

Now the memory is permanently saved.

---

## 6. Deduplication Guard

Deduplication prevents the same GitHub event from creating repeated memory commits.

Each GitHub event gets a deduplication key:

```text
repository|branch|commit_sha
```

Example:

```text
jobfynder/hermes|refs/heads/main|2a9c370ca349bff0d7708e3a53f65ee8cb84d485
```

Processed keys are stored in:

```text
engineering-memory/events/_processed-events.txt
```

If the same event is processed again, the script skips it:

```text
Duplicate GitHub event already processed. Skipping memory generation.
```

This protects us from duplicate commits caused by retries or repeated webhook runs.

---

## 7. Failure Alerts

Failure alerting is handled by:

```text
Engineering Memory Failure Alerts
```

If the main workflow fails, this alert workflow sends messages to:

- Telegram
- Email

The alert includes:

- Workflow name
- Execution ID
- Failed node
- Error message
- Execution URL
- Execution mode

Example:

```text
Jobfynder Engineering Memory Automation Failed

Workflow: Engineering Memory GitHub Webhook
Execution ID: 231
Failed Node: SSH
Error: Example error message
Execution URL: https://connect.jobfynder.com/execution/workflow/1/231
Mode: trigger
```

This means failures should not go unnoticed.

---

## 8. Important Scripts

### Memory generation and persistence script

```text
scripts/generate-and-persist-engineering-memory.sh
```

This script:

1. Pulls latest `jobfynder-docs`
2. Receives GitHub event input
3. Checks deduplication
4. Calls Hermes
5. Copies generated memory files
6. Updates latest and index files
7. Commits and pushes the memory update

### Memory index script

```text
scripts/update-engineering-memory-index.sh
```

This updates:

```text
LATEST.md
LATEST.json
_index.json
```

### Memory reader script

```text
scripts/read-engineering-memory.sh
```

This helps read the latest Engineering Memory from the server.

---

## 9. Important Files

### Latest daily memory

```text
engineering-memory/daily/LATEST.md
```

This is the easiest file to read.

### Latest structured memory

```text
engineering-memory/daily/LATEST.json
```

This is useful for automation or future AI processing.

### Memory index

```text
engineering-memory/daily/_index.json
```

This tracks available memory files.

### Event archive

```text
engineering-memory/events/
```

This stores full GitHub webhook events.

### Processed events list

```text
engineering-memory/events/_processed-events.txt
```

This prevents duplicate processing.

### Closure note

```text
engineering-memory/MODULE_CLOSURE.md
```

This records that the Engineering Memory module reached a production-ready baseline.

---

## 10. How To Check If It Worked

After a GitHub push, run this on INTEL:

```bash
cd /opt/jobfynder-docs
git pull --rebase origin main
git log --oneline -8
grep -n "Source:\|Repository:\|Branch:\|Head SHA:\|Commit count:" engineering-memory/daily/LATEST.md
```

A healthy repo-aware memory entry should show:

```text
Source: GitHub webhook
Repository: jobfynder/hermes
Branch: main
Head SHA: abc1234
Commit count: 1
```

---

## 11. How To Check The Latest Archived Event

Run:

```bash
cd /opt/jobfynder-docs
LATEST_EVENT="$(ls -t engineering-memory/events/*-github-event.json | head -1)"
echo "$LATEST_EVENT"
python3 -m json.tool "$LATEST_EVENT" >/dev/null && echo "JSON_VALID=yes"
```

Healthy result:

```text
JSON_VALID=yes
```

---

## 12. How To Check Deduplication

Run:

```bash
cd /opt/jobfynder-docs
tail -5 engineering-memory/events/_processed-events.txt
```

You should see keys like:

```text
jobfynder/hermes|refs/heads/main|commit_sha
```

---

## 13. What To Do If Something Fails

If the automation fails, first check Telegram and email alerts.

The alert will show the failed node and execution URL.

Then check:

1. n8n workflow execution logs
2. INTEL server command output
3. Hermes container status
4. Git status in `/opt/hermes`
5. Git status in `/opt/jobfynder-docs`

Useful commands:

```bash
docker ps
docker logs hermes-api --tail 100
cd /opt/hermes && git status --short
cd /opt/jobfynder-docs && git status --short
```

---

## 14. Current Production Status

Engineering Memory is now stable as a baseline infrastructure memory system.

It provides:

- Automatic memory generation
- Repo-aware context
- Permanent GitHub archive
- Duplicate protection
- Failure alerts
- Simple latest-memory access

---

## 15. Future Improvements

These are optional future improvements, not blockers.

- Add GitHub HMAC signature verification
- Add richer summaries using project conversation context
- Add weekly and monthly Engineering Memory rollups
- Add repo-specific sections for frontend, backend, infra, and Hermes
- Add dashboard view for memory history
- Move remaining `jobfynder-admin` repositories into the `jobfynder` organization later

---

## 16. Simple Summary

Engineering Memory helps Jobfynder remember engineering work automatically.

It watches GitHub changes, sends them to Hermes, stores the result in `jobfynder-docs`, and alerts us if anything fails.

This gives Jobfynder a reliable engineering history that can be used by humans, automation, and future AI agents.
