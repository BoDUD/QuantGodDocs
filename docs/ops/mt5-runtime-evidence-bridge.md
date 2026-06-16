# MT5 Runtime Evidence Bridge

P3-2.1 connects the existing Telegram push-only advisory monitor to HFM/MT5 EA-written runtime evidence files.

The bridge is intentionally narrow:

- Read local MT5/HFM runtime JSON files.
- Validate schema, freshness, symbol, price, kline arrays and safety flags.
- Normalize the data into the existing AI Analysis V2 snapshot shape.
- Let `run_mt5_ai_telegram_monitor.py` send advisory-only Telegram messages through the existing push-only notifier.
- Record Telegram evidence through the existing SQLite notification record path.

It does **not** add broker execution, webhook receiving, Telegram commands, email delivery, credential storage, order submission, position close/cancel, live preset mutation or Kill Switch override.

## Runtime directory

The bridge reads the same local runtime directory used by existing QuantGod tools:

```powershell
$env:QG_RUNTIME_DIR="C:\Program Files\HFM Metatrader 5\MQL5\Files"
```

On macOS, when HFM/MT5 is writing files through a synced folder or manual copy, point `QG_RUNTIME_DIR` to that local folder:

```bash
export QG_RUNTIME_DIR="$HOME/QuantGod/runtime"
```

The CLI also accepts `--runtime-dir`.

## File names

The preferred EA output file is one JSON file per broker symbol:

```text
QuantGod_MT5RuntimeSnapshot_USDJPYc.json
QuantGod_MT5RuntimeSnapshot_EURUSDc.json
QuantGod_MT5RuntimeSnapshot_XAUUSDc.json
```

`QuantGod_Dashboard.json` remains supported as a compatibility source if it contains embedded runtime snapshots or symbol rows.

## Minimal schema

```json
{
  "schema": "quantgod.mt5.runtime_snapshot.v1",
  "source": "hfm_ea_runtime",
  "generatedAt": "2026-05-03T05:00:00Z",
  "account": {
    "broker": "HFM",
    "loginRedacted": "***",
    "serverRedacted": "***",
    "balance": 10000.0,
    "equity": 10020.5,
    "margin": 0.0,
    "freeMargin": 10020.5
  },
  "symbol": "USDJPYc",
  "current_price": {
    "symbol": "USDJPYc",
    "bid": 155.12,
    "ask": 155.14,
    "last": 155.13,
    "spread": 0.02,
    "timeIso": "2026-05-03T05:00:00Z"
  },
  "open_positions": [],
  "kline_m15": [],
  "kline_h1": [],
  "kline_h4": [],
  "kline_d1": [],
  "kill_switch_status": {
    "locked": true,
    "canOverride": false
  },
  "safety": {
    "readOnly": true,
    "orderSendAllowed": false,
    "closeAllowed": false,
    "cancelAllowed": false,
    "credentialStorageAllowed": false,
    "livePresetMutationAllowed": false,
    "telegramCommandExecutionAllowed": false,
    "telegramWebhookReceiverAllowed": false
  }
}
```

Do not include passwords, API tokens, API keys, secrets, authorization headers, MT5 password values, Telegram tokens, broker credentials or order request payloads.

## CLI

Check bridge defaults:

```powershell
python tools\run_mt5_runtime_bridge.py config
```

Create sample runtime files for local smoke testing:

```powershell
python tools\run_mt5_runtime_bridge.py sample --runtime-dir .\runtime --symbols USDJPYc --overwrite
```

Check runtime availability and freshness:

```powershell
python tools\run_mt5_runtime_bridge.py status --runtime-dir .\runtime --symbols USDJPYc
```

Validate one symbol:

```powershell
python tools\run_mt5_runtime_bridge.py validate --runtime-dir .\runtime --symbol USDJPYc
```

Emit the normalized snapshot that AI Analysis V2 will consume:

```powershell
python tools\run_mt5_runtime_bridge.py snapshot --runtime-dir .\runtime --symbol USDJPYc --timeframes M15,H1,H4,D1
```

If the market is closed or you are testing old copied files, use `--allow-stale` for diagnostics only. The production advisory path should prefer fresh files.

## Telegram advisory smoke test

After `.env.telegram.local` is configured and Telegram push is explicitly enabled:

```powershell
python tools\run_mt5_ai_telegram_monitor.py scan-once --runtime-dir .\runtime --symbols USDJPYc --force --send
```

The Telegram message should show a runtime source such as `hfm_ea_runtime`, `fallback: False`, `runtimeFresh: True` and an age in seconds. It should no longer show `snapshotSource=mt5_python_unavailable` when a fresh runtime snapshot exists.

## Safety gates

The bridge rejects runtime snapshots that contain credential-like keys such as `password`, `token`, `apiKey`, `secret`, `authorization` or `bearer`.

The bridge also rejects truthy execution flags:

```text
canExecuteTrade
orderSendAllowed
closeAllowed
cancelAllowed
credentialStorageAllowed
livePresetMutationAllowed
canOverrideKillSwitch
telegramCommandExecutionAllowed
telegramWebhookReceiverAllowed
webhookReceiverAllowed
emailDeliveryAllowed
```

This keeps P3-2.1 inside the same advisory-only and push-only boundary as P3-2.

## Troubleshooting

If the status command reports `missing_runtime_snapshot`, confirm the EA is writing one of the supported file names into `QG_RUNTIME_DIR`.

If `/api/mt5-readonly/snapshot` reports `MISSING_EA_SNAPSHOT`, the frontend has enough evidence to stop showing a vague waiting state. Restore the matching HFM/MT5 terminal and EA dashboard writer, confirm `QuantGod_Dashboard.json` exists in `QG_RUNTIME_DIR` / `QG_MT5_FILES_DIR`, then refresh until `_freshness.status` becomes `FRESH_EA_SNAPSHOT`.

If it reports `stale_runtime_snapshot`, confirm MT5/HFM is running and the EA is updating `generatedAt` or `current_price.timeIso`.

If Telegram still shows `mt5_python_unavailable`, run the snapshot command. If the snapshot command returns `fallback: true`, the AI monitor is correctly refusing missing or stale runtime evidence and falling back to its existing safe path.
