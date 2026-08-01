# 贡献与维护规则

QuantGod 现在是四仓库体系。提交前先判断改动归属。

## 改动归属

- MQL5、Python tools、Node API、AI、Governance、ParamLab：改 `QuantGodBackend`。
- Vue 页面、service wrapper、Kline、Monaco、Ant Design：改 `QuantGodFrontend`。
- workspace、dist 同步、本地部署脚本：改 `QuantGodInfra`。
- 文档、API contract、runbook、phase 状态：改 `QuantGodDocs`。

## API 变化流程

1. Backend 新增 route 和 tests。
2. Docs 更新 `api-contract.json`。
3. Docs 渲染 `api-contract.md`。
4. Frontend 更新 service wrapper。
5. Infra 只有构建/部署方式变化时才需要改。

## 提交前检查

每个仓库都应先跑自己的 CI 命令。涉及跨仓库联动时，再运行 Infra workspace `verify` 和 `test`。
