# Hermes Smoke Test

Status: Production Baseline
Owner: Jobfynder-Infra
Stream: HERMES-100 Core Platform

---

## What This Is

Hermes now has a simple smoke test script.

The smoke test confirms Hermes is healthy, RBAC is working, and the Docker image is clean.

---

## Script Location

/opt/hermes/scripts/hermes-smoke-test.sh

---

## What It Checks

- /health is public and returns HTTP 200.
- Protected security endpoint blocks requests without token.
- Admin token can access security status.
- n8n token cannot access security status.
- Parser endpoint blocks requests without token.
- Parser endpoint works with admin token.
- .git is not present inside the Hermes container.

---

## How To Run

cd /opt/hermes
./scripts/hermes-smoke-test.sh

---

## Rule

Run this smoke test after every Hermes deployment or important core platform change.
