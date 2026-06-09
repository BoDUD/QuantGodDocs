# HFM Crypto CFD Sim-To-Live Plan

## 结论

可以把 HFM 官方提供的 crypto CFD 纳入现有 QuantGod 系统，并作为后续跟单或实盘自动化的目标市场。更合适的路线不是直接接 Hyperliquid 私钥/钱包，而是复用当前 MT5/HFM 的账户、dashboard、kill switch、symbol、spread 和 execution feedback 体系。

当前实现状态：系统已经有 HFM crypto CFD shadow lane、HFM evidence kit、live readiness pipeline、dry-run review、runtime preflight、MT5 request contract、adapter review shell、adapter sandbox review bundle、disabled adapter harness、live pilot activation review、receipt reconciliation review、EA request reader review、live execution cutover review、live execution implementation spec、adapter writer review、EA request consumption review、broker order send review，以及 `QuantGod_LiveEvidenceIntake.json` 证据接入总览。它们全部保持 review-only，不会写订单请求，也不会调用 broker。

新增的 `QuantGod_LivePromotionCandidates.json` 和 `QuantGod_LivePromotionController.json` 把“模拟好就进入实盘评审”自动化：前者挑出达标 lane，后者在出现候选时自动生成 review packet、approval draft、dry-run plan 和 pipeline。它们只写本地审查 artifact，不写 MT5 request 文件。

HFM crypto CFD 候选目录按 HFM 官方 crypto USD CFD 页面扩展，不再只覆盖 BTC/ETH/SOL/XRP/DOGE/LTC。模板、MT5 symbol normalizer、contract-spec export 和 execution-spec review 现在会识别 AAVE、ADA、ALGO、APT、ATOM、AVAX、BCH、BNB、BTC、CRV、DOGE、DOT、ETC、ETH、FET、FIL、FLOW、GALA、GRT、HBAR、ICP、IMX、IOTA、LINK、LTC、NEAR、SAND、SHIB、SOL、THETA、TRX、UNI、XLM、XRP、XTZ 的 USD CFD 形态，以及 HFM 常见 `#SYMBOL`、`#SYMBOLr` 和 KATANA 的 `#BTCUSDx/#ETHUSDx/#XRPUSDx`。这只是候选目录，实盘前仍以本机 HFM MT5 导出的实际 broker symbol 和 contract spec 为准。

## 目标

1. 让 HFM 官方 crypto CFD 成为系统内的一等市场。
2. 让 Moss/策略/跟单信号先进入 shadow 与模拟审查。
3. 模拟达标后自动进入 sim-to-live 审查链，而不是直接实盘。
4. 所有真实执行都走 MT5/HFM 风控：kill switch、账户/server、symbol 映射、点差、滑点、日亏损、dry-run replay、人工审批。
5. 只保留 HFM/MT5 作为当前实盘执行路径，避免非 HFM/MT5 市场参与主交易链路。

## 当前缺口

2026-05-31 的真实 runtime 结论已经从“还在等账号数据”推进到“账号已连接，但账号/服务器未下发 crypto CFD”。MT5 快照显示账号 `186054398` 已授权，服务器是 `HFMarketsGlobal-Live12`，币种 `USC`，terminal/account/expert trade 权限为可用；只读 EA 导出的 `QuantGod_HFMCryptoSymbolSpecs.json` 证明 broker symbol 清单已经拿到。

当前 broker symbol 诊断：

- `brokerSymbolTotalAll=56`
- `brokerSymbolTotalMarketWatch=13`
- `brokerCryptoLikeCountAll=0`
- `brokerCryptoLikeCountMarketWatch=0`
- 样本都是 `ForexCent`、黄金和账户币种相关 symbol，例如 `USDJPYc`、`XAUUSDc`、`USDUSC`，没有 BTC/ETH/SOL 等 HFM crypto CFD。

