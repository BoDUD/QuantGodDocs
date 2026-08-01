# USDJPY Shadow advisory 闭环与每日自动复盘

## 目的

USDJPY Shadow advisory 闭环把“策略政策、EA 影子观察、Shadow/ReadOnly preset、运行快照”合并成一份中文运营证据。它回答三个问题：

- 当前 USDJPY 策略是否具备新鲜、可复核的影子建议证据。
- 如果没有建议，原因是行情、证据缺失、policy 阻断，还是 Shadow preset 漂移。
- 每日待办和每日复盘是否已经把 USDJPY 自动链路跑完。

## 安全边界

该闭环只写本地 evidence 和 Telegram 中文说明。当前生产 EA 已物理移除 `Trade.mqh`、`CTrade`、`Buy/Sell`、`PositionClose`、`OrderSend` 与 `TRADE_ACTION_*` broker mutation 原语；它不能下单、平仓、撤单或修改订单。`executionLaneExists=false`、`existingEaOwnsExecution=false`，preset 也不能恢复执行能力。

## 主要文件

Backend 会写入：

- `runtime/live/QuantGod_USDJPYLiveLoopStatus.json`
- `runtime/live/QuantGod_USDJPYLiveIntent.json`
- `runtime/live/QuantGod_USDJPYDailyAutopilot.json`
- `runtime/live/QuantGod_USDJPYLiveLoopLedger.csv`

这些 `live/` 路径和 schema 名是兼容文件名，不代表 live execution。每日自动任务会在 `QuantGod_DailyAutopilot.json` 中附带 `usdJpyLiveLoopSummary`，前端显示“为什么尚无影子建议”和“下一步证据动作”。主要字段是 `topAdvisoryPolicy` / `topShadowPolicy`、`advisoryRouteZh` 与 fail-closed `safety`。

## 手动验证

```bash
python tools/run_usdjpy_live_loop.py --runtime-dir ./runtime once --write
python tools/run_usdjpy_live_loop.py --runtime-dir ./runtime telegram-text --refresh
python tools/run_daily_autopilot.py --runtime-dir ./runtime --once
```

## 判断规则

- `SHADOW_ADVISORY_READY`：运行快照新鲜、策略政策可用于影子建议、preset 仍严格保持 `ShadowMode=true`、`ReadOnlyMode=true`、自动交易关闭；只表示可以继续观察与复核。
- `POLICY_BLOCKED`：证据存在但策略政策仍阻断，只保留 Shadow 观察并继续 retune/backtest。
- `POLICY_READY_PRESET_BLOCKED`：策略政策已就绪，但 Shadow/ReadOnly preset 缺失或漂移；系统 fail-closed。
- `EVIDENCE_MISSING`：运行快照或核心 evidence 缺失；系统 fail-closed。

旧 artifact 中的 `READY_FOR_EXISTING_EA` 只能在前端降级显示为“影子建议已就绪（旧契约）”，不能解释为 EA 可下单、交易 ready 或执行授权。普通 `READY` / `POLICY_READY` 也不能自动显示绿色。
