# QuantGod Backend API Contract

本文由 `docs/contracts/api-contract.json` 渲染生成，用于人工 review。
机器可读版本仍以 JSON contract 为准。

## Contract 摘要

- Endpoint 总数：`380`。
- Backend API base：`http://127.0.0.1:8080/api`。
- Backend `/api/*` route surface 以 `QuantGodBackend/tools/api_route_registry.py` 输出为准。
- 任何新增、删除或重命名 `/api/*` route，都必须同步更新 JSON contract、本文档和 Frontend service wrapper。

## 通用安全语义

Phase 1/2/3 的 API contract 必须保持本地优先和安全受控：

| 字段 | 期望值 | 含义 |
|---|---:|---|
| `localOnly` | `true` | Contract default |
| `advisoryOnly` | `true` | Contract default |
| `readOnlyDataPlane` | `true` | Contract default |
| `orderSendAllowed` | `false` | Contract default |
| `closeAllowed` | `false` | Contract default |
| `cancelAllowed` | `false` | Contract default |
| `credentialStorageAllowed` | `false` | Contract default |
| `livePresetMutationAllowed` | `false` | Contract default |
| `canOverrideKillSwitch` | `false` | Contract default |
| `canMutateGovernanceDecision` | `false` | Contract default |
| `telegramCommandExecutionAllowed` | `false` | Contract default |

`guarded-control` 不代表开放交易权限。它只表示 endpoint 是受控动作面，
仍必须受 Backend、EA、dryRun、Kill Switch 和手动授权约束。

## Endpoint Groups

### backend-core-and-control

- Phase / Domain：`backend-core`。
- Endpoint 数量：`23`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/latest` | `read-only` | Latest local dashboard state with service metadata. |
| GET | `/api/daily-review` | `read-only` | Daily review API wrapper. |
| GET | `/api/daily-autopilot` | `read-only` | Daily autopilot API wrapper. |
| GET | `/api/phase1` | `read-only` | Phase 1 workspace route/config alias. |
| GET | `/api/mt5-readonly` | `read-only` | MT5 read-only bridge snapshot alias. |
| GET | `/api/mt5-readonly/:endpoint` | `read-only` | Legacy MT5 read-only bridge endpoint wrapper. |
| GET | `/api/mt5-symbol-registry` | `read-only` | MT5 symbol registry. |
| GET | `/api/mt5-symbol-registry/:endpoint` | `read-only` | MT5 symbol registry sub-endpoint. |
| GET | `/api/mt5-backtest-loop` | `research-only` | Backend backtest loop status/result. |
| GET | `/api/mt5-backtest-loop/run` | `research-only` | Trigger research-only backend backtest loop. |
| POST | `/api/paramlab/auto-tester` | `guarded-control` | ParamLab auto-tester base route alias; action routes remain guarded. |
| POST | `/api/paramlab/auto-tester/:action` | `guarded-control` | ParamLab auto-tester actions; must not bypass Version Gate or live authorization. |
| GET | `/api/mt5-pending-worker/status` | `read-only` | Pending worker status. |
| POST | `/api/mt5-pending-worker/run` | `guarded-control` | Run pending worker under backend safety controls. |
| GET | `/api/mt5-adaptive-control/status` | `read-only` | Adaptive control status. |
| POST | `/api/mt5-adaptive-control/run` | `guarded-control` | Run adaptive control under backend safety controls. |
| GET | `/api/mt5-platform` | `read-only` | MT5 platform store base endpoint. |
| ANY | `/api/mt5-platform/:endpoint` | `guarded-control` | MT5 platform store sub-endpoints; not a direct order API. |
| GET | `/api/mt5-trading` | `guarded-control` | MT5 trading bridge status; defaults locked by dryRun/killSwitch. |
| ANY | `/api/mt5-trading/:endpoint` | `guarded-control` | MT5 trading bridge sub-endpoint; must remain guarded by backend and EA controls. |
| GET | `/api/mt5` | `guarded-control` | Compatibility alias for MT5 trading status. |
| ANY | `/api/mt5/:endpoint` | `guarded-control` | Compatibility alias for MT5 trading bridge sub-endpoints. |
| DELETE | `/api/mt5/order/:ticket` | `guarded-control` | Order cancel route; must remain blocked/guarded unless explicitly authorized. |

### hfm-crypto-cfd

- Phase / Domain：`backend-core`。
- Endpoint 数量：`28`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/hfm-crypto` | `read-only` | HFM Crypto CFD shadow lane status alias; scans local MT5/HFM symbol evidence and Moss backtest profile metadata. |
| GET | `/api/hfm-crypto/status` | `read-only` | Read HFM Crypto CFD shadow lane status, detected crypto CFD symbols, Moss backtest profile summary, account brokerSymbolDiagnostics, operatorChecklist, blockers, and safety flags. Frontend first paint must use the compact view=summary variant and may pass scope=secondary/live16 to use the HFM Live16 crypto CFD account. Query variants: `?view=summary`: Preserves status, statusZh, nextRequiredActionZh, operatorChecklist, symbolEvidence.brokerSymbolDiagnostics, blockers, sourceFiles, and safety while omitting bulky review bundles for fast account diagnostics.; `?view=summary&scope=secondary`: Uses the configured secondary/Live16 MT5 Files directory for HFM crypto CFD evidence while preserving the same read-only safety boundary. Aliases include scope=live16 and scope=hfm-live16. |
| GET | `/api/hfm-crypto/symbols` | `read-only` | Read detected HFM Crypto CFD symbol evidence from local MT5 Bases roots; no order execution. |
| GET | `/api/hfm-crypto/contract-spec-export` | `read-only` | Read the HFM Crypto CFD contract-spec export that converts MT5 symbol registry data into review input. |
| GET | `/api/hfm-crypto/execution-spec` | `read-only` | Read the HFM Crypto CFD contract-spec review generated from local MT5/HFM broker symbol specs. |
| GET | `/api/hfm-crypto/simulation-profile` | `read-only` | Read the HFM Crypto CFD simulation-profile review for ROI, Sharpe, drawdown, trade count, and liquidation evidence. |
| GET | `/api/hfm-crypto/evidence-kit` | `read-only` | Read the HFM Crypto CFD evidence kit with contract-spec templates and read-only collection commands. |
| GET | `/api/hfm-crypto/evidence-bootstrap` | `read-only` | Read the HFM evidence bootstrap artifact with draft input paths, filled-input validation, and sim-to-live blocker summary. |
| GET | `/api/hfm-crypto/mt5-exporter-review` | `read-only` | Read the MT5 EA exporter review that checks whether the installed QuantGod EA can emit HFM crypto symbol specs. |
| GET | `/api/hfm-crypto/mt5-upgrade-bundle` | `read-only` | Read the staged MT5 EA exporter upgrade bundle manifest; it is manual-only and does not mutate MT5 files. |
| GET | `/api/hfm-crypto/mt5-exporter-deploy-plan` | `read-only` | Read the manual MT5 exporter deploy and rollback plan; it describes operator steps only and does not copy files, compile, or mutate MT5. |
| GET | `/api/hfm-crypto/standalone-exporter-bundle` | `read-only` | Read the standalone read-only HFM crypto symbol-spec exporter bundle for manual MT5 review; it does not select symbols, send orders, or change presets. |
| GET | `/api/hfm-crypto/mt5-post-upgrade-verify` | `read-only` | Read the post-upgrade verifier that checks installed EA source, compiled ex5, exported HFM crypto specs, and contract-spec review status. |
| GET | `/api/hfm-crypto/post-upgrade-controller` | `read-only` | Read the HFM post-upgrade controller that coordinates exporter review, manual upgrade bundle, post-upgrade verify, and local contract-spec refresh. |
| GET | `/api/hfm-crypto/filled-input-validator` | `read-only` | Read the HFM review-input validator that checks manual filled specs/profile or passing contract-spec/simulation review artifacts before promotion review. |
| POST | `/api/hfm-crypto/build` | `read-only` | Rebuild HFM Crypto CFD shadow state and optional Moss backtest profile mapping; writes local evidence only. |
| POST | `/api/hfm-crypto/contract-spec-export/build` | `read-only` | Build a local HFM Crypto CFD contract-spec export from MT5 symbol registry JSON or optional live read-only MT5 registry access. |
| POST | `/api/hfm-crypto/execution-spec/build` | `read-only` | Build the HFM Crypto CFD contract-spec review from a local JSON/CSV export; does not create MT5 order requests. |
| POST | `/api/hfm-crypto/simulation-profile/build` | `read-only` | Build the HFM Crypto CFD simulation-profile review from an explicit local Moss/backtest JSON or auto-discovered saved HFM profile artifact; does not unlock execution. |
| POST | `/api/hfm-crypto/evidence-kit/build` | `read-only` | Write local HFM Crypto CFD evidence-kit JSON/CSV templates; no MT5 mutation or broker call is made. |
| POST | `/api/hfm-crypto/evidence-bootstrap/build` | `read-only` | Write local HFM evidence bootstrap drafts and review artifact summaries without writing filled inputs, MT5 request files, or broker calls. |
| POST | `/api/hfm-crypto/mt5-exporter-review/build` | `read-only` | Build the local MT5 EA exporter review; it does not copy files into MT5, compile an EA, change presets, or send orders. |
| POST | `/api/hfm-crypto/mt5-upgrade-bundle/build` | `read-only` | Stage the reviewed QuantGod EA source and manifest under runtime for manual MT5 upgrade; no installed files are modified. |
| POST | `/api/hfm-crypto/mt5-exporter-deploy-plan/build` | `read-only` | Build the manual MT5 exporter deploy and rollback plan; it writes local review evidence only and does not mutate MT5. |
| POST | `/api/hfm-crypto/standalone-exporter-bundle/build` | `read-only` | Build the standalone read-only HFM crypto symbol-spec exporter bundle for manual review; it writes local review evidence only and cannot send orders. |
| POST | `/api/hfm-crypto/mt5-post-upgrade-verify/build` | `read-only` | Build the post-upgrade verifier and, when specs are present, refresh local contract-spec review artifacts without mutating MT5 or sending orders. |
| POST | `/api/hfm-crypto/post-upgrade-controller/build` | `read-only` | Run the HFM post-upgrade controller; it may write local review artifacts but never copies into MT5, compiles an EA, changes presets, or sends orders. |
| POST | `/api/hfm-crypto/filled-input-validator/build` | `read-only` | Build the HFM review-input validator artifact from manual filled specs/profile or already passing auto review artifacts; it writes review evidence only and cannot create order requests. |

