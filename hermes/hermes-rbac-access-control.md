# Hermes RBAC Access Control

Status: Production Baseline
Owner: Jobfynder-Infra
Stream: HERMES-100 Core Platform

---

## What This Is

Hermes now has token-based RBAC.
Only approved users or systems can access protected Hermes endpoints.

## Access Model

Public endpoint:
- /health

Protected endpoints:
- /security/rbac/status
- /v1/engineering-memory/generate
- /mission-control
- /session-brief
- /workspace
- /actions

## Current Users

Users are stored outside Git:
/opt/hermes-runtime/access-control/users.json

Baseline users:
- pavan-admin: admin access
- n8n-engineering-memory: Engineering Memory automation access

## Token Storage

Tokens are stored outside Git:
- /root/hermes-admin-token.txt
- /root/hermes-n8n-token.txt

Never paste tokens in chat, commits, logs, screenshots, or documentation.

## Validation Completed

- /health works without token.
- Security status fails without token.
- Admin token can access security status.
- n8n token cannot access security status.
- n8n token can generate Engineering Memory.
- Full Engineering Memory script works with RBAC enabled.

## Current Status

HERMES-100 Access Control and RBAC is production baseline complete.

---

## User Management Script

Hermes includes a simple server-side script to manage RBAC users:

/opt/hermes/scripts/hermes-access-control.py

List users:

python3 /opt/hermes/scripts/hermes-access-control.py list

Add a user:

python3 /opt/hermes/scripts/hermes-access-control.py add \
  --id user-id \
  --name "User Name" \
  --role viewer \
  --permissions messages:understand,jobs:parse

Disable a user:

python3 /opt/hermes/scripts/hermes-access-control.py disable \
  --id user-id

When a user is added, the token is saved outside Git under:

/root/hermes-token-user-id.txt

Never print or share the token publicly.
