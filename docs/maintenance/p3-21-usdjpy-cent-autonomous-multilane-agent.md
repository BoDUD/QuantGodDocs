# P3-21 维护记录：USDJPY 美分账户三车道自主 Agent

P3-21 将 QuantGod 从单一 USDJPY 自主治理门扩展为三车道自主生命周期。v2.5 在此基础上补齐 Agent 今日待办、Agent 每日复盘、下一阶段任务、字段语义硬化和美分账户快速晋级门。

```text
Live Lane              USDJPYc / RSI_Reversal / LONG / cent account
MT5 Shadow Lane        USDJPY 多策略模拟、回放、tester 和 ranking
HFM Crypto CFD Shadow Lane 品种证据扫描、Moss 回测 profile 映射和 shadow-only 研究
```

## 本阶段新增

```text
tools/autonomous_lifecycle/
tools/daily_autopilot_v2/
tools/run_daily_autopilot_v2.py
```

新增 API：

```text
GET  /api/usdjpy-strategy-lab/autonomous-agent/lifecycle
GET  /api/usdjpy-strategy-lab/autonomous-agent/lanes
GET  /api/usdjpy-strategy-lab/autonomous-agent/mt5-shadow
GET  /api/usdjpy-strategy-lab/autonomous-agent/hfm-crypto-shadow
GET  /api/usdjpy-strategy-lab/autonomous-agent/ea-repro
GET  /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2
GET  /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/status
POST /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/run
GET  /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/telegram-text
GET  /api/usdjpy-strategy-lab/daily-todo
GET  /api/usdjpy-strategy-lab/daily-todo/status
POST /api/usdjpy-strategy-lab/daily-todo/run
GET  /api/usdjpy-strategy-lab/daily-todo/telegram-text
GET  /api/usdjpy-strategy-lab/daily-review
GET  /api/usdjpy-strategy-lab/daily-review/status
POST /api/usdjpy-strategy-lab/daily-review/run
GET  /api/usdjpy-strategy-lab/daily-review/telegram-text
```

## 字段语义

旧的人工审批语义被替换为自主治理字段：

```text
patchWritable=true
liveMutationAllowed=false
executionStage=SHADOW / FAST_SHADOW / TESTER_ONLY / PAPER_LIVE_SIM / MICRO_LIVE / LIVE_LIMITED
requiresAutonomousGovernance=true
autoApplyAllowed=stage_gated
completedByAgent=true
autoAppliedByAgent=true/false
```

`patchWritable` 只表示 Agent 可以写受控 patch 文件；`liveMutationAllowed=false` 表示 Agent 不能直接修改 live preset。

自主链路只输出上面的 Agent 字段，不再暴露人工审批或旧 patch 命名语义。

## 安全边界

- Live Lane 只允许 USDJPYc / RSI_Reversal / LONG；
- MT5 Shadow Lane 可以多策略模拟，但不能直接进真钱实盘；
- HFM Crypto CFD 永远不连接钱包、不保存 broker 凭证、不下单；
- 最大 2.0 是上限，不是固定仓位；
- Agent 不修改 `.mq5` 源码；
- Agent 不写 MT5 OrderRequest；
- Telegram 只推送，不接交易命令；
- Daily Autopilot 只生成中文计划、Agent 今日待办和 Agent 每日复盘，不越权交易。
- Agent 自动回滚不可被 DeepSeek、Telegram 或前端关闭。
- Strategy JSON、GA Evolution 和独立 Telegram Gateway 只作为 `WAITING_NEXT_PHASE` 任务输出，不假装已完成。

## v2.5 下一阶段任务

Daily Autopilot 2.0 额外输出：

```text
strategyJsonTodo
gaEvolutionTodo
telegramGatewayTodo
```

这些任务由 Agent 自动生成，状态保持 `WAITING_NEXT_PHASE`，用于提醒下一阶段实现 Strategy JSON DSL、GA Evolution Engine 和独立 Telegram Gateway。它们不会改变当前交易权限，也不会让 Telegram 接收交易命令。

## 验证

```powershell
cd C:\QuantGod\QuantGodBackend

python -m unittest tests.test_autonomous_lifecycle tests.test_usdjpy_autonomous_agent -v
node --test tests\node\test_autonomous_lifecycle_guard.mjs tests\node\test_usdjpy_autonomous_agent_guard.mjs

cd C:\QuantGod\QuantGodFrontend
npm run usdjpy-evolution
npm run test:usdjpy-evolution
```