因此当前 HFM crypto 状态应显示为 `WAITING_HFM_ACCOUNT_CRYPTO_CFD_SYMBOLS`，中文状态是“当前 HFM 账号未下发 Crypto CFD symbols”。这不是前端没拿到数据，也不是 MT5 没登录，而是当前 HFM 账号/服务器没有开放 crypto CFD symbol。下一步必须换用开通 HFM crypto CFD 的 HFM 账号/服务器，或提供该账号真实 MT5 crypto symbol specs。

必须补齐三类 HFM 证据：

- Broker symbol 证据：HFM MT5 的 BTC/ETH/SOL/BNB/LINK/AAVE 等官方 crypto CFD history/tick 目录，或 EA 导出的 `QuantGod_HFMCryptoSymbolSpecs.json`。
- 合约规格：`contractSize`、`tickSize`、`tickValue`、`minLot`、`lotStep`、`maxLot`。
- 模拟 profile：ROI、Sharpe、最大回撤、交易笔数、爆仓次数。

## 阶段计划

### Phase 0: HFM Crypto 证据接入

- 先确认 HFM 账号/服务器是否下发官方 crypto CFD symbols。若只读 EA 已经导出 broker symbol 清单但 `brokerCryptoLikeCountAll=0`，不要继续把页面显示成等待态，应直接阻塞为 `HFM_MT5_ACCOUNT_NO_CRYPTO_CFD_SYMBOLS`。
- 在开通 crypto CFD 的 HFM MT5 账号中显示或下载官方 crypto CFD symbols。
- 用 EA 只读导出 `QuantGod_HFMCryptoSymbolSpecs.json`，同步内嵌 `hfmCryptoSymbolSpecs` 的 `QuantGod_Dashboard.json`，或用 Python MT5 registry 导出 `mt5_symbol_registry_crypto.json`。
- 前端 HFM Crypto CFD 工作区必须在顶部显示账号可用性：MT5 账号、服务器、broker symbol 总数、Market Watch 数、crypto-like 数、样本表和下一步，不允许把“账号已连接但 crypto 为 0”伪装成加载中。
- 初始页面加载必须使用 `/api/hfm-crypto/status?view=summary&scope=secondary` 和少量关键接口先渲染 Live16 crypto 账号诊断；`standalone-exporter-bundle`、post-upgrade、filled-input-validator 等完整审查证据只能在展开技术证据或执行完整审查时再加载。
- `/api/hfm-crypto/status?view=summary` 必须返回 `operatorChecklist`，把“账号链路已通”“crypto CFD symbols 缺失”“contract specs 被锁住”“保持 review-only 禁止下单”显示成结构化状态，避免前端把已知阻断误显示为等待数据；`scope=secondary/live16` 必须解析到 HFM Live16 MT5 Files。
- `/api/live-automation/status?scope=secondary` 也必须即时继承同一 HFM crypto 账号状态：HFM lane 要带 `accountNoCryptoSymbols=true` 或 Live16 ready 状态、`accountCryptoAvailability.operatorChecklist`，并在无 crypto 时把 `HFM_MT5_ACCOUNT_NO_CRYPTO_CFD_SYMBOLS` 放在 reviewBlockers 前面，不能继续提示“去运行 exporter”。
- 运行 `tools/run_hfm_crypto_cfd.py mt5-exporter-review --write` 确认当前 MT5 安装目录里的 EA 已经包含 crypto exporter；如果显示 `WAITING_MT5_EA_EXPORTER_UPGRADE`，先运行 `tools/run_hfm_crypto_cfd.py mt5-upgrade-bundle --write` 生成人工升级包，再升级并重新加载 EA。
- 人工升级、MetaEditor 编译、重新加载 EA 后，运行 `tools/run_hfm_crypto_cfd.py mt5-post-upgrade-verify --write` 复核 installed EA、`.ex5`、dashboard specs，并在 specs 出现时自动刷新合约规格审查。
- 日常复跑可以改用 `tools/run_hfm_crypto_cfd.py post-upgrade-controller --write`。它会串联 exporter review、manual bundle、post-upgrade verify、contract-spec export 和 execution-spec review；只写本地审查文件，不复制 MT5 文件、不编译、不改 preset、不下单。
- 运行 `tools/run_hfm_crypto_cfd.py evidence-kit --write` 生成模板。
- 运行 `tools/run_hfm_crypto_cfd.py evidence-bootstrap --write` 生成 `.draft.json` 草稿、filled 校验摘要和 sim-to-live 当前阻塞；草稿不会自动当成真实 filled 输入。
- 运行 `tools/run_live_automation_readiness.py evidence-intake --write --refresh-sources` 查看缺口。

