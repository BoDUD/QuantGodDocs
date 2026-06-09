# v2.8 Strategy JSON → EA Contract Adapter

This maintenance step adds a read-only MQL5 contract adapter for Strategy JSON candidates.

Scope:

- Backend contract builder under `tools/strategy_contract_adapter`;
- CLI `tools/run_strategy_contract_adapter.py`;
- USDJPY strategy-lab API endpoints for status/build/telegram text;
- MQL5 read-only adapter inside `QuantGod_MultiStrategy.mq5`;
- frontend Evolution status card and detail section.
- EA-side shadow evaluation ledger:
  `QuantGod_StrategyJsonEAShadowEvaluationStatus.json` and
  `QuantGod_StrategyJsonEAShadowEvaluationLedger.jsonl`.
- EA-side shadow evaluation currently supports `RSI_Reversal`, `MA_Cross`,
  `BB_Triple`, `MACD_Divergence`, `SR_Breakout`,
  `USDJPY_TOKYO_RANGE_BREAKOUT`, `USDJPY_NIGHT_REVERSION_SAFE`, and
  `USDJPY_H4_TREND_PULLBACK` Strategy JSON families; unsupported families stay
  in adapter-gap evidence until their read-only adapters are added.
- Evidence OS Case Memory consumes EA shadow evaluation rows and turns
  `SHADOW_WOULD_ENTER`, adapter gaps, or safety rejections into bounded GA seed
  hints.

Safety:

- no MT5 order execution;
- no close/cancel/modify action;
- no live preset mutation;
- no Telegram command receiver;
- no external market real-money path;
- GA candidates remain limited to shadow/tester/paper lane evaluation.

Verification:

```bash
python3 -m py_compile tools/run_strategy_contract_adapter.py tools/strategy_contract_adapter/*.py
python3 -m unittest tests.test_strategy_contract_adapter -v
node --test tests/node/test_strategy_contract_adapter_guard.mjs
python3 tools/run_strategy_contract_adapter.py --runtime-dir runtime build
```

Operational check:

```text
1. Generate the contract from Backend.
2. Reload the EA so it reads the new contract file.
3. Confirm `QuantGod_StrategyJsonEAContractEAStatus.json` appears.
4. Confirm `QuantGod_StrategyJsonEAShadowEvaluationLedger.jsonl` grows over time.
5. Run Evidence OS and verify Case Memory can see contract shadow signals.
```
