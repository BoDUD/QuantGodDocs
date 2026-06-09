# QuantGod Perfect Edition 完成度对照总结

日期：2026-05-12  
对照范围：当前本地代码主线与此前《QuantGod Perfect Edition 设计书 v1.0》及后续 v2.5/v2.6 设计目标。  
代码范围：`QuantGodBackend`、`QuantGodFrontend`、`QuantGodDocs`、`QuantGodInfra`。

## 结论摘要

QuantGod 现在已经完成了“USDJPY 自进化交易 OS”的主体工程骨架：

- USDJPY-only 实盘主线已经收口。
- MT5 多策略 shadow lane 已保留并接入 Strategy JSON / EA shadow adapter。
- HFM Crypto CFD 已保持 shadow-only，只做本地品种证据和 Moss 回测 profile 映射。
- Strategy JSON、GA trace、SQLite backtest、walk-forward、Deep Parity、Execution Feedback、Case Memory、Telegram Gateway 都已经有代码主线。
- 前端已收敛到 Dashboard / MT5 / Evolution / HFM Crypto CFD 的 operator workbench。

但还不能说“Perfect Edition 全部完成”。剩余缺口主要不是大架构，而是：

- 历史数据深度与持续同步是否长期稳定 PASS。
- 所有 strategy family 的 Strategy JSON / Python Backtest / MQL5 EA parity 是否全面覆盖。
- LiveExecutionFeedback 和 Case Memory 需要更多真实执行样本。
- GA 已能评分和审计，但还需要足够数据与多代搜索来证明正 EV。
- Telegram Gateway 已可观测，但仍需继续观察真实定时投递稳定性。

## 当前仓库状态

| 仓库 | 当前观察到的主线能力 |
|---|---|
| Backend | Strategy JSON、GA、SQLite backtest、Parity、Execution Feedback、Case Memory、Telegram Gateway、Daily Autopilot、News Gate、EA contract adapter、Evidence OS |
| Frontend | Dashboard / MT5 / Evolution / HFM Crypto CFD 主工作区，GA 审计、Evidence OS、Telegram Gateway、history production、deep parity 可视化 |
| Docs | Strategy JSON、Backtest、Evidence OS、Telegram Gateway、Agent lifecycle 等维护文档 |
| Infra | Agent loop / Telegram dispatch / runtime automation 相关启动配置 |

## 已完成部分

### 1. USDJPY-only 实盘主线

状态：已完成主线收口。

已实现：

- Live Lane 只允许 `USDJPYc / RSI_Reversal / LONG` 作为第一实盘路线。
- 非 USDJPY、SELL、非 RSI 策略不得直接进入 live。
- `maxLot=2.0` 作为上限，不是固定仓位。
- 美分账户模式、micro/opportunity/standard lot 分层已经接入。

仍需观察：

- EA 真实运行中是否持续遵守 preset / Strategy JSON / Agent patch 的同一套参数。

### 2. MT5 Shadow Lane 多策略模拟

状态：已完成主体。

已实现策略族：

- `RSI_Reversal`
- `MA_Cross`
- `BB_Triple`
- `MACD_Divergence`
- `SR_Breakout`
- `USDJPY_TOKYO_RANGE_BREAKOUT`
- `USDJPY_NIGHT_REVERSION_SAFE`
- `USDJPY_H4_TREND_PULLBACK`

已实现：

- 多策略 shadow ranking。
- Strategy JSON contract adapter。
- EA shadow adapter 已扩展到 USDJPY 专用研究策略和通用策略族。
- Shadow 结果可喂给 GA / Case Memory。

剩余缺口：

- 需要继续观察真实 EA shadow ledger 是否长期稳定产出 `SHADOW_OBSERVE / SHADOW_WOULD_ENTER`。
- 需要确保每个策略族的 family-specific 参数在 Python backtest 与 MQL5 shadow adapter 中完全一致。

### 3. HFM Crypto CFD Shadow Lane

状态：shadow-only 主体完成。

已实现：

- HFM Crypto CFD 继续作为本地品种证据扫描、Moss 回测 profile 映射和 shadow-only 研究。
- 不连接真实钱包。
- 不签名、不下单、不撤单、不赎回。
- Daily Autopilot / Telegram / frontend 中已体现 shadow/quarantine 语义。

剩余缺口：

- HFM Crypto CFD symbol scan plan 仍需要持续观察，确认黄字待办不会长期滞留。
- HFM Crypto CFD profile 与 USDJPY 风险提示之间的影响仍是软参考，不是完整跨市场因子模型。

### 4. News Gate v2.5.1

状态：已完成。

已实现：

- 默认 `QG_NEWS_GATE_MODE=SOFT`。
- 普通新闻不再硬阻断，只降仓或降级。
- 高冲击新闻继续 HARD block。
- 新闻源 UNKNOWN 不阻断，只轻微降仓并记录数据质量问题。
- Replay / Daily Autopilot / Frontend / Telegram 已接入新闻门禁摘要。

未做且不应做：

