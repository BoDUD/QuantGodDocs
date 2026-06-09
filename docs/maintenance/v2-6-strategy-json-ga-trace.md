# v2.6 Strategy JSON GA Evolution Trace

## Summary

QuantGod v2.6 introduces a USDJPY-only Strategy JSON GA trace. It makes the genetic search process inspectable instead of presenting only the final result.

## Backend

New backend modules:

```text
tools/strategy_json/
tools/strategy_ga/
tools/run_strategy_ga.py
```

New local evidence:

```text
runtime/ga/QuantGod_GAStatus.json
runtime/ga/QuantGod_GAGenerationLatest.json
runtime/ga/QuantGod_GAGenerationLedger.jsonl
runtime/ga/QuantGod_GACandidateRuns.jsonl
runtime/ga/QuantGod_GAEliteStrategies.json
runtime/ga/QuantGod_GABlockerSummary.json
runtime/ga/QuantGod_GAEvolutionPath.json
runtime/ga/QuantGod_GAFitnessCache.json
runtime/ga/QuantGod_GALineage.json
runtime/ga/QuantGod_GARunLimiter.json
```

## v2.6.2 Hardening

The GA trace has been hardened so it can use the evidence loop created by
Execution Feedback and Case Memory:

```text
Case Memory queued for GA -> Strategy JSON shadow seed
Strategy fingerprint + evidence signature -> cached fitness score
Mutation / crossover / case origin -> lineage trace
Generation run timestamp -> optional frequency limiter
```

This makes repeated GA runs more auditable and less noisy:

- Case Memory seeds are generated only from `QUEUED_FOR_GA` cases and stay in `SHADOW`.
- Fitness cache entries are invalidated whenever replay, walk-forward, backtest, parity, execution quality, or Case Memory evidence changes.
- Lineage records parent seeds, crossover parents, and case-memory origins.
- The run limiter is off by default but can be enabled with `QG_GA_MIN_RUN_INTERVAL_SECONDS`.

These additions do not add live execution, live preset mutation, Telegram commands,
or external real-money market access.

New API surface:

```text
GET  /api/usdjpy-strategy-lab/ga
GET  /api/usdjpy-strategy-lab/ga/status
POST /api/usdjpy-strategy-lab/ga/run-generation
GET  /api/usdjpy-strategy-lab/ga/generations
GET  /api/usdjpy-strategy-lab/ga/candidates
GET  /api/usdjpy-strategy-lab/ga/candidate/:seedId
GET  /api/usdjpy-strategy-lab/ga/evolution-path
GET  /api/usdjpy-strategy-lab/ga/blockers
GET  /api/usdjpy-strategy-lab/ga/telegram-text
```

## Frontend

The USDJPY Evolution panel now includes:

```text
GA status cards
generation timeline
candidate table
selected seed detail
fitness breakdown
Strategy JSON preview
blocker summary
```

This is a process audit page, not just a result page.

## Daily Autopilot

Daily Autopilot v2.6 treats Strategy JSON and GA trace as active Agent tasks:

```text
GENERATE_GA_SEEDS
RUN_GA_GENERATION
PROMOTE_GA_ELITES_TO_SHADOW
```

Telegram Gateway remains a next-phase item.

## Safety

No new trading execution was added.

The GA system cannot:

```text
place MT5 orders
close or cancel orders
modify MT5 live preset
enter MICRO_LIVE directly
connect a external wallet real-money path
execute Telegram commands
generate arbitrary code
```

GA candidates may only enter:

```text
MT5 Shadow Lane
Tester-only validation
Paper-live simulation
Autonomous governance evidence
```

Live Lane remains:

```text
USDJPYc / RSI_Reversal / LONG
```

## Verification

Run:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m unittest tests.test_strategy_json_ga -v
node --test tests/node/test_strategy_ga_guard.mjs
python3 tools/run_strategy_ga.py --runtime-dir ./runtime run-generation --write
python3 tools/run_strategy_ga.py --runtime-dir ./runtime telegram-text --refresh
```

Frontend:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodFrontend
npm run usdjpy-evolution
npm run test:usdjpy-evolution
```

Docs:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
```
