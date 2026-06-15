# Backend 文档

Backend 是 QuantGod 的本地交易研究与受控执行仓库，负责 MT5/HFM、Node API、Python tools、MQL5 EA、ParamLab、Governance、AI 分析、Vibe Coding 后端和通知服务。

## 关键入口

- [API Contract](api-contract.md)
- [安全边界](safety-boundaries.md)
- [Runtime Evidence Integrity](../ops/runtime-evidence-integrity.md)

## Backend 维护原则

1. 新增 `/api/*` route 时，同步更新 Docs API contract。
2. 修改 runtime JSON/CSV schema 时，同步更新 Frontend service wrapper。
3. 后端 guard 只检查后端安全，不再检查 Vue 源码。
4. 任何交易相关 action surface 都必须保留 dryRun、Kill Switch、authorization lock 和 EA guard。
5. AI、Vibe Coding、Telegram 不得直接触发交易。
