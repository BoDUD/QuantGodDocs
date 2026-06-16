# P4-6 Production Evidence Validation

P4-6 verifies whether the current QuantGod production evidence is strong enough to trust the autonomous USDJPY workflow.

It validates five evidence areas:

1. Core runtime evidence integrity.
2. USDJPY historical data production status.
3. Strategy JSON / Python / EA parity coverage by strategy family.
4. Live and shadow execution feedback field coverage.
5. GA multi-generation stability evidence.

It also imports Case Memory taxonomy coverage from the core runtime evidence manifest. If Case Memory is missing required categories or target sample counts, P4-6 must remain blocked even when the evidence files themselves are present and hashed.

This stage is read-only. It does not place orders, close positions, cancel orders, mutate live presets, connect external wallets, or receive Telegram trading commands.

## Core Runtime Evidence Integrity

The first section now embeds the core evidence manifest produced by `runtime_evidence_integrity`.
It hashes and schema-checks the files that downstream promotion relies on:

```text
runtime/live/QuantGod_USDJPYLiveLoopStatus.json
runtime/live/QuantGod_USDJPYLiveLoopLedger.csv
runtime/agent/QuantGod_ProductionExecutionPolicy.json
runtime/adaptive/QuantGod_AutoExecutionPolicy.json
runtime/adaptive/QuantGod_AutoExecutionPolicyLedger.csv
runtime/ga_factory/QuantGod_GAFactoryArtifactManifest.json
runtime/execution/QuantGod_LiveExecutionQualityReport.json
runtime/execution/QuantGod_LiveExecutionFeedback.jsonl
runtime/case_memory/QuantGod_CaseMemoryArtifactManifest.json
runtime/production_validation/QuantGod_ProductionEvidenceValidationReport.json
```

If any required file is missing, declares the wrong schema, lacks artifact hashes, or still contains a legacy `/Users/.../Quard/QuantGod/...` absolute path, the production evidence report becomes `FAIL`. This keeps stale or split-brain runtime evidence from entering GA, case memory, or promotion review.

## History Production Gate

The history section is now a strict GA / promotion prerequisite. It requires all core USDJPY timeframes to pass together:

```text
M1
M5
M15
H1
```

Each timeframe must satisfy:

- `spanOk`: enough 6-12 month lookback coverage.
- `densityOk`: enough bars for that timeframe.
- `freshnessOk`: latest bar lag is within the production threshold.

The report also reads `runtime/backtest/QuantGod_USDJPYHistoryProductionStatus.json`. If that artifact says `historyTargetSatisfied=false`, P4-6 keeps `historyProduction.status=WARN` even when the SQLite tables exist. A common interpretation is: coverage may be good, but the background history sync is stale, so GA and promotion must stay blocked until `sync-klines` refreshes M1/M5/M15/H1.

P4-6 now exposes a per-timeframe recovery queue so stale history does not appear as a vague blocker:

```text
historyProduction.staleTimeframes
historyProduction.freshnessRecoveryQueue
historyProduction.nextRecoveryActionZh
```

Each `freshnessRecoveryQueue` row includes the timeframe, priority, current lag, max allowed lag, source artifacts, a `sync-klines` refresh command, a `production-status` verify command, acceptance criteria, allowed lanes, and forbidden side effects. Treat this queue as an evidence recovery plan only. It may refresh local SQLite/backtest artifacts, but it must not place orders, close positions, mutate live presets, write MT5 order request/receipt files, authorize wallets, or bypass `orderSendAllowed=false`.

When coverage and density are already true but freshness is stale, the expected recovery path is:

```bash
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime sync-klines --months 12 --timeframes M1,M5,M15,H1
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime production-status --months 12 --max-latest-lag-hours 96
```

Only after all queue rows show `spanOk=true`, `densityOk=true`, `freshnessOk=true`, `passed=true`, and `historyTargetSatisfied=true` can history stop blocking GA or champion promotion.

## Case Memory Coverage Gate

Case Memory promotion evidence is separate from core file integrity. A manifest can pass schema and hash checks while the promotion gate still blocks because the learning set is too narrow.

P4-6 surfaces the Case Memory coverage plan through:

```text
caseMemoryCoverage.status
caseMemoryCoverage.missingCategories
caseMemoryCoverage.missingRows
caseMemoryCoverage.nextCollectionQueue
caseMemoryCoverage.targetSampleCount
caseMemoryCoverage.observedSampleCount
caseMemoryCoverage.remainingTargetSampleCount
```

Required taxonomy coverage:

```text
BAD_ENTRY
MISSED_OPPORTUNITY
EARLY_EXIT
SPREAD_DAMAGE
NEWS_DAMAGE
GA_OVERFIT
```

`missingRows` is the audit table used by the frontend. It includes the required sample target, remaining count, priority, source artifacts, collection endpoint, next action, and acceptance criteria for each missing category.

`nextCollectionQueue` is the actionable queue for evidence collection. It may point to execution-feedback, GA blocker, or bar-replay endpoints, but those endpoints remain read-only, shadow, tester, or replay-only. They must not place orders, close positions, cancel orders, mutate live presets, write MT5 request or receipt files, authorize wallets, or bypass `orderSendAllowed=false`.

When both history freshness and Case Memory coverage are blocked, fix them independently:

- refresh M1/M5/M15/H1 history until `freshnessOk=true` and the history production target is satisfied;
- collect enough Case Memory samples for the missing categories through replay, shadow, tester, and execution feedback.

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
runtime/integrity/QuantGod_CoreRuntimeEvidenceManifest.json
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
