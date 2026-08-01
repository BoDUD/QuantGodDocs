# 四仓库拆分架构

QuantGod 已从单一混合仓库拆分为 Backend、Frontend、Infra、Docs 四个仓库。拆分目标不是简单移动目录，而是建立清晰的维护边界，让小模块改动尽量只影响一个仓库。

## 仓库关系

```text
QuantGodBackend
  提供 localhost /api/*

QuantGodFrontend
  通过 service layer 调用 /api/*
  构建 dist/

QuantGodInfra
  管理 workspace、批量 pull/test/build、同步 frontend dist

QuantGodDocs
  记录架构、API contract、运维和安全边界
```

## Backend 保留内容

Backend 负责本地交易研究与受控执行面：

- `MQL5/` EA、preset、MT5 Files runtime 边界。
- `Dashboard/` Node server、API route、`vue-dist/` 静态产物。
- `tools/` Python 工具，包括 AI、ParamLab、Governance、Vibe Coding、notify。
- `tests/` 后端测试、Node API contract 测试、safety guard。

Backend 不应该再包含 Vue 源码、基础设施源码或长篇文档中心。

## Frontend 保留内容

Frontend 只负责 Vue 工作台源码：

- `src/` Vue components、services、workspaces。
- `package.json`、Vite 配置、前端测试和 contract guard。
- UI 组件库、KlineCharts、Monaco、Ant Design Vue。

Frontend 不应该读取 `/QuantGod_*.json` 或 `/QuantGod_*.csv`，也不应该包含 `MQL5/`、`Dashboard/`、`tools/`。

## Infra 保留内容

Infra 负责四仓库联动：

- workspace 配置和 helper。
- 批量 pull/status/test/build。
- 前端 dist 同步到 Backend `Dashboard/vue-dist`。
- 本地部署与进程编排配置。

Infra 不应该包含交易策略、EA、Vue 页面实现或运行时凭据。

## Docs 保留内容

Docs 是四仓库的 contract hub：

- 架构与模块边界。
- API contract 和 safety defaults。
- Phase 1/2/3 交付状态。
- 本地 runbook、Telegram、MT5/HFM live pilot 运维说明。

Docs 不应该包含可执行交易代码、runtime 文件或任何 token/key。