### live-automation-readiness

- Phase / Domain：`backend-core`。
- Endpoint 数量：`108`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/live-automation` | `read-only` | Live automation readiness dossier alias; summarizes sim-to-live review status without writing orders. |
| GET | `/api/live-automation/status` | `read-only` | Build a current read-only live automation readiness dossier from USDJPY MT5 gates and HFM crypto shadow evidence; HFM account-no-crypto blockers, accountCryptoAvailability, and operatorChecklist must pass through without enabling execution. |
| GET | `/api/live-automation/readiness` | `read-only` | Build a transient live automation readiness view from USDJPY MT5 gates and HFM crypto shadow evidence. |
| POST | `/api/live-automation/build` | `read-only` | Write a local readiness dossier for review; must keep orderSendAllowed and live preset mutation disabled. |
| GET | `/api/live-automation/review-packet` | `read-only` | Read the local live execution review packet with dry-run order intent specs and blockers. |
| POST | `/api/live-automation/review-packet/build` | `read-only` | Write a local live execution review packet; it must not create MT5 order requests, presets, or credentials. |
| GET | `/api/live-automation/approval-draft` | `read-only` | Read the local operator approval draft that lists required final-review acknowledgements. |
| POST | `/api/live-automation/approval-draft/build` | `read-only` | Write a local operator approval draft; it does not accept secrets or unlock live execution. |
| GET | `/api/live-automation/approval-evidence` | `read-only` | Read the local operator approval evidence review; accepted evidence still cannot unlock live execution. |
| POST | `/api/live-automation/approval-evidence/build` | `read-only` | Validate a local operator approval JSON against the review packet hash and required acknowledgements without writing orders. |
| GET | `/api/live-automation/dry-run-plan` | `read-only` | Read the dry-run live execution plan; it must keep MT5 pending order writes disabled. |
| POST | `/api/live-automation/dry-run-plan/build` | `read-only` | Write the dry-run live execution plan for review; no real order files or broker calls are produced. |
| GET | `/api/live-automation/execution-lane-spec` | `read-only` | Read the future MT5 execution lane implementation spec; it remains non-executing. |
| POST | `/api/live-automation/execution-lane-spec/build` | `read-only` | Write the future execution lane handoff spec after approval evidence and dry-run intents; it still forbids order files and broker calls. |
| GET | `/api/live-automation/dry-run-replay` | `read-only` | Read the dry-run intent replay review; replay success still cannot write orders. |
| POST | `/api/live-automation/dry-run-replay/build` | `read-only` | Replay approved dry-run intents against the execution lane spec without creating MT5 order files or broker calls. |
| GET | `/api/live-automation/runtime-preflight` | `read-only` | Read the runtime preflight probe that checks fresh MT5 dashboard, live-pilot mode, account, symbol, spread, trade permission, and kill switch evidence without writing orders. |
| POST | `/api/live-automation/runtime-preflight/build` | `read-only` | Build the runtime preflight probe from approved dry-run replay and live-pilot MT5 dashboard evidence; it still forbids order files and broker calls. |
| GET | `/api/live-automation/order-request-contract` | `read-only` | Read the MT5 order request contract that defines future reviewed request and receipt fields without creating request files. |
| POST | `/api/live-automation/order-request-contract/build` | `read-only` | Build the MT5 order request contract from runtime preflight evidence; it remains contract-only and cannot write broker request files. |
| GET | `/api/live-automation/pipeline` | `read-only` | Read the sim-to-live automation pipeline that summarizes every review stage without enabling execution. |
| POST | `/api/live-automation/pipeline/build` | `read-only` | Run the full sim-to-live review pipeline and write local review artifacts; it still cannot write MT5 request files or broker calls. |
| GET | `/api/live-automation/adapter-review` | `read-only` | Read the execution adapter review shell that validates future request and receipt contracts without side effects. |
| POST | `/api/live-automation/adapter-review/build` | `read-only` | Build the execution adapter review shell from the sim-to-live pipeline and MT5 request contract; no request files or broker calls are produced. |
| GET | `/api/live-automation/evidence-intake` | `read-only` | Read the live evidence intake summary for missing HFM crypto files, review artifacts, MT5 dashboard evidence, and safe refresh commands. |
| POST | `/api/live-automation/evidence-intake/build` | `read-only` | Build the live evidence intake artifact and optional local review artifacts; it cannot write MT5 request files or make broker calls. |
| GET | `/api/live-automation/promotion-candidates` | `read-only` | Read the live promotion candidate selector that ranks simulation-qualified lanes for operator review without enabling execution. |
| POST | `/api/live-automation/promotion-candidates/build` | `read-only` | Build the live promotion candidate selector from readiness, evidence intake, review packet, and pipeline artifacts; no order request files or broker calls are produced. |
| GET | `/api/live-automation/promotion-controller` | `read-only` | Read the sim-to-live promotion controller that automates operator review packet generation when a lane is simulation-qualified. |
| POST | `/api/live-automation/promotion-controller/build` | `read-only` | Build the promotion controller and, when candidates exist, write review packet, approval draft, dry-run plan, and pipeline artifacts without enabling execution. |
| GET | `/api/live-automation/adapter-sandbox` | `read-only` | Read the adapter sandbox review bundle that validates future MT5 request and receipt serialization without writing MT5 request files. |
| POST | `/api/live-automation/adapter-sandbox/build` | `read-only` | Build a local review-only adapter sandbox bundle with sample request and receipt payloads; it cannot call a broker or write request files. |
| GET | `/api/live-automation/adapter-contract-validator` | `read-only` | Read the adapter contract validator artifact that checks future MT5 request JSON against the approved request and receipt contract without side effects. |
| POST | `/api/live-automation/adapter-contract-validator/build` | `read-only` | Build the review-only adapter contract validator; it validates request JSON and emits review-only receipts without writing MT5 request files or calling a broker. |
| GET | `/api/live-automation/orchestrator` | `read-only` | Read the sim-to-live orchestrator state machine across evidence, promotion, approval, dry-run, preflight, request contract, adapter review gates, and post-adapter live execution review stages. |
| POST | `/api/live-automation/orchestrator/build` | `read-only` | Run the full sim-to-live orchestrator and write local review artifacts, including liveExecutionStages for disabled harness, live pilot activation, receipt reconciliation, and EA request reader runtime review; it never writes MT5 request files or calls a broker. |
| GET | `/api/live-automation/adapter-harness` | `read-only` | Read the disabled execution adapter harness that plans request and receipt paths for review without writing MT5 Files. |
| POST | `/api/live-automation/adapter-harness/build` | `read-only` | Build the disabled adapter harness with idempotency, atomic-write, and review-only receipt checks; it never writes request files or calls a broker. |
| GET | `/api/live-automation/live-pilot-activation-review` | `read-only` | Read the live pilot activation review packet that summarizes orchestrator, preflight, adapter harness, and deployment runbook gates without enabling execution. |
| POST | `/api/live-automation/live-pilot-activation-review/build` | `read-only` | Build the live pilot activation review packet; it never writes MT5 request files, mutates presets, stores credentials, or calls a broker. |
| GET | `/api/live-automation/receipt-reconciliation-review` | `read-only` | Read the receipt reconciliation review artifact that matches review-only receipts to planned requests and describes auto-disable rules without side effects. |
| POST | `/api/live-automation/receipt-reconciliation-review/build` | `read-only` | Build the receipt reconciliation review artifact from the disabled harness or a local receipt JSON; it never writes receipt files, mutates auto-disable state, or calls a broker. |
| GET | `/api/live-automation/ea-request-reader-review` | `read-only` | Read the EA request reader review artifact that checks source safety markers and upstream review readiness without consuming request files. |
| POST | `/api/live-automation/ea-request-reader-review/build` | `read-only` | Build the EA request reader review artifact; it inspects source markers, upstream review artifacts, and optional EA runtime status JSON/dashboard evidence, but never reads MT5 request files, writes receipts, mutates presets, or calls a broker. |
| GET | `/api/live-automation/live-execution-cutover-review` | `read-only` | Read the final live execution cutover review artifact that summarizes all review-only prerequisites before a separate implementation review. |
| POST | `/api/live-automation/live-execution-cutover-review/build` | `read-only` | Build the final cutover review artifact from orchestrator, activation, receipt, EA reader, preflight, approval, order contract, and disabled harness evidence; it never writes request or receipt files, consumes MT5 requests, mutates presets, or calls a broker. |
| GET | `/api/live-automation/live-execution-implementation-spec` | `read-only` | Read the live execution implementation spec that splits post-cutover work into separate adapter, EA reader, broker send, receipt, and rollback implementation review contracts. |
| POST | `/api/live-automation/live-execution-implementation-spec/build` | `read-only` | Build the post-cutover implementation spec; it writes a review artifact only and never writes request files, consumes MT5 requests, writes receipts, mutates presets, or calls a broker. |
| GET | `/api/live-automation/live-execution-adapter-write-review` | `read-only` | Read the adapter writer review artifact with canonical request serialization, idempotency hashes, and atomic write planning. |
| POST | `/api/live-automation/live-execution-adapter-write-review/build` | `read-only` | Build the adapter writer review artifact; it embeds serialized request payloads for review but never writes MT5 request files, writes receipts, consumes requests, mutates presets, or calls a broker. |
| GET | `/api/live-automation/ea-request-consumption-review` | `read-only` | Read the EA request consumption review artifact that aligns adapter writer plans with the EA reader contract and disabled runtime status. |
| POST | `/api/live-automation/ea-request-consumption-review/build` | `read-only` | Build the EA request consumption review artifact; it creates reject-only consumption plans but never reads request files, writes receipts, consumes requests, mutates presets, or calls a broker. |
| GET | `/api/live-automation/broker-order-send-review` | `read-only` | Read the broker order send wrapper review artifact that binds reviewed EA consumption plans to account, symbol, risk, and receipt obligations. |
| POST | `/api/live-automation/broker-order-send-review/build` | `read-only` | Build the broker order send wrapper review artifact; it creates blocked broker-send contract plans but never calls a broker, writes request files, writes receipts, mutates presets, or enables order sending. |
| GET | `/api/live-automation/champion-promotion-gate` | `read-only` | Read the champion promotion gate review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/champion-tester-forward-request` | `read-only` | Read the champion tester forward request review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/champion-tester-run-gate` | `read-only` | Read the champion tester run gate review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/champion-tester-lock-draft` | `read-only` | Read the champion tester lock draft review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/live-execution-rollback-review` | `read-only` | Read the live execution rollback review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-readiness-refresh` | `read-only` | Read the release readiness refresh review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-minimal-diff-review` | `read-only` | Read the release minimal diff review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-token-evidence-review` | `read-only` | Read the release token evidence review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-token-signoff-draft` | `read-only` | Read the release token signoff draft review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-token-signoff-input-template` | `read-only` | Read the release token signoff input template review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-token-signoff-input-review` | `read-only` | Read the release token signoff input review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-token-signoff-handoff` | `read-only` | Read the release token signoff handoff review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/release-token-signoff-evidence-matrix` | `read-only` | Read the release token signoff evidence matrix review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/lane-selector` | `read-only` | Read the lane selector review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-runtime-handoff` | `read-only` | Read the forex live12 runtime handoff review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-capacity-expansion-review` | `read-only` | Read the forex live12 capacity expansion review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-capacity-expansion-roadmap` | `read-only` | Read the forex live12 capacity expansion roadmap review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-micro-expansion-review` | `read-only` | Read the forex live12 micro expansion review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-rsi-repair-plan` | `read-only` | Read the forex live12 RSI repair plan review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-rsi-shadow-candidate` | `read-only` | Read the forex live12 RSI shadow candidate review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-rsi-tester-request` | `read-only` | Read the forex live12 RSI tester request review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-rsi-tester-run-gate` | `read-only` | Read the forex live12 RSI tester run gate review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-rsi-candidate-promotion-gate` | `read-only` | Read the forex live12 RSI candidate promotion gate review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/forex-live12-rsi-tester-lock-draft` | `read-only` | Read the forex live12 RSI tester lock draft review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/sim-target-execution-review-summary` | `read-only` | Read the sim target execution review summary artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/ace-execution-candidate-pack` | `read-only` | Read the ace execution candidate pack review artifact or status; exposes evidence only and must keep execution disabled. |
| GET | `/api/live-automation/ace-upgrade-action-plan` | `read-only` | Read the ace upgrade action plan review artifact or status; exposes evidence only and must keep execution disabled. |
| POST | `/api/live-automation/champion-promotion-gate/build` | `read-only` | Build or refresh the champion promotion gate review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/champion-tester-forward-request/build` | `read-only` | Build or refresh the champion tester forward request review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/champion-tester-run-gate/build` | `read-only` | Build or refresh the champion tester run gate review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/champion-tester-lock-draft/build` | `read-only` | Build or refresh the champion tester lock draft review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/live-execution-rollback-review/build` | `read-only` | Build or refresh the live execution rollback review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-readiness-refresh/build` | `read-only` | Build or refresh the release readiness refresh review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-minimal-diff-review/build` | `read-only` | Build or refresh the release minimal diff review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-token-evidence-review/build` | `read-only` | Build or refresh the release token evidence review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-token-signoff-draft/build` | `read-only` | Build or refresh the release token signoff draft review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-token-signoff-input-template/build` | `read-only` | Build or refresh the release token signoff input template review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-token-signoff-input-review/build` | `read-only` | Build or refresh the release token signoff input review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-token-signoff-handoff/build` | `read-only` | Build or refresh the release token signoff handoff review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/release-token-signoff-evidence-matrix/build` | `read-only` | Build or refresh the release token signoff evidence matrix review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/lane-selector/build` | `read-only` | Build or refresh the lane selector review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-runtime-handoff/build` | `read-only` | Build or refresh the forex live12 runtime handoff review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-capacity-expansion-review/build` | `read-only` | Build or refresh the forex live12 capacity expansion review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-capacity-expansion-roadmap/build` | `read-only` | Build or refresh the forex live12 capacity expansion roadmap review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-micro-expansion-review/build` | `read-only` | Build or refresh the forex live12 micro expansion review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-rsi-repair-plan/build` | `read-only` | Build or refresh the forex live12 RSI repair plan review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-rsi-shadow-candidate/build` | `read-only` | Build or refresh the forex live12 RSI shadow candidate review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-rsi-tester-request/build` | `read-only` | Build or refresh the forex live12 RSI tester request review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-rsi-tester-run-gate/build` | `read-only` | Build or refresh the forex live12 RSI tester run gate review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-rsi-candidate-promotion-gate/build` | `read-only` | Build or refresh the forex live12 RSI candidate promotion gate review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/forex-live12-rsi-tester-lock-draft/build` | `read-only` | Build or refresh the forex live12 RSI tester lock draft review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/sim-target-execution-review-summary/build` | `read-only` | Build or refresh the sim target execution review summary artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/ace-execution-candidate-pack/build` | `read-only` | Build or refresh the ace execution candidate pack review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |
| POST | `/api/live-automation/ace-upgrade-action-plan/build` | `read-only` | Build or refresh the ace upgrade action plan review artifact; review-only and must not write MT5 order requests, mutate presets, store credentials, or call a broker. |

### mt5-readonly

- Phase / Domain：`phase1`。
- Endpoint 数量：`13`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/mt5-readonly/status` | `read-only` | MT5 read-only bridge status. |
| GET | `/api/mt5-readonly/account` | `read-only` | Account snapshot, no credentials. |
| GET | `/api/mt5-readonly/positions` | `read-only` | Open positions snapshot. |
| GET | `/api/mt5-readonly/orders` | `read-only` | Open/pending orders snapshot. |
| GET | `/api/mt5-readonly/symbols` | `read-only` | MT5 symbol list. |
| GET | `/api/mt5-readonly/quote` | `read-only` | Quote for one symbol. |
| GET | `/api/mt5-readonly/snapshot` | `read-only` | Combined MT5 monitor snapshot. |
| GET | `/api/mt5-readonly/kline` | `read-only` | K-line bars for KlineCharts. |
| GET | `/api/mt5-readonly/trades` | `read-only` | Trade markers for chart overlay. |
| GET | `/api/mt5-readonly/shadow-signals` | `read-only` | Shadow signal markers for chart overlay. |
| GET | `/api/shadow-signals` | `read-only` | Compatibility alias for shadow signal overlay. |
| GET | `/api/mt5-readonly-secondary` | `read-only` | Secondary MT5 read-only bridge snapshot alias for the secondary account. |
| GET | `/api/mt5-readonly-secondary/:endpoint` | `read-only` | Secondary MT5 read-only bridge sub-endpoint wrapper. |

