# Runtime Evidence Integrity

`tools/run_runtime_evidence_integrity.py` builds a read-only integrity manifest for the core QuantGod runtime evidence chain.

It exists for the P3 hardening lane: operators should be able to prove that live-loop, production policy, GA Factory, execution feedback, Case Memory, and production validation artifacts all have stable schemas, runtime-relative paths, byte sizes, and `sha256` hashes before any promotion review trusts them.

## Command

Run from `QuantGodBackend`:

```bash
python3 tools/run_runtime_evidence_integrity.py --runtime-dir ./runtime verify
python3 tools/run_runtime_evidence_integrity.py --runtime-dir ./runtime build
```

`verify` prints the manifest and exits non-zero when a required artifact is missing, a JSON/JSONL schema drifts, a CSV header is absent, an artifact manifest lacks per-file hashes, or a core artifact contains an old `/Quard/QuantGod/` legacy absolute path.

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

