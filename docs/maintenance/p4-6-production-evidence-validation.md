# P4-6 Maintenance: Production Evidence Validation

Run P4-6 after major changes to Strategy JSON, GA Factory, Case Memory, parity, execution feedback, or USDJPY history sync.

## Checks

```powershell
python -m py_compile tools\run_production_evidence_validation.py tools\production_evidence_validation\schema.py tools\production_evidence_validation\report.py
python -m unittest tests.test_production_evidence_validation -v
node --test tests\node\test_production_evidence_validation_guard.mjs
```

## Operational interpretation

- `PASS`: all evidence areas are usable for observation.
- `WARN`: the system can continue observing but should not promote weak candidates.
- `FAIL`: fix parity or evidence blockers before promotion.

History production is strict: M1, M5, M15, and H1 must all pass coverage, density, and latest-bar freshness. If only the SQLite tables exist but `QuantGod_USDJPYHistoryProductionStatus.json` reports stale bars, P4-6 must remain `WARN` and GA/promotion should stay blocked.

P4-6 does not change strategy stages by itself. Daily Autopilot and GA promotion gates may consume the report in later phases.