### ai-analysis-v1

- Phase / Domain：`phase1`。
- Endpoint 数量：`8`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/ai-analysis` | `advisory` | AI Analysis V1 config/status alias. |
| POST | `/api/ai-analysis/run` | `advisory` | Run Technical/Risk/Decision V1 analysis. |
| GET | `/api/ai-analysis/latest` | `read-only` | Latest AI V1 report. |
| GET | `/api/ai-analysis/history` | `read-only` | AI V1 report history list. |
| GET | `/api/ai-analysis/history/:id` | `read-only` | One AI V1 report by id. |
| GET | `/api/ai-analysis/config` | `read-only` | AI V1 local config/status. |
| GET | `/api/ai-analysis/agent-health` | `read-only` | Latest local AI agent health evidence. |
| GET | `/api/ai-analysis/agent-health/history` | `read-only` | Historical local AI agent health evidence. |

### phase2-file-facade

- Phase / Domain：`phase2`。
- Endpoint 数量：`32`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/governance/advisor` | `read-only` | QuantGod_GovernanceAdvisor.json |
| GET | `/api/governance/version-registry` | `read-only` | QuantGod_StrategyVersionRegistry.json |
| GET | `/api/governance/promotion-gate` | `read-only` | QuantGod_VersionPromotionGate.json |
| GET | `/api/governance/optimizer-v2` | `read-only` | QuantGod_OptimizerV2Plan.json |
| GET | `/api/paramlab/status` | `read-only` | QuantGod_ParamLabStatus.json |
| GET | `/api/paramlab/results` | `read-only` | QuantGod_ParamLabResults.json |
| GET | `/api/paramlab/scheduler` | `read-only` | QuantGod_ParamLabAutoScheduler.json |
| GET | `/api/paramlab/recovery` | `read-only` | QuantGod_ParamLabRunRecovery.json |
| GET | `/api/paramlab/report-watcher` | `read-only` | QuantGod_ParamLabReportWatcher.json |
| GET | `/api/paramlab/tester-window` | `read-only` | QuantGod_AutoTesterWindow.json |
| GET | `/api/research/stats` | `read-only` | QuantGod_MT5ResearchStats.json |
| GET | `/api/research/entry-blockers` | `read-only` | QuantGod_MT5EntryBlockers.json |
| GET | `/api/dashboard/state` | `read-only` | QuantGod_Dashboard.json |
| GET | `/api/dashboard/backtest-summary` | `read-only` | QuantGod_BacktestSummary.json |
| GET | `/api/trades/journal` | `read-only-csv` | QuantGod_TradeJournal.csv |
| GET | `/api/trades/close-history` | `read-only-csv` | QuantGod_CloseHistory.csv |
| GET | `/api/trades/outcome-labels` | `read-only-csv` | QuantGod_TradeOutcomeLabels.csv |
| GET | `/api/trades/trading-audit` | `read-only-csv` | QuantGod_MT5TradingAuditLedger.csv |
| GET | `/api/shadow/signals` | `read-only-csv` | QuantGod_ShadowSignalLedger.csv |
| GET | `/api/shadow/outcomes` | `read-only-csv` | QuantGod_ShadowOutcomeLedger.csv |
| GET | `/api/shadow/candidates` | `read-only-csv` | QuantGod_ShadowCandidateLedger.csv |
| GET | `/api/shadow/candidate-outcomes` | `read-only-csv` | QuantGod_ShadowCandidateOutcomeLedger.csv |
| GET | `/api/paramlab/results-ledger` | `read-only-csv` | QuantGod_ParamLabResultsLedger.csv |
| GET | `/api/paramlab/scheduler-ledger` | `read-only-csv` | QuantGod_ParamLabAutoSchedulerLedger.csv |
| GET | `/api/paramlab/report-watcher-ledger` | `read-only-csv` | QuantGod_ParamLabReportWatcherLedger.csv |
| GET | `/api/paramlab/recovery-ledger` | `read-only-csv` | QuantGod_ParamLabRunRecoveryLedger.csv |
| GET | `/api/paramlab/tester-window-ledger` | `read-only-csv` | QuantGod_AutoTesterWindowLedger.csv |
| GET | `/api/research/stats-ledger` | `read-only-csv` | QuantGod_MT5ResearchStatsLedger.csv |
| GET | `/api/research/entry-blockers-ledger` | `read-only-csv` | QuantGod_MT5EntryBlockersLedger.csv |
| GET | `/api/research/strategy-evaluation` | `read-only-csv` | QuantGod_StrategyEvaluationReport.csv |
| GET | `/api/research/regime-evaluation` | `read-only-csv` | QuantGod_RegimeEvaluationReport.csv |
| GET | `/api/research/manual-alpha` | `read-only-csv` | QuantGod_ManualAlphaLedger.csv |

