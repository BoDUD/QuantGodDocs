# Telegram 中文消息合同

QuantGod 的 Telegram 只负责把本地 Shadow / ReadOnly 证据压缩成易读的出站通知。它不是交易终端，也不能通过聊天命令触发下单、平仓、撤单、改单或参数变更。

## 固定结构

所有自动日报、GA、策略 Agent、巡检、Gateway 和 AI 观察消息必须按以下顺序生成：

```text
🟡 QuantGod · 主题
结论：一句话说明当前状态和是否需要关注
关键：最多四个关键数字或状态
原因：最多两个主要原因；没有原因时整行省略
下一步：唯一、可执行的采集或复核动作
时间：MM-DD HH:MM JST
边界：永久 Shadow｜无执行通道｜Telegram 只推送、不接收命令。
```

约束：

- 每条自动消息不超过 700 个字符，目标为 6 至 8 行。
- 结论必须在第二行；不得先堆账户、内部枚举、seed、lineage 或调试字段。
- 缺失值不补成“安全”或数字 `0`；无法确认时显示“未确认”。
- 空列表、空原因和无意义的“暂无”段落必须省略。
- 禁止使用“AI 实盘建议”“实盘车道”“建议仓位”“交易计划”“自动执行”等会暗示存在执行通道的标题或字段。
- 消息裁剪时必须完整保留最后一行安全边界。

## 状态语义

标题颜色只描述通知本身，不代表系统具有交易资格：

- `🟢`：本地只读链路正常。
- `🔵`：信息状态，例如推送主动关闭或等待首次证据。
- `🟡`：证据过期、候选被阻断、等待复核或待投递。
- `🔴`：安全配置异常、硬风控触发或投递失败。

投递状态只允许以下语义：

- 仅预览
- 已入队
- 已投递
- 已去重
- 已限频
- 失败
- 未确认

只有（`sent=true` 或 `delivery.ok=true`）且同时存在 Telegram 消息回执或真正的发送时间时，前端才能显示“已投递”。`createdAt`、`timestamp`、`processedAtIso`、普通 API 请求成功、已生成文本或已入队都不等于已发送。多条结果中只要有一条失败或未确认，整体状态必须 fail-closed，不得显示“已投递”。

## 发送与频率

- 所有 `GET .../telegram-text` 接口只生成本地预览，绝不产生外部发送。
- HTTP 外部发送必须是明确的 push-only `POST`，并在 JSON body 中同时提供 `send=true`、`dryRun=false`；query 参数 `send=1` 必须拒绝。本地 CLI 必须带显式 `--send`。两类入口都必须通过本机开关和安全检查。
- `force` 默认且通常应为 `false`；只有人工诊断重复消息去重问题时才可临时显式启用，不能由页面或定时任务暗中开启。
- 自动收集继续使用稳定去重键和 Gateway 限频；相同日报每天最多形成一个可投递事件。
- GA 和 Agent 报告应以状态变化、阻断变化或回滚为主，日常总览由每日状态消息承担。
- Telegram 命令执行开关的任何真值写法都必须 fail-closed。

## 永久边界

```text
executionLaneExists = false
telegramCommandExecutionAllowed = false
orderSendAllowed = false
closeAllowed = false
cancelAllowed = false
livePresetMutationAllowed = false
```

Telegram Bot token 和 chat ID 只保存在本机未提交配置中。Gateway ledger 只应保存投递所需的最小脱敏元数据，不保存完整 chat 对象、完整业务 payload 或 Telegram 返回的消息正文副本。