### Phase 1: 合约规格审查

- 将 EA/registry 规格转成 `QuantGod_HFMCryptoContractSpecExport.json`。
- 导入 `execution-spec` 审查，确认 tick/lot/contract size 全部有效。
- 不允许用静态候选名代替 broker 证据，必须来自本机 HFM MT5 或人工确认的官方规格。
- `QuantGod_HFMCryptoCfdState.json` 的 symbol evidence 是多源判定：本机 MT5 Bases、EA/registry contract-spec export、通过的 execution-spec review 都可以证明 broker symbol 已出现。这样人工/EA specs 先到时，不会再被缺少 history/tick 目录误卡。
- 人工补齐文件优先于旧的空 export：`hfm_crypto_contract_specs.filled.json` 会覆盖空的 `QuantGod_HFMCryptoContractSpecExport.json`，`hfm_crypto_simulation_profile.filled.json` 会在没有显式 profile 参数时自动进入 evidence intake / promotion candidates。
- 使用人工补齐文件，或已经生成 `QuantGod_HFMCryptoContractSpecExport.json` / `QuantGod_HFMCryptoSimulationProfileReview.json` 时，先运行 `tools/run_hfm_crypto_cfd.py filled-input-validator --write`。它会写 `QuantGod_HFMCryptoFilledInputValidator.json`，独立检查合约规格字段和模拟 profile 门槛是否都能进入实盘评审链；人工 `.filled.json` 优先，缺少人工文件时可接受通过的自动 review artifact。
- `tools/run_hfm_crypto_cfd.py simulation-profile --write` 不传路径时会自动寻找 `hfm_crypto_simulation_profile.filled.json`、`QuantGod_HFMCryptoMossBacktestProfile.json`、`runtime/moss_backtest.json` 等本地 profile，并在 artifact 中写入 `sourceSelection` 与 `autoProfileCandidates`。
- 自动发现且过线的 simulation-profile review 会回填到 `QuantGod_HFMCryptoCfdState.json.mossBacktestProfile`，确保 promotion candidates 与 review packet 能看到同一份 agentId、ROI、Sharpe、回撤、交易数和爆仓证据。
- `QuantGod_HFMCryptoEvidenceBootstrap.json` 只负责生成 `hfm_crypto_contract_specs.draft.json`、`hfm_crypto_simulation_profile.draft.json` 和 `operator_approval.draft.json`。确认真实数据后，需要另存为 `.filled.json` 再跑校验。

### Phase 3: 模拟与跟单信号审查

- Moss 或本地模拟 profile 必须包含 ROI、Sharpe、最大回撤、交易笔数、爆仓次数。
- 只有 profile 过线，HFM crypto lane 才能成为 review candidate。
- 跟单信号先进入 shadow mapping：比例、max notional、止损、价差保护都保持审查字段，不直接执行。

### Phase 4: Sim-To-Live 审查链

- 自动生成 review packet、approval draft、dry-run plan、execution lane spec、dry-run replay、runtime preflight、MT5 request contract。
- 当前 pipeline 只推进到“可评审”边界，不会生成 MT5 request 文件。
- Runtime preflight 必须从新鲜 `QuantGod_Dashboard.json` 看到 `livePilotMode=true`、`readOnlyMode=false`、`executionEnabled=true` 和 `tradeAllowed=true`；shadow/read-only dashboard 即使 symbol、价差和 kill switch 都正常，也不能进入 live pilot 预检通过态。
- 人工审批证据即使通过，也只允许进入下一层代码评审，不直接开实盘。

### Phase 5: 单独执行 adapter 评审

