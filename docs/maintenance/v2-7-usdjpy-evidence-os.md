# v2.7 USDJPY Evidence OS

Date: 2026-05-07

## Scope

This maintenance step lays the Perfect Edition evidence foundation:

- real USDJPY K-line incremental ingest from MT5 runtime snapshots;
- multi-timeframe SQLite audit context for M15/H1/H4/D1;
- Strategy JSON backtest evidence for GA fitness;
- Strategy JSON / Python Replay / MQL5 EA parity report;
- standardized EA `quantgod.live_execution_feedback.v1` rows from real-time trade transactions, order-send results, and broker history rebuilds;
- live execution feedback ingestion and execution quality report;
- Case Memory for missed opportunities, early exits, execution rejects, slippage, latency, ack/fill drift, policy mismatch, and GA blocker drift;
- push-only Telegram Gateway ledger.

## Evidence Deepening

The Evidence OS now sends richer real execution data into the learning loop:

- parity vectors include Strategy JSON RSI, entry, exit, and risk parameters;
- MQL5 RSI diagnostics are compared against Strategy JSON family, direction, RSI period, timeframe, signal direction, route, and guard state;
- execution feedback derives dominant reject reason, accepted-without-fill count, max latency, reject rate, slippage, latency, and policy mismatch;
- Case Memory creates explicit `EXECUTION_REJECT`, `EXECUTION_SLIPPAGE`, `EXECUTION_LATENCY`, and `POLICY_MISMATCH` cases;
- GA fitness applies bounded execution and case-memory penalties so candidates are not judged only by replay/backtest profit.

This is still an audit and learning plane. It does not grant GA or DeepSeek authority to trade.

## Safety Boundary

No trading execution was added:

- no order send;
- no close;
- no cancel;
- no live preset mutation;
- no Telegram command receiver;
- no external market real-money path.

## Operator Impact

The Evolution panel can now show:

- real USDJPY K-line ingest counts;
- parity status;
- execution feedback rows, rejects, slippage, and net R;
- Case Memory items queued for GA;
- a single Evidence OS action that runs the whole audit chain.

## Validation

Required checks:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m unittest tests.test_usdjpy_evidence_os -v
node --test tests/node/test_usdjpy_evidence_os_guard.mjs

cd /Users/bowen/Desktop/Quard/QuantGodFrontend
npm run usdjpy-evolution
npm test
npm run build

cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python3 -m unittest discover tests -v
```
