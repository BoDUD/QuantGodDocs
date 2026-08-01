# P3-14 USDJPY 单品种多策略实验室

本阶段把 QuantGod 自动化主线收窄为 **只研究 USDJPYc**。

不再让 EURUSD、XAUUSD 或其他品种参与当前 USDJPY 研究评分或 Telegram 主报告。它们可以存在于 runtime 目录里，但会被标记为非研究品种并忽略。

## 目标

```text
USDJPYc 运行快照
→ USDJPY 多策略评分
→ USDJPY 专用 Shadow Advisory 政策（兼容 AutoExecution 文件名）
→ EA 干跑决策
→ 中文 Telegram / 前端策略矩阵
```

核心问题从“哪个品种能做”改为：

```text
USDJPY 当前哪种策略、哪个方向、哪个 regime 最值得运行？
```

## 输出文件

```text
runtime/adaptive/QuantGod_USDJPYStrategyScoreboard.json
runtime/adaptive/QuantGod_USDJPYStrategyScoreboard.csv
runtime/adaptive/QuantGod_USDJPYAutoExecutionPolicy.json
runtime/adaptive/QuantGod_USDJPYEADryRunDecision.json
runtime/adaptive/QuantGod_USDJPYEADryRunDecisionLedger.csv
```

## 策略状态

| 状态 | 含义 |
|---|---|
| `STANDARD_ENTRY` | 标准 Shadow 候选，核心证据和战术确认都通过 |
| `OPPORTUNITY_ENTRY` | 机会 Shadow 候选，核心证据通过、战术确认最多缺一项，仅用于较低权重模拟 |
| `BLOCKED` | 阻断，缺核心证据、方向负期望、快通道降级、运行快照陈旧等 |

## lot 字段的当前解释

兼容 artifact 中的 `maxLot` 和 `recommendedLot` 只是研究、回放与 UI 展示值，不是可执行仓位。

实际建议仓位会根据：

```text
策略评分
入场模式
风险百分比
机会入场倍率
最小手数 / 手数步进
```

计算。阻断时研究建议值永远是 `0`，其余值也不能进入 broker order。

机会入场现在额外经过 `centSamplingGate`：

- `OPPORTUNITY_ENTRY` 只允许美分口径的模拟采样；
- USD 账户对机会入场只做 `PAPER_MIRROR_ONLY`；
- 点差轻微偏宽时继续降低研究权重；
- `centSamplingGate.recommendedLotBeforeCap` 和 `recommendedLotAfterCap` 会记录限仓前后差异。

## CLI

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime sample --overwrite
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime build --write
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime dry-run --write
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime telegram-text --refresh
```

发送 Telegram：

```powershell
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime telegram-text --refresh --send
```

## API

```text
GET  /api/usdjpy-strategy-lab/status
GET  /api/usdjpy-strategy-lab/scoreboard
GET  /api/usdjpy-strategy-lab/dry-run
GET  /api/usdjpy-strategy-lab/telegram-text?refresh=1
POST /api/usdjpy-strategy-lab/run
```

这些 API 都只运行本地证据链和政策生成，不下单；`executionLaneExists=false`。

## 前端

Dashboard 新增 USDJPY 策略政策面板：

- 标准入场数量
- 机会入场数量
- 阻断数量
- 当前优先策略
- 推荐仓位
- 缺失证据
- USDJPY 多策略矩阵

## 安全边界

本阶段不做：

```text
下单
平仓
撤单
修改订单
修改 MT5 SL/TP
修改 live preset
写 MT5 OrderRequest
Telegram 交易命令
Webhook 执行入口
存储密码、token、private key
```

本阶段只做 USDJPY 单品种策略政策和 EA 干跑证据。


## EA 干跑文件

```text
tools/usdjpy_strategy_lab/QuantGodUSDJPYPolicyDryRun.mq5
```

把它复制到 MT5 的 `MQL5/Experts` 后编译挂载，它只读取 `QuantGod_USDJPYAutoExecutionPolicy.json` 并写出干跑决策，不会调用下单、平仓或改单函数。
