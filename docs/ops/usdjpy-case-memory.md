# USDJPY Case Memory Strategy Candidates

P4-3 introduced the first bridge from Case Memory into shadow Strategy JSON candidates and GA seed hints.
P4-7 productionizes that bridge as a strategy-structure learning layer: it keeps the existing `/api/case-memory/*` surface, adds `strategy_structure_lab` metadata, and makes the root-cause → candidate → GA seed path explicit.

It is still a learning and audit step, not a trading executor.

## Flow

```text
Replay / execution feedback / strategy contract shadow / GA blocker
→ Case Memory
→ root cause
→ proposed mutation
→ shadow Strategy JSON candidate
→ GA seed
```

If parity is `PARITY_FAIL`, candidate generation is blocked. The operator must fix Strategy JSON / Python replay / MQL5 EA consistency before the candidate can move into shadow or GA elite review.

## Runtime Outputs

```text
runtime/evidence_os/QuantGod_CaseMemory.jsonl
runtime/evidence_os/QuantGod_CaseMemorySummary.json
runtime/case_memory/QuantGod_CaseMemoryStrategyCandidates.json
runtime/case_memory/QuantGod_CaseMemoryStrategyCandidateLedger.jsonl
runtime/case_memory/QuantGod_CaseMemoryArtifactManifest.json
runtime/strategy-json/candidates/*.json
```

`QuantGod_CaseMemoryArtifactManifest.json` records the candidate report and
candidate ledger with runtime-relative paths, byte sizes, and `sha256` hashes.
It is an audit manifest only; it does not change candidate scoring or execution
eligibility.

The P4-7 compatibility layer is exposed through:

```text
tools/strategy_structure_lab/
```

It wraps the existing Case Memory implementation instead of replacing it.

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_case_memory.py --runtime-dir ./runtime status
python3 tools/run_case_memory.py --runtime-dir ./runtime build --write
python3 tools/run_case_memory.py --runtime-dir ./runtime telegram-text --refresh
```

For a local smoke test:

```bash
tmp="$(mktemp -d)"
python3 tools/run_case_memory.py --runtime-dir "$tmp" sample --overwrite
python3 tools/run_case_memory.py --runtime-dir "$tmp" build --write
python3 tools/run_case_memory.py --runtime-dir "$tmp" telegram-text --refresh
```

## API

```text
GET  /api/case-memory/status
POST /api/case-memory/build
GET  /api/case-memory/telegram-text
```

The frontend uses `src/services/caseMemoryApi.js` and the Evolution workspace panel. It does not read runtime files directly.

## Coverage Plan

`/api/case-memory/status` exposes `coveragePlan` so the operator can see exactly why Case Memory still blocks GA or champion promotion. The gate is not satisfied by a raw case count alone; it requires coverage across the taxonomy that can explain bad entries, missed opportunities, early exits, spread or news damage, and GA overfit.

Important fields:

```text
coveragePlan.status
coveragePlan.missingCategories
coveragePlan.missingRows
coveragePlan.nextCollectionQueue
coveragePlan.targetSampleCount
coveragePlan.observedSampleCount
coveragePlan.remainingTargetSampleCount
```

`missingRows` is the table-friendly view. Each row includes:

```text
category
observedCount
targetCount
remainingCount
priority
sourceArtifacts
collectionEndpoint
collectionCommand
caseMemoryBuildCommand
verifyCommand
nextActionZh
acceptanceZh
```

`collectionCommand` refreshes the upstream read-only/shadow/tester evidence for that category. `caseMemoryBuildCommand` rebuilds the Case Memory candidate report from those artifacts. `verifyCommand` reruns the core runtime evidence integrity gate. These commands may write local evidence reports, but they are not trading instructions.

`nextCollectionQueue` is the operator work queue sorted by priority and remaining evidence. It should be read as an evidence collection plan, not as a trading instruction. Current high-priority examples are:

- `BAD_ENTRY`: collect entry-context feedback or bar-replay samples where MAE expands quickly, MFE stays weak, or a reverse signal appears after entry.
- `GA_OVERFIT`: collect GA candidates that look good in train but fail walk-forward, forward, or champion retest.
- `MISSED_OPPORTUNITY`: collect shadow signals that were blocked by spread, session, news, or cooldown and then moved profitably.
- `EARLY_EXIT`: collect exits where price continues favorably after close, with MFE giveback and profit-capture ratio.
- `NEWS_DAMAGE`: collect news-window loss or missed-opportunity replay cases with the gate decision and later market impact.

Allowed collection endpoints are read-only or tester/shadow evidence surfaces such as:

```text
/api/usdjpy-strategy-lab/evidence-os/execution-feedback
/api/usdjpy-strategy-lab/ga/blockers
/api/usdjpy-strategy-lab/bar-replay/entry
/api/usdjpy-strategy-lab/bar-replay/exit
/api/usdjpy-strategy-lab/bar-replay/status
```

Do not satisfy these gaps by editing live presets, forcing entries, writing MT5 order request files, or enabling live execution. The right fix is to collect better replay, shadow, tester, and execution-feedback evidence until the required categories and sample targets are met.

## Safety

- No order send.
- No close.
- No cancel.
- No MT5 live preset mutation.
- No Telegram trading command.
- No external market real-money path.
- Candidates remain `SHADOW_STRATEGY_JSON_CANDIDATE`.
- Candidates remain GA seed hints until replay, backtest, parity, and promotion evidence accept them.
- `PARITY_FAIL` blocks candidate generation and promotion evidence.