### notify

- Phase / Domain：`phase2`。
- Endpoint 数量：`7`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/notify/config` | `read-only` | Notification config status; no secret values. |
| GET | `/api/notify/history` | `read-only` | Notification delivery history. |
| POST | `/api/notify/test` | `push-only` | Send one test notification; never accepts trading commands. |
| POST | `/api/notify/daily-digest` | `push-only` | Trigger AI ops daily digest push; advisory-only output. |
| POST | `/api/notify/runtime-scan` | `push-only` | Trigger runtime scan notification; never accepts trading commands. |
| GET | `/api/notify/mt5-ai-monitor/config` | `read-only` | MT5 AI monitor config status; no secret values. |
| POST | `/api/notify/mt5-ai-monitor/run` | `push-only` | Run MT5 AI monitor analysis; advisory-only, push-only. |

### phase3-vibe-ai-kline

- Phase / Domain：`phase3`。
- Endpoint 数量：`23`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/ai-analysis/deepseek-telegram/config` | `read-only` | DeepSeek-Telegram fusion config status. |
| POST | `/api/ai-analysis/deepseek-telegram/run` | `advisory` | Run DeepSeek-Telegram fusion analysis. |
| GET | `/api/ai-analysis/deepseek-telegram/latest` | `read-only` | Latest DeepSeek-Telegram fusion result. |
| GET | `/api/vibe-coding` | `research-only` | Vibe Coding config alias. |
| GET | `/api/vibe-coding/config` | `research-only` | Vibe Coding config. |
| POST | `/api/vibe-coding/generate` | `research-only` | Generate sandboxed Python strategy code from natural language. |
| POST | `/api/vibe-coding/import-library` | `research-only` | Import a research-only strategy library candidate into the Vibe Coding sandbox. |
| POST | `/api/vibe-coding/iterate` | `research-only` | Iterate a generated strategy. |
| POST | `/api/vibe-coding/backtest` | `research-only` | Run local research-only backtest. |
| POST | `/api/vibe-coding/analyze` | `advisory` | Analyze backtest result. |
| GET | `/api/vibe-coding/strategies` | `read-only` | List generated strategy versions. |
| GET | `/api/vibe-coding/strategy` | `read-only` | Vibe Coding strategy detail base route alias. |
| GET | `/api/vibe-coding/strategy/:id` | `read-only` | Fetch generated strategy detail. |
| GET | `/api/ai-analysis-v2` | `advisory` | AI Analysis V2 config alias. |
| GET | `/api/ai-analysis-v2/config` | `read-only` | AI Analysis V2 config. |
| POST | `/api/ai-analysis-v2/run` | `advisory` | Run V2 multi-agent debate analysis. |
| GET | `/api/ai-analysis-v2/latest` | `read-only` | Latest AI V2 analysis. |
| GET | `/api/ai-analysis-v2/history` | `read-only` | AI V2 history list. |
| GET | `/api/ai-analysis-v2/history/:id` | `read-only` | One AI V2 report. |
| GET | `/api/kline` | `read-only` | K-line enhancement config alias. |
| GET | `/api/kline/ai-overlays` | `read-only` | AI BUY/SELL/HOLD overlay markers. |
| GET | `/api/kline/vibe-indicators` | `read-only` | Vibe indicator overlay descriptors. |
| GET | `/api/kline/realtime-config` | `read-only` | K-line polling config. |

