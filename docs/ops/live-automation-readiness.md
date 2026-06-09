# Live Automation Readiness

`/api/live-automation/*` turns the sim-to-live question into a local review dossier. It combines the USDJPY MT5 promotion gates, the USD deployment gate, execution feedback, and the HFM Crypto CFD shadow lane.

This lane does not send, close, cancel, or modify orders. It also does not store broker credentials, wallet authorization material, API keys, or MT5 presets.

## Outputs

- `tools/run_live_automation_readiness.py build --write` writes `runtime/agent/QuantGod_LiveAutomationReadiness.json`.
- `tools/run_live_automation_readiness.py review-packet --write` writes `runtime/agent/QuantGod_LiveExecutionReviewPacket.json`.
- `tools/run_live_automation_readiness.py approval-draft --write` writes `runtime/agent/QuantGod_LiveOperatorApprovalDraft.json`.
- `tools/run_live_automation_readiness.py approval-evidence --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_LiveOperatorApprovalEvidenceReview.json`.
- `tools/run_live_automation_readiness.py dry-run-plan --write` writes `runtime/agent/QuantGod_DryRunLiveExecutionPlan.json`.
- `tools/run_live_automation_readiness.py execution-lane-spec --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_LiveExecutionLaneSpec.json`.
- `tools/run_live_automation_readiness.py dry-run-replay --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_LiveDryRunIntentReplay.json`.
- `tools/run_live_automation_readiness.py runtime-preflight --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_LiveRuntimePreflightProbe.json`.
- `tools/run_live_automation_readiness.py order-request-contract --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_MT5OrderRequestContract.json`.
- `tools/run_live_automation_readiness.py pipeline --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_SimToLiveAutomationPipeline.json`.
- `tools/run_live_automation_readiness.py adapter-review --write --operator-approval-json <path>` writes `runtime/agent/QuantGod_ExecutionAdapterReview.json`.
- `tools/run_live_automation_readiness.py adapter-sandbox --write --refresh-sources` writes `runtime/agent/QuantGod_AdapterSandboxReviewBundle.json`.
- `tools/run_live_automation_readiness.py adapter-contract-validator --write --refresh-sources` writes `runtime/agent/QuantGod_AdapterContractValidator.json`.
- `tools/run_live_automation_readiness.py adapter-harness --write --refresh-sources` writes `runtime/agent/QuantGod_ExecutionAdapterHarness.json`.
- `tools/run_live_automation_readiness.py live-pilot-activation-review --write --refresh-sources` writes `runtime/agent/QuantGod_LivePilotActivationReview.json`.
- `tools/run_live_automation_readiness.py receipt-reconciliation-review --write --refresh-sources` writes `runtime/agent/QuantGod_ReceiptReconciliationReview.json`.
- `tools/run_live_automation_readiness.py live-execution-cutover-review --write --refresh-sources` writes `runtime/agent/QuantGod_LiveExecutionCutoverReview.json`.
- `tools/run_live_automation_readiness.py live-execution-implementation-spec --write` writes `runtime/agent/QuantGod_LiveExecutionImplementationSpec.json`.
- `tools/run_live_automation_readiness.py live-execution-adapter-write-review --write` writes `runtime/agent/QuantGod_LiveExecutionAdapterWriteReview.json`.
- `tools/run_live_automation_readiness.py ea-request-consumption-review --write` writes `runtime/agent/QuantGod_EARequestConsumptionReview.json`.
- `tools/run_live_automation_readiness.py broker-order-send-review --write` writes `runtime/agent/QuantGod_BrokerOrderSendReview.json`.
- `tools/run_live_automation_readiness.py ea-request-reader-review --write --refresh-sources --ea-status-json <QuantGod_EARequestReaderReviewStatus.json>` writes `runtime/agent/QuantGod_EARequestReaderReview.json`; without the explicit path it only auto-discovers local synced status/dashboard snapshots.
- `tools/run_live_automation_readiness.py evidence-intake --write --refresh-sources` writes `runtime/agent/QuantGod_LiveEvidenceIntake.json`.
- `tools/run_live_automation_readiness.py promotion-candidates --write --refresh-sources` writes `runtime/agent/QuantGod_LivePromotionCandidates.json`.
- `tools/run_live_automation_readiness.py promotion-controller --write --refresh-sources` writes `runtime/agent/QuantGod_LivePromotionController.json`.
- `tools/run_hfm_crypto_cfd.py post-upgrade-controller --write` writes `runtime/hfm_crypto/QuantGod_HFMCryptoPostUpgradeController.json`.
- `tools/run_hfm_crypto_cfd.py evidence-bootstrap --write` writes `runtime/hfm_crypto/QuantGod_HFMCryptoEvidenceBootstrap.json` and operator draft files.
- `GET /api/live-automation/status` reads the saved dossier, or builds an in-memory fallback.
- `GET /api/live-automation/readiness` builds a transient readiness view.
- `POST /api/live-automation/build` writes the dossier for operator review.
- `GET /api/live-automation/review-packet` reads the execution review packet.
- `POST /api/live-automation/review-packet/build` writes the execution review packet.
- `GET /api/live-automation/approval-draft` reads the final-approval draft.
- `POST /api/live-automation/approval-draft/build` writes the final-approval draft.
- `GET /api/live-automation/approval-evidence` reads the operator approval evidence review.
- `POST /api/live-automation/approval-evidence/build` validates a local operator approval JSON against the review packet hash and required acknowledgements.
- `GET /api/live-automation/dry-run-plan` reads the dry-run live execution plan.
- `POST /api/live-automation/dry-run-plan/build` writes the dry-run live execution plan.
- `GET /api/live-automation/execution-lane-spec` reads the future execution lane handoff spec.
- `POST /api/live-automation/execution-lane-spec/build` writes the future execution lane handoff spec after approval evidence and dry-run intents are reviewed.
- `GET /api/live-automation/dry-run-replay` reads the dry-run intent replay review.
- `POST /api/live-automation/dry-run-replay/build` replays approved dry-run intents against the execution lane spec without creating MT5 order files or broker calls.
- `GET /api/live-automation/runtime-preflight` reads the runtime preflight probe.
- `POST /api/live-automation/runtime-preflight/build` checks the approved dry-run replay against a fresh MT5 dashboard snapshot, live-pilot mode, account/server, broker symbol, spread evidence, trade permission, and kill switch field without creating MT5 order files or broker calls.
- `GET /api/live-automation/order-request-contract` reads the future MT5 request and receipt contract.
- `POST /api/live-automation/order-request-contract/build` builds the MT5 request contract from runtime preflight evidence without creating MT5 request files or broker calls.
- `GET /api/live-automation/pipeline` reads the sim-to-live automation pipeline.
- `POST /api/live-automation/pipeline/build` runs the full review pipeline from simulation evidence through MT5 request contract review without creating MT5 request files or broker calls.
- `GET /api/live-automation/adapter-review` reads the execution adapter review shell.
- `POST /api/live-automation/adapter-review/build` validates the future adapter request/receipt contract without creating MT5 request files or broker calls.
- `GET /api/live-automation/adapter-sandbox` reads the adapter sandbox review bundle.
- `POST /api/live-automation/adapter-sandbox/build` builds local sample request/receipt payloads for adapter code review without creating MT5 request files or broker calls.
- `GET /api/live-automation/adapter-contract-validator` reads the adapter contract validator.
- `POST /api/live-automation/adapter-contract-validator/build` validates future MT5 request JSON and emits review-only receipts without creating MT5 request files or broker calls.
- `GET /api/live-automation/orchestrator` reads the full sim-to-live state machine.
- `POST /api/live-automation/orchestrator/build` runs the full review-only orchestrator across evidence intake, candidate selection, approval evidence, dry-run replay, runtime preflight, request contract, adapter review, sandbox, adapter contract validation, and the post-adapter live execution review stages.
- `GET /api/live-automation/adapter-harness` reads the disabled execution adapter harness.
- `POST /api/live-automation/adapter-harness/build` builds request/receipt path plans, idempotency checks, atomic-write checks, and review-only receipts without writing MT5 request files or calling a broker.
- `GET /api/live-automation/live-pilot-activation-review` reads the final live-pilot activation review packet.
- `POST /api/live-automation/live-pilot-activation-review/build` summarizes orchestrator, runtime preflight, approval evidence, adapter contract validation, disabled harness, and a deployment runbook. It does not write MT5 request files, mutate presets, store credentials, or call a broker.
- `GET /api/live-automation/receipt-reconciliation-review` reads the receipt reconciliation review artifact.
- `POST /api/live-automation/receipt-reconciliation-review/build` matches review-only receipts to planned requests and describes auto-disable rules. It does not write receipt files, mutate auto-disable state, or call a broker.
- `GET /api/live-automation/ea-request-reader-review` reads the EA request reader review artifact.
- `POST /api/live-automation/ea-request-reader-review/build` checks EA source markers and the activation/order-contract/receipt-reconciliation chain before any request-reader implementation review. It does not read MT5 request files, write receipts, mutate presets, or call a broker.
- `GET /api/live-automation/live-execution-cutover-review` reads the final live execution cutover review artifact.
- `POST /api/live-automation/live-execution-cutover-review/build` summarizes orchestrator, live pilot activation, receipt reconciliation, EA request reader, runtime preflight, operator approval, order contract, and disabled harness evidence before a separate live execution cutover implementation review. It does not write request files, write receipt files, mutate presets, read/consume request files, or call a broker.
- `GET /api/live-automation/live-execution-implementation-spec` reads the live execution implementation spec.
- `POST /api/live-automation/live-execution-implementation-spec/build` turns a ready cutover review into a separate-PR implementation contract for adapter request writing, EA request consumption, broker order send, receipt reconciliation, and rollback/auto-disable. It still writes only the review artifact and does not write request files, consume request files, write receipt files, mutate presets, or call a broker.
- `GET /api/live-automation/live-execution-adapter-write-review` reads the adapter writer review artifact.
- `POST /api/live-automation/live-execution-adapter-write-review/build` validates the first implementation contract: stable request JSON serialization, idempotency hash, temp/final file naming, and atomic write planning. It embeds review payloads in the artifact but still does not write MT5 request files, write receipt files, consume request files, mutate presets, or call a broker.
- `GET /api/live-automation/ea-request-consumption-review` reads the EA request consumption review artifact.
- `POST /api/live-automation/ea-request-consumption-review/build` validates the second implementation contract: adapter writer paths, EA reader contract directories, runtime disabled status, idempotency, and reject-only receipt planning. It does not read MT5 request files, consume request files, write receipts, mutate presets, or call a broker.
- `GET /api/live-automation/broker-order-send-review` reads the broker order send wrapper review artifact.
- `POST /api/live-automation/broker-order-send-review/build` validates the third implementation contract: the future broker wrapper must enter only from reviewed EA consumption, bind account/server, symbol mapping, lot/risk controls, spread/slippage fuses, request hashes, and receipt obligations. It does not call a broker, write request files, write receipt files, mutate presets, or enable order sending.
- `GET /api/live-automation/evidence-intake` reads the HFM/live evidence intake summary.
- `POST /api/live-automation/evidence-intake/build` refreshes the evidence intake summary and local review-only artifacts without creating MT5 request files or broker calls.
- HFM-side helper: `GET /api/hfm-crypto/evidence-bootstrap` and `POST /api/hfm-crypto/evidence-bootstrap/build` expose the draft/filled-input bootstrap for the HFM evidence lane.
- `GET /api/live-automation/promotion-candidates` reads the live promotion candidate selector.
- `POST /api/live-automation/promotion-candidates/build` ranks simulation-qualified lanes for operator review without creating MT5 request files or broker calls.
- `GET /api/live-automation/promotion-controller` reads the sim-to-live promotion controller.
- `POST /api/live-automation/promotion-controller/build` automatically writes review packet, approval draft, dry-run plan, and pipeline artifacts when a lane qualifies, without creating MT5 request files or broker calls.

