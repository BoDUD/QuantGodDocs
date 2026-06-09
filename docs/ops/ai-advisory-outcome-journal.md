# AI Advisory Outcome Journal

P3-5 adds a local, single-user outcome journal for QuantGod Telegram advisories.
It turns every MT5/DeepSeek Telegram advisory into a shadow sample, then scores
that sample against later read-only runtime prices.

## Scope

This feature is intentionally narrow:

- records Telegram advisory output as local JSONL evidence
- scores shadow direction after later runtime prices are available
- summarizes win rate, average shadow R, and weak symbols/directions
- pauses weak signal families before they reach Telegram as active-looking advice
- keeps all new Telegram human-facing lines in Chinese

It does not add order sending, position closing, cancellation, broker execution,
credential storage, Telegram command handling, webhook receivers, external market
wallet integration, user accounts, or billing.

## Runtime files

The journal writes under the runtime directory:

```text
runtime/journal/QuantGod_AIAdvisoryJournal.jsonl
runtime/journal/QuantGod_AIAdvisoryOutcomes.jsonl
runtime/journal/QuantGod_AISignalKillSwitch.json
```

These files are local evidence. They are not API keys or credentials.

## CLI

```powershell
python tools\run_ai_journal.py status --runtime-dir .\runtime
python tools\run_ai_journal.py list --runtime-dir .\runtime --limit 20
python tools\run_ai_journal.py score --runtime-dir .\runtime --horizon 4h
python tools\run_ai_journal.py summary --runtime-dir .\runtime --text
python tools\run_ai_journal.py kill-switch --runtime-dir .\runtime --symbol USDJPYc --direction LONG
```

## Signal-level kill switch

This is not the MT5 kill switch. It only downgrades advisory text.

Default behavior:

```text
QG_AI_JOURNAL_KILL_SWITCH_ENABLED=1
QG_AI_JOURNAL_MIN_SAMPLES=5
QG_AI_JOURNAL_AVG_R_THRESHOLD=-0.25
QG_AI_JOURNAL_HIT_RATE_THRESHOLD=0.4
QG_AI_JOURNAL_CONSECUTIVE_LOSSES=5
QG_AI_JOURNAL_COOLDOWN_SECONDS=86400
```

If one symbol/direction family performs poorly, future reports are downgraded to
Chinese pause language:

```text
暂停，不开新仓，仅观察复核
```

The system still does not execute trades.

## Telegram language requirement

Before Telegram delivery, messages are passed through `ensure_chinese_telegram_text()`.
Operational terms such as `finalAction`, `WATCH_LONG`, `validator`, `advisoryOnly`,
`true`, `false`, `KillSwitch`, `bid`, and `ask` are normalized into Chinese.

Symbols such as `USDJPYc`, timestamps, and model identifiers may remain unchanged.
The human instruction and safety text must be Chinese.

## Safety defaults

```text
localOnly=true
readOnlyDataPlane=true
advisoryOnly=true
shadowTradingOnly=true
telegramPushOnly=true
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
brokerExecutionAllowed=false
externalMarketOrderAllowed=false
walletIntegrationAllowed=false
```
