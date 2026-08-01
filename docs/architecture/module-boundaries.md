# 模块边界

模块边界用于决定一次改动应该进入哪个仓库，以及是否需要同步更新其他仓库。

## Backend 模块

Backend 模块包括：

- MT5 read-only bridge。
- MT5 trading bridge 和受控 action surface。
- ParamLab、Governance、Version Gate。
- AI Analysis V1 / V2。
- Vibe Coding 后端服务和 research-only backtest connector。
- Notify push-only 服务。
- Dashboard Node API route。

只要改动涉及 `/api/*` route、Python tools、MQL5、preset、runtime JSON/CSV schema，就优先属于 Backend。

## Frontend 模块

Frontend 模块包括：

- Vue App shell。
- Workspaces：AI、AI V2、Kline、Vibe Coding、Governance、ParamLab、MT5 Monitor、Research。
- Service layer：所有 runtime data 都从 `/api/*` 获取。
- UI 状态、表格、图表、编辑器和响应式布局。

Frontend 不能直接读取 Backend runtime 文件，也不能直接写入任何交易控制面。

## Infra 模块

Infra 模块包括：

- 四仓库 workspace 配置。
- 批量测试和构建命令。
- 前端 dist 同步。
- 本地部署配置。

Infra 只能编排，不决定交易策略和风控策略。

## Docs 模块

Docs 模块包括：

- 人工文档。
- 机器可读 contract。
- 安全边界说明。
- Runbook 和维护流程。

Docs 变更不能替代代码变更；如果 contract 描述和 Backend 实现不一致，必须修到一致。