- 另开一个隔离 PR/分支设计 MT5 execution adapter。
- Adapter 必须只接收已经审查过的 request contract，输出 receipt，支持幂等、防重复、原子写、回滚。
- 当前可先生成 `QuantGod_AdapterSandboxReviewBundle.json`，用样例 request、receipt、hash 和 validation rows 审查序列化逻辑，但仍不写 MT5 Files 请求目录。
- `QuantGod_ExecutionAdapterHarness.json` 会在总控与合同验证都通过后生成禁用态写入计划：未来 request/receipt 路径、原子写临时文件、幂等 hash 和 review-only 回执；它仍不写任何 MT5 Files。
- `QuantGod_LivePilotActivationReview.json` 会在总控、runtime preflight、审批证据、合同验证和 disabled harness 都通过后，汇总 live pilot 激活评审清单与部署 runbook；它仍只说明下一步应该单独评审真实 adapter / EA request reader / rollback 机制，不会打开实盘执行。
- `QuantGod_ReceiptReconciliationReview.json` 会把 review-only receipts 与 planned request 逐一对账，并列出缺 receipt、孤儿 receipt、review-only 阶段出现 ticket 等情况的自动暂停规则；它仍不写 receipt 文件、不修改自动暂停状态、不调用 broker。
- `QuantGod_EARequestReaderReview.json` 会检查 EA 源码是否显式包含 request reader 安全标记：默认关闭、schema 校验、requestId 幂等、kill switch、receipt writer、真实下单另审。仓库 EA 已经包含默认关闭的 review harness，会在 dashboard 中输出 `eaRequestReaderReview` 并写 `QuantGod_EARequestReaderReviewStatus.json`；review artifact 现在也会验证这份运行时状态仍是 `effectiveEnabled=false`、没有读取 request、没有写 receipt、没有 broker 调用，缺这份 MT5 运行时证据就不会进入 EA 实现评审。
- `QuantGod_LiveExecutionCutoverReview.json` 会把总控、live pilot 激活、receipt 对账、EA request reader、runtime preflight、人工审批、request contract 和 disabled harness 汇总成最终切换前审查包。它只说明是否可以开启一个单独 live execution cutover 实现 PR，仍不写 request/receipt、不读取 request、不调用 broker。
- `QuantGod_LiveExecutionImplementationSpec.json` 会把 cutover 后的真实实现拆成五个独立评审合同：adapter request writer、EA request reader consumption、broker order send、receipt reconciliation、rollback/auto-disable。它只写实现规格审查包，不会写 request/receipt、不读取 request、不调用 broker。
- `QuantGod_LiveExecutionAdapterWriteReview.json` 会落地第一块 `live_execution_adapter_write_path` 的审查合同：稳定 request JSON 序列化、幂等 hash、temp/final 文件名、原子写计划和目录隔离。它只把 payload 嵌进审查包，不写 MT5 request 文件。
- `QuantGod_EARequestConsumptionReview.json` 会落地第二块 `ea_request_reader_consumption_path` 的审查合同：把 adapter writer 的 request/receipt 路径计划，与 EA reader contract 和运行时 disabled status 对齐，并生成 reject-only consumption plan。它不读取 request 文件、不消费 request、不写 receipt、不下单。
- `QuantGod_BrokerOrderSendReview.json` 会落地第三块 `broker_order_send_path` 的审查合同：未来 broker wrapper 必须只从已验收 EA consumption 路径进入，并绑定账户/server、symbol、lot、spread/slippage、daily loss、request hash 和 receipt obligation。它不调用 broker、不写 request、不写 receipt、不下单。
- 上线前必须通过 fresh dashboard、kill switch、spread、daily loss、symbol mapping、dry-run replay 和 operator approval hash。
- 这一阶段才讨论真实 request 文件和 EA 执行，不和当前 evidence intake 混在一起。

## 验收标准

