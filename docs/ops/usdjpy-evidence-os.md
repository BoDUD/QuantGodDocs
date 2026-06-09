# USDJPY Evidence OS

USDJPY Evidence OS is the first Perfect Edition evidence layer. It connects the Strategy JSON backtest, Python replay, MQL5 EA diagnostics, live execution feedback, Case Memory, and a push-only Telegram Gateway into one auditable chain.

It is still a research and audit plane. It does not send orders, close positions, cancel orders, mutate live presets, connect external real-money market access, or receive Telegram trading commands.

## Evidence Flow

```text
QuantGod_MT5RuntimeSnapshot_USDJPYc.json
→ SQLite K-line ingest
→ Strategy JSON backtest
→ Strategy JSON / Python Replay / MQL5 EA parity
→ Live execution feedback
→ Case Memory
→ GA fitness evidence
→ Telegram Gateway push-only summary
```

## Runtime Outputs

```text
runtime/backtest/usdjpy.sqlite
runtime/backtest/QuantGod_USDJPYKlineIngestReport.json
runtime/backtest/QuantGod_StrategyBacktestReport.json
runtime/evidence_os/QuantGod_StrategyParityReport.json
runtime/evidence_os/QuantGod_LiveExecutionQualityReport.json
runtime/evidence_os/QuantGod_LiveExecutionFeedback.jsonl
runtime/evidence_os/QuantGod_CaseMemory.jsonl
runtime/evidence_os/QuantGod_CaseMemorySummary.json
runtime/evidence_os/QuantGod_USDJPYEvidenceOSStatus.json
runtime/notifications/QuantGod_NotificationEventQueue.jsonl
runtime/notifications/QuantGod_TelegramGatewayStatus.json
runtime/notifications/QuantGod_TelegramGatewayLedger.jsonl
```

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime sync-klines
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime run --write
python3 tools/run_usdjpy_evidence_os.py --runtime-dir ./runtime once --write
python3 tools/run_usdjpy_evidence_os.py --runtime-dir ./runtime telegram-text --refresh
python3 tools/run_telegram_gateway.py --runtime-dir ./runtime status
python3 tools/run_telegram_gateway.py --runtime-dir ./runtime enqueue --text '【QuantGod 测试】Gateway 只做中文 push，不接收交易命令。'
python3 tools/run_telegram_gateway.py --runtime-dir ./runtime dispatch
```

## Execution Feedback

Execution feedback now reads multiple local evidence sources when present:

- `QuantGod_LiveExecutionFeedback.jsonl` written by `QuantGod_MultiStrategy.mq5` in real time from order-send results and `OnTradeTransaction`.
- `QuantGod_LiveExecutionFeedbackHistory.jsonl` rebuilt by the EA from broker trade history during dashboard export.
- `QuantGod_RuntimeTradeEvents.jsonl` from the MT5 fast lane exporter.
- `live/QuantGod_USDJPYLiveLoopLedger.csv`.
- trade journal, trade event link, outcome label, close history, and EA dry-run ledgers.
- latest live-loop status as a low-fidelity fallback.

The EA emits the standard `quantgod.live_execution_feedback.v1` schema with `feedbackId`, `eventType`, `policyId`, `strategyId`, `intentId`, `expectedPrice`, `fillPrice`, `slippagePips`, `spreadAtEntry`, `latencyMs`, `retcode`, `rejectReason`, `exitReason`, `profitR`, `profitUSC`, `mfeR`, and `maeR`. The report normalizes fills, closes, accepted order requests, rejects, retcodes, slippage, latency, profitR, MFE/MAE, policy mismatch, and execution quality gates. It also derives `dominantRejectReason`, `acceptedWithoutFillCount`, `maxLatencyMs`, reject rate, slippage gates, latency gates, and accepted-without-fill gates. It appends stable feedback IDs to `runtime/evidence_os/QuantGod_LiveExecutionFeedback.jsonl` so repeated runs do not duplicate rows.

GA fitness consumes these execution quality fields. High reject rate, excessive slippage, high latency, accepted-without-fill drift, or policy mismatch increase `executionFeedback.penalty`; repeated execution cases add a bounded `caseMemory.penalty`. This keeps GA from promoting strategies that only look good in replay but degrade when the real EA/broker feedback is poor.

## Case Memory

Case Memory converts replay, execution, news-gate, and GA blockers into reusable learning cases:

- `MISSED_BIG_MOVE`
- `EARLY_EXIT`
- `BAD_ENTRY`
- `NEWS_DAMAGE`
- `POLICY_MISMATCH`
- `EXECUTION_REJECT`
- `EXECUTION_SLIPPAGE`
- `EXECUTION_LATENCY`
- `GA_OVERFIT`

Each case carries a mutation hint such as `relax_rsi_crossback`, `let_profit_run`, `tighten_execution_filter`, `inspect_execution_quality`, `reduce_execution_latency`, `verify_execution_ack_fill_sync`, or `reduce_mutation_rate`, which lets GA seed generation use actual operating evidence instead of free-form guessing.

## Independent Telegram Gateway

The Gateway is now a separate push-only notification service:

- Queue: `runtime/notifications/QuantGod_NotificationEventQueue.jsonl`
- Ledger: `runtime/notifications/QuantGod_TelegramGatewayLedger.jsonl`
- Status: `runtime/notifications/QuantGod_TelegramGatewayStatus.json`

It receives `NotificationEvent` objects from local tools, applies dedupe and rate limits, and writes a delivery ledger. It does not receive Telegram commands and it refuses to send if `QG_TELEGRAM_COMMANDS_ALLOWED=1`.

API endpoints:

```text
GET  /api/usdjpy-strategy-lab/telegram-gateway/status
POST /api/usdjpy-strategy-lab/telegram-gateway/test-event
POST /api/usdjpy-strategy-lab/telegram-gateway/dispatch
```

`dispatch?send=1` only sends when `QG_TELEGRAM_PUSH_ALLOWED=1`, token/chat ID are present, and command execution remains disabled.

## Parity Deepening

Parity now checks more than a static contract marker:

- Strategy JSON backtest parity vector exists.
- Backtest evidence persisted into SQLite-backed reports.
- USDJPY live-loop policy agrees with the backtest strategy family and direction when both are available.
- EA RSI diagnostics are merged into parity as a warning/pass layer when present.
- The parity vector now includes Strategy JSON RSI, entry, exit, and risk parameters.
- The EA comparison checks strategy family, direction, RSI period, RSI timeframe, buy-band/oversold tolerance, signal direction, route state, and guard state.
- The report emits `parityDimensions` so the frontend and Telegram can explain the Strategy JSON / Live Loop / MQL5 EA comparison without reading raw files.

Missing live diagnostics produce `WARN`/`MISSING` evidence, not fake passes. Safety failures remain blockers for promotion evidence.

## Safety

- Focus symbol is `USDJPYc`.
- Strategy JSON is used as an audit contract, not a direct order instruction.
- Telegram Gateway is push-only and records a delivery ledger.
- `QG_TELEGRAM_COMMANDS_ALLOWED=1` is rejected by the gateway sender.
- Parity failures block promotion evidence; they do not place or cancel trades.
