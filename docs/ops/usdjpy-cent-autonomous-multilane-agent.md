# QuantGod v2.5 三车道自主 Agent

QuantGod v2.5 的总纲是：实盘要窄，模拟要宽，升降级要快，回滚要硬。

这版把 USDJPY 美分账户主线、自主治理 Agent、MT5 多策略模拟、HFM Crypto CFD shadow-only 研究、Agent 今日待办、Agent 每日复盘和下一阶段工程任务收到同一套生命周期里。取消人工审核不等于取消风控；Agent 只能写受控 patch，不能改源码、不能改 live preset，也不能绕过硬门禁。

## 三车道

### Live Lane

实盘车道只允许：

```text
USDJPYc
RSI_Reversal
LONG
cent account
MICRO_LIVE / LIVE_LIMITED
```

禁止 USDJPY SELL 实盘、非 RSI 实盘、非 USDJPY 实盘、前端 Quick Trade、Telegram 交易命令、DeepSeek 直接批准交易。

### MT5 Shadow Lane

MT5 模拟车道继续跑多策略，至少包括：

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

这些策略可以进入 shadow、fast shadow、tester-only 和 paper live sim，但不能抢 `topLiveEligiblePolicy`。影子第一名只代表研究价值，不代表实盘资格。

### HFM Crypto CFD Shadow Lane

HFM Crypto CFD 只做本地 HFM/MT5 品种证据扫描、Moss 回测 profile 映射和 shadow-only 研究。它不连接钱包，不保存 broker 凭证，不下单、不平仓、不撤单、不改仓。

前端统一展示为“品种证据 / Moss 回测 / 安全边界”，避免误解成已经具备实盘执行能力。

## 美分账户加速

默认配置：

```text
QG_ACCOUNT_MODE=cent
QG_ACCOUNT_CURRENCY_UNIT=USC
QG_CENT_ACCOUNT_ACCELERATION=1
QG_CENT_FAST_PROMOTION=1
QG_CENT_MICRO_LIVE_MIN_SAMPLES=10
QG_AUTO_MAX_LOT=2.0
QG_CENT_MICRO_LIVE_LOT=0.05
QG_CENT_OPPORTUNITY_LOT=0.10
QG_CENT_STANDARD_LOT=0.35
```

`2.0` 是系统仓位上限，不是固定下单手数。Agent 会按阶段、风险预算和硬风控计算当前允许仓位。

## 输出文件

```text
runtime/agent/QuantGod_AutonomousLifecycle.json
runtime/agent/QuantGod_MT5ShadowStrategyRanking.json
runtime/agent/QuantGod_MT5ShadowStrategyLedger.csv
runtime/agent/QuantGod_HFMCryptoShadowLane.json
runtime/agent/QuantGod_EABuildReproducibility.json
runtime/agent/QuantGod_DailyAutopilotV2.json
```

## 命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime lifecycle --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime lanes --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime mt5-shadow --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime hfm-crypto-shadow --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime ea-repro --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime build --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime daily-todo --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime daily-review --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime telegram-text --refresh --write
```

## Agent 今日待办和每日复盘

Daily Autopilot 2.0 不再生成“等待人工回灌”的事项。它会输出：

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

`historyProductionStatus` 会同步进入 Daily Autopilot、Agent 每日复盘和 Telegram 中文摘要。若 USDJPY SQLite 历史生产状态不是 `PASS`，日报会明确说明 GA 当前只能使用 shadow/tester 研究证据，不能把候选晋级为可推广策略。

每条待办都必须标记车道：

```text
LIVE
MT5_SHADOW
HFM_CRYPTO_CFD_SHADOW
```

状态由 Agent 自动更新：

```text
PENDING → COMPLETED_BY_AGENT → PROMOTED / MICRO_LIVE / ROLLBACK
```

Agent 可以自动完成待办、生成复盘、推动 stage-gated patch 或触发回滚，但不能直接修改 live preset，不能绕过 runtime、fastlane、spread、高冲击新闻、连续亏损和日亏损硬门禁。普通新闻默认只降仓/降级，不单独阻断。

## v2.5 下一阶段任务

Daily Autopilot 2.0 会自动生成下一阶段任务，但这些任务不会被假装成已完成能力：

```text
strategyJsonTodo      Strategy JSON DSL
gaEvolutionTodo       GA population / mutation / crossover / fitness
telegramGatewayTodo   独立 Telegram Gateway
```

这些任务的状态是：

```text
status=WAITING_NEXT_PHASE
completedByAgent=false
autoAppliedByAgent=false
requiresAutonomousGovernance=true
```

它们只表示 Agent 已经把下一阶段纳入路线图。当前版本仍以 USDJPY replay、walk-forward、三车道生命周期和 Daily Autopilot 为主，不会声称 Strategy JSON、GA 或独立 Telegram Gateway 已经实现。

## 硬风控

以下条件不能被 AI、前端或 Telegram 放宽：

- 非 USDJPY；
- 非 RSI LONG 进入实盘；
- runtime 缺失、fallback 或陈旧；
- 快通道不是 `FAST` / `EA_DASHBOARD_OK`；
- 点差异常；
- 高冲击新闻窗口；
- 连续亏损达到阈值；
- 当日亏损达到阈值；
- HFM Crypto CFD 下单、平仓、撤单或改仓；
- 修改 EA 源码或 live preset。

## Frontend

前端只做 operator workbench，不做交易按钮。Dashboard / Evolution 应显示：

- Live Lane；
- MT5 Shadow Lane；
- HFM Crypto CFD Shadow Lane；
- 美分账户状态；
- 当前执行阶段；
- 自动回滚状态；
- Daily Autopilot 2.0；
- Agent 今日待办；
- Agent 每日复盘；
- EA source / preset / input hash 对账。

## DeepSeek 角色

DeepSeek 只解释晋级、回滚、参数变化和日报，不批准 live，不取消回滚，不提高 `maxLot`，不放宽 spread、runtime、fastlane 或高冲击新闻硬门禁。

## 下一阶段边界

当前已经完成的是三车道自主生命周期和 Agent 化日报闭环。完整 Strategy JSON DSL、GA population / mutation / crossover / fitness，以及独立 Telegram Gateway 属于下一阶段，不在 v2.5 里假装完成。
