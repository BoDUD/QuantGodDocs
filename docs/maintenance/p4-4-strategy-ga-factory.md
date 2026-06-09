# P4-4 Strategy GA Factory

Date: 2026-05-12

## Scope

P4-4 adds a productionization layer around the existing Strategy JSON GA trace:

- factory state;
- elite archive;
- strategy graveyard;
- lineage tree;
- CSV ledger;
- Chinese Telegram text;
- frontend Evolution panel.

It does not replace the GA runner. It reads the existing generation, candidate, elite, blocker, and lineage evidence, then turns that evidence into a stable factory surface for the next generation.

## Backend

New backend surface:

```text
tools/strategy_ga_factory/
tools/run_strategy_ga_factory.py
tools/run_ga_factory.py
Dashboard/strategy_ga_factory_api_routes.js
Dashboard/ga_factory_api_routes.js
tests/test_strategy_ga_factory.py
tests/test_ga_factory.py
tests/node/test_strategy_ga_factory_guard.mjs
tests/node/test_ga_factory_guard.mjs
```

## Runtime Outputs

```text
runtime/ga_factory/QuantGod_GAFactoryState.json
runtime/ga_factory/QuantGod_GAEliteArchive.json
runtime/ga_factory/QuantGod_GAStrategyGraveyard.json
runtime/ga_factory/QuantGod_GALineageTree.json
runtime/ga_factory/QuantGod_GAFactoryLedger.csv
```

## Safety Boundary

No execution capability was added:

- no MT5 order send;
- no close;
- no cancel;
- no MT5 live preset mutation;
- no MT5 `OrderRequest` write;
- no Telegram trading command;
- no external wallet or real-money path.

Factory output can only describe `SHADOW`, `FAST_SHADOW`, `TESTER_ONLY`, or `PAPER_LIVE_SIM` candidates.

## Validation

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m unittest tests.test_ga_factory tests.test_strategy_ga_factory -v
node --test tests/node/test_ga_factory_guard.mjs tests/node/test_strategy_ga_factory_guard.mjs

cd /Users/bowen/Desktop/Quard/QuantGodFrontend
npm run ga-factory
npm run test:ga-factory
npm run build

cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
```
