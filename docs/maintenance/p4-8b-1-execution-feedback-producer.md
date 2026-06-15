# P4-8B.1 Execution Feedback Producer Maintenance

This maintenance note covers the USDJPY execution feedback producer.

## Purpose

P4-8B reported execution feedback coverage precisely. In live runtime, coverage may remain `NO_SAMPLES` until MT5 or shadow paths write normalized feedback. P4-8B.1 adds a producer that can normalize existing shadow and close-history evidence into the feedback ledger.

The producer also writes `runtime/execution/QuantGod_LiveExecutionFeedbackArtifactManifest.json`.
The manifest has schema `quantgod.execution_feedback_producer.artifact_manifest.v1`
and records the execution feedback ledger and producer report with
runtime-relative paths, byte sizes, and `sha256` hashes. This keeps the evidence
chain auditable without embedding machine-specific absolute paths.

## Safety

The producer is read-only with respect to trading. It does not send orders, close positions, modify presets, or accept Telegram commands.

## Validation

Run:

```powershell
python -m py_compile tools\run_execution_feedback_producer.py tools\execution_feedback_producer\schema.py tools\execution_feedback_producer\io_utils.py tools\execution_feedback_producer\producer.py tools\execution_feedback_producer\telegram_text.py
python -m unittest tests.test_execution_feedback_producer -v
node --test tests\node\test_execution_feedback_producer_guard.mjs
```
