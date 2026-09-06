# Recover RabbitMQ

## Confirmed

RabbitMQ is the platform's durable event backbone (see `ADR-0005`) — handles background tasks and the COMM intake pipeline with retry, dead-letter handling, and idempotency. A default RabbitMQ credential was found live in production and fixed on 2026-08-21 (see `Infrastructure/CHANGELOG.md`) — worth confirming that fix is still in place before assuming credentials are safe.

## Unknown — needs someone with live access to fill in

Actual recovery/rebuild steps, whether queued-but-undelivered messages are backed up anywhere, and current credential rotation status.