### p2-3-sqlite-state-layer

- Phase / Domain：`phase2`。
- Endpoint 数量：`7`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/state` | `read-only` | SQLite state layer status alias; local evidence persistence only. |
| GET | `/api/state/status` | `read-only` | SQLite state layer schema, table counts, and safety defaults. |
| GET | `/api/state/config` | `read-only` | Resolved local SQLite state configuration; no secrets. |
| GET | `/api/state/events` | `read-only` | Normalized local evidence events from SQLite. |
| GET | `/api/state/ai-analysis` | `read-only` | Advisory-only AI analysis run index from SQLite. |
| GET | `/api/state/vibe-strategies` | `read-only` | Research-only Vibe strategy index from SQLite. |
| GET | `/api/state/notifications` | `read-only` | Push-only notification event index from SQLite. |

### p3-12-automation-chain-runner

- Phase / Domain：`phase3`。
- Endpoint 数量：`4`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/automation-chain` | `read-only` | Automation chain status alias; no trading execution. |
| GET | `/api/automation-chain/status` | `read-only` | Latest automation chain status and missing evidence. |
| GET | `/api/automation-chain/telegram-text` | `push-preview` | Chinese Telegram preview text for automation chain. |
| POST | `/api/automation-chain/run` | `local-advisory-control` | Run local evidence chain; writes runtime evidence but does not place orders. |

### P3-14 USDJPY 单品种多策略实验室

