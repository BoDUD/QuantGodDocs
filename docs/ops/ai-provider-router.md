# AI Provider Router

This runbook documents QuantGod's local single-user AI provider router.

## Scope

The router centralizes configuration and health checks for advisory AI features:

```text
DeepSeek / OpenRouter / mock provider config
JSON chat interface
secret redaction
local health checks
shared safety payload
```

It is intentionally **not** a user system, billing system, broker adapter, Telegram command receiver, webhook receiver, or trading gateway.

## Safety boundary

The router is advisory/research-only. It must never:

- send, close, cancel, or modify orders;
- write live preset mutations;
- store credentials in the repository;
- receive Telegram trading commands;
- create webhook receivers;
- override Kill Switch or governance decisions;
- promote AI text to execution.

The provider safety payload keeps these flags false:

```text
orderSendAllowed=false
closeAllowed=false
cancelAllowed=false
credentialStorageAllowed=false
livePresetMutationAllowed=false
canOverrideKillSwitch=false
telegramCommandExecutionAllowed=false
telegramWebhookReceiverAllowed=false
webhookReceiverAllowed=false
emailDeliveryAllowed=false
walletIntegrationAllowed=false
externalMarketOrderAllowed=false
```

## Local setup

Backend repository:

```powershell
cd C:\QuantGod\QuantGodBackend
Copy-Item .env.ai.local.example .env.ai.local
notepad .env.ai.local
```

Recommended DeepSeek config:

```text
QG_AI_ENABLED=1
QG_AI_PROVIDER=deepseek
QG_AI_MODEL=deepseek-v4-flash
QG_AI_BASE_URL=https://api.deepseek.com
QG_AI_API_KEY=<local key only>
QG_AI_REQUIRE_JSON=1
```

Keep `.env.ai.local` uncommitted. The example file keeps the key blank.

Existing `.env.deepseek.local` remains compatible. The router reads `.env.deepseek.local` first and then lets `.env.ai.local` override it.

## Commands

Config without leaking secrets:

```powershell
python tools\run_ai_provider.py config
```

Readiness without a network call:

```powershell
python tools\run_ai_provider.py status
python tools\run_ai_provider.py models
python tools\run_ai_provider.py health
```

Live provider call:

```powershell
python tools\run_ai_provider.py health --live
```

Dry-run JSON request:

```powershell
python tools\run_ai_provider.py chat-json --user-json "{\"symbol\":\"USDJPYc\"}"
```

Live JSON request:

```powershell
python tools\run_ai_provider.py chat-json --live --user-json "{\"symbol\":\"USDJPYc\"}"
```

## Why this exists

QuantGod now has multiple AI surfaces:

```text
MT5 DeepSeek Telegram advisory fusion
AI Analysis V2 local multi-agent engine
Vibe Coding research/backtest
future journal/outcome summaries
future external market read-only event context
```

The router prevents each feature from inventing its own API-key handling and safety checks.

## Verification

```powershell
python -m py_compile tools\run_ai_provider.py tools\ai_analysis\providers\base.py tools\ai_analysis\providers\deepseek_provider.py tools\ai_analysis\providers\mock_provider.py tools\ai_analysis\providers\openrouter_provider.py tools\ai_analysis\providers\router.py
python -m unittest discover tests -v
node --test tests\node\test_ai_provider_router_guard.mjs
python tools\run_ai_provider.py status
python tools\run_ai_provider.py models
python tools\run_ai_provider.py health
```