## Promotion Meaning

`READY_FOR_EXECUTION_REVIEW` means one or more lanes may be ready to review for a separately designed execution lane. It does not mean the system may trade live now.

`READY_FOR_EXECUTION_ADAPTER_IMPLEMENTATION_REVIEW` from `QuantGod_SimToLiveOrchestrator.json` means the adapter-side review-only stage chain has passed and the next adapter work is a separate implementation/code review. The same artifact now also exposes `liveExecutionStages` for the remaining post-adapter chain: disabled adapter harness, live pilot activation review, receipt reconciliation review, and EA request reader runtime review. Only when those pass does it show `READY_FOR_LIVE_EXECUTION_IMPLEMENTATION_REVIEW`; even then it still keeps `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `writesMt5OrderRequest`, `requestWritesAllowed`, `requestFilesWritten`, and `brokerCallsMade` false.

`READY_FOR_DISABLED_ADAPTER_IMPLEMENTATION_HARNESS_REVIEW` from `QuantGod_ExecutionAdapterHarness.json` means the system can review a disabled adapter implementation plan: request path, receipt path, idempotency key, atomic write plan, and review-only receipt reconciliation. It still keeps `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `writesMt5OrderRequest`, `requestWritesAllowed`, `requestFilesWritten`, `adapterExecutionAllowed`, and `brokerCallsMade` false.

