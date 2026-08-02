# AI Infrastructure — Final Summary & Lessons Learned (2026-08-02)

## Context
User built the AI infrastructure: LiteLLM Gateway + Redis caching + Langfuse + DeepInfra embeddings, replacing the Portkey path (rolled back). All credentials live in Bitwarden, NOT in this file or git.

---

## 1. FINALIZED CONFIGURATIONS

### LiteLLM Gateway (Elestio, separate VM)
- **Service**: `litellm-gateway-u14612.vm.elestio.app` ; Public URL `https://gateway.jobfynder.com` (Cloudflare-proxied); IP `159.195.1.254`
- **Version**: latest (observed 1.83.x); Admin UI at `/ui/` (`admin` user — vaulted)
- **Master key**: LITELLM_MASTER_KEY (vaulted) — required for all /v1/* calls; unauthenticated = 401 ✓
- **DB**: POSTGRES_DB=litellm, POSTGRES_USER=postgres, db service on `db:5432`; STORE_MODEL_IN_DB=True
- **Model aliases** (in config.yaml, route to deepseek-chat): `jf-fast`, `jf-structured`, `jf-reasoning`, `jf-writing` + `deepseek-chat`. `jf-embedding` still points at deepseek-chat — **PENDING repoint to deepinfra/BAAI/bge-m3** in config.yaml
- **Virtual keys (5)**: jf-hermes-production ($100, 60rpm, all 5 aliases), jf-core-production ($20, 15, fast+writing), jf-n8n-production ($25, 20, fast+structured+writing), jf-evaluation-production ($20, 5, reasoning+writing), jf-development ($10, 10, all 5, 90-day expiry)
- **Teams**: jobfynder-production (a745d0e6; hermes/core/n8n), jobfynder-development (8b6809d3), jobfynder-evaluation (0522861a)

### Redis for LiteLLM (Elestio-managed — cache ONLY)
- **Host**: `redis-ai-gateway-u14612.vm.elestio.app` / public `152.53.202.147` / **private `10.30.71.5`**
- **Port**: **26379** (NOT 6379 — that is Langfuse's *internal* Redis on this server)
- **User/pass**: default / `eoN-...` **lowercase-o** (uppercase `eON` fails -WRONGPASS; ONLY lowercase authenticates)
- **Env on LiteLLM**: REDIS_HOST=10.30.71.5, REDIS_PORT=26379, REDIS_USER=default, REDIS_PASSWORD=eoN-... (lowercase), LITELLM_CACHE_TYPE=redis
- **Cache activation requires config.yaml block** (see Lesson 5), NOT just env vars
- **Firewall**: 26379 restricted to `159.195.1.254/32` only (UFW + Docker DOCKER-USER). 22/80/443 untouched. Verified closed from outside, caching still healthy
- **Verified working**: /cache/ping healthy (redis, set=success); 3 identical calls → 1.4s / 0.75s / 0.76s identical output = cache hits
- **Decision (user)**: Redis is STRICTLY for LiteLLM caching. Langfuse gets NO LiteLLM-Redis access

### Langfuse (self-hosted on INTEL)
- **URL**: `https://langfuse.jobfynder.com` ; version **4.1.0**; health OK
- **Org/Project**: jobfynder / `jobfynder-ai` (project id `cmsbr7woa0006qh07me6rfbas`)
- **Admin**: pavan@jobfynder.com (vaulted); **AUTH_DISABLE_SIGNUP=true** (verified: /auth/sign-up → 404, sign-in → 200); NEXTAUTH_URL set
- **Prompts**: **92** imported (all chat type, 1 version, created 2026-08-02, label `dev`, domains 20) — confirmed by screenshot; 14 prompts have cache=true (6×24h TTL, 3×1h TTL)
- **Observations (7d)**: 0 — no live LLM traffic through Langfuse YET (awaiting LiteLLM env keys)
- **API keys** (per project, all verified HTTP 200, vaulted):
  - litellm-production → Bitwarden `f06b724a`
  - hermes-production → Bitwarden `2295c691`
  - CORE → existing pk-lf-8b8a5e74-... on item `8e0353f1`
- **To enable tracing**, LiteLLM .env needs: LANGFUSE_HOST=https://langfuse.jobfynder.com, LANGFUSE_PUBLIC_KEY/SECRET_KEY (litellm-production pair). Without LANGFUSE_HOST it silently defaults to cloud.langfuse.com

### DeepInfra (embeddings)
- **Key**: vaulted Bitwarden `90a7e7c7` (this is a real API key — the two deepinfra.com vault items are website logins only, NOT API keys)
- **Model**: `deepinfra/BAAI/bge-m3` (mode: embedding, 1024-dim) — registered via API but DB registration does NOT override config.yaml
- **Status**: jf-embedding still routes to deepseek-chat (HTTP 400 on /v1/embeddings). **PENDING config.yaml repoint**

### Server / rollback state (INTEL)
- hermes-api on `hermes-hermes-api:latest` (base, pristine), health HTTP 200, only TYPESENSE_API_KEY in .env
- Portkey/Langfuse-docker artifacts removed; Bitwarden cleanup done; docs registry clean
- Gateways (bots): DeepSeek direct, NOT via Portkey — preserved decision

---

## 2. LESSONS LEARNED

1. **Elestio UI pitfalls**: The plain **Restart button does NOT re-read changed env vars** — use **Update & Restart** (full recreate) or Stop→Start. The generic Restart only restarts the process.
2. **ENV tab vs Docker Compose tab**: The Update App Stack Config modal has two toggles. Pasting env text into the Docker Compose (YAML) tab corrupts the config and crashes the stack: `yaml: unmarshal errors: line 1: cannot unmarshal !!str SOFTWAR... into cli.named`. ALWAYS use the ENV tab for env lines.
3. **Redis passwords are case-sensitive**: `eON` vs `eoN` — the screenshot showed uppercase but only lowercase authenticates (+OK). Always verify with a live AUTH test; don't trust the dashboard screenshot.
4. **LiteLLM v1.83 does NOT build the cache from env vars alone**: `litellm_cache_params` stayed `{}` and `/cache/ping` returned `503 Cache not initialized` despite LITELLM_CACHE_TYPE=redis + REDIS_*. The cache must be configured inside **config.yaml** (under litellm_settings / general_settings) — verified working only after that.
5. **config.yaml model list overrides DB-registered models**: Registering a model via /model/new with STORE_MODEL_IN_DB=True returns a model_id but does NOT override/wire aliases that are defined in config.yaml. To change an alias target, edit config.yaml directly.
6. **/cache/ping is the authoritative cache check**; a real cache-hit proof = 3 identical calls (cold ~1.4s, hot ~0.75s, identical content). `prompt_cache_hit_tokens` on DeepSeek is a provider-side field and stays 0 even when Redis cache hits — ignore it.
7. **Langfuse self-hosted API quirks**: `/api/public/prompts` → 400, `/api/public/traces` → 404 in 4.1.0 — these are endpoint quirks, not proof of failure. Use the UI (screenshot) or the /api/public/projects 200 check to verify keys.
8. **Langfuse is a Next.js SPA**: HTTP status of /auth/sign-up is not fully authoritative; a 404 after AUTH_DISABLE_SIGNUP=true + login 200 is the practical confirmation.
9. **Langfuse keys are per-project**: the old cloud public key pk-lf-c561... (us.cloud.langfuse.com) is NOT valid for the self-hosted project. Credentials must be created in the self-hosted instance's Project Settings → API Keys.
10. **TWO DIFFERENT REDIS INSTANCES — never conflate**: LiteLLM cache Redis = Elestio, port **26379** (10.30.71.5); Langfuse internal Redis = this server `172.17.0.1:6379`. Changing LiteLLM to 6379 would break caching. Also: it is EXPECTED that our box cannot connect to 26379 (firewalled to LiteLLM only).
11. **Trust only your own tool output / live probes**. Multiple "ISSUE RESOLVED" claims during this session were false (cache 'healthy', model registered, 92/92 verified). Ground truth = your own curl/docker/bw results; reconcile contradictions before recording.
12. **Elestio redeploy / Change-version drops config.yaml customizations** (cache block, callbacks, aliases). Mitigation: `postDeploy.sh` via elestio.yml `postDeployCommand` must re-inject them; verify after every redeploy.
13. **DeepInfra website logins ≠ API keys**: the two deepinfra.com vault items were 14-char site passwords only. API keys are longer and created at deepinfra.com/dashboard/api.
14. **Elestio Redis defaults to public 0.0.0.0/0; lockdown requires TWO layers**: UFW rule AND Docker DOCKER-USER chain. Remove both, add one allow-rule for the app IP only; leave 22/80/443/26380/18446/18374/4242 untouched.
15. **Do not rotate/wholesale-change a Redis password via env only**: LiteLLM must auth against the CURRENT server password. Rotating requires changing both server-side and env together, otherwise caching silently fails. (Recommended: generate separate passwords per service because the same one is reused across LiteLLM admin/Postgres/AWS/Langfuse.)
16. **The `no-cache: true` flag on a DB-registered model is cosmetic when global cache is enabled in config.yaml** — repeat-call speedup proves real cache hits even with the flag present. Don't risk restarts for cosmetic PATCHes.
17. **Bitwarden item creation**: use base64-encoded JSON as the argument (plain arg/stdin fail with 'Error parsing the encoded request data'). Store API keys as fields; secure notes (type 2) have no login object.
18. **Formatting discipline in env editors**: no spaces around `=`, no quotes around values, no trailing garbage — malformed lines silently break the service or get ignored.

