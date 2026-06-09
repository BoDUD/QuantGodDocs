# P4-6 Production Evidence Validation

P4-6 verifies whether the current QuantGod production evidence is strong enough to trust the autonomous USDJPY workflow.

It validates four evidence areas:

1. USDJPY historical data production status.
2. Strategy JSON / Python / EA parity coverage by strategy family.
3. Live and shadow execution feedback field coverage.
4. GA multi-generation stability evidence.

This stage is read-only. It does not place orders, close positions, cancel orders, mutate live presets, connect external wallets, or receive Telegram trading commands.

## CLI

```powershell
python tools\run_production_evidence_validation.py --runtime-dir .\runtime build --write
python tools\run_production_evidence_validation.py --runtime-dir .\runtime telegram-text --refresh
```

## API

```text
GET  /api/production-evidence-validation/status
POST /api/production-evidence-validation/run
GET  /api/production-evidence-validation/telegram-text?refresh=1
```

## Outputs

```text
runtime/production_validation/QuantGod_ProductionEvidenceValidationReport.json
runtime/production_validation/QuantGod_StrategyFamilyParityMatrix.json
runtime/production_validation/QuantGod_LiveExecutionFeedbackCoverage.json
runtime/production_validation/QuantGod_GAMultiGenerationStabilityReport.json
```

## Strategy Family Parity Matrix

P4-8A upgrades the parity audit from a single-file check into a family coverage matrix. The audit now accounts for:

```text
runtime/parity/QuantGod_StrategyParityReport.json
runtime/evidence_os/QuantGod_StrategyParityReport.json
runtime/parity/QuantGod_StrategyParityLedger.csv
runtime/backtest/QuantGod_StrategyBacktestReport.json
MT5 Strategy JSON EA shadow evaluation ledger/status files
```

Every required USDJPY strategy family must appear in the matrix:

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

Valid non-failing outcomes are:

```text
PASS
SHADOW_RESEARCH_ONLY
WATCH
```

`PASS` means the live-eligible route or direct parity evidence is covered. `SHADOW_RESEARCH_ONLY` means the family has Strategy JSON backtest coverage but remains a research candidate and cannot seize the USDJPY RSI live lane. `WATCH` means partial shadow adapter evidence exists and should be observed.

## Execution Feedback Coverage

P4-8B expands the execution feedback section from a coarse sample warning into a coverage report. It measures:

```text
sampleCount
completeSamples
coreCompleteSamples
fieldCoverage
coreCoverage
coverageGrade
evidenceUsability
missingFieldCounts
modeCounts
eventTypeCounts
strategyCoverage
numericSummary
recommendationsZh
```

The required execution feedback fields are:

```text
strategyId
eventType
expectedPrice
fillPrice
slippagePips
latencyMs
spreadAtEntry
profitR
mfeR
maeR
```

## Safety

The report is advisory and read-only. Any `PARITY_FAIL` must block promotion. Missing execution feedback should keep candidates in observation until more samples are collected.