`READY_FOR_LIVE_PILOT_ACTIVATION_REVIEW` from `QuantGod_LivePilotActivationReview.json` means the review-only chain has enough evidence to open a separate live adapter / EA request reader / rollback implementation review. It still keeps `livePilotActivationAllowed`, `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `writesMt5OrderRequest`, `requestWritesAllowed`, `requestFilesWritten`, `adapterExecutionAllowed`, and `brokerCallsMade` false.

`READY_FOR_RECEIPT_RECONCILIATION_REVIEW` from `QuantGod_ReceiptReconciliationReview.json` means the planned request/receipt pairs and review-only receipt rejection behavior can be reviewed before any real adapter work. It still keeps `receiptWritesAllowed`, `receiptFilesWritten`, `autoDisableMutationAllowed`, `livePilotActivationAllowed`, `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `requestWritesAllowed`, `requestFilesWritten`, and `brokerCallsMade` false.

`READY_FOR_EA_REQUEST_READER_IMPLEMENTATION_REVIEW` from `QuantGod_EARequestReaderReview.json` means the EA source has the explicit request-reader safety markers, the running EA exported `QuantGod_EARequestReaderReviewStatus.json` or dashboard `eaRequestReaderReview` proving the reader is still effectively disabled, and the activation/order-contract/receipt-reconciliation chain is ready for a separate EA implementation PR. It still keeps `eaRequestReaderAllowed`, `eaRequestReaderEnabled`, `eaRequestFilesRead`, `eaRequestFilesConsumed`, `eaOrderSendAllowed`, `receiptWritesAllowed`, `livePilotActivationAllowed`, `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `requestWritesAllowed`, `requestFilesWritten`, and `brokerCallsMade` false.

`READY_FOR_SEPARATE_LIVE_EXECUTION_CUTOVER_IMPLEMENTATION_REVIEW` from `QuantGod_LiveExecutionCutoverReview.json` means every review-only prerequisite has passed and the next step is a separate implementation PR for the real adapter, EA request reader consumption path, broker order send path, receipt writer/reconciliation path, and rollback/auto-disable path. It still keeps `liveExecutionCutoverAllowed`, `livePilotActivationAllowed`, `eaRequestReaderAllowed`, `requestWritesAllowed`, `receiptWritesAllowed`, `requestFilesWritten`, `receiptFilesWritten`, `brokerCallsMade`, `orderSendAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false.

