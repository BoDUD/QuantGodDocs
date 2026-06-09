# P4-3 Case Memory Strategy Candidate

Date: 2026-05-12

## Scope

P4-3 adds the missing bridge from Case Memory to Strategy JSON candidates:

- read existing replay, execution feedback, strategy contract shadow, and GA blocker cases;
- keep a normalized Case Memory report;
- convert root cause into proposed mutation hints;
- generate shadow Strategy JSON candidates;
- expose GA seed hints for the next GA factory step;
- show the result in the Evolution workspace as a read-only panel.

This does not replace the existing Evidence OS Case Memory. It makes the next step explicit and reviewable.

## Safety Boundary

No trading execution was added:

- no order send;
- no close;
- no cancel;
- no live preset mutation;
- no Telegram command receiver;
- no external wallet or real-money path.

`PARITY_FAIL` remains a hard blocker. A strategy cannot enter shadow, GA elite, or micro-live promotion evidence while Strategy JSON / Python replay / MQL5 EA parity is failing.

## Backend

New backend surface:

```text
tools/case_memory/
tools/run_case_memory.py
Dashboard/case_memory_api_routes.js
tests/test_case_memory.py
tests/node/test_case_memory_guard.mjs
```

Outputs:

```text
runtime/case_memory/QuantGod_CaseMemoryStrategyCandidates.json
runtime/case_memory/QuantGod_CaseMemoryStrategyCandidateLedger.jsonl
```

## Frontend

New frontend surface:

```text
src/services/caseMemoryApi.js
src/components/USDJPYCaseMemoryPanel.vue
scripts/frontend_case_memory_guard.mjs
tests/frontend_case_memory_guard.test.mjs
```

The panel shows:

- Case Memory count;
- parity gate status;
- root cause;
- proposed mutation;
- shadow Strategy JSON candidate;
- GA seed count.

## Validation

Required checks:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m unittest tests.test_case_memory -v
node --test tests/node/test_case_memory_guard.mjs

cd /Users/bowen/Desktop/Quard/QuantGodFrontend
npm run case-memory
npm run test:case-memory
npm run build

cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 -m unittest discover tests -v
```

## Next Step

After this passes, the next step is GA Factory Productionization: feed these candidates into multi-generation population, mutation, crossover, elite archive, and blocker-aware promotion evidence.
