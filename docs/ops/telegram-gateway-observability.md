# Telegram Gateway Observability

P4-5 turns the existing push-only Telegram Gateway into an operator-facing observability surface. It does not add Telegram commands and does not change trading logic.

## Runtime Evidence

```text
runtime/notifications/QuantGod_TelegramGatewayStatus.json
runtime/notifications/QuantGod_TelegramGatewayLedger.jsonl
runtime/notifications/QuantGod_NotificationEventQueue.jsonl
```

The ops layer summarizes:

```text
queue count
pending delivery count
actual sent count
duplicate / rate-limit suppressed count
failure count
latest delivery by topic
pending delivery by topic
Chinese push preview
```

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_telegram_gateway_ops.py --runtime-dir ./runtime status
python3 tools/run_telegram_gateway_ops.py --runtime-dir ./runtime collect
python3 tools/run_telegram_gateway_ops.py --runtime-dir ./runtime telegram-text --refresh
```

## API

```text
GET  /api/telegram-gateway/status
GET  /api/telegram-gateway/telegram-text?refresh=1
POST /api/telegram-gateway/collect
```

`collect` only queues scheduled operator reports through the existing Gateway. It does not accept Telegram commands.

## Safety

Telegram Gateway remains push-only:

```text
telegramCommandExecutionAllowed = false
gatewayReceivesCommands = false
orderSendAllowed = false
closeAllowed = false
cancelAllowed = false
livePresetMutationAllowed = false
externalMarketRealMoneyAllowed = false
```

The frontend panel is read-only plus a local collect button. It cannot submit orders, close positions, cancel orders, mutate MT5 live presets, or connect a external wallet.
