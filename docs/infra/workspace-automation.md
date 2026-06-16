# Workspace 自动化

`QuantGodInfra/scripts/qg-workspace.py` 是四仓库联动入口。

## 常用命令

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json status
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

## Test 语义

`test` 应该覆盖：

- Backend Python unittest。
- Backend Node API contract test。
- Backend `tools/ci_guard.py`。
- Frontend contract guard、unit test、build。
- Docs link/contract/unit test。

Node API contract test 不能使用 `check=False`，也不能依赖 shell glob。应由 Python 枚举 test 文件，或直接运行 `npm test`。

## Verify 语义

`verify` 应该检查：

- Backend 不含 `frontend/` 和 `cloudflare/`。
- Frontend 不含 `MQL5/`、`Dashboard/`、`tools/`。
- Infra 不含交易代码和 Vue 页面实现。
- Docs 不含 runtime 文件和执行代码。
- Docs API contract 必须用 `--strict-extra --min-endpoints 100` 匹配 Backend 实际 `/api/*` 路由。
- Backend core runtime evidence integrity 必须通过 `tools/run_runtime_evidence_integrity.py --runtime-dir ./runtime verify`。

`verify` 只做只读检查和本地证据校验；它不能写 MT5 order request/receipt、不能修改 live preset，也不能开启 broker execution。