- 不允许 Agent 自动关闭所有新闻保护。
- 不允许新闻逻辑绕过 runtime / fastlane / spread / loss rollback 硬门禁。

### 5. Strategy JSON 契约

状态：v1 主体完成。

已实现：

- `quantgod.strategy.v1` schema。
- Strategy JSON validator / normalizer / safety / fingerprint。
- 危险字段扫描：`OrderSend`、`CTrade`、`privateKey`、`wallet`、`eval`、`exec`、`import` 等。
- Strategy JSON 进入 GA seed、backtest、parity、EA shadow adapter。

剩余缺口：

- Strategy JSON 仍是 v1 契约，后续需要继续增强：
  - 更完整的指标表达。
  - 更严格的 family-specific 参数 schema。
  - Strategy JSON 与 EA input/preset 的版本映射。

### 6. USDJPY SQLite Backtest Engine

状态：核心实现已完成，生产数据深度仍需持续确认。

已实现：

- `runtime/backtest/usdjpy.sqlite` 方向的 SQLite backtest engine。
- K线 store、history sync、cost model、historical news、indicators、strategy runner、metrics、quality、walk-forward。
- 支持 GA seed 的 PF、胜率、maxDD、Sharpe、Sortino、tradeCount 等指标。
- MQL5 CopyRates exporter fallback 已用于绕开 macOS MetaTrader5 Python wheel 限制。

剩余缺口：

- 需要确认 M1/M5/M15/H1 的 6-12 个月数据持续补满并保持 PASS。
- `historyProductionStatus` 需要长期保持 PASS，否则 GA 应继续降权或阻断晋级。
- 高保真回测仍需继续验证与 MT5 Strategy Tester / EA 诊断的一致性。

### 7. GA Evolution Engine

状态：从 trace 升级到可评分 GA，仍未达到“证明正 EV”的最终状态。

已实现：

- Strategy JSON seed。
- population / mutation / crossover。
- fitness。
- generation runner。
- trace writer。
- blocker explainer。
- lineage / elite path。
- GA candidate table/detail/equity/lineage 可视化。
- per-seed backtest metrics。
- per-seed train / validation / forward walk-forward 评分。
- fitness 纳入 PF、胜率、maxDD、Sharpe、Sortino、tradeCount、parity、execution feedback penalty。

剩余缺口：

- 需要更多历史深度和更多代数验证，才能说“科学找正 EV”已经成熟。
- 需要确认没有 elite 时自动扩大搜索空间的行为长期有效。
- 需要继续扩展 strategy family 参数空间和 mutation hint 质量。

### 8. Deep Parity / Evidence OS

状态：核心框架完成。

已实现：

- Strategy JSON / Python Replay / MQL5 EA deep parity。
- parity vector。
- Python replay report。
- MQL5 diagnostics adapter。
- MT5 / Evolution 首屏可显示 deepParity 与 evidenceSync。
- Evidence OS 汇总 parity、execution feedback、case memory、telegram gateway。

剩余缺口：

- 所有 strategy family 的完整 parity 覆盖仍需扩展。
- 需要继续观察 live runtime 中是否长期维持“三方口径一致 / 证据已同步”。

### 9. Live Execution Feedback

状态：字段契约与同步链路已实现，真实样本量仍需积累。

已实现字段方向：

- `policyId`
- `intentId`
- entry/fill/exit 时间
- fill price / expected price
- slippage pips
- latency ms
- reject reason
- exit reason
- profitR
- MFE / MAE

已实现：

- Backend reader/report。
- Field completeness。
- MT5 首屏显示 EA 字段契约。
- PASS / WARN / BLOCKED 语义。

剩余缺口：

- 需要真实 EA 长时间输出不同事件类型后确认字段不缺。
- Case Memory / GA 对真实 execution quality 的利用仍依赖更多真实事件。

### 10. Case Memory

状态：框架完成，真实经验库仍需扩大。

已实现：

- Case builder / candidate builder / report。
- 支持 missed opportunity、early exit、bad entry、spread damage、news damage、execution slippage、GA overfit 等方向。
- Case 可转 GA seed hint。
- Frontend / Evidence OS 可显示最大 case 与下一代 GA 修复方向。

剩余缺口：

- 需要更多真实交易与 shadow evaluation 样本。
- Case → GA seed 的质量需要持续观察。

### 11. Daily Autopilot / Agent Lifecycle

状态：v2.5 Agent 自主日报/待办主线完成。

已实现：

- 三车道状态汇总。
- Agent Daily Todo。
- Daily Review。
- 自动升降级/回滚摘要。
- GA / history production / Telegram Gateway / HFM Crypto CFD symbol scan 状态接入。
- 不再以人工审批作为主流程。

剩余缺口：

- Daily Autopilot 是否每天稳定定时跑，需要继续观察调度周期。
- HFM Crypto CFD symbol scan 的 WARN 语义已经收口过，但仍需确认不再长期滞留。

### 12. Telegram Gateway

状态：push-only gateway 与可观测性已完成，仍需长期投递观察。

已实现：

