# Recover RabbitMQ

## Confirmed

RabbitMQ is the platform's durable event backbone (see `ADR-0005`) — handles background tasks and the COMM intake pipeline with retry, dead-letter handling, and idempotency. Runs as container `jobfynder-rabbitmq` (`rabbitmq:3-management`) on `jobfynder-comm1`.

A default RabbitMQ credential was found live in production and fixed on 2026-08-21 (see `Infrastructure/CHANGELOG.md`). **Re-verified 2026-09-07: still fixed** — `rabbitmqctl list_users` shows only `hermes_graph` and `jobfynder` (administrator); no default `guest` account present.

## Unknown — needs someone with live access to fill in

Actual recovery/rebuild steps if the container/data volume is lost, whether queued-but-undelivered messages are backed up anywhere, and current credential rotation policy (the two users exist and aren't default, but rotation schedule isn't documented).
