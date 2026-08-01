# Forex Live-Automation Readiness

`/api/live-automation/*` turns the sim-to-live question into a local, review-only dossier for the foreign-exchange system. USDJPY is the current primary pair. HFM remains supported as an FX broker; non-FX instruments and exchange or wallet integrations are outside the product scope.

Readiness is evidence, not permission. A passing review may create a research packet, but it must never write an MT5 request, call a broker, change a live preset, or bypass the kill switch.

## Scope

The active pipeline combines:

- USDJPY MT5 runtime freshness and account-mode evidence;
- historical bar coverage and synchronization quality;
- replay, walk-forward and Strategy JSON parity;
- execution feedback and sample sufficiency;
- GA blockers and promotion-gate state;
- spread, high-impact news, loss and rollback hard guards;
- dry-run review artifacts and operator-facing explanations.

Other FX pairs may be added only after their symbol mapping, historical data, contract costs, replay parity and safety gates are reviewed. They do not inherit USDJPY eligibility automatically.

## Safety Contract

Every readiness artifact and endpoint must preserve these effective values:

```text
executionReady=false
orderSendAllowed=false
mt5OrderSendAllowed=false
brokerExecutionAllowed=false
writesMt5OrderRequest=false
requestWritesAllowed=false
requestFilesWritten=false
receiptWritesAllowed=false
brokerCallsMade=false
livePresetMutationAllowed=false
```

Missing, stale, malformed or version-incompatible evidence is `UNKNOWN` or `STALE`, never a pass. `READY_FOR_OPERATOR_REVIEW_PACKET` means only that the local research dossier may be assembled.

## Active Read-Only Endpoints

The contract is generated from Backend routes. The active forex documentation covers these route families:

```text
GET  /api/live-automation/status
POST /api/live-automation/build
GET  /api/live-automation/pipeline
GET  /api/live-automation/promotion-candidates
GET  /api/live-automation/review-packet
GET  /api/live-automation/runtime-preflight
GET  /api/live-automation/mt5-request-contract
GET  /api/live-automation/telegram-text
```

Exact routes, methods and schemas are defined in `docs/contracts/api-contract.json` after regeneration from the forex-only Backend. A `GET` endpoint must be pure read. Refreshing or building evidence must use `POST` and return an explicit command result.

## Evidence Inputs

The pipeline should bind all inputs to one snapshot lineage:

```text
QuantGod_Dashboard.json
QuantGod_USDJPYHistoryProductionStatus.json
QuantGod_USDJPYStrategyBacktestReport.json
QuantGod_USDJPYWalkForwardReport.json
QuantGod_USDJPYStrategyParityReport.json
QuantGod_ExecutionFeedbackCoverage.json
QuantGod_GAStatus.json
QuantGod_PromotionGate.json
```

An input is usable only when it carries or can be wrapped with:

- schema and version;
- `observedAt`, `dataAsOf` and expiry;
- source repository revision;
- dataset and artifact hashes;
- explicit status and reason codes.

Files from different snapshot IDs must not be merged into a green summary.

## Review Flow

```text
fresh MT5/read-only evidence
  -> history production quality
  -> replay and walk-forward
  -> Strategy JSON / Python / MQL5 parity
  -> execution-feedback coverage
  -> GA and promotion blockers
  -> dry-run review packet
  -> operator-facing report
```

At every transition, the worst input status wins. A service process being alive cannot override stale market data, failed parity, insufficient samples or a blocked promotion gate.

## Runtime Preflight

Runtime preflight must verify:

1. the MT5 snapshot is recent and was produced by the expected read-only EA build;
2. symbol and server identity match the selected FX profile without exposing the account identifier;
3. the requested symbol is an allowed FX symbol;
4. spread, market session and high-impact news gates are explicit;
5. kill switch and daily-loss fuses are observable;
6. read-only/shadow mode is effective;
7. every execution flag remains false.

An HFM account is valid here only as an FX broker account. Broker branding must never imply that another asset class is enabled.

## Promotion Candidates

`QuantGod_LivePromotionCandidates.json` ranks only eligible FX research lanes. Ranking must include the evidence score and all blockers; it must not auto-promote a candidate or mutate a preset.

The current live doctrine remains narrow:

```text
USDJPYc / RSI_Reversal / LONG
```

All other USDJPY strategy families and all additional FX pairs remain `SHADOW`, `FAST_SHADOW`, `TESTER_ONLY` or `PAPER_LIVE_SIM` until a separate execution-lane RFC is reviewed. The present system still keeps execution disabled.

## Operator Acceptance

The readiness view is acceptable only when:

- stale or missing evidence never displays as healthy;
- HTTP success plus `ok:false` is displayed as failure;
- account identifiers are masked;
- the UI shows service health, data health, research readiness and execution permission separately;
- the execution-permission card remains `DISABLED`;
- no non-FX route, evidence checklist item or workspace is present;
- rerunning a review cannot place, close, cancel or modify an order.

## Local Verification

Use the project-wide checks after Backend route cleanup and contract regeneration:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py \
  --contract docs/contracts/api-contract.json \
  --backend ../QuantGodBackend \
  --strict-extra
python3 -m unittest discover tests -v
```

The API checks intentionally fail if the generated contract or Backend still exposes a crypto-only route. This is a scope guard, not a temporary warning.