`READY_FOR_LIVE_EXECUTION_IMPLEMENTATION_SPEC_REVIEW` from `QuantGod_LiveExecutionImplementationSpec.json` means the implementation work has been split into explicit review contracts: `live_execution_adapter_write_path`, `ea_request_reader_consumption_path`, `broker_order_send_path`, `receipt_writer_and_reconciliation_path`, and `rollback_and_auto_disable_path`. This spec only makes the future PR boundaries reviewable; it still keeps `liveExecutionCutoverAllowed`, `requestWritesAllowed`, `receiptWritesAllowed`, `eaRequestReaderAllowed`, `eaRequestFilesRead`, `brokerCallsMade`, `orderSendAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false.

`READY_FOR_LIVE_EXECUTION_ADAPTER_WRITE_REVIEW` from `QuantGod_LiveExecutionAdapterWriteReview.json` means the future adapter writer has a deterministic payload serializer, idempotency hash, final path, temp-file pattern, and atomic write contract ready for code review. It is not a request writer yet: `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `adapterExecutionAllowed`, `orderSendAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` stay false.

`READY_FOR_EA_REQUEST_CONSUMPTION_REVIEW` from `QuantGod_EARequestConsumptionReview.json` means the future EA request consumption path can be reviewed against the adapter writer's request plans and the EA reader's contract/runtime disabled status. It is not a reader runtime yet: `eaRequestReaderAllowed`, `eaRequestReaderEnabled`, `eaRequestFilesRead`, `eaRequestFilesConsumed`, `receiptWritesAllowed`, `receiptFilesWritten`, `brokerCallsMade`, `orderSendAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` stay false.

`READY_FOR_BROKER_ORDER_SEND_REVIEW` from `QuantGod_BrokerOrderSendReview.json` means the future broker wrapper contract can be reviewed after EA consumption, runtime preflight, request contract, and adapter writer review are all ready. It is not a broker runtime yet: `brokerCallsMade`, `brokerExecutionAllowed`, `orderSendAllowed`, `mt5OrderSendAllowed`, `eaOrderSendAllowed`, `requestWritesAllowed`, `receiptWritesAllowed`, and `writesMt5OrderRequest` stay false.

`canPromoteToLiveNow`, `autoPromotionToLiveAllowed`, `livePilotActivationAllowed`, `liveExecutionCutoverAllowed`, `receiptWritesAllowed`, `autoDisableMutationAllowed`, `eaRequestReaderAllowed`, and `eaOrderSendAllowed` must remain `false` until a future reviewed execution lane exists.

## Execution Review Packet

The review packet is the bridge between good simulation evidence and a future live execution lane. It contains per-lane broker scope, symbol scope, risk limits, blockers, and a `dryRunOrderIntentSpec`.

The `dryRunOrderIntentSpec` is a contract, not an order. It lists the fields a future execution lane must provide after separate review, including symbol, side, volume, stop-loss, take-profit, spread/slippage limits, kill switch status, daily loss status, and final operator approval id. The packet explicitly keeps `writesMt5OrderRequest` false.

## Approval Draft And Dry-Run Plan

The approval evidence review is still non-executing. `OPERATOR_APPROVAL_EVIDENCE_ACCEPTED_EXECUTION_STILL_DISABLED` only means the local approval JSON matched the current review packet hash, approved candidate lanes, risk-limit acknowledgement, kill-switch acknowledgement, external credential acknowledgement, dry-run-first acknowledgement, and any lane-specific acknowledgements such as HFM contract specs. It keeps `approvalCanUnlockLiveExecution`, `canPromoteToLiveNow`, `orderSendAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false.

`QuantGod_LiveExecutionLaneSpec.json` is the next handoff artifact after approval evidence. `READY_FOR_EXECUTION_LANE_IMPLEMENTATION_REVIEW` means the system has an approved dry-run intent contract that a future execution adapter can be reviewed against. It still keeps `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false, and it explicitly requires a separate execution-lane code review before any MT5 order request file or broker call can exist.

