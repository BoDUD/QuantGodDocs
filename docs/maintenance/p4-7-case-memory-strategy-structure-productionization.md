# P4-7 Case Memory Strategy Structure Productionization

Date: 2026-05-12

## Scope

P4-7 productionizes the existing Case Memory candidate bridge without replacing the current API or frontend panel.

It adds a compatibility layer:

```text
tools/strategy_structure_lab/
```

That layer wraps the existing:

```text
tools/case_memory/
tools/run_case_memory.py
Dashboard/case_memory_api_routes.js
src/components/USDJPYCaseMemoryPanel.vue
```

The goal is to make this flow explicit and auditable:

```text
missed move / early exit / execution feedback / parity blocker / GA blocker
→ Case Memory
→ root cause
→ proposed mutation
→ shadow Strategy JSON candidate
→ GA seed hint
```

## Why It Does Not Overwrite P4-3

The current main branch already has a richer Case Memory implementation than the original P4-7 overlay.
P4-7 therefore keeps the current runtime shape and adds production metadata instead of downgrading:

```text
p4Stage = P4-7
strategyStructureProduction = true
strategyStructureProductionOnly = true
shadowStrategyJsonCandidateOnly = true
gaSeedHintOnly = true
```

## Safety Boundary

No trading execution was added:

- no order send;
- no close;
- no cancel;
- no MT5 live preset mutation;
- no MT5 OrderRequest write;
- no Telegram trading command receiver;
- no external wallet or real-money path.

Candidates remain shadow Strategy JSON candidates and GA seed hints. `PARITY_FAIL` remains a hard blocker.

## Validation

Required checks:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 -m py_compile \
  tools/run_case_memory.py \
  tools/strategy_structure_lab/schema.py \
  tools/strategy_structure_lab/io_utils.py \
  tools/strategy_structure_lab/builder.py \
  tools/strategy_structure_lab/candidate_builder.py \
  tools/strategy_structure_lab/report.py \
  tools/strategy_structure_lab/telegram_text.py

python3 -m unittest tests.test_case_memory -v
node --test tests/node/test_case_memory_guard.mjs

python3 tools/run_case_memory.py --runtime-dir /tmp/qg_case_test sample --overwrite
python3 tools/run_case_memory.py --runtime-dir /tmp/qg_case_test build --write
python3 tools/run_case_memory.py --runtime-dir /tmp/qg_case_test telegram-text --refresh
```

Docs:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python3 -m unittest discover tests -v
```

## Next Step

After P4-7, the next production gap is not another Case Memory endpoint. It is higher-quality evidence:

- more live execution feedback samples;
- more complete strategy-family parity matrix;
- more GA multi-generation stability evidence;
- more Case Memory seed outcomes feeding GA fitness.
