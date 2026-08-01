# USDJPY Shadow / ReadOnly 自主 Agent

本文件保留 v2.5 “multilane” 路径，作为旧 artifact 和 API 字段的兼容说明；旧 Live Lane 设计已经退役，不能作为当前运维指引。

当前系统是 forex-only 的本地研究与观察系统。HFM 只作为外汇 broker 数据来源保留。生产 EA 已物理移除 broker mutation 原语，所有策略（包括 `USDJPYc / RSI_Reversal / LONG`）都保持 Shadow / ReadOnly：

```text
executionLaneExists=false
existingEaOwnsExecution=false
orderSendAllowed=false
livePresetMutationAllowed=false
```

## 当前两类证据视图

### Shadow Advisory

Shadow Advisory 可以生成、排序和复核以下 USDJPY 策略，但不会生成订单、仓位或执行授权：

```text
RSI_Reversal
MA_Cross
BB_Triple
MACD_Divergence
SR_Breakout
USDJPY_TOKYO_RANGE_BREAKOUT
USDJPY_NIGHT_REVERSION_SAFE
USDJPY_H4_TREND_PULLBACK
```

成功状态是 `SHADOW_ADVISORY_READY`。旧 artifact 中的 `READY_FOR_EXISTING_EA`、`MICRO_LIVE`、`LIVE_LIMITED` 和 `LIVE` 车道标签只能降级显示为历史兼容字段，不能证明 EA 有执行能力。

### MT5 Shadow / Tester

MT5 侧继续运行模拟、回放、tester、paper simulation 和 ranking。影子第一名只代表研究价值；所有 lot、stage 和 promotion 字段都只是研究估计。

美分账户标识可以用于归一化历史报表和采样统计，但不能解锁自动交易或把推荐 lot 变成 broker 参数。

## 输出文件

```text
runtime/agent/QuantGod_AutonomousLifecycle.json
runtime/agent/QuantGod_MT5ShadowStrategyRanking.json
runtime/agent/QuantGod_MT5ShadowStrategyLedger.csv
runtime/agent/QuantGod_EABuildReproducibility.json
runtime/agent/QuantGod_DailyAutopilotV2.json
```

这些文件名和 schema 可能继续包含旧 `live` / `multilane` 单词，均为兼容命名，不代表 execution lane。

## 命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime lifecycle --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime lanes --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime mt5-shadow --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime ea-repro --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime build --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime daily-todo --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime daily-review --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime telegram-text --refresh --write
```

这些命令只重建本地证据。运行前后都必须保持 Shadow preset、`ReadOnlyMode=true` 和 MT5 自动交易关闭。

## Agent 今日待办和每日复盘

Daily Autopilot 2.0 可以自动完成研究待办、生成复盘和写入受控研究 patch：

```text
dailyTodo.completedByAgent=true
dailyTodo.autoAppliedByAgent=true/false
dailyTodo.requiresAutonomousGovernance=true

dailyReview.completedByAgent=true
dailyReview.autoAppliedByAgent=true/false
dailyReview.requiresAutonomousGovernance=true

historyProductionStatus.status=PASS/WARN/MISSING
historyProductionStatus.promotionGateStatus=PASS/BLOCKED
```

`autoAppliedByAgent=true` 只表示研究 patch 已更新，不表示交易已执行。当前状态流只允许：

```text
PENDING → COMPLETED_BY_AGENT → PROMOTED_TO_SHADOW / NEEDS_MORE_DATA / ROLLBACK
```

## 硬边界

以下条件不能被 AI、前端、Telegram、preset 或兼容 artifact 改写：

- 当前没有 execution lane；
- EA 不得包含或恢复 `OrderSend`、`CTrade`、`Buy/Sell`、`PositionClose` 或 `TRADE_ACTION_*`；
- runtime 缺失、fallback 或陈旧时必须 fail closed；
- 快通道、点差、新闻或证据完整性异常时不得发布就绪建议；
- 非外汇品种不得进入活动研究链；
- Agent 不得修改 EA 源码、preset 或 broker 状态；
- Frontend 和 Telegram 只能展示、解释和推送只读证据。

## Frontend

Dashboard / Evolution 应显示：

- Shadow Advisory；
- MT5 Shadow / Tester；
- 当前研究阶段与证据质量；
- fail-closed 阻断；
- Daily Autopilot 2.0；
- Agent 今日待办和每日复盘；
- EA source / Shadow preset / input hash 对账。

不得显示“执行候选”“扩仓”“等待 EA 权限”或其他暗示当前可下单的文案。

## DeepSeek 角色

DeepSeek 只解释研究晋级、回滚、参数变化和日报，不能批准执行、取消 fail-closed 阻断、修改 preset 或提高可执行仓位；当前不存在可提高的执行仓位。