`QuantGod_LiveDryRunIntentReplay.json` validates the approved dry-run intents against the execution lane spec. `DRY_RUN_INTENT_REPLAY_ACCEPTED_EXECUTION_STILL_DISABLED` means the intent fields, lane mapping, review hash, and no-order-output flags are internally consistent. It still keeps `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, `mt5PendingOrderIntentsWritten`, and `writesMt5OrderRequest` false.

`QuantGod_LiveRuntimePreflightProbe.json` is the next runtime-only gate. `READY_FOR_RUNTIME_PREFLIGHT_REVIEW` means the approved dry-run replay also matches a fresh `QuantGod_Dashboard.json` snapshot with `runtime.livePilotMode=true`, `runtime.readOnlyMode=false`, `runtime.executionEnabled=true`, `runtime.tradeAllowed=true`, account/server evidence, a clear inactive kill switch field, symbol mapping, and spread/risk fields. A shadow/read-only dashboard is now blocked even if the symbol and spread are present. The probe still keeps `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, `mt5PendingOrderIntentsWritten`, and `writesMt5OrderRequest` false.

`QuantGod_MT5OrderRequestContract.json` fixes the future adapter/EA handoff before any implementation can write request files. `READY_FOR_ORDER_REQUEST_CONTRACT_REVIEW` means the runtime preflight is strong enough to review the MT5 request schema, receipt schema, idempotency key, atomic-write rule, required fuses, and rollback checklist. It still keeps `requestWritesAllowed`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, `mt5PendingOrderIntentsWritten`, and `writesMt5OrderRequest` false.

`QuantGod_SimToLiveAutomationPipeline.json` is the one-command state machine for the user's "good simulation can enter live review" workflow. It runs readiness, review packet, approval evidence, dry-run plan, execution lane spec, dry-run replay, runtime preflight, and MT5 request contract, then reports the current `autoStage`. `READY_FOR_SEPARATE_EXECUTION_ADAPTER_REVIEW` means the review chain has reached the edge where a separate execution adapter code review can start. It still keeps `requestWritesAllowed`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, `mt5PendingOrderIntentsWritten`, `autoPromotionToLiveAllowed`, and `writesMt5OrderRequest` false.

The pipeline also writes `evidenceChecklist`, a compact list of the missing review inputs: candidate lane, HFM crypto symbol evidence, simulation profile, contract spec, USDJPY live candidate, operator approval evidence, dry-run replay, runtime preflight, and MT5 request contract review.

`QuantGod_ExecutionAdapterReview.json` is the review-only shell for the future adapter implementation. `READY_FOR_EXECUTION_ADAPTER_CODE_REVIEW` means the pipeline and MT5 request contract are strong enough to review adapter code that validates requests and emits receipts. It still keeps `adapterExecutionAllowed`, `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, `mt5PendingOrderIntentsWritten`, and `writesMt5OrderRequest` false.

`QuantGod_AdapterSandboxReviewBundle.json` is the next review-only artifact for the future MT5 adapter. It materializes sample MT5 request payloads, sample receipt payloads, idempotency/hash fields, and validation rows from the approved contract so adapter serialization can be reviewed before any execution lane exists. `READY_FOR_ADAPTER_SANDBOX_REVIEW` means the bundle is suitable for code review only. It still keeps `adapterExecutionAllowed`, `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false.

`QuantGod_AdapterContractValidator.json` is the review-only validator for future adapter requests. It checks request JSON or adapter sandbox sample requests against the approved MT5 request contract: required fields, types, enum values, review packet hash, runtime preflight hash, lane mapping, kill switch, runtime freshness, spread probe, symbol mapping, and dry-run replay fuses. It can emit review-only receipts inside the artifact, but it still keeps `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `adapterExecutionAllowed`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false.

`QuantGod_ExecutionAdapterHarness.json` is the disabled implementation harness after orchestrator and adapter contract validation pass. It maps each reviewed request to a future request filename, future receipt filename, atomic temp-file pattern, idempotency hash, and review-only rejected receipt. This artifact is intentionally a plan and validator, not an adapter runtime: `wouldWriteRequestFile`, `wouldWriteReceiptFile`, `requestFilesWritten`, `brokerCallsMade`, `adapterExecutionAllowed`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` remain false.

`QuantGod_LiveEvidenceIntake.json` is the operator-facing intake map for HFM crypto and future sim-to-live work. It lists the expected local files, whether they exist, which HFM/pipeline checklist items are still missing, the current MT5 dashboard summary, and the exact read-only commands to rerun after evidence appears. `HFM_REVIEW_INPUTS_PRESENT` only means the HFM symbol/spec/simulation inputs are present enough to continue review. It still keeps `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `adapterExecutionAllowed`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` false.

`QuantGod_LivePromotionCandidates.json` is the automatic selector for the user's "good simulation can enter live review" workflow. It ranks USDJPY and HFM crypto lanes by simulation qualification, review-candidate status, and evidence score. `READY_FOR_OPERATOR_REVIEW_PACKET` means the system may automatically generate review packet, approval draft, dry-run plan, and pipeline artifacts for a human operator. It does not mean live execution is enabled: `canPromoteToLiveNow`, `autoPromotionToLiveAllowed`, `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `adapterExecutionAllowed`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` remain false.

