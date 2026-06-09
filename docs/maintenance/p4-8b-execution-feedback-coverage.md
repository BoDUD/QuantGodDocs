# P4-8B Execution Feedback Sampling Coverage

P4-8B closes the second Production Evidence WARN by making live and shadow execution feedback measurable.

## Scope

This pass enhances the existing P4-6 Production Evidence Validation report. It does not create a separate API family or separate production evidence truth source.

## What Changed

Execution feedback coverage now reports:

```text
sampleCount
completeSamples
coreCompleteSamples
fieldCoverage
coreCoverage
coverageGrade
evidenceUsability
missingFieldCounts
modeCounts
eventTypeCounts
strategyCoverage
numericSummary
recommendationsZh
```

The audit keeps the existing safety boundary:

```text
orderSendAllowed=false
closeAllowed=false
cancelAllowed=false
livePresetMutationAllowed=false
telegramCommandExecutionAllowed=false
externalMarketRealMoneyAllowed=false
```

## Frontend

The Evolution page shows an execution feedback coverage card. It reads only `/api/production-evidence-validation/*` and does not read runtime files directly.

## Validation

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m py_compile tools/production_evidence_validation/execution_feedback_audit.py tools/production_evidence_validation/report.py
python3 -m unittest tests.test_execution_feedback_sampling_coverage -v
node --test tests/node/test_execution_feedback_sampling_coverage_guard.mjs
python3 tools/run_production_evidence_validation.py --runtime-dir ./runtime build --write
python3 tools/run_production_evidence_validation.py --runtime-dir ./runtime telegram-text --refresh
```

```bash
cd /Users/bowen/Desktop/Quard/QuantGodFrontend
npm run execution-feedback-coverage
npm run test:execution-feedback-coverage
npm run build
```

Expected result:

```text
strategyFamilyParity: PASS
liveExecutionFeedbackCoverage: PASS or quantified WARN
gaMultiGenerationStability: WARN until enough generations exist
```
