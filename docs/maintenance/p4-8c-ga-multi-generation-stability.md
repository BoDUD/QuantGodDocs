# P4-8C — GA Multi-generation Stability Run

## 背景

P4-6 生产证据报告已经暴露：历史数据和策略族 parity 可以通过，但 GA 多代稳定性还需要更多可观察证据。

## 验收

运行：

```powershell
python tools\run_ga_multi_generation_stability.py --runtime-dir .\runtime build --write
python tools\run_production_evidence_validation.py --runtime-dir .\runtime build --write
```

观察：

- `generationCount`
- `candidateCount`
- `eliteCount`
- `graveyardCount`
- `lineageNodeCount`
- `lineageEdgeCount`
- `stabilityGrade`
- `evidenceUsability`

## 禁止范围

- 不下单
- 不改 live preset
- 不改仓位规则
- 不接 Telegram 交易命令
- 不接 外部市场真钱