`QuantGod_LivePromotionController.json` is the automation step after candidate selection. When no lane qualifies it returns `WAITING_PROMOTION_CANDIDATE`. When a lane qualifies it returns `OPERATOR_REVIEW_PACKET_AUTOMATED` and writes only local review artifacts: review packet, approval draft, dry-run plan, and pipeline. It still keeps the broker/data-plane boundary closed: `reviewArtifactsWrittenByThisRun` may be true, but `requestWritesAllowed`, `requestFilesWritten`, `brokerCallsMade`, `adapterExecutionAllowed`, `executionReady`, `orderSendAllowed`, `brokerExecutionAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` stay false.

`QuantGod_EARequestReaderReview.json` is the final review-only bridge before touching EA request-reader code. It inspects the EA source for explicit safety markers: default-off reader, request schema validation, requestId idempotency, kill switch, receipt writer, and a separate order-send review marker. It also verifies the runtime status export from `QuantGod_EARequestReaderReviewStatus.json` or `QuantGod_Dashboard.json.eaRequestReaderReview`: schema must be `quantgod.mql5.ea_request_reader_review_status.v1`, `effectiveEnabled` must be false, all runtime marker checks must pass, and `requestFilesRead`, `requestFilesConsumed`, `receiptFilesWritten`, `orderSendAllowed`, `mt5OrderSendAllowed`, `brokerCallsMade`, `livePresetMutationAllowed`, and `credentialStorageAllowed` must stay false. Even when all markers and upstream artifacts pass, this artifact still does not read request files, write receipt files, mutate MT5 presets, or call a broker.

`QuantGod_LiveExecutionCutoverReview.json` is the final review-only handoff after orchestrator, live pilot activation review, receipt reconciliation review, EA request reader review, runtime preflight, operator approval evidence, MT5 request contract, and disabled adapter harness are all present. It records the exact future request/receipt directories, review packet hash, runtime preflight hash, operator approval id, planned write count, review-only receipt count, and required future implementation PRs. It intentionally stops at handoff: `liveExecutionCutoverAllowed`, `requestWritesAllowed`, `receiptWritesAllowed`, `eaRequestReaderAllowed`, `eaRequestFilesRead`, `eaRequestFilesConsumed`, `brokerCallsMade`, and all order-send flags remain false.

`QuantGod_LiveExecutionImplementationSpec.json` is the first artifact after cutover review. It does not implement live execution. It fixes the implementation sequence, target files, required tests, and forbidden side effects for the five future PRs that would make live automation real: Python adapter request writer, MT5 EA request reader consumption, broker order-send wrapper, receipt writer/reconciliation, and rollback/auto-disable. It is the checklist that prevents "just flip execution on" changes.

`QuantGod_LiveExecutionAdapterWriteReview.json` is the first implementation-contract artifact. It reads the implementation spec, disabled adapter harness, adapter contract validator, and sandbox request samples, then serializes each request into stable canonical JSON with a payload hash and idempotency hash. It records the future final request path and temp-file pattern, but it sets `allowedToWriteLiveRequest=false`, `wouldWriteToMt5RequestDirectory=false`, and `requestFilesWritten=false` for every plan row.

`QuantGod_EARequestConsumptionReview.json` is the second implementation-contract artifact. It reads the implementation spec, adapter writer review, and EA request reader review, then builds reject-only consumption plans that line up requestDirectory/receiptDirectory, requestId/idempotencyKey, schema validation, kill switch, and receipt requirements. It keeps `wouldReadRequestFile=false`, `wouldConsumeRequestFile=false`, `wouldWriteReceiptFile=false`, `receiptFilesWritten=false`, and all order-send/broker flags false.

`QuantGod_BrokerOrderSendReview.json` is the third implementation-contract artifact. It reads the implementation spec, EA request consumption review, runtime preflight, MT5 request contract, and adapter writer review, then builds blocked broker wrapper plans. Each plan binds the request to account/server evidence, broker symbol, side, lot size, spread/slippage limits, daily-loss fuses, request hashes, and future receipt obligations. It keeps `wouldCallBroker=false`, `brokerCallsMade=false`, `orderSendAllowed=false`, `mt5OrderSendAllowed=false`, `brokerExecutionAllowed=false`, and all request/receipt write flags false.

`QuantGod_LiveOperatorApprovalDraft.json` records the exact acknowledgement fields a human operator must supply later: packet hash, approved lanes, max daily loss acknowledgement, kill switch acknowledgement, external credential acknowledgement, dry-run-first acknowledgement, and final human approval text. The draft itself never counts as approval.

`QuantGod_DryRunLiveExecutionPlan.json` converts review-candidate lane contracts into blocked dry-run intents. These intents are for inspection only. They keep `mt5PendingOrderIntentsWritten`, `writesMt5OrderRequest`, `orderSendAllowed`, and `brokerExecutionAllowed` false.

## HFM Crypto CFD

The HFM crypto lane requires local HFM/MT5 crypto symbol evidence and a Moss/backtest profile that passes basic ROI, Sharpe, drawdown, trade-count, and liquidation checks. Even when those pass, HFM crypto remains blocked by `HFM_CRYPTO_EXECUTION_SPEC_REVIEW_REQUIRED` until symbol mapping, contract specs, spread/slippage rules, kill switch behavior, and MT5 order request format are reviewed.

