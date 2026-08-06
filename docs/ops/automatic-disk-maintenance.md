# 本地自动磁盘维护

QuantGod 的 `com.quantgod.disk-maintenance` LaunchAgent 每小时执行一次，只清理 QuantGod 自己生成、可以重建且命中精确白名单的旧分析快照和失效状态临时文件。它不会扩大清理范围到用户下载、照片、废纸篓、浏览器缓存或其他应用数据。

## 目标

- 防止 Shadow / ReadOnly 系统长期运行时被可再生分析历史占满磁盘，并与独立的日志归档、SQLite 备份和前端回滚保留任务共同控制容量；
- 保留最新运行证据、当前数据库和可恢复的前端版本；
- 在容量压力仍然存在时明确报警，而不是偷偷删除白名单之外的数据；
- 保持 `orderSendAllowed=false`、`mt5MutationAllowed=false`，不改变账号、EA、preset 或订单状态。

## 压力分级与滞回

默认策略：

| 状态 | 空闲空间 | AI 历史保留 | 行为 |
| --- | ---: | ---: | --- |
| 正常 | `>= 20%` | 14 天且至少最新 500 份 | 清理过期的可再生历史 |
| 告警 | `>= 10%` 且 `< 20%` | 14 天且至少最新 500 份 | 继续按白名单回收并报告 WARN |
| 临界 | `< 10%` | 3 天且至少最新 100 份 | 启用压力策略，单次最多删除 2 GiB |

进入临界状态后，空闲空间达到 `12%` 才退出压力模式。这一滞回可避免磁盘在 10% 附近反复切换策略。

## 自动清理白名单

维护器只接受安装器传入并通过 canonical-path 校验的 Backend runtime、当前 MT5 Files、私有 status 和 lock 根目录。候选必须是精确白名单命名的普通文件，并且不能是符号链接或硬链接。

允许清理：

- `ai_analysis/history/` 中符合 QuantGod 时间戳命名的旧 JSON 分析快照；
- `~/.quantgod/status/` 中超过 24 小时、对应 PID 已不存在的精确临时文件。

Frontend 发布工具独立管理 `Dashboard/vue-dist.previous-*`：仅在新版本完成同步和校验后保留最近一份回滚；发布失败时保留现场并恢复当前版本。`log_archive/`、`jsonl_archive/` 以及 MT5 terminal/MQL5 日志由既有 `com.quantgod.log-maintenance` 独占管理，不属于磁盘维护器的删除面。两个小时级任务因此不会并发删除同一归档文件。

SQLite 备份也不属于磁盘维护器的删除根。现有备份任务会先验证新备份，再独立执行保留最近 3 套的策略；磁盘维护器不会绕过该验证或直接删除备份。

始终保护：

- `*.sqlite`、`*.db`、`*-wal`、`*-shm` 及当前 K 线数据；
- `QuantGod_Dashboard.json`、最新自动化报告、生产证据和 Case Memory；
- `latest.json`、`latest_v2.json` 与 AI memory；
- MQL5 Experts、EX5、Presets、Profiles、账号配置和 Wine prefix；
- `HFM_MT5_Tester_Isolated`、Git 工作树和四个源码仓库；
- 用户目录中的 Downloads、Documents、Pictures、Trash 和第三方应用缓存。

## 执行保护

- CLI 默认是 dry-run，只有 LaunchAgent 显式传入 `--execute` 才会删除候选；
- 非阻塞文件锁阻止两个维护周期并发；
- 单次删除预算默认为 2048 MiB、最多 500 个文件；
- 每个候选都重新执行 `lstat`、根目录边界和链接检查；
- 报告使用临时文件加原子替换写入，并保持私有权限；
- 白名单清理后仍低于目标时返回 `PRESSURE_REMAINS`，不得自动扩大范围。

## 状态与操作

安装本地 Shadow profile 后，服务会随登录启动并每小时运行：

```bash
python3 scripts/qg-macos-launchd.py install --profile local-shadow
```

查看服务：

```bash
python3 scripts/qg-macos-launchd.py status
launchctl print "gui/$(id -u)/com.quantgod.disk-maintenance"
```

查看最近一次审计报告：

```bash
python3 -m json.tool ~/.quantgod/status/QuantGod_DiskSpaceMaintenanceStatus.json
```

报告 schema 为 `quantgod.disk_space_maintenance.v1`，至少包含：清理前后空闲率、本轮实际应用策略的 `appliedPressureLevel`、清理后的压力层级、压力仍在时距 12% 恢复线的剩余字节、删除预算、实际删除字节、跳过原因、允许根目录和不可变安全边界。

Frontend 的“运行磁盘”卡片只展示最近维护时间、释放容量和剩余压力，不提供任何删除按钮。维护证据默认超过 2 小时会明确显示“维护状态已过期”；该提示不覆盖实时 `statfs` 磁盘判断。

若报告显示 `PRESSURE_REMAINS`，先人工检查磁盘占用。不要通过扩大自动白名单来清理个人数据；需要删除已退役的独立 MT5 prefix 或其他大目录时，应先确认没有进程、LaunchAgent 或当前配置引用，再作为一次性、明确目标的维护操作执行。
