# GA 多代稳定性证据

P4-8C 用于把 P4-6 生产证据报告里的 `GA 多代稳定性不足` 从笼统 WARN 升级为可量化指标。

## 目标

- 统计 GA 代数、候选数量、elite、graveyard、lineage 节点和边。
- 读取 GA Factory 与 GA generation trace 的现有证据。
- 输出可用于 Daily Autopilot / Frontend / Telegram 的中文建议。

## 输出

```text
runtime/production_validation/QuantGod_GAMultiGenerationStabilityReport.json
runtime/production_validation/QuantGod_GAMultiGenerationStabilityLedger.csv
```

## 安全边界

本功能只读验证，不下单、不平仓、不撤单、不修改 MT5 live preset，不写 MT5 OrderRequest，也不接收 Telegram 交易命令。

GA 候选只能进入 `SHADOW / FAST_SHADOW / TESTER_ONLY / PAPER_LIVE_SIM`，不能直接或间接创建实盘执行能力；当前 `executionLaneExists=false`。
