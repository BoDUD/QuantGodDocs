# USDJPY 策略实验室 API

`/api/usdjpy-strategy-lab/*` 是 USDJPY 单品种策略工厂的数据面。它只读或生成本地研究证据，不执行交易。

## 主要端点

| 端点 | 说明 |
|---|---|
| `GET /api/usdjpy-strategy-lab/status` | 当前 USDJPY 策略政策状态 |
| `POST /api/usdjpy-strategy-lab/run` | 重新生成策略政策 |
| `GET /api/usdjpy-strategy-lab/catalog` | 三条新增 shadow 策略目录 |
| `GET /api/usdjpy-strategy-lab/signals` | 最近 shadow 候选信号 |
| `POST /api/usdjpy-strategy-lab/signals/run` | 刷新候选信号 |
| `GET /api/usdjpy-strategy-lab/backtest-plan` | 新策略回测计划 |
| `POST /api/usdjpy-strategy-lab/backtest-plan/build` | 重新生成回测计划 |
| `GET /api/usdjpy-strategy-lab/imported-backtests` | 已导入的 USDJPY 回测结果 |
| `POST /api/usdjpy-strategy-lab/import-backtest` | 导入本机 CSV/JSON 回测结果，只写研究证据 |
| `GET /api/usdjpy-strategy-lab/risk-check` | 运行快照、快通道、新闻和隔离状态检查 |
| `GET /api/usdjpy-strategy-lab/evidence` | 策略评分与候选信号合并视图 |
| `GET /api/usdjpy-strategy-lab/candidate-policy` | 候选策略政策 |
| `POST /api/usdjpy-strategy-lab/candidate-policy/build` | 生成候选策略政策 |
| `GET /api/usdjpy-strategy-lab/bar-replay` | USDJPY 因果 bar/tick 回放总报告别名 |
| `GET /api/usdjpy-strategy-lab/bar-replay/status` | USDJPY 因果 bar/tick 回放总报告 |
| `POST /api/usdjpy-strategy-lab/bar-replay/build` | 重建因果回放报告和 replay ledger |
| `GET /api/usdjpy-strategy-lab/bar-replay/entry` | current vs relaxed_entry_v1 入场候选对比 |
| `GET /api/usdjpy-strategy-lab/bar-replay/exit` | current vs let_profit_run_v1 出场候选对比 |
| `GET /api/usdjpy-strategy-lab/bar-replay/telegram-text` | 因果回放中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/walk-forward/status` | USDJPY walk-forward 稳定性筛选报告 |
| `POST /api/usdjpy-strategy-lab/walk-forward/build` | 重建 walk-forward 报告、参数选择和治理提案 |
| `GET /api/usdjpy-strategy-lab/walk-forward/selection` | 读取 train / validation / forward 后的参数选择 |
| `GET /api/usdjpy-strategy-lab/walk-forward/proposal` | 读取 stage-gated live config proposal |
| `GET /api/usdjpy-strategy-lab/walk-forward/telegram-text` | walk-forward 中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/state` | USDJPY 自主治理 Agent 当前阶段和 patch 状态 |
| `POST /api/usdjpy-strategy-lab/autonomous-agent/run` | 运行自主治理门；只写受控 patch 和回滚证据 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/decision` | 读取自主晋级决策 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/patch` | 读取受控 config patch |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/lifecycle` | 读取 v2.5 三车道自主生命周期 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/lanes` | 读取 Live / MT5 Shadow / HFM Crypto CFD Shadow 三车道摘要 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/mt5-shadow` | 读取 MT5 多策略模拟车道排名 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/hfm-crypto-shadow` | 读取 HFM Crypto CFD 品种证据、Moss 回测 profile 和 shadow-only 状态 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/ea-repro` | 读取 EA source / preset / input / ex5 对账证据 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2` | 读取 Daily Autopilot 2.0 中文计划和复盘 |
| `POST /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/run` | 重建 Daily Autopilot 2.0 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/telegram-text` | Daily Autopilot 2.0 中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/daily-todo` | 读取 Agent 今日待办，含车道、状态、指标和回滚状态 |
| `GET /api/usdjpy-strategy-lab/daily-todo/status` | 读取 Agent 今日待办状态别名 |
| `POST /api/usdjpy-strategy-lab/daily-todo/run` | 由 Agent 重建并写入今日待办 |
| `GET /api/usdjpy-strategy-lab/daily-todo/telegram-text` | Agent 今日待办中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/daily-review` | 读取 Agent 每日复盘，含净 R、最大不利 R、错失机会、早出场和升降级 |
| `GET /api/usdjpy-strategy-lab/daily-review/status` | 读取 Agent 每日复盘状态别名 |
| `POST /api/usdjpy-strategy-lab/daily-review/run` | 由 Agent 重建并写入每日复盘 |
| `GET /api/usdjpy-strategy-lab/daily-review/telegram-text` | Agent 每日复盘中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/telegram-text` | 自主治理中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/strategy-backtest/status` | 读取 Strategy JSON USDJPY SQLite 回测状态和最新报告 |
| `POST /api/usdjpy-strategy-lab/strategy-backtest/sample` | 写入确定性 USDJPY H1 示例 K线到本地 SQLite，用于 smoke 和测试 |
| `POST /api/usdjpy-strategy-lab/strategy-backtest/run` | 运行 Strategy JSON 回测，输出 report、trades、equity curve 和 GA fitness evidence |
| `GET /api/usdjpy-strategy-lab/strategy-backtest/telegram-text` | Strategy JSON 回测中文 Telegram 文案 |
| `POST /api/usdjpy-strategy-lab/strategy-backtest/sync-klines` | 从 MT5 Python 或 MQL5 CopyRates CSV 增量同步 USDJPY M1/M5/M15/H1 到 SQLite |
| `GET /api/usdjpy-strategy-lab/strategy-backtest/quality` | 读取 USDJPY SQLite 回测历史覆盖、数据来源和同步质量状态 |
| `GET /api/usdjpy-strategy-lab/strategy-backtest/production-status` | 读取 USDJPY SQLite 历史数据生产验收状态，包含覆盖深度、K线密度和最新延迟 |
| `GET /api/usdjpy-strategy-lab/evidence-os` | `evidence-os/status` 的兼容别名，读取 Evidence OS 审计状态 |
| `GET /api/usdjpy-strategy-lab/evidence-os/status` | 读取 Strategy JSON / Python Replay / MQL5 EA parity、执行反馈、Case Memory 和 Telegram Gateway 状态 |
| `POST /api/usdjpy-strategy-lab/evidence-os/run` | 生成完整 USDJPY evidence OS 审计包 |
| `GET /api/usdjpy-strategy-lab/evidence-os/parity` | 重建 Strategy JSON / Python Replay / MQL5 EA parity report |
| `GET /api/usdjpy-strategy-lab/evidence-os/execution-feedback` | 重建 live execution feedback / execution quality report |
| `GET /api/usdjpy-strategy-lab/evidence-os/case-memory` | 重建 Case Memory，总结错失、早出和执行偏差 |
| `GET /api/usdjpy-strategy-lab/evidence-os/telegram-text` | 生成 evidence OS 中文 Telegram 文案，走 push-only Gateway |
| `GET /api/case-memory/status` | 读取 P4-7 Case Memory → Strategy JSON candidate / GA seed hint 状态 |
| `POST /api/case-memory/build` | 生成 shadow Strategy JSON candidate 与 GA seed hint；PARITY_FAIL 阻断 |
| `GET /api/case-memory/telegram-text` | 生成 Case Memory 策略结构候选中文 Telegram 文案 |
| `GET /api/strategy-ga-factory/status` | 读取 P4-4 Strategy JSON GA Factory 状态 |
| `POST /api/strategy-ga-factory/build` | 生成 elite archive、strategy graveyard、lineage tree、reflection report 和 factory ledger |
| `GET /api/strategy-ga-factory/intent-plan` | 读取自然语言 Strategy Factory intent plan |
| `POST /api/strategy-ga-factory/intent-plan/build?prompt=...` | 从大白话生成 shadow-only Strategy JSON seed、五维信号计划、30+ 参数和性格锁进化计划 |
| `GET /api/strategy-ga-factory/hyperliquid-shadow` | 读取 Hyperliquid/Moss 只读影子车道状态 |
| `POST /api/strategy-ga-factory/hyperliquid-shadow/build?targetAgentUrl=...&targetAgentProfileJson=...` | 写入 Moss agent 链接和可选本地 profile JSON 到只读 shadow mapping，不授权钱包、不下单 |
| `GET /api/strategy-ga-factory/telegram-text` | 生成 GA Factory 中文 Telegram 文案 |
| `GET /api/ga-factory/status` | `strategy-ga-factory/status` 的短别名 |
| `POST /api/ga-factory/build` | `strategy-ga-factory/build` 的短别名 |
| `GET /api/ga-factory/telegram-text` | `strategy-ga-factory/telegram-text` 的短别名 |
| `GET /api/telegram-gateway/status` | 读取 P4-5 Telegram Gateway 运维观测状态 |
| `POST /api/telegram-gateway/collect` | 收集日报、GA、Agent 和 HFM Crypto CFD 报告进入 push-only Gateway 队列 |
| `GET /api/telegram-gateway/telegram-text` | 生成 Telegram Gateway 运维中文预览 |
| `GET /api/usdjpy-strategy-lab/agent-ops-health` | 读取 Agent ops health 状态别名 |
| `GET /api/usdjpy-strategy-lab/agent-ops-health/status` | 读取 Agent loop、Evidence OS、Telegram Gateway 和 runtime 健康状态 |
| `GET /api/usdjpy-strategy-lab/telegram-gateway` | `telegram-gateway/status` 的兼容别名 |
| `GET /api/usdjpy-strategy-lab/telegram-gateway/status` | 读取独立 Telegram Gateway 队列、ledger、去重、限频和 push-only 状态 |
| `POST /api/usdjpy-strategy-lab/telegram-gateway/test-event` | 写入一条中文测试 NotificationEvent 到 Gateway 队列；不发送交易命令 |
| `POST /api/usdjpy-strategy-lab/telegram-gateway/dispatch` | 处理 Gateway 队列；默认只写 ledger，`send=1` 时仍要求 push allowed 且 commands disabled |

## v2.6 Strategy JSON GA 端点

`ga` 端点负责 Strategy JSON 全过程审计，不是交易执行器：

- 每一代记录 generation、candidate、fitness breakdown、blocker、elite、mutation 和 crossover；
- Case Memory 中 `QUEUED_FOR_GA` 的经验会被转换成 `CASE_MEMORY` shadow seed；
- GA 使用 Strategy JSON fingerprint 与 evidence signature 缓存 fitness，证据变化后自动失效；
- GA fitness 会读取 `historyProductionStatus`；若 USDJPY SQLite 历史生产状态不是 `PASS`，候选仍可保留研究证据，但不能晋级为可推广策略；
- Daily Autopilot / Daily Review / Telegram 中文摘要会同步输出 `historyProductionStatus`，让早晚报直接说明 GA 是否使用生产级历史样本评分；
- `QuantGod_GALineage.json` 记录 case-memory origin、mutation parent 和 crossover parents；
- `QuantGod_GARunLimiter.json` 记录最近一次 generation，部署可用 `QG_GA_MIN_RUN_INTERVAL_SECONDS` 控制频率；
- 候选只能进入 MT5 Shadow、tester-only、paper-live-sim 或 autonomous evidence；
- GA 不得直接进入 live、不得改 live preset、不得发 MT5 订单、不得打开 HFM Crypto CFD 执行授权。

## v2.8 Strategy JSON → EA 只读契约端点

`strategy-contract` 端点把最新 GA / Strategy JSON candidate 转成 MQL5 EA 可读取的只读契约：

| Endpoint | 说明 |
|---|---|
| `GET /api/usdjpy-strategy-lab/strategy-contract` | 读取 Strategy JSON → EA contract 状态兼容别名。 |
| `GET /api/usdjpy-strategy-lab/strategy-contract/status` | 读取 Strategy JSON → EA contract 状态、已选 seed、fingerprint 和 EA 回执。 |
| `POST /api/usdjpy-strategy-lab/strategy-contract/build` | 生成 `QuantGod_StrategyJsonEAContract.json` 与 `QuantGod_StrategyJsonEAContract_EA.txt`，供 EA 只读评估。 |
| `GET /api/usdjpy-strategy-lab/strategy-contract/telegram-text` | 生成中文契约摘要；可选 push-only 发送。 |

安全边界：

- contract mode 只允许 `SHADOW_EVALUATION_ONLY`、`TESTER_EVALUATION_ONLY`、`PAPER_LIVE_SIM_EVALUATION_ONLY`；
- EA 只读取 `QuantGod_StrategyJsonEAContract_EA.txt` 并回写 `QuantGod_StrategyJsonEAContractEAStatus.json`；
- 不下单、不平仓、不撤单、不写 `OrderRequest`、不修改 live preset；
- GA 产物即使表现优秀，也只能先进入 shadow/tester/paper lane，不会直接抢 `USDJPYc / RSI_Reversal / LONG` 实盘路线。

## P3-19 因果回放端点

`bar-replay` 端点必须保持因果约束：

- 后验窗口只用于评分，不能决定当时是否入场；
- `relaxed_entry_v1` 只放宽 RSI / 战术确认一档；
- session、spread、runtime freshness、fastlane、cooldown、仓位容量和高冲击新闻不能被放宽；
- 普通新闻默认是软风险：只降仓或降级，不单独阻断 USDJPY RSI LONG；
- 输出以 `R` 为主口径，`pips` 辅助，`USC` 只作账面参考。

## P3-20 自主治理端点

`walk-forward` 和 `autonomous-agent` 端点取消人工审批语义，但仍保持机器硬风控：

- `autoApplyAllowed=stage_gated`；
- `requiresAutonomousGovernance=true`；
- `completedByAgent=true` 用于 Agent 待办和复盘；
- `autoAppliedByAgent=true/false` 表示 Agent 是否自动推动受控 patch 或阶段状态；
- Agent 只能写 `QuantGod_AutonomousConfigPatch.json`；
- 连续亏损、日亏损、runtime 陈旧、快通道异常、点差异常和高冲击新闻会自动暂停或回滚；
- 普通新闻风险进入 Daily Autopilot 和 replay 复盘，但不作为常态硬阻断；
- DeepSeek 只解释，不批准 live、不取消回滚、不提高仓位上限；
- HFM Crypto CFD 永远 shadow-only。

## P3-21 三车道自主生命周期端点

`autonomous-agent/lifecycle` 系列端点把 v2.5 的三车道语义合并到同一个 operator view：

- Live Lane 只允许 `USDJPYc / RSI_Reversal / LONG` 进入 `MICRO_LIVE` 或 `LIVE_LIMITED`；
- MT5 Shadow Lane 继续跑多策略模拟、回放、tester 和 ranking；
- HFM Crypto CFD Shadow Lane 只做本地品种证据扫描、Moss 回测 profile 映射和 shadow-only 研究；
- 美分账户加速允许更快采样，但不能绕过 runtime、fastlane、spread、高冲击新闻和亏损回滚；
- `patchWritable=true` 只表示 Agent 可以写受控 patch，`liveMutationAllowed=false` 表示不能直接改 live preset；
- Daily Autopilot 2.0 生成中文早盘计划、Agent 今日待办、Agent 每日复盘和 Telegram 文案，不执行交易。
- `strategyJsonTodo`、`gaEvolutionTodo`、`telegramGatewayTodo` 是下一阶段任务，状态保持 `WAITING_NEXT_PHASE`，不会被假装成已完成能力。

## v2.6.1 Strategy JSON USDJPY 回测端点

`strategy-backtest` 端点把 Strategy JSON 从“可审计种子”推进为“可执行研究契约”：

- 只处理 `USDJPYc`；
- 读取安全的 `quantgod.strategy.v1`；
- 写入 `runtime/backtest/usdjpy.sqlite`；
- 优先用本机 MT5 Python `copy_rates_range` 增量同步；macOS 没有 `MetaTrader5` wheel 时自动读取实盘 `MQL5/Files/backtest/exported_klines` 的 CopyRates CSV；
- 每次同步写出 `QuantGod_USDJPYHistoricalKlineSyncReport.json` 与 `QuantGod_USDJPYHistoryProductionStatus.json`，要求 M1/M5/M15/H1 同时满足 6-12 个月级别覆盖、K线密度和最新延迟阈值；
- 输出 `QuantGod_StrategyBacktestReport.json`、`QuantGod_StrategyTrades.csv`、`QuantGod_StrategyEquityCurve.csv`；
- 覆盖 `RSI_Reversal`、`MA_Cross`、`BB_Triple`、`MACD_Divergence`、`SR_Breakout`、东京突破、夜盘回归和 H4 回调这些 USDJPY shadow 策略族；
- 将每个 Strategy JSON seed 独立写入 GA fitness evidence，不共用 stale latest report；
- 输出 cost model 和 parity vector，供 Evidence OS 审计；
- 把回测指标提供给 GA fitness；
- 不下单、不平仓、不撤单、不改 live preset。

当前版本是 USDJPY Strategy JSON research runner，不是 MT5 Strategy Tester 替代品；tick 级成交建模和 broker 特定滑点分布仍属于后续增强。

## Perfect Edition Evidence OS 端点

`evidence-os` 端点把 Strategy JSON 回测、Python replay、MQL5 EA 诊断、执行反馈、Case Memory 和 Telegram Gateway 串成同一份审计证据：

- `QuantGod_StrategyParityReport.json`：Strategy JSON / Python Replay / MQL5 EA parity，包含 SQLite 持久化、live-loop policy 和 EA RSI 诊断一致性检查；
- `QuantGod_LiveExecutionQualityReport.json` 和 `QuantGod_LiveExecutionFeedback.jsonl`：优先读取 EA 实时写出的 `QuantGod_LiveExecutionFeedback.jsonl` 与历史重建 `QuantGod_LiveExecutionFeedbackHistory.jsonl`，再合并 fastlane trade events、live-loop ledger、trade journal、close history 和 EA dry-run ledger，归一化成交、平仓、订单接受、拒单、滑点、延迟、profitR / MFE / MAE；
- `QuantGod_CaseMemory.jsonl` 和 summary：错失机会、早出场、新闻损伤、执行偏差、GA 过拟合风险转成 GA mutation 线索；
- `QuantGod_NotificationEventQueue.jsonl`、`QuantGod_TelegramGatewayLedger.jsonl` 和 `QuantGod_TelegramGatewayStatus.json`：独立中文 push-only Gateway，统一队列、去重、限频、投递 ledger，不接命令。

这些端点只写本地 evidence，不下单、不平仓、不撤单、不修改 live preset。

## 返回原则

返回内容必须中文优先，并明确显示：

- 新策略是否 shadow-only
- 是否允许真实下单
- 当前候选信号来自哪条路线
- 缺少哪些证据
- 下一步是回测、等待采样还是治理复核

## 禁止事项

这些端点不得：

- 下单
- 平仓
- 撤单
- 修改订单
- 修改 live preset
- 接收 Telegram 交易命令
- 写入凭据

新增策略想进入实盘，必须先通过 USDJPY 自主治理门和受控 patch 阶梯；这些 API 本身不会执行交易。