- Phase / Domain：`unknown`。
- Endpoint 数量：`117`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/usdjpy-strategy-lab` | `read-only` | USDJPY 策略实验室基础状态别名。 |
| GET | `/api/usdjpy-strategy-lab/status` | `read-only` | 读取 USDJPY-only 策略政策状态。 |
| GET | `/api/usdjpy-strategy-lab/scoreboard` | `read-only` | 读取 USDJPY 多策略评分矩阵。 |
| GET | `/api/usdjpy-strategy-lab/dry-run` | `read-only` | 生成或读取 USDJPY EA 干跑决策。 |
| GET | `/api/usdjpy-strategy-lab/telegram-text` | `read-only` | 生成 USDJPY 策略政策的中文 Telegram 文案。 |
| POST | `/api/usdjpy-strategy-lab/run` | `read-only` | 运行 USDJPY 策略政策生成；不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/catalog` | `read-only` | 读取 USDJPY 策略工厂目录，包含东京突破、夜盘回归和 H4 回调三条新增 shadow 策略。 |
| GET | `/api/usdjpy-strategy-lab/signals` | `read-only` | 读取 USDJPY shadow 候选信号，用于确认新增策略是否正在采样。 |
| POST | `/api/usdjpy-strategy-lab/signals/run` | `read-only` | 刷新 USDJPY shadow 候选信号；只解析证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/backtest-plan` | `read-only` | 读取 USDJPY 新策略回测计划。 |
| POST | `/api/usdjpy-strategy-lab/backtest-plan/build` | `read-only` | 生成 USDJPY 新策略回测计划；不会启动真实交易。 |
| GET | `/api/usdjpy-strategy-lab/candidate-policy` | `read-only` | 读取 USDJPY 候选策略政策。 |
| POST | `/api/usdjpy-strategy-lab/candidate-policy/build` | `read-only` | 生成 USDJPY 候选策略政策；新策略仍保持 shadow-only。 |
| GET | `/api/usdjpy-strategy-lab/evidence` | `read-only` | 读取 USDJPY 策略评分和候选信号的证据合并视图。 |
| GET | `/api/usdjpy-strategy-lab/risk-check` | `read-only` | 读取 USDJPY 策略工厂风险检查结果。 |
| GET | `/api/usdjpy-strategy-lab/imported-backtests` | `read-only` | 读取已导入的 USDJPY 回测结果账本。 |
| POST | `/api/usdjpy-strategy-lab/import-backtest` | `read-only` | 导入本机 USDJPY 回测 CSV/JSON 结果；只写研究证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/live-loop` | `read-only` | 读取 USDJPY 实盘 EA 恢复状态、阻断原因和下一步自动动作。 |
| POST | `/api/usdjpy-strategy-lab/live-loop/run` | `read-only` | 重建 USDJPY 实盘闭环 evidence；只写本地状态和 intent，不直接执行交易。 |
| GET | `/api/usdjpy-strategy-lab/live-loop/telegram-text` | `read-only` | 生成或发送 USDJPY 实盘闭环中文 Telegram 文案。 |
| GET | `/api/usdjpy-strategy-lab/evolution` | `read-only` | 读取 USDJPY 自学习闭环状态别名，包含数据集、回放、参数候选和配置提案。 |
| GET | `/api/usdjpy-strategy-lab/evolution/status` | `read-only` | 读取 USDJPY 自学习闭环状态，包含数据集、回放、参数候选和配置提案。 |
| POST | `/api/usdjpy-strategy-lab/evolution/build` | `read-only` | 重建 USDJPY 运行数据集、回放、参数候选和配置提案；只写本地研究证据。 |
| GET | `/api/usdjpy-strategy-lab/evolution/replay` | `read-only` | 读取或刷新 USDJPY 回放复盘，解释错失机会和过早出场。 |
| GET | `/api/usdjpy-strategy-lab/evolution/tune` | `read-only` | 读取或刷新 USDJPY tester-only 参数候选；不会自动应用到实盘。 |
| GET | `/api/usdjpy-strategy-lab/evolution/proposal` | `read-only` | 读取或刷新 USDJPY 实盘配置提案；提案进入自主治理门，stage-gated，不再等待人工审批。 |
| GET | `/api/usdjpy-strategy-lab/evolution/telegram-text` | `read-only` | 生成或发送 USDJPY 自学习闭环中文 Telegram 文案。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay` | `read-only` | 读取 USDJPY 因果 bar/tick 回放报告别名；等同 status。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/status` | `read-only` | 读取 USDJPY 因果 bar/tick 回放报告；后验窗口只用于评分，不参与入场触发。 |
| POST | `/api/usdjpy-strategy-lab/bar-replay/build` | `read-only` | 重建 USDJPY 因果回放报告、入场候选对比、出场候选对比和 replay ledger；不会执行交易。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/entry` | `read-only` | 读取 USDJPY current vs relaxed_entry_v1 入场候选对比；硬门禁不会放宽。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/exit` | `read-only` | 读取 USDJPY current vs let_profit_run_v1 出场持有候选对比；只重估已发生入场的出场表现。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/telegram-text` | `read-only` | 生成或发送 USDJPY 因果回放中文 Telegram 文案；后续由 P3-20 自主治理门评估。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward` | `read-only` | 读取 USDJPY walk-forward 稳定性筛选报告别名。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/status` | `read-only` | 读取 USDJPY train / validation / forward 三段稳定性筛选报告。 |
| POST | `/api/usdjpy-strategy-lab/walk-forward/build` | `read-only` | 重建 USDJPY walk-forward 报告、参数选择和 stage-gated 提案；不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/selection` | `read-only` | 读取 USDJPY walk-forward 参数选择结果。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/proposal` | `read-only` | 读取 USDJPY stage-gated live config proposal。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/telegram-text` | `read-only` | 生成或发送 USDJPY walk-forward 中文 Telegram 文案。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent` | `read-only` | 读取 USDJPY 自主治理 Agent 状态别名。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/state` | `read-only` | 读取 USDJPY 自主治理 Agent 当前阶段、受控 patch 和回滚状态。 |
| POST | `/api/usdjpy-strategy-lab/autonomous-agent/run` | `read-only` | 运行 USDJPY 自主治理门；只写受控 patch 和回滚证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/decision` | `read-only` | 读取 USDJPY 自主晋级决策。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/patch` | `read-only` | 读取 USDJPY 受控 config patch。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/lifecycle` | `read-only` | 读取 QuantGod v2.5 三车道自主生命周期，包含 Live Lane、MT5 Shadow Lane、HFM Crypto CFD Shadow Lane、美分账户、EA 对账摘要和下一阶段任务状态。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/lanes` | `read-only` | 读取 Live / MT5 Shadow / HFM Crypto CFD Shadow 三车道摘要；实盘只允许 USDJPY RSI LONG，模拟继续多策略。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/mt5-shadow` | `read-only` | 读取 MT5 多策略模拟车道排名和升降级阶段；shadow 策略不能直接进入实盘路线。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/hfm-crypto-shadow` | `read-only` | 读取 HFM Crypto CFD 品种证据、Moss 回测 profile 和 shadow-only 状态；不连接钱包、不保存 broker 凭证、不下单。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/ea-repro` | `read-only` | 读取 EA source、preset、input 和 ex5 hash 对账证据，帮助确认当前实盘 EA 是否来自受控版本。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2` | `read-only` | 读取 Daily Autopilot 2.0 中文早盘计划、夜盘复盘、三车道今日动作，以及 Strategy JSON GA Trace 状态和 Telegram Gateway 下一阶段任务。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/status` | `read-only` | 读取 Daily Autopilot 2.0 状态别名，包含下一阶段任务等待状态。 |
| POST | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/run` | `read-only` | 重建 Daily Autopilot 2.0 中文计划、复盘和下一阶段任务；只写本地证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/telegram-text` | `read-only` | 生成或发送 Daily Autopilot 2.0 中文 Telegram 文案，并说明 Strategy JSON / GA Trace 已进入 shadow/tester 过程审计，Telegram Gateway 等待下一阶段；Telegram 仍只推送，不接命令。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest` | `read-only` | 读取 USDJPY Strategy JSON SQLite 回测状态别名；只展示本地研究证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/status` | `read-only` | 读取 USDJPY Strategy JSON SQLite 回测状态、K线数量、最新报告和只读安全边界。 |
| POST | `/api/usdjpy-strategy-lab/strategy-backtest/sample` | `read-only` | 写入确定性 USDJPY H1 示例 K线到本地 SQLite，用于本地 smoke 和测试；不触达 MT5 交易。 |
| POST | `/api/usdjpy-strategy-lab/strategy-backtest/run` | `read-only` | 运行 USDJPY Strategy JSON 回测，输出 report、trades、equity curve 和 GA 可读 fitness evidence。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/telegram-text` | `read-only` | 生成或发送中文 Strategy JSON 回测摘要；Telegram 仍只推送，不接命令。 |
| POST | `/api/usdjpy-strategy-lab/strategy-backtest/sync-klines` | `read-only` | 从 MT5 Python 或 MQL5 CopyRates CSV 增量同步 USDJPY M1/M5/M15/H1 K线到本地 SQLite；只写回测证据。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/production-status` | `read-only` | 读取 USDJPY SQLite 历史数据生产验收状态，包含 M1/M5/M15/H1 覆盖深度、K线密度、最新延迟和后台同步来源。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/quality` | `read-only` | 读取 USDJPY Strategy JSON SQLite 回测质量状态，包含历史覆盖、数据来源和同步目标满足情况；只展示回测证据。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os` | `read-only` | 读取 USDJPY Evidence OS 审计状态；与 /evidence-os/status 保持兼容。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/status` | `read-only` | 读取 USDJPY Strategy JSON / Python Replay / MQL5 EA parity、执行反馈、Case Memory 和 Telegram Gateway 审计状态。 |
| POST | `/api/usdjpy-strategy-lab/evidence-os/run` | `read-only` | 生成 USDJPY evidence OS 审计包：parity、execution feedback、case memory 和 push-only notification ledger。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/parity` | `read-only` | 重建并读取 Strategy JSON / Python Replay / MQL5 EA parity report。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/execution-feedback` | `read-only` | 重建并读取 USDJPY live execution feedback / execution quality report。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/case-memory` | `read-only` | 重建并读取 USDJPY Case Memory，总结错失机会、早出、执行偏差和下一代 GA 线索。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/telegram-text` | `read-only` | 生成 USDJPY evidence OS 中文 Telegram 文案；走 push-only Gateway，不接命令。 |
| GET | `/api/case-memory` | `read-only` | 读取 P4-7 Case Memory → shadow Strategy JSON candidate / GA seed hint 状态别名；不执行交易。 |
| GET | `/api/case-memory/status` | `read-only` | 读取 Case Memory strategy structure report、parity gate、shadow Strategy JSON candidate 和 GA seed 线索。 |
| POST | `/api/case-memory/build` | `read-only` | 把 Case Memory root cause 转成 proposed mutation、shadow Strategy JSON candidate 和 GA seed hint；PARITY_FAIL 会阻断。 |
| GET | `/api/case-memory/telegram-text` | `push-preview` | 生成 Case Memory 策略结构候选中文 Telegram 文案；push-only，不接交易命令。 |
| GET | `/api/usdjpy-strategy-lab/ga` | `read-only` | 读取 USDJPY Strategy JSON GA 总状态别名；只展示 GA 过程审计，不直接进入实盘。 |
| GET | `/api/usdjpy-strategy-lab/ga/status` | `read-only` | 读取 USDJPY Strategy JSON GA 当前代数、种群、最佳 fitness、阻断数量和下一步动作。 |
| POST | `/api/usdjpy-strategy-lab/ga/run-generation` | `read-only` | 运行一代 USDJPY Strategy JSON GA，写入 generation、candidate、elite、blocker 和 evolution path 证据；不下单、不改 preset。 |
| GET | `/api/usdjpy-strategy-lab/ga/generations` | `read-only` | 读取 GA generation ledger，用于展示每一代如何生成、评分、保留和淘汰。 |
| GET | `/api/usdjpy-strategy-lab/ga/candidates` | `read-only` | 读取 GA candidate runs，包含 seedId、Strategy JSON、fitness 分解、rank、阶段和阻断原因。 |
| GET | `/api/usdjpy-strategy-lab/ga/candidate` | `read-only` | GA candidate 详情路由前缀；实际查询使用 seedId 子路径，不读取或修改交易状态。 |
| GET | `/api/usdjpy-strategy-lab/ga/candidate/:seedId` | `read-only` | 读取单个 GA seed 的 Strategy JSON、父代来源、fitness 分解、replay/walk-forward 状态和阻断解释。 |
| GET | `/api/usdjpy-strategy-lab/ga/evolution-path` | `read-only` | 读取 GA 进化路径，展示每代 bestFitness、bestStrategy、avgFitness 和阻断趋势。 |
| GET | `/api/usdjpy-strategy-lab/ga/blockers` | `read-only` | 读取 GA blocker summary，解释 schema、safety、样本、walk-forward、过拟合、max adverse 等失败原因。 |
| GET | `/api/usdjpy-strategy-lab/ga/telegram-text` | `read-only` | 生成或发送中文 GA 进化报告；Telegram 仍只推送，不接收交易命令。 |
| GET | `/api/usdjpy-strategy-lab/daily-todo` | `read-only` | 读取 Agent 今日待办，含车道、状态、指标、升降级、回滚状态和下一阶段任务；无需人工回灌。 |
| GET | `/api/usdjpy-strategy-lab/daily-todo/status` | `read-only` | 读取 Agent 今日待办状态别名，包含下一阶段任务等待状态。 |
| POST | `/api/usdjpy-strategy-lab/daily-todo/run` | `read-only` | 由 Agent 重建并写入今日待办和下一阶段任务；只写本地证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/daily-todo/telegram-text` | `read-only` | 生成或发送 Agent 今日待办中文 Telegram 文案，包含下一阶段任务；Telegram 仍只推送，不接命令。 |
| GET | `/api/usdjpy-strategy-lab/daily-review` | `read-only` | 读取 Agent 每日复盘，含净 R、最大不利 R、错失机会、早出场、升降级、回滚状态和下一阶段任务。 |
| GET | `/api/usdjpy-strategy-lab/daily-review/status` | `read-only` | 读取 Agent 每日复盘状态别名，包含下一阶段任务等待状态。 |
| POST | `/api/usdjpy-strategy-lab/daily-review/run` | `read-only` | 由 Agent 重建并写入每日复盘和下一阶段任务；只写本地证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/daily-review/telegram-text` | `read-only` | 生成或发送 Agent 每日复盘中文 Telegram 文案，包含下一阶段任务；Telegram 仍只推送，不接命令。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/telegram-text` | `read-only` | 生成或发送 USDJPY 自主治理中文 Telegram 文案。 |
| GET | `/api/telegram-gateway` | `read-only` | 读取 P4-5 Telegram Gateway 运维观测状态别名；只做 push-only 队列、去重、限频、ledger 观测。 |
| GET | `/api/telegram-gateway/status` | `read-only` | 读取 P4-5 Telegram Gateway 运维观测状态，包含队列、待投递、真实发送、抑制、失败和 topic 视图。 |
| POST | `/api/telegram-gateway/collect` | `push-preview` | 收集 Daily Autopilot、GA、Agent 和 HFM Crypto CFD 报告进入 push-only Gateway 队列；不接收 Telegram 命令。 |
| GET | `/api/telegram-gateway/telegram-text` | `push-preview` | 生成 Telegram Gateway 运维中文预览；仍只推送，不接 Telegram 命令。 |
| GET | `/api/usdjpy-strategy-lab/agent-ops-health` | `read-only` | 读取 USDJPY Agent operations health 状态别名；只汇总本地证据与心跳，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/agent-ops-health/status` | `read-only` | 读取 USDJPY Agent loop、Evidence OS、Telegram Gateway 和本地 runtime 健康状态。 |
| GET | `/api/strategy-ga-factory` | `read-only` | 读取 P4-4 Strategy JSON GA Factory 状态别名；只做工厂归档，不执行交易。 |
| GET | `/api/strategy-ga-factory/status` | `read-only` | 读取 GA Factory state、elite archive、strategy graveyard 和 lineage tree 摘要。 |
| POST | `/api/strategy-ga-factory/build` | `read-only` | 生成 GA Factory state、elite archive、strategy graveyard、lineage tree、reflection report 和 ledger；不下单、不改 preset。 |
| GET | `/api/strategy-ga-factory/intent-plan` | `read-only` | 读取自然语言 Strategy Factory intent plan；只生成 shadow-only Strategy JSON 和性格锁计划。 |
| POST | `/api/strategy-ga-factory/intent-plan/build` | `read-only` | 从大白话生成 shadow-only Strategy JSON seed、五维信号计划、30+ 参数和性格锁进化计划；不触发交易。 |
| GET | `/api/strategy-ga-factory/hyperliquid-shadow` | `read-only` | 读取 Hyperliquid/Moss 只读影子车道状态。 |
| POST | `/api/strategy-ga-factory/hyperliquid-shadow/build` | `read-only` | 写入 Moss agent 链接和可选本地 profile JSON 到只读 shadow mapping；不授权钱包、不下单。 |
| GET | `/api/strategy-ga-factory/telegram-text` | `push-preview` | 生成 GA Factory 中文 Telegram 文案；push-only，不接交易命令。 |
| GET | `/api/ga-factory` | `read-only` | 读取 GA Factory 状态短别名；等同 /api/strategy-ga-factory。 |
| GET | `/api/ga-factory/status` | `read-only` | 读取 GA Factory 状态短别名；等同 /api/strategy-ga-factory/status。 |
| POST | `/api/ga-factory/build` | `read-only` | 构建 GA Factory 短别名；等同 /api/strategy-ga-factory/build。 |
| GET | `/api/ga-factory/telegram-text` | `push-preview` | 生成 GA Factory 中文 Telegram 文案短别名。 |
| GET | `/api/usdjpy-strategy-lab/telegram-gateway/status` | `read-only` | 读取独立 Telegram Gateway 队列、ledger、去重、限频和 push-only 状态。 |
| POST | `/api/usdjpy-strategy-lab/telegram-gateway/test-event` | `read-only` | 写入中文测试 NotificationEvent 到 Gateway 队列；不发送交易命令。 |
| POST | `/api/usdjpy-strategy-lab/telegram-gateway/dispatch` | `read-only` | 处理 Gateway 队列；默认只写 ledger，send=1 时仍要求 push allowed 且 commands disabled。 |
| GET | `/api/usdjpy-strategy-lab/telegram-gateway` | `read-only` | 读取独立 Telegram Gateway 状态兼容别名。 |
| GET | `/api/usdjpy-strategy-lab/strategy-contract` | `read-only` | 读取 Strategy JSON → MQL5 EA 只读契约状态兼容别名；只用于 shadow/tester/paper lane 评估。 |
| GET | `/api/usdjpy-strategy-lab/strategy-contract/status` | `read-only` | 读取 Strategy JSON → MQL5 EA 只读契约状态、所选 seed、fingerprint 和 EA 回执；只用于 shadow/tester/paper lane 评估。 |
| POST | `/api/usdjpy-strategy-lab/strategy-contract/build` | `read-only` | 生成 EA 可读取的 Strategy JSON contract 文件；不下单、不改 live preset。 |
| GET | `/api/usdjpy-strategy-lab/strategy-contract/telegram-text` | `read-only` | 生成 Strategy JSON → EA 只读契约中文摘要；Telegram 仍只推送，不接命令。 |

