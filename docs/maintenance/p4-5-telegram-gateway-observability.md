# P4-5 Telegram Gateway Observability

P4-5 adds a management and observability layer around the existing Telegram Gateway.

## Scope

Backend adds:

```text
tools/telegram_gateway_ops/
tools/run_telegram_gateway_ops.py
Dashboard/telegram_gateway_ops_api_routes.js
tests/test_telegram_gateway_ops.py
tests/node/test_telegram_gateway_ops_guard.mjs
```

Frontend adds:

```text
src/services/telegramGatewayOpsApi.js
src/components/TelegramGatewayOpsPanel.vue
scripts/frontend_telegram_gateway_ops_guard.mjs
tests/frontend_telegram_gateway_ops_guard.test.mjs
```

Docs add this maintenance note and the operator runbook in `docs/ops/telegram-gateway-observability.md`.

## What It Observes

```text
queued reports
pending reports
actual sends
duplicate suppression
rate-limit suppression
delivery failures
latest delivery by topic
pending delivery by topic
Chinese Telegram preview
```

## What It Does Not Do

```text
Telegram trade commands
order send
position close
order cancel
MT5 live preset mutation
MT5 OrderRequest writes
external wallet or real-money trading
```

## Validation

```bash
python3 -m py_compile \
  tools/run_telegram_gateway_ops.py \
  tools/telegram_gateway_ops/schema.py \
  tools/telegram_gateway_ops/io_utils.py \
  tools/telegram_gateway_ops/status.py \
  tools/telegram_gateway_ops/telegram_text.py

python3 -m unittest tests.test_telegram_gateway_ops -v
node --test tests/node/test_telegram_gateway_ops_guard.mjs

python3 tools/run_telegram_gateway_ops.py --runtime-dir ./runtime status
python3 tools/run_telegram_gateway_ops.py --runtime-dir ./runtime collect
python3 tools/run_telegram_gateway_ops.py --runtime-dir ./runtime telegram-text --refresh
```

Frontend:

```bash
npm run telegram-gateway-ops
npm run test:telegram-gateway-ops
npm test
npm run build
```

Docs:

```bash
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python3 -m unittest discover tests -v
```
