# Strategy JSON GA Evolution Trace

QuantGod v2.6 adds an auditable Strategy JSON evolution trace for USDJPY research. The goal is not to let GA trade; the goal is to make every generation, seed, fitness score, blocker, mutation, crossover, and elite decision visible to the operator.

## Scope

This system is USDJPY-only and writes local research evidence under:

```text
runtime/ga/
```

It may create and score Strategy JSON candidates for:

```text
MT5 Shadow Lane
Tester-only validation
Paper-live simulation
Daily Autopilot research tasks
```

It must not affect:

```text
USDJPY Live Lane execution
MT5 OrderSend / CTrade
close / cancel / order modification
live preset mutation
external wallet real-money path
Telegram trade commands
```

## Trace Files

The GA runner writes:

```text
QuantGod_GAStatus.json
QuantGod_GAGenerationLatest.json
QuantGod_GAGenerationLedger.jsonl
QuantGod_GACandidateRuns.jsonl
QuantGod_GAEliteStrategies.json
QuantGod_GABlockerSummary.json
QuantGod_GAEvolutionPath.json
QuantGod_GAFitnessCache.json
QuantGod_GALineage.json
QuantGod_GARunLimiter.json
```

Each candidate run records:

```text
generationId
seedId
strategyId
source
replayStatus
walkForwardStatus
fitness
fitnessBreakdown
rank
blockerCode
reasonZh
promotionStage
strategyJson
cacheHit
evidenceSignature
```

## Case Memory Seeds

GA can turn operating evidence from Case Memory into safe shadow research seeds.
Only cases with `status=QUEUED_FOR_GA` are used, and each case seed remains:

```text
symbol = USDJPYc
strategyFamily = RSI_Reversal
direction = LONG
stage = SHADOW
maxLot <= 2.0
```

Case Memory may suggest mutation hints such as:

```text
relax_rsi_crossback
let_profit_run
tighten_entry_filter
inspect_execution_quality
reduce_execution_latency
verify_execution_ack_fill_sync
```

These hints create Strategy JSON candidates for GA scoring. They do not change the
live preset, do not grant live permissions, and do not let GA bypass hard gates.

## Fitness Cache And Lineage

GA scoring now uses an evidence signature derived from the current replay,
walk-forward, Strategy JSON backtest, parity, execution quality, and Case Memory
files. When the Strategy JSON fingerprint and evidence signature match a previous
score, GA reuses the cached fitness entry in `QuantGod_GAFitnessCache.json`.

This prevents repeated generations from rescoring identical strategies against
unchanged evidence while still invalidating the cache whenever the underlying
evidence files change.

The runner also writes `QuantGod_GALineage.json`, which tracks:

```text
case-memory seed origin
mutation parent
crossover parents
candidate source
```

This makes it possible to answer not only which seed won, but where it came from.

`QuantGod_GARunLimiter.json` records the last generation run. By default the
limiter is permissive; deployments may set `QG_GA_MIN_RUN_INTERVAL_SECONDS` to
prevent noisy repeated GA runs.

## GA Factory

P4-4 adds a factory layer under `runtime/ga_factory/`. It reads the GA trace and
produces:

```text
QuantGod_GAFactoryState.json
QuantGod_GAEliteArchive.json
QuantGod_GAStrategyGraveyard.json
QuantGod_GALineageTree.json
QuantGod_GAFactoryLedger.csv
```

This layer makes elite reuse, blocked-strategy avoidance, and next-generation
production status visible without granting live execution authority.

## Strategy JSON Safety

Every seed must validate as `quantgod.strategy.v1`. The validator rejects:

```text
non-USDJPY symbols
live stages such as MICRO_LIVE / LIVE_LIMITED
maxLot above 2.0
OrderSend / CTrade / TRADE_ACTION_DEAL
eval / exec / import / function bodies
privateKey / wallet / Telegram command execution
external real-money market permissions
```

The validator accepts explicit `false` safety fields, for example `orderSendAllowed=false`. Those fields are required as safety declarations and must not be confused with permission grants.

## Fitness

Fitness is not pure profit. It combines:

```text
netR
profitCaptureRatio
missedOpportunityReduction
maxAdverseR penalty
drawdown / instability / overfit penalties
sample-count penalty
trade-frequency penalty
```

Candidates with insufficient evidence remain `NEEDS_MORE_DATA` or `SHADOW`; they are not promoted to live.

Fitness also consumes execution feedback and Case Memory penalties. Excessive
rejects, slippage, latency, accepted-without-fill drift, policy mismatch, or
repeated Case Memory warnings reduce score so GA does not promote strategies that
only look good in replay.

## Frontend

The Evolution workspace must show the full process:

```text
generation timeline
candidate table
seed detail drawer
Strategy JSON preview
fitness breakdown
blocker summary
elite / mutation / crossover source
```

The page must make it clear that GA only enters shadow/tester/paper research and cannot directly trade.

## Telegram

The GA Telegram report is Chinese and push-only. It summarizes:

```text
current generation
population size
best seed / best fitness
elite count
blocked candidate count
main blockers
next action
safety boundary
```

Telegram still cannot receive or execute trading commands.
