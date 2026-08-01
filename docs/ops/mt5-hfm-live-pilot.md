# MT5 / HFM Live Pilot（历史 / 已退役）

> **Historical / Retired:** 本文件名仅为链接兼容。旧 live-pilot 操作方式已经退役，不得作为当前启动或交易 runbook。当前产品永久保持 Shadow / ReadOnly，没有 execution lane。

## 当前运行结论

HFM 仅保留外汇 broker 数据与账号只读观测角色。当前生产 EA 已物理移除 broker mutation 原语；preset、环境变量、前端按钮或 EA 输入都不能恢复下单、平仓、撤单或改单能力。

每次启动都必须满足：

```text
ShadowMode=true
ReadOnlyMode=true
AutoTrading=false
executionLaneExists=false
existingEaOwnsExecution=false
```

只允许把仓库中的精确 Shadow preset 复制到真实 MT5 terminal。任何声称使用 `FAST_WARMUP`、lot、stage 或 live-pilot 标志即可恢复执行的旧说明都已经失效。

## 启动与编译保护

- 只编译当前仓库的 Shadow EA；编译失败必须 fail closed。
- 启动器必须验证 source / preset / input / ex5 hash，不得回退到未知旧产物。
- MT5 AutoTrading 必须保持关闭。
- Dashboard 只能把账号显示为“已连接（Shadow / ReadOnly）”，不能显示“交易就绪”。
- `SHADOW_ADVISORY_READY` 只表示新鲜证据可供观察与复核。
- 旧 `READY_FOR_EXISTING_EA` 只能显示为“影子建议已就绪（旧契约）”。

## 不允许

- AI、Agent、Telegram 或 Frontend 直接或间接发单。
- 恢复 `Trade.mqh`、`CTrade`、`OrderSend`、`Buy/Sell`、`PositionClose` 或 `TRADE_ACTION_*`。
- Vibe Coding、GA 或治理结果写入可执行 preset。
- Frontend 直接写入 MT5 runtime 文件。
- 使用本文件名中的 `live-pilot` 作为存在 execution lane 的证据。

## 日常只读检查

```powershell
cd C:\QuantGod\QuantGodBackend
python tools\ci_guard.py
python tools\run_ai_analysis.py latest
python tools\run_ai_analysis_v2.py latest
python tools\run_notify.py history --limit 20
```

这些命令只检查或重建本地证据，不会重启 MT5、启用 AutoTrading 或改变 broker 状态。