- 当 HFM 账号已授权但 crypto-like symbol 为 0 时，`/api/hfm-crypto/status` 必须返回 `WAITING_HFM_ACCOUNT_CRYPTO_CFD_SYMBOLS`，并包含 `symbolEvidence.brokerSymbolDiagnostics` 的 broker symbol 总数、Market Watch 数、crypto-like 数和样本。
- `/api/hfm-crypto/status?view=summary&scope=secondary` 必须保留 Live16 账号诊断、`operatorChecklist` 和安全字段，同时省略完整 review bundle；2026-05-31 已实测 Live16 返回 `READY_FOR_SHADOW_RESEARCH`、broker symbols 346、crypto-like 39。
- 前端 HFM Crypto CFD 工作区必须显示“账号可用性 / HFM Crypto CFD 探测结果”，并在账号无 crypto CFD 时明确显示“账号已连接，但未下发 HFM crypto CFD symbol”，不能只显示等待数据。
- 前端 HFM Crypto CFD 的“实盘准入”面板必须继承 live-readiness 中的账号阻断，显示“当前 HFM 账号未下发 Crypto CFD symbols”，不能降级成“继续补证据”。
- HFM crypto symbol/spec/profile 三项证据全部 present。
- `QuantGod_LiveEvidenceIntake.json` 显示 HFM review inputs present。
- `QuantGod_SimToLiveAutomationPipeline.json` 至少推进到 runtime preflight 或 request contract review。
- `QuantGod_ExecutionAdapterReview.json` 显示可进入 adapter code review。
- `QuantGod_AdapterSandboxReviewBundle.json` 在 contract ready 后显示 `READY_FOR_ADAPTER_SANDBOX_REVIEW`，并且所有 validation rows 通过。
- `QuantGod_AdapterContractValidator.json` 在 request contract 和 sandbox 样本可用后显示 `READY_FOR_ADAPTER_CONTRACT_VALIDATION_REVIEW`，并且只生成 review-only receipts。
- `QuantGod_LivePromotionController.json` 在有候选时显示 `OPERATOR_REVIEW_PACKET_AUTOMATED`，并只写 review artifacts。
- `QuantGod_SimToLiveOrchestrator.json` 显示当前总控阶段；adapter 侧 review-only stage 通过时显示 `READY_FOR_EXECUTION_ADAPTER_IMPLEMENTATION_REVIEW`，同时还会列出 `liveExecutionStages`：disabled adapter harness、live pilot activation、receipt reconciliation、EA request reader runtime review。只有这些后半段也通过时才显示 `READY_FOR_LIVE_EXECUTION_IMPLEMENTATION_REVIEW`，这仍然只是进入单独 live execution 实现评审，不是开实盘。
- `QuantGod_ExecutionAdapterHarness.json` 在总控和合同验证都通过后显示 `READY_FOR_DISABLED_ADAPTER_IMPLEMENTATION_HARNESS_REVIEW`，并且 `wouldWriteRequestFile`、`requestFilesWritten`、`brokerCallsMade`、`adapterExecutionAllowed` 都保持 false。
- `QuantGod_LivePilotActivationReview.json` 在 disabled harness、orchestrator、preflight、审批证据和 validator 都通过后显示 `READY_FOR_LIVE_PILOT_ACTIVATION_REVIEW`，并且 `livePilotActivationAllowed`、`requestWritesAllowed`、`requestFilesWritten`、`brokerCallsMade`、`adapterExecutionAllowed` 都保持 false。
- `QuantGod_ReceiptReconciliationReview.json` 在 review-only receipts 与 planned requests 全部匹配后显示 `READY_FOR_RECEIPT_RECONCILIATION_REVIEW`，并且 `receiptWritesAllowed`、`receiptFilesWritten`、`autoDisableMutationAllowed`、`brokerCallsMade`、`adapterExecutionAllowed` 都保持 false。
- `QuantGod_EARequestReaderReview.json` 只有在前置 activation/order-contract/receipt-reconciliation、EA 安全标记、以及 MT5 运行时 status/dashboard 禁用证据都通过后才显示 `READY_FOR_EA_REQUEST_READER_IMPLEMENTATION_REVIEW`，并且 `eaRequestReaderAllowed`、`eaRequestReaderEnabled`、`eaRequestFilesRead`、`eaRequestFilesConsumed`、`eaOrderSendAllowed` 都保持 false。
- `QuantGod_LiveExecutionCutoverReview.json` 只有在 orchestrator、activation、receipt reconciliation、EA request reader、runtime preflight、人工审批、request contract 和 disabled harness 全部通过后才显示 `READY_FOR_SEPARATE_LIVE_EXECUTION_CUTOVER_IMPLEMENTATION_REVIEW`，并且 `liveExecutionCutoverAllowed`、`requestWritesAllowed`、`receiptWritesAllowed`、`eaRequestReaderAllowed`、`eaRequestFilesRead`、`eaOrderSendAllowed`、`brokerCallsMade` 都保持 false。
- `QuantGod_LiveExecutionImplementationSpec.json` 只有在 cutover review ready 后才显示 `READY_FOR_LIVE_EXECUTION_IMPLEMENTATION_SPEC_REVIEW`，并列出 `live_execution_adapter_write_path`、`ea_request_reader_consumption_path`、`broker_order_send_path`、`receipt_writer_and_reconciliation_path`、`rollback_and_auto_disable_path` 五个后续 PR 的验收条件；所有执行开关仍保持 false。
- `QuantGod_LiveExecutionAdapterWriteReview.json` 只有在 implementation spec、disabled harness、adapter contract validator 和 request 样本全部通过后才显示 `READY_FOR_LIVE_EXECUTION_ADAPTER_WRITE_REVIEW`；每行 write plan 都必须保持 `allowedToWriteLiveRequest=false`、`wouldWriteToMt5RequestDirectory=false`、`requestFilesWritten=false`、`brokerCallsMade=false`。
- `QuantGod_EARequestConsumptionReview.json` 只有在 implementation spec、adapter writer review、EA request reader review、runtime disabled status、request/receipt 目录对账全部通过后才显示 `READY_FOR_EA_REQUEST_CONSUMPTION_REVIEW`；每行 consumption plan 都必须保持 `wouldReadRequestFile=false`、`wouldConsumeRequestFile=false`、`wouldWriteReceiptFile=false`、`receiptFilesWritten=false`、`brokerCallsMade=false`。
- `QuantGod_BrokerOrderSendReview.json` 只有在 implementation spec、EA request consumption、runtime preflight、MT5 request contract 和 adapter writer review 全部通过后才显示 `READY_FOR_BROKER_ORDER_SEND_REVIEW`；每行 broker send plan 都必须保持 `wouldCallBroker=false`、`brokerCallsMade=false`、`orderSendAllowed=false`、`mt5OrderSendAllowed=false`、`requestFilesWritten=false`、`receiptFilesWritten=false`。
- `QuantGod_HFMCryptoPostUpgradeController.json` 在 EA 升级和 specs 出现后显示 `HFM_CRYPTO_POST_UPGRADE_REVIEW_AUTOMATED`，并且所有执行 flag 仍为 false。
- `QuantGod_HFMCryptoEvidenceBootstrap.json` 显示当前 draft/filled 状态和总控阶段；它不能让空模板进入 evidence intake。
- `QuantGod_HFMCryptoFilledInputValidator.json` 在 specs/profile 输入都有效时显示 `FILLED_HFM_INPUTS_READY_FOR_REVIEW_CHAIN`；输入可以来自人工 `.filled.json`，也可以来自 EA/MT5 contract-spec export 与 simulation-profile review artifact。它的 `orderSendAllowed`、`mt5OrderSendAllowed`、`writesMt5OrderRequest` 仍为 false。
- 所有 review-only artifact 中 `orderSendAllowed`、`mt5OrderSendAllowed`、`writesMt5OrderRequest`、`requestWritesAllowed`、`brokerCallsMade`、`livePilotActivationAllowed`、`liveExecutionCutoverAllowed`、`receiptWritesAllowed`、`autoDisableMutationAllowed`、`eaRequestReaderAllowed`、`eaRequestFilesRead`、`eaOrderSendAllowed` 保持 false，直到单独执行 adapter 和 EA request reader 审查完成。