### P4-6 Production Evidence Validation

- Phase / Domain：`unknown`。
- Endpoint 数量：`10`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/production-evidence-validation` | `read-only` | Read the production evidence validation status alias across core runtime evidence integrity, history, parity, execution feedback, and GA stability. |
| GET | `/api/production-evidence-validation/status` | `read-only` | Read the production evidence validation status across core runtime evidence integrity, history, parity, execution feedback, and GA stability. |
| POST | `/api/production-evidence-validation/run` | `review-only-build` | Build local production evidence validation artifacts; review-only and must not write orders, mutate presets, or call a broker. |
| GET | `/api/production-evidence-validation/burn-in` | `read-only` | Read the production burn-in evidence report without enabling execution. |
| GET | `/api/production-evidence-validation/burn-in/status` | `read-only` | Read the production burn-in evidence status without enabling execution. |
| POST | `/api/production-evidence-validation/burn-in/run` | `review-only-build` | Build local burn-in evidence artifacts; review-only and must not write orders, mutate presets, or call a broker. |
| GET | `/api/production-evidence-validation/rsi-lineage-closure` | `read-only` | Read the guarded RSI lineage closure evidence without enabling execution. |
| GET | `/api/production-evidence-validation/rsi-lineage-closure/status` | `read-only` | Read the guarded RSI lineage closure status without enabling execution. |
| POST | `/api/production-evidence-validation/rsi-lineage-closure/run` | `review-only-build` | Build local guarded RSI lineage closure evidence; review-only and must not write orders, mutate presets, or call a broker. |
| GET | `/api/production-evidence-validation/telegram-text` | `read-only` | Preview production evidence Telegram text; push preview only, no command execution. |

## 更新清单

Backend route surface 变化时，按下面顺序维护：

1. 先更新 Backend route 和 Node/Python contract tests。
2. 运行 `python ../QuantGodBackend/tools/api_route_registry.py --format json` 确认 Backend route registry 已暴露新路由。
3. 再更新 `docs/contracts/api-contract.json`。
4. 运行 `python scripts/render_api_contract_markdown.py` 重新生成本文。
5. 更新 Frontend service wrapper，确保前端仍只走 `/api/*`。
6. 运行跨仓库对齐检查：

```powershell
python scripts\check_api_contract_matches_backend.py `
  --contract docs\contracts\api-contract.json `
  --backend ..\QuantGodBackend
```
