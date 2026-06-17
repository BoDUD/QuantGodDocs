# Runtime Evidence Integrity

`tools/run_runtime_evidence_integrity.py` builds a read-only integrity manifest for the core QuantGod runtime evidence chain.

It exists for the P3 hardening lane: operators should be able to prove that live-loop, production policy, GA Factory, execution feedback, Case Memory, and production validation artifacts all have stable schemas, runtime-relative paths, byte sizes, and `sha256` hashes before any promotion review trusts them.

## Command

Run from `QuantGodBackend`:

```bash
python3 tools/run_runtime_evidence_integrity.py --runtime-dir ./runtime verify
python3 tools/run_runtime_evidence_integrity.py --runtime-dir ./runtime summary
python3 tools/run_runtime_evidence_integrity.py --runtime-dir ./runtime build
```

`verify` prints the manifest and exits non-zero when a required artifact is missing, a JSON/JSONL schema drifts, a CSV header is absent, an artifact manifest lacks per-file hashes, or a core artifact contains an old `/Quard/QuantGod/` legacy absolute path.

`summary` prints a compact, frontend-friendly envelope with `status`, `promotionGateStatus`, bounded `promotionBlockers`, bounded `promotionRecoveryQueue`, overflow counts, `nextActionZh`, and the immutable safety block. It is read-only and does not write runtime files.

`build` writes:

```text
runtime/integrity/QuantGod_CoreRuntimeEvidenceManifest.json
```

The output is an audit artifact only. It does not write MT5 order requests, mutate presets, call a broker, authorize wallets, or enable order sending.

## Covered Artifacts

- `live/QuantGod_USDJPYLiveLoopStatus.json`
- `live/QuantGod_USDJPYLiveLoopLedger.csv`
- `agent/QuantGod_ProductionExecutionPolicy.json`
- `adaptive/QuantGod_AutoExecutionPolicy.json`
- `adaptive/QuantGod_AutoExecutionPolicyLedger.csv`
- `ga_factory/QuantGod_GAFactoryArtifactManifest.json`
- `execution/QuantGod_LiveExecutionQualityReport.json`
- `execution/QuantGod_LiveExecutionFeedback.jsonl`
- `case_memory/QuantGod_CaseMemoryArtifactManifest.json`
- `production_validation/QuantGod_ProductionEvidenceValidationReport.json`

## Promotion Recovery Queue

The manifest separates file integrity from promotion readiness. A run can have
`status=PASS` while `promotionGateStatus=BLOCKED` when the runtime files are
present and hashed, but history freshness or Case Memory taxonomy coverage is
not good enough for GA/champion promotion review.

When that happens, read:

```text
promotionBlockers
promotionRecoveryQueueCount
promotionRecoveryQueue
```

`promotionRecoveryQueue` is the operator-facing repair plan consumed by the
dashboard. The same rows are also exposed in compact form through
`coreRuntimeEvidenceSummary` on `/api/production-evidence-validation/status`.
It merges:

- history freshness rows for `M1`, `M5`, `M15`, and `H1`, including the
  `sync-klines` refresh command, `production-status` verify command, lag, and
  acceptance criteria;
- Case Memory missing-category rows, including the taxonomy category, source
  artifacts, collection endpoint, target sample count, and acceptance criteria;
- a missing candidate-report row when the Case Memory candidate report cannot
  be read.

Every row is evidence-only. Allowed lanes remain `READ_ONLY_RESEARCH`,
`SHADOW`, and `TESTER_ONLY`; forbidden side effects include order sending,
position closing, live preset mutation, MT5 request/receipt writes, and wallet
authorization.

## Safety Invariant

The manifest safety block must keep every execution flag false:

- `orderSendAllowed`
- `mt5OrderSendAllowed`
- `brokerExecutionAllowed`
- `writesMt5OrderRequest`
- `livePresetMutationAllowed`
- `telegramCommandExecutionAllowed`
- `walletIntegrationAllowed`

Use this guard as evidence quality input. It is not proof that live trading should start.