The candidate catalog tracks HFM's official crypto USD CFD surface beyond BTC/ETH/LTC/XRP. The evidence kit and symbol normalizer now cover AAVE, ADA, ALGO, APT, ATOM, AVAX, BCH, BNB, BTC, CRV, DOGE, DOT, ETC, ETH, FET, FIL, FLOW, GALA, GRT, HBAR, ICP, IMX, IOTA, LINK, LTC, NEAR, SAND, SHIB, SOL, THETA, TRX, UNI, XLM, XRP, and XTZ USD forms, including common `#SYMBOL`, `#SYMBOLr`, and KATANA `#BTCUSDx/#ETHUSDx/#XRPUSDx` variants. This catalog is only a search/template seed; the execution review still requires broker-exported specs for the actual HFM account.

`tools/run_hfm_crypto_cfd.py execution-spec --write --contract-spec-json <path>` writes `runtime/hfm_crypto/QuantGod_HFMCryptoExecutionSpecReview.json`. The input can be JSON or CSV exported from a broker/MT5 symbol-spec source and should include at least `brokerSymbol`, `canonicalSymbol`, `contractSize`, `tickSize`, `tickValue`, `minLot`, `lotStep`, and `maxLot`.

`tools/run_hfm_crypto_cfd.py contract-spec-export --write --symbol-registry-json <path>` writes `runtime/hfm_crypto/QuantGod_HFMCryptoContractSpecExport.json`. It converts a read-only MT5 symbol registry export into the contract-spec rows expected by the review step. The command is still local-only and does not call `symbol_select`, write MT5 files, or send orders. On macOS, where the Python MetaTrader5 bridge is usually unavailable, the MT5 EA can instead write `QuantGod_HFMCryptoSymbolSpecs.json` from `SymbolInfo*`; running `contract-spec-export --write` with no manual path auto-discovers that EA file from the runtime/MT5 Files candidates.

`QuantGod_HFMCryptoCfdState.json` treats symbol evidence as multi-source. Local MT5 Bases history/tick directories are accepted, but an EA/registry-derived contract-spec export or a passing execution-spec review also counts as HFM crypto symbol evidence. This prevents the sim-to-live chain from staying blocked on missing history folders after the operator has already supplied broker-exported specs. The state records these inputs under `symbolEvidence.sources`, while all execution flags remain false.

When both files exist, manually filled operator inputs take precedence over a stale generated export. `hfm_crypto_contract_specs.filled.json` is selected before `QuantGod_HFMCryptoContractSpecExport.json`, and `hfm_crypto_simulation_profile.filled.json` is auto-selected when no explicit Moss/profile path is passed. `QuantGod_LiveEvidenceIntake.json` records the selected path and source in `inputs.effectiveContractSpecSource` and `inputs.effectiveSimulationProfileSource`.

`QuantGod_HFMCryptoEvidenceBootstrap.json` is the operator bootstrap for the current front-of-chain blockers. It writes `.draft.json` files only: `hfm_crypto_contract_specs.draft.json`, `hfm_crypto_simulation_profile.draft.json`, and `operator_approval.draft.json`. These drafts do not enter evidence intake automatically. The operator can either fill real HFM/MT5 specs and Moss/simulation metrics into `hfm_crypto_contract_specs.filled.json` / `hfm_crypto_simulation_profile.filled.json`, or provide EA/MT5 contract-spec export plus a passing simulation-profile review artifact. `filled-input-validator` accepts those reviewed sources but still rejects empty templates as broker evidence.

`QuantGod_HFMCryptoSimulationProfileReview.json` now records `sourceSelection` and `autoProfileCandidates`. If no explicit profile path is supplied, `simulation-profile --write` auto-discovers `hfm_crypto_simulation_profile.filled.json`, `QuantGod_HFMCryptoMossBacktestProfile.json`, and common local `moss_backtest.json` names under runtime before declaring the simulation profile missing.

`QuantGod_HFMCryptoCfdState.json` now normalizes a passing auto-discovered simulation-profile review back into `mossBacktestProfile`. That keeps the shadow lane, promotion candidates, review packet, and operator draft aligned on the same `agentId`, ROI, Sharpe, drawdown, trade-count, and liquidation evidence even when no explicit profile path was passed.

Before refreshing promotion candidates from manual files, run:

```bash
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime evidence-bootstrap --write
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime filled-input-validator --write
```

This writes `runtime/hfm_crypto/QuantGod_HFMCryptoFilledInputValidator.json`. `FILLED_HFM_INPUTS_READY_FOR_REVIEW_CHAIN` means the manual HFM contract spec contains valid crypto USD CFD rows and the simulation profile passes ROI/Sharpe/drawdown/trade/liquidation thresholds. It still keeps `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `writesMt5OrderRequest`, `requestWritesAllowed`, and `brokerCallsMade` false.

`READY_FOR_EXECUTION_CONTRACT_REVIEW` means contract-size and lot/tick fields are present enough to review. It still does not unlock live trading: `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, and `writesMt5OrderRequest` remain false. After this point the remaining blocker becomes the separately reviewed MT5 execution lane, kill switch, daily loss limits, spread/slippage policy, and final operator approval.

