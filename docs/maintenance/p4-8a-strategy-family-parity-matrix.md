# P4-8A Strategy Family Parity Matrix Completion

P4-8A completes the Production Evidence parity matrix so P4-6 no longer treats covered USDJPY strategy families as raw missing evidence.

## Scope

This maintenance pass updates the Backend production evidence audit only. It does not add trading execution, modify MT5 live presets, connect external wallets, or enable Telegram commands.

## What Changed

The parity audit now combines:

```text
explicit parity reports
evidence OS parity reports
parity ledgers
Strategy JSON backtest coverage matrix
MQL5 EA shadow adapter ledgers/status
```

It reports every required USDJPY family with a clear status:

```text
PASS
SHADOW_RESEARCH_ONLY
WATCH
FAIL
MISSING
```

`SHADOW_RESEARCH_ONLY` is intentional. It means the family is accounted for by Strategy JSON backtest coverage but remains a shadow research strategy and cannot take the `USDJPYc / RSI_Reversal / LONG` live route.

## Required Families

```text
RSI_Reversal
MA_Cross
BB_Triple
MACD_Divergence
SR_Breakout
USDJPY_TOKYO_RANGE_BREAKOUT
USDJPY_NIGHT_REVERSION_SAFE
USDJPY_H4_TREND_PULLBACK
```

## Validation

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m py_compile tools/run_production_evidence_validation.py tools/production_evidence_validation/*.py
python3 -m unittest tests.test_production_evidence_validation -v
node --test tests/node/test_production_evidence_validation_guard.mjs
python3 tools/run_production_evidence_validation.py --runtime-dir ./runtime build --write
python3 tools/run_production_evidence_validation.py --runtime-dir ./runtime telegram-text --refresh
```

Expected production evidence after this pass:

```text
historyProduction: PASS
strategyFamilyParity: PASS
liveExecutionFeedbackCoverage: WARN until more samples exist
gaMultiGenerationStability: WARN until more GA generations exist
```
