# USDJPY 自主治理 Agent

P3-20 把 USDJPY 参数提案从“等待人工复核”升级为自主研究治理门。Agent 只能在 walk-forward、tester/shadow 和证据门禁通过后写入受控研究 patch；当前没有 execution lane。

## 输出文件

```text
runtime/agent/QuantGod_AutonomousAgentState.json
runtime/agent/QuantGod_AutonomousPromotionDecision.json
runtime/agent/QuantGod_AutonomousConfigPatch.json
runtime/agent/QuantGod_AutonomousRollbackLedger.csv
```

## 当前阶段契约

```text
REJECTED
SHADOW_ONLY
TESTER_ONLY
PAPER_LIVE_SIM
ROLLBACK_PAUSED
```

旧 artifact 中的 `MICRO_LIVE` 与 `LIVE_LIMITED` 是已退役历史阶段，只能降级映射到 Shadow / ReadOnly 证据，不能恢复 broker execution。所有当前输出必须保持 `executionLaneExists=false`、`existingEaOwnsExecution=false`。

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

DeepSeek 可以解释研究晋级、回滚和参数变化；不能产生执行授权、取消回滚、把 lot 建议变成订单参数、覆盖 replay / walk-forward 评分，或放宽新闻、点差、runtime、快通道证据门禁。
