# Execution Feedback Producer

P4-8B.1 adds a read-only producer that converts existing USDJPY shadow / close-history evidence into normalized execution feedback rows.

It writes:

```text
runtime/execution/QuantGod_LiveExecutionFeedback.jsonl
runtime/execution/QuantGod_LiveExecutionFeedbackProducerReport.json
```

The producer is designed to help P4-8B coverage reporting move from `NO_SAMPLES` toward usable evidence once real or shadow outcomes exist.

## Scope

Allowed:

```text
read local runtime evidence
normalize USDJPY shadow outcomes
normalize USDJPY close-history rows when enough fields exist
write execution feedback evidence
produce Chinese Telegram summary text
```

Forbidden:

```text
order send
close / cancel
MT5 live preset mutation
MT5 OrderRequest writes
Telegram trade commands
external wallet / real-money trading
```

## Commands

```powershell
python tools\run_execution_feedback_producer.py --runtime-dir .\runtime status
python tools\run_execution_feedback_producer.py --runtime-dir .\runtime build --write
python tools\run_execution_feedback_producer.py --runtime-dir .\runtime telegram-text --refresh
```
