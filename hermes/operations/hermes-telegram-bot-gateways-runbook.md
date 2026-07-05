# Hermes Telegram Bot Gateways Runbook

Status: Production baseline completed
Server: jobfynder-intel-01
Snapshot: completed after successful setup

## Purpose

Jobfynder runs two separate Hermes Telegram gateways:

1. Public bot for normal users
2. Admin bot for infrastructure operations

This separation is mandatory for safety.

## Public Bot

Bot: @Jobfynderbot

Purpose:
- Public/global Jobfynder user assistant
- Safe for normal users
- No terminal access
- No file access
- No server/admin operations

Service:
- hermes-gateway

Hermes home:
- /root/.hermes

Access config:
- TELEGRAM_ALLOWED_USERS=*
- GATEWAY_ALLOW_ALL_USERS=true

Allowed Telegram tools:
- clarify only

Important rule:
- Public bot must never receive terminal or file tools.

## Admin Bot

Bot: @jobfynderaibot

Purpose:
- Admin-only infrastructure assistant
- Used to check and operate jobfynder-intel-01 safely

Service:
- hermes-admin-gateway

Hermes home:
- /root/.hermes-admin

Access config:
- TELEGRAM_ALLOWED_USERS=8373412917
- GATEWAY_ALLOW_ALL_USERS=false

Allowed Telegram tools:
- clarify
- terminal
- file

Terminal backend:
- local

This means the admin bot checks the real INTEL host directly.

## Verified Working State

Verified after setup:

- Public bot is global and safe
- Admin bot is admin-only
- Admin bot checks the real INTEL host
- Admin bot no longer asks for SSH
- hermes-gateway is active
- hermes-admin-gateway is active
- Hermes API container is running
- Typesense is running
- Nginx Proxy Manager is running
- Server CPU, memory, and disk are healthy
- Snapshot completed after success

## Health Check Commands

Check both gateway services:

    systemctl is-active hermes-gateway hermes-admin-gateway

Expected:

    active
    active

Check service status:

    systemctl status hermes-gateway --no-pager -l
    systemctl status hermes-admin-gateway --no-pager -l

Check Hermes API:

    curl -fsS http://localhost:8000/health

Check Docker containers:

    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

## Safe Admin Bot Test Prompt

Send this to @jobfynderaibot:

Use the local terminal tool and check real INTEL host status. Run only read-only checks: hostname, uptime, free -h, df -h /, systemctl is-active hermes-gateway hermes-admin-gateway, and docker ps --format table. Do not ask for SSH. Do not show secrets.

Expected behavior:
- It should not ask for SSH
- It should confirm jobfynder-intel-01
- It should show uptime, memory, disk, Hermes services, and Docker containers
- It must not show secrets

## Security Rules

Never paste Telegram bot tokens, API keys, passwords, or private keys into ChatGPT.

If a token is accidentally pasted:
1. Revoke/regenerate it immediately
2. Update the token only directly on the server
3. Clean shell history if needed

Admin bot must always remain restricted:

    TELEGRAM_ALLOWED_USERS=8373412917
    GATEWAY_ALLOW_ALL_USERS=false

Never set admin bot access to wildcard.

## Clean Restart Procedure

Use clean stop/start instead of rapid restart:

    systemctl stop hermes-gateway hermes-admin-gateway
    sleep 10
    systemctl start hermes-gateway
    sleep 20
    systemctl start hermes-admin-gateway
    sleep 20
    systemctl is-active hermes-gateway hermes-admin-gateway

## Completion

This setup is complete and snapshot-protected.
