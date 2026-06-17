# USDJPY EA 策略工厂

本文档记录 `QuantGod Usdjpy Ea Strategy Design` 的落地边界。目标是在不改变现有 RSI 实盘恢复状态的前提下，把新增 USDJPY 策略先接入 shadow / dry-run 研究链路，快速累积手机端可读的模拟数据。

## 当前范围

新增三条 USDJPY shadow 策略：

- 东京箱体突破：`USDJPY_TOKYO_RANGE_BREAKOUT`
- 夜盘安全均值回归：`USDJPY_NIGHT_REVERSION_SAFE`
- H4 趋势回调：`USDJPY_H4_TREND_PULLBACK`

保留现有路线：

- `RSI_Reversal`
- `MA_Cross`
- `BB_Triple`
- `MACD_Divergence`
- `SR_Breakout`

## 安全边界

新增三条路线只写 shadow candidate ledger，不调用下单、平仓、撤单、改单，也不修改 live preset。

现有 RSI live 路线保持恢复状态；新增策略和 `MA_Cross` 等非 RSI 路线在当前 doctrine 下只能进入 shadow / tester / paper-live-sim 研究 lane，不能抢占 live eligibility，也不能通过 Dashboard、GA 或 Telegram 文案直接升级为实盘。

如果未来要让非 RSI 路线真实执行，必须另开单独执行 lane RFC，并先完成 API contract、runtime preflight、request/receipt contract、EA request reader、broker send wrapper、rollback 和 operator approval 的独立评审。

## 运行数据

EA 会把三条新路线写入：

- `QuantGod_ShadowCandidateLedger.csv`
- `QuantGod_ShadowCandidateOutcomeLedger.csv`
- Dashboard strategy diagnostic JSON

Backend 会通过 `/api/usdjpy-strategy-lab/*` 展示策略目录、候选信号、回测计划、风险检查和候选政策。

回测结果可以通过 `import-backtest` 导入本机 CSV/JSON 文件。导入结果进入 `QuantGod_USDJPYBacktestImports*.json*`，只作为研究证据，不会启动 tester 或恢复实盘。

## 今日判断

这一步不是恢复更多实盘策略，而是让 USDJPY 策略池先开始大规模模拟采样。等样本量、胜率、Profit Factor、MFE/MAE 和阻断原因稳定后，也只能决定哪条策略进入人工研究复核；真实执行仍需要未来单独 lane RFC。
