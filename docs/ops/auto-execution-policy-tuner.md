# P3-11 Shadow Advisory 调参器（兼容旧 AutoExecution 文件名）

## 目标

P3-11 用来解决两个研究问题：

1. Shadow 信号过严，导致候选长期不足、无法评估错失机会。
2. 模拟出场太早，导致回放无法验证更长持有窗口。

这一步不会下单，也不会修改 MT5 preset。它只生成 Shadow / dry-run 可读取的策略政策文件；文件名中的 `AutoExecution` 是历史兼容命名：

```text
runtime/adaptive/QuantGod_AutoExecutionPolicy.json
runtime/adaptive/QuantGod_AutoExecutionPolicyLedger.csv
```

## 核心思路

原来的入场逻辑容易变成：

```text
全部条件 100% 通过才允许入场
```

这会非常安全，但也会错过很多机会。P3-11 改成三档：

| 状态 | 含义 | 研究 lot 字段 |
|---|---|---|
| 标准建议 | 核心安全和入场确认都通过 | 仅作回放与展示估计 |
| 机会建议 | 核心安全通过，但战术确认缺一项 | 仅作较低权重模拟 |
| 阻断 | 核心安全缺失或历史方向为负 | 0 |

## 不能放宽的核心安全

下面任一项失败，必须阻断：

- runtime 快照缺失或陈旧
- fallback=true
- 快通道质量降级或缺失
- 动态止盈止损计划缺失
- 历史方向明显负期望
- 自适应入场闸门包含核心阻断原因

也就是说，P3-11 不是“乱放宽”，而是允许在核心安全通过时，把 M1/M5 二次确认、bar close、回踩确认这类战术项降一级处理。

## lot 字段的当前解释

兼容 artifact 可能包含 `maxLot`、`recommendedLot` 和风险预算字段。它们只用于研究排序、回放和 UI 展示，不能成为 MT5 order 参数。研究建议由这些因素共同决定：

- 最大仓位
- 单笔风险百分比
- 入场等级
- 综合评分
- 机会入场折扣

机会建议使用较低研究权重，以便比较错失机会，同时保持 `executionLaneExists=false`。

## 出场调参

P3-11 会根据影子样本表现输出出场参数：

- 保本延后 R 值
- 移动止损启动 R 值
- 时间止损 K 线数量
- 出场模式

如果近期样本为正，会倾向于：

```text
保本延后半档，移动止损延后半档，让盈利单多跑一段
```

如果只是机会入场，则仍然更快保护本金。

## 命令

```powershell
python tools\run_auto_execution_policy.py --runtime-dir .\runtime config

python tools\run_auto_execution_policy.py --runtime-dir .\runtime build `
  --symbols USDJPYc `
  --write

python tools\run_auto_execution_policy.py --runtime-dir .\runtime plan `
  --symbol USDJPYc `
  --direction LONG

python tools\run_auto_execution_policy.py --runtime-dir .\runtime telegram-text `
  --symbols USDJPYc
```

发送中文 Telegram：

```powershell
python tools\run_auto_execution_policy.py --runtime-dir .\runtime telegram-text `
  --symbols USDJPYc `
  --send
```

## 本地配置边界

复制：

```powershell
Copy-Item .env.auto.local.example .env.auto.local
```

旧 `.env.auto.local` 键只允许影响 Shadow 建议计算。它们不能启用 AutoTrading、创建 execution lane、修改 preset 或恢复 broker mutation 原语。活动运维文档不再提供可被误当成实盘仓位配置的数值示例。

## 安全边界

P3-11 不做：

- 下单
- 平仓
- 撤单
- 修改订单 SL/TP
- 修改 live preset
- 写 MT5 OrderRequest
- 接收 Telegram 交易命令
- 开放 webhook 执行入口
- 存储密码、token、private key

EA 读取 `QuantGod_AutoExecutionPolicy.json` 时只能生成 Shadow / dry-run 证据。生产 EA 不得包含保证金下单流程、order request 或 broker send 逻辑。