- Gateway status。
- Delivery ledger。
- Dedupe / suppress 语义。
- 最近真实发送 / 最近抑制。
- Dashboard 健康卡。
- Daily / GA / rollback / HFM Crypto CFD symbol scan 等 topic 可进入统一投递链路。

剩余缺口：

- 需要继续观察 1-2 个以上真实调度周期，确认 `最近真实发送` 稳定更新。
- 目前仍是 push-only，不接收 Telegram 交易命令。这是正确边界，不是缺口。

### 13. Frontend Operator Workbench

状态：主导航收口基本完成，仍有旧 workspace 源码残留。

已完成：

- 主工作区聚焦：
  - Dashboard
  - MT5
  - Evolution
  - HFM Crypto CFD
- MT5 首屏显示：
  - Live Loop
  - RSI diagnostics
  - Evidence OS
  - field completeness
  - deepParity
  - execution feedback
- Evolution 显示：
  - GA candidates
  - lineage
  - backtest metrics
  - Strategy JSON / parity / case memory
- HFM Crypto CFD 文案已向 shadow-only / 品种证据靠拢。

剩余缺口：

- 源码里仍存在旧 workspace：
  - phase1/phase2/phase3
  - governance
  - paramlab
  - research
  - backtest-ai
- 如果这些已经不再服务主线，应继续 archive 或从 registry 中彻底隐藏。
- Evolution 页面仍可继续做中文化和视觉压缩优化。

## 还没有完全完成的重点清单

### P0：影响“科学找正 EV”的核心缺口

1. USDJPY SQLite 历史数据生产级深度  
   代码已实现，但需要持续证明 M1/M5/M15/H1 至少 6-12 个月数据完整、增量同步稳定、`historyProductionStatus=PASS`。

2. 全策略 family 的高保真 parity  
   RSI 与主路径较完整，其他 family 需要继续确保 Strategy JSON / Python Backtest / MQL5 EA shadow adapter 完全一致。

3. 真实 LiveExecutionFeedback 样本量  
   字段契约已 PASS，但 Case Memory / GA 需要更多真实 fill、reject、slippage、latency、exit quality 样本。

4. GA 正 EV 证明  
   GA 已有 backtest/walk-forward/fitness/lineage，但还需要更多历史数据、更多 seed、多代进化和样本外稳定性，才能证明可持续正 EV。

### P1：闭环质量缺口

1. Case Memory → GA seed hint 的长期有效性。
2. Daily Autopilot 定时调度稳定性。
3. Telegram Gateway 真实发送长期稳定性。
4. HFM Crypto CFD symbol scan plan 不再长期黄字滞留。
5. EA build / ex5 / preset hash 与 GitHub commit 的长期对账。

### P2：前端与文档收口

1. 旧页面源码/路由残留清理。
2. Evolution 页面中文化、布局美化、信息密度优化。
3. K线图固定 USDJPY 并合理归入 MT5。
4. README / docs 继续统一成专业产品文档，避免旧阶段描述混杂。

## 明确不应该完成的内容

这些不是遗漏，而是安全边界：

- GA 不能直接进入 live。
- Strategy JSON 不能包含任意代码。
- HFM Crypto CFD 不保存 broker 凭证、不下单。
- Telegram 不接交易命令。
- Frontend 不提供交易按钮。
- DeepSeek 不批准 live、不取消回滚、不提高 maxLot。
- 非 USDJPY 不进入 live。
- USDJPY SELL 和非 RSI 策略不进入第一实盘路线。

## 建议下一步

建议先继续做 P0 的生产验证，而不是继续扩新功能：

1. 让 `historyProductionStatus` 长期保持 PASS。  
   目标：确认 USDJPY SQLite 历史数据深度、同步、质量都稳定。

2. 对所有 strategy family 跑一轮 batch parity。  
   目标：输出每个 family 的 Strategy JSON / Python Backtest / MQL5 EA parity 状态。

3. 继续收集真实 LiveExecutionFeedback。  
   目标：让 Case Memory 和 GA fitness 从“框架正确”进入“真实执行质量驱动”。

4. 连续跑多代 GA。  
   目标：验证 per-seed walk-forward 是否能筛掉 train 好但 validation/forward 差的 seed，并观察是否开始出现稳定 elite。

## 完成度判断

| 模块 | 当前完成度 |
|---|---:|
| USDJPY Live Lane 安全主线 | 85% |
| MT5 Shadow Lane 多策略 | 80% |
| HFM Crypto CFD Shadow Lane | 75% |
| Strategy JSON 契约 | 70% |
| USDJPY SQLite Backtest | 70% |
| GA Evolution Engine | 65% |
| Deep Parity / Evidence OS | 75% |
| LiveExecutionFeedback | 70% |
| Case Memory | 60% |
| Daily Autopilot | 75% |
| Telegram Gateway | 70% |
| Frontend Operator Workbench | 70% |

总体判断：

```text
QuantGod 已经完成自进化交易 OS 的主体工程骨架。
距离 Perfect Edition 还差的是生产级数据深度、全策略一致性、真实执行样本和长期自动调度稳定性。
```
