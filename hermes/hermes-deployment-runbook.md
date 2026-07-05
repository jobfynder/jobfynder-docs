# Hermes Deployment Runbook

Status: Production Baseline
Owner: Jobfynder-Infra
Stream: HERMES-100 Core Platform

---

## Purpose

This runbook gives simple commands to operate Hermes safely.

---

## Hermes Location

/opt/hermes

---

## Check Status

cd /opt/hermes
git status --short
docker ps --filter "name=hermes-api"
curl -s http://localhost:8000/health

---

## Rebuild and Restart Hermes

cd /opt/hermes
docker compose up -d --build hermes-api

---

## Run Smoke Test

cd /opt/hermes
./scripts/hermes-smoke-test.sh

---

## View Logs

cd /opt/hermes
docker logs --tail 100 hermes-api

---

## Push Hermes Changes

cd /opt/hermes
git status --short
git add FILES
git commit -m "message"
git push origin feature/hermes-memory-engine

---

## Rule

After every Hermes deployment, run the smoke test.

If the smoke test fails, do not continue with the next module until the issue is fixed.
