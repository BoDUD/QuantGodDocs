# MT5 / HFM Live Pilot 运维

QuantGod 的 MT5/HFM live pilot 应保持小资金、强约束和人工授权优先。

## 运行原则

- live lot size 必须保持低风险。
- Pilot route 不能绕过 EA 内部 guard。
- Kill Switch 状态必须在 Dashboard 中可见。
- Governance、ParamLab、Version Gate 的状态必须作为 live route 前置条件。
- 启动保护模式必须显式写在 preset 中，避免重启后误入场。

## 启动保护模式

EA 支持三种 `PilotStartupEntryGuardMode`：

| 模式 | 用途 |
|---|---|
| `H1_STRICT` | 默认严格模式，等待最小时间和下一根 H1 K 线，适合稳态 live。 |
| `FAST_WARMUP` | live pilot 快速恢复模式，等待最小分钟数和新 M1 bars，减少“刚启动等一小时”的慢进场。 |
| `BACKTEST_OFF` | 回测模式关闭启动等待，避免污染历史测试。 |

Live pilot preset 使用 `FAST_WARMUP`，Backtest preset 使用 `BACKTEST_OFF`。任何模式都不能绕过新闻、点差、session、持仓容量、kill switch 和策略政策门禁。

## 不允许

- AI 直接发单。
- Vibe Coding 策略直接进入 live preset。
- Telegram 指令触发交易。
- Frontend 直接写入 MT5 runtime 文件。

## 日常检查

```powershell
cd C:\QuantGod\QuantGodBackend
python tools\ci_guard.py
python tools\run_ai_analysis.py latest
python tools\run_ai_analysis_v2.py latest
python tools\run_notify.py history --limit 20
```