`tools/run_hfm_crypto_cfd.py evidence-kit --write` writes the local evidence collection kit and templates:

- `runtime/hfm_crypto/QuantGod_HFMCryptoEvidenceKit.json`
- `runtime/hfm_crypto/QuantGod_HFMCryptoContractSpecTemplate.json`
- `runtime/hfm_crypto/QuantGod_HFMCryptoContractSpecTemplate.csv`
- `runtime/hfm_crypto/QuantGod_HFMCryptoSimulationProfileTemplate.json`

The HFM evidence workflow can then produce:

- `runtime/hfm_crypto/QuantGod_HFMCryptoMt5ExporterReview.json`
- `runtime/hfm_crypto/QuantGod_HFMCryptoContractSpecExport.json`
- `runtime/hfm_crypto/QuantGod_HFMCryptoSymbolSpecs.json`

The kit includes read-only collection commands. When the MT5 Python bridge is available, first export the registry:

```bash
python3 tools/mt5_symbol_registry.py --endpoint registry --group "*Crypto*" --limit 500 > runtime/hfm_crypto/mt5_symbol_registry_crypto.json
```

Then convert it into HFM contract-spec input and import that into the contract-spec review:

```bash
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime contract-spec-export --write --symbol-registry-json runtime/hfm_crypto/mt5_symbol_registry_crypto.json
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime execution-spec --write --contract-spec-json runtime/hfm_crypto/QuantGod_HFMCryptoContractSpecExport.json
```

When using the EA exporter, run the EA on the HFM MT5 terminal and copy/sync `QuantGod_HFMCryptoSymbolSpecs.json` into `runtime/hfm_crypto/` or the MT5 Files snapshot directory. If only `QuantGod_Dashboard.json` is synced, the backend can also auto-discover the embedded `hfmCryptoSymbolSpecs` object. Then let the backend auto-discover it:

```bash
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime mt5-exporter-review --write
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime contract-spec-export --write
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime execution-spec --write --contract-spec-json runtime/hfm_crypto/QuantGod_HFMCryptoContractSpecExport.json
```

`QuantGod_HFMCryptoMt5ExporterReview.json` compares the repository EA with the installed MT5 EA source and the latest dashboard snapshot. `WAITING_MT5_EA_EXPORTER_UPGRADE` means the running terminal still has an older EA that cannot emit `hfmCryptoSymbolSpecs`; the review only reports this gap and never copies files into MT5, compiles an EA, changes presets, or sends orders.

If the installed EA is behind the repository exporter, `tools/run_hfm_crypto_cfd.py mt5-upgrade-bundle --write` writes `runtime/hfm_crypto/QuantGod_HFMCryptoMt5ExporterUpgradeBundle.json` and stages the reviewed `QuantGod_MultiStrategy.mq5` under `runtime/hfm_crypto/mt5_ea_upgrade_bundle/`. The bundle is manual-only: it records hashes, target paths, and operator steps, but it does not copy into the MT5 installation, compile the EA, change presets, or send orders.

After the manual copy, MetaEditor compile, and EA reload, run `tools/run_hfm_crypto_cfd.py mt5-post-upgrade-verify --write`. It writes `runtime/hfm_crypto/QuantGod_HFMCryptoMt5PostUpgradeVerify.json`, compares the installed source hash with the staged bundle, checks that `QuantGod_MultiStrategy.ex5` is not older than the source, looks for `hfmCryptoSymbolSpecs`, and refreshes the local contract-spec export/review if specs exist. It still does not copy, compile, mutate presets, or send orders.

For repeated operator checks, run `tools/run_hfm_crypto_cfd.py post-upgrade-controller --write`. It writes `runtime/hfm_crypto/QuantGod_HFMCryptoPostUpgradeController.json` and coordinates exporter review, manual bundle status, post-upgrade verify, contract-spec export, execution-spec review, and HFM crypto state refresh. `HFM_CRYPTO_POST_UPGRADE_REVIEW_AUTOMATED` only means the local review artifacts were refreshed after specs appeared; `executionReady`, `orderSendAllowed`, `mt5OrderSendAllowed`, `writesMt5OrderRequest`, `requestWritesAllowed`, `brokerCallsMade`, and `hfmCryptoExecutionAllowed` remain false.

The simulation profile has its own review artifact:

```bash
python3 tools/run_hfm_crypto_cfd.py --runtime-dir runtime simulation-profile --write --simulation-profile-json runtime/hfm_crypto/hfm_crypto_simulation_profile.filled.json
```

`SIMULATION_PROFILE_QUALIFIED` means the imported profile passed the HFM crypto thresholds: positive ROI, Sharpe at least 1.0, max drawdown no more than 15%, at least 20 trades, and zero liquidations. This only makes the lane eligible for execution review; it still does not send orders or unlock MT5 writes.
