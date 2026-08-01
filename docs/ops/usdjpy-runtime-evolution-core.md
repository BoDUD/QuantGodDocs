# USDJPY 自学习闭环

USDJPY 自学习闭环把 MT5/EA 的运行证据整理成可复盘的数据集，再自动生成回放报告、参数候选、walk-forward 稳定性筛选和自主治理 patch。它的目标不是让 AI 裸奔改实盘，而是每天用证据回答：

- 为什么 EA 没买；
- 哪些阻断是合理的；
- 哪些机会可能被错过；
- 哪些盈利单可能被过早保护出场；
- 明天应该拿哪些参数进入 tester-only / shadow 验证。

## 输出文件

```text
runtime/datasets/usdjpy/QuantGod_USDJPYRuntimeDataset.json
runtime/datasets/usdjpy/QuantGod_USDJPYDecisionSamples.jsonl
runtime/replay/usdjpy/QuantGod_USDJPYReplayReport.json
runtime/replay/usdjpy/QuantGod_USDJPYMissedOpportunityReport.json
runtime/replay/usdjpy/QuantGod_USDJPYExitHoldReport.json
runtime/adaptive/QuantGod_USDJPYParamCandidates.json
runtime/adaptive/QuantGod_USDJPYParamTuningReport.json
runtime/adaptive/QuantGod_USDJPYLiveConfigProposal.json
runtime/replay/usdjpy/QuantGod_USDJPYWalkForwardReport.json
runtime/replay/usdjpy/QuantGod_USDJPYParameterSelection.json
runtime/agent/QuantGod_AutonomousAgentState.json
runtime/agent/QuantGod_AutonomousPromotionDecision.json
runtime/agent/QuantGod_AutonomousConfigPatch.json
runtime/agent/QuantGod_AutonomousRollbackLedger.csv
```

## P3-18 回放精度口径

P3-18 把回放从“粗略事项列表”升级为“可比较的研究证据”。核心变化：

- 主计量口径统一为 `R` 倍数，辅助口径为 `pips`；
- `USC` 金额只保留为账面参考，不再和 `MFE/MAE` 混算；
- 错失机会会尽量记录 15 / 30 / 60 / 120 分钟后验表现；
- 盈利早出会计算 `profitCaptureRatio`，判断利润捕获比例；
- 回放报告新增候选对比：`current`、`relaxed_entry_v1`、`let_profit_run_v1`。

这仍然不是完整 tick/bar 级策略优化器。如果后验路径不足，报告会明确写成：

```text
NEEDS_BAR_REPLAY
```

这类结论只能进入 replay / tester-only / shadow 验证，不能直接修改实盘 preset。

## P3-19 因果 bar/tick 回放

P3-19 新增独立的 USDJPY 因果回放模拟器。它比较：

```text
current
relaxed_entry_v1
let_profit_run_v1
```

这一步最重要的边界是：15 / 30 / 60 / 120 分钟后的后验表现只能用于评分，不能用于当时是否入场。`relaxed_entry_v1` 只放宽 RSI / 战术确认一档，不会放宽 session、spread、runtime freshness、fastlane、cooldown 或高冲击新闻。普通新闻默认只降仓/降级。

输出文件：

```text
runtime/replay/usdjpy/QuantGod_USDJPYBarReplayReport.json
runtime/replay/usdjpy/QuantGod_USDJPYEntryVariantComparison.json
runtime/replay/usdjpy/QuantGod_USDJPYExitVariantComparison.json
runtime/replay/usdjpy/QuantGod_USDJPYReplayLedger.csv
```

## 日常命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime status --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime replay --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime tune --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime proposal --write
python tools\run_usdjpy_walk_forward.py --runtime-dir .\runtime build --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime build --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime telegram-text --refresh
```

## 安全边界

这条链路只写本地研究证据和受控 Agent patch，不会下单、平仓、撤单，也不会修改 MT5 live preset。P3-20 开始取消人工审批语义，但不取消机器硬风控。所有 USDJPY 配置提案和 Agent patch 必须保持：

```text
autoApplyAllowed=stage_gated
requiresAutonomousGovernance=true
completedByAgent=true
autoAppliedByAgent=false
requiresAutonomousGovernance=true
agentMayWriteConfigPatch=true
agentMayMutateSource=false
agentMayMutateLivePreset=false
orderSendAllowed=false
```

参数候选只能通过 autonomous research gate 进入 `SHADOW_ONLY`、`TESTER_ONLY` 或 `PAPER_LIVE_SIM`。旧 artifact 中的 `MICRO_LIVE` / `LIVE_LIMITED` 是已退役阶段，必须降级解释为 Shadow / ReadOnly；`executionLaneExists=false`。

## P3-20 自主治理门

P3-20 把旧流程：

```text
replay → 参数候选 → live config proposal → legacy review queue
```

改成：

```text
replay → walk-forward → autonomous promotion gate → controlled config patch → auto rollback
```

Agent 可以自动写入 `QuantGod_AutonomousConfigPatch.json`，但不能改 `.mq5`、不能改 preset、不能写 MT5 OrderRequest、不能让 DeepSeek 产生执行授权，也不能解除 high-impact news / spread / runtime / fastlane 的 fail-closed 证据阻断。

## 前端位置

Dashboard 会显示 “USDJPY 自学习闭环” 面板。它展示数据集样本、错失机会、过早出场、参数候选、walk-forward 结果和自主治理 Agent 状态。这个面板是只读运营视图，按钮只触发证据重建和受控 patch 生成，不触发交易。

前端会额外展示“回放候选对比”和“预期影响 / 风险变化”。这些字段来自：

```text
QuantGod_USDJPYReplayReport.json
QuantGod_USDJPYParamTuningReport.json
QuantGod_USDJPYLiveConfigProposal.json
QuantGod_AutonomousAgentState.json
```
