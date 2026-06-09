# USDJPY 自主治理 Agent

P3-20 把 USDJPY 参数提案从“等待人工复核”升级为“自主治理门”。取消人工审批不等于取消风控：Agent 只能在 walk-forward、tester/shadow 和硬风控通过后写入受控配置 patch。

## 输出文件

```text
runtime/agent/QuantGod_AutonomousAgentState.json
runtime/agent/QuantGod_AutonomousPromotionDecision.json
runtime/agent/QuantGod_AutonomousConfigPatch.json
runtime/agent/QuantGod_AutonomousRollbackLedger.csv
```

## 阶段

```text
REJECTED
SHADOW_ONLY
TESTER_ONLY
PAPER_LIVE_SIM
MICRO_LIVE
LIVE_LIMITED
ROLLBACK_PAUSED
```

`MICRO_LIVE` 只允许极小仓试点，`LIVE_LIMITED` 仍受最大仓位 2.0、日亏损、连续亏损、点差、新闻和快通道质量限制。

## 命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_walk_forward.py --runtime-dir .\runtime build --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime decision --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime patch --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime state --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime telegram-text --refresh
```

## 硬风控

以下条件不能被 AI 或前端放宽：

- 非 USDJPY；
- runtime 缺失、fallback 或陈旧；
- 快通道不是 `FAST` / `EA_DASHBOARD_OK`；
- 点差异常；
- 高冲击新闻窗口；
- 连续亏损达到 2 笔；
- 当日亏损达到 `-1.0R`；
- 外部市场真钱交易。

## 允许写什么

Agent 只允许写：

```text
QuantGod_AutonomousConfigPatch.json
```

它不能写 `.mq5` 源码，不能修改 live preset，不能写 MT5 OrderRequest，不能通过 Telegram 接收交易命令。

## DeepSeek 角色

DeepSeek 可以解释晋级、回滚和参数变化；不能批准 live、取消回滚、提高 `maxLot`、覆盖 replay / walk-forward 评分，或放宽新闻、点差、runtime、快通道硬门禁。
