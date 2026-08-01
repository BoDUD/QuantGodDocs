# 本地部署

QuantGod 当前是 local-first 架构。MT5/HFM 终端仍运行在本机，Backend Node server 提供本地 API 和 Vue dist。

## 本地链路

```text
MT5 / HFM Terminal
  -> MQL5/Files runtime JSON/CSV
  -> QuantGodBackend Dashboard server
  -> http://127.0.0.1:8080/api/*
  -> QuantGodFrontend Vue workbench
```

正式日常运行只使用 Backend `8080` 提供的已编译 Vue 产物。Vite `5173` 仅用于开发，不属于 `local-shadow` 生产 profile。

## local-shadow 安全合同

所有由 launchd 管理的本地服务必须继承以下不可放宽的合同：

```text
mode=SHADOW_READONLY
executionLaneExists=false
orderSendAllowed=false
liveExpansionAllowed=false
unattendedLiveExpansionAllowed=false
operatorApprovalRequired=true
```

安装或恢复服务前必须验证 Shadow preset hash、单实例锁和 canonical runtime。当前运行目录以 `/api/operator/overview` 返回的 `canonicalDataRoot.id` 为准；工具不得静默回退到仓库 `runtime`。

### MT5 登录身份的本地注入

仓库内的 MT5 preset 永远只保存 synthetic 登录占位符，不能直接拿来启动真实 HFM 会话。`Start_QuantGod_mac.sh` 会在启动前从已登录的 portable terminal `common.ini`（或成对提供的本机私有变量）读取账号身份，原子生成用户私有 Shadow runtime config：

- 只接受纯数字 Login 和精确的 `HFMarketsGlobal-Live12` server；
- 不复制、不保存 Password；运行配置权限固定为 `0600`；
- launchd wrapper 在启动 Wine 前，将 runtime Login 与独立的 LoginOnly 私有参考值做常量时间比较；缺失、重复、大小写漂移或 synthetic 值都 fail closed；
- repo preset、日志、状态 JSON 和 launchd 环境中都不得出现账号或密码。

更换 HFM 账号后，先在对应 portable MT5 中人工登录一次，再以 `QG_MT5_START_MODE=off` 运行 Backend 启动脚本完成私有配置 hydration，随后重新安装 `local-shadow` profile。这个流程只恢复登录身份与只读证据，不改变 `AllowLiveTrading=0`、DLL 禁用和 Shadow/ReadOnly 边界。

## 健康与就绪

```bash
curl -fsS http://127.0.0.1:8080/healthz
curl -sS http://127.0.0.1:8080/readyz
curl -fsS http://127.0.0.1:8080/api/operator/overview
```

- `/healthz` 只表示 Node 进程和事件循环仍可响应。
- `/readyz` 聚合 canonical runtime、writer、broker、账号授权、quote、market session、历史数据、自动化、生产证据和磁盘；不就绪返回 HTTP 503。
- `/api/operator/overview` 始终返回可展示的三轴状态和 reason codes，供前端诊断。
- 周末 `marketSession.state=CLOSED` 是中性休市，不等于 broker 故障；`tradingReady` 在当前架构中固定为 false。

HTTP 200、快照文件存在或账号曾经授权，都不能单独代表运营就绪。

## 历史数据恢复

安全的一次性同步命令：

```bash
cd QuantGodBackend
tools/run_mac_usdjpy_history_sync_loop.sh --once
```

同步优先使用本机 MT5 Python；macOS 未安装该模块时，从 `MQL5/Files/backtest/exported_klines` 的 CopyRates CSV 增量写入 SQLite。必需阶段失败必须返回非零；质量报告可以成功生成 `BLOCKED` 结论，但不得伪装成策略就绪。

验收：

```bash
sqlite3 "$QG_RUNTIME_DIR/backtest/usdjpy.sqlite" "PRAGMA journal_mode; PRAGMA quick_check;"
```

期望为 `wal` 和 `ok`。历史生产状态通过不等于策略通过；缺少历史新闻、成本标定或 OOS 证据时 GA 保持冻结。

## 本地备份与校验

```bash
cd QuantGodBackend
python3 tools/run_local_shadow_backup.py backup
python3 tools/run_local_shadow_backup.py verify
```

备份使用 SQLite online backup API、SHA-256 和原子目录发布，只包含 allowlist 内的数据库和运营证据，不包含凭据文件。默认目录权限为仅当前用户可读写。

默认备份仍与运行目录处于同一物理磁盘，只能作为快速恢复点。正式灾备还必须把已验证备份复制到加密的第二故障域，并定期执行恢复演练；当前工具不会自动上传到任何外部服务。

## 前端发布到 Backend

```powershell
cd C:\QuantGod\QuantGodFrontend
npm install
npm run build

cd C:\QuantGod\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

同步后 Backend 应提供：

```text
http://127.0.0.1:8080/vue/
```

## 外网暴露原则

Backend API 只能绑定本机 loopback，不提供公网反向代理、远程快照上传或交易控制面外网入口。