---

## 3. OPEN ITEMS (do NOT close without evidence)
1. **jf-embedding** → repoint config.yaml alias `jf-embedding` litellm_params.model to `deepinfra/BAAI/bge-m3` (backup config.yaml first). Verify /v1/embeddings → 200, dim=1024.
2. **LiteLLM → Langfuse tracing** → add LANGFUSE_HOST + LANGFUSE_PUBLIC_KEY/SECRET_KEY (vault f06b724a) to LiteLLM .env (ENV tab), Update & Restart, then verify: readiness success_callbacks includes langfuse, one live call, trace appears (observations 0→>0).
3. **postDeploy.sh review** → confirm it uses $REDIS_HOST/$REDIS_PASSWORD env vars (not hardcoded uppercase-O), and that it restores cache block + Langfuse callbacks + deepinfra model after redeploy.
4. **Backup admin user in Langfuse UI** before signup-disable is final (per checklist).
5. **Password reuse** → rotate the shared e0blpY... password into per-service values (highest security priority).
6. **Label strategy** → prompts are label `dev`; decide fetch-by-dev vs promote-to-production when apps go live.
7. **Langfuse UI tasks (checklist 4–16)**: Playground→LiteLLM connection (gateway.jobfynder.com/v1), folders via '/' in names (e.g. extraction/job-description), starter prompts, evaluation datasets/scores, standardized trace names, cost tracking, PII masking future.
8. **Swap `redisgateway.jobfynder.com` DNS** to point at 152.53.202.147 (currently Cloudflare anycast, not the Elestio VM) if the friendly name is needed.

---

## 4. KEY VERIFICATION COMMANDS (runbook)
- LiteLLM health: `curl -H "Authorization: Bearer <key>" https://litellm-gateway-u14612.vm.elestio.app/health`
- Cache: `.../cache/ping` → expect {"status":"healthy","cache_type":"redis","set_cache_response":"success"}
- Cache-hit proof: identical POST /v1/chat/completions ×3 → cold ~1.4s, hot ~0.75s, identical output
- Redis AUTH: `redis-cli -h 10.30.71.5 -p 26379 AUTH default <password>` from LiteLLM box → +OK (lowercase-o ONLY)
- Langfuse keys: `curl -u <pk>:<sk> https://langfuse.jobfynder.com/api/public/projects` → 200 + project jobfynder-ai
- Langfuse signup: `/auth/sign-up` → 404 ; `/auth/sign-in` → 200
- Redis public lock: TCP check 152.53.202.147:26379 → closed/filtered (OK); 22/80/443 → open
- Embeddings (post-fix): `POST /v1/embeddings {"model":"jf-embedding","input":"..."}` → 200, dim 1024

---
*Status recorded in .hermes-state.json. Credentials NOT stored in this repo.*
