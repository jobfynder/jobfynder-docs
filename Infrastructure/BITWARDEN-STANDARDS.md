# Bitwarden Standards

## The rule

All new passwords, keys, and credentials go to Bitwarden via the `bw` CLI. Never in this repo, never in `.env` committed to git, never in a config file that gets version-controlled.

## Confirmed items actually stored there

n8n API Key, Centrifugo (Hermes Server), Hermes WebUI (Tailscale), Reoon Email Verifier, Langfuse (litellm-production and hermes-production key pairs, plus the CORE key), LiteLLM master key, DeepInfra API key.

## Known operational gotchas (from real incidents, not guesses)

- **Item creation via CLI:** use base64-encoded JSON as the argument — a plain arg or stdin fails with "Error parsing the encoded request data."
- **Secure notes (type 2) have no login object** — don't try to force credentials into that type.
- **A shared password was found reused across multiple services** (LiteLLM admin, Postgres, AWS, Langfuse) and flagged as a real security priority to rotate into separate per-service passwords. If that rotation hasn't happened yet, it should.
- **Two DeepInfra vault items were website logins, not API keys** — a real API key is longer and is created separately at deepinfra.com/dashboard/api. Don't assume a vault item with a plausible name is the credential type you need without checking.

## Unknown — needs someone with live vault access

Full vault folder structure, sharing/access-control conventions, and rotation schedule beyond the one incident above.
