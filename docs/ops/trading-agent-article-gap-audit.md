# Trading Agent Article Gap Audit

This page maps the Moss/Codex trading-agent article to the current QuantGod implementation.

## Summary

QuantGod now implements the safe local trading-agent foundation:

- Codex skill: done, repo-local and installed under `~/.codex/skills/quantgod-trading-agent`.
- Plain-language strategy intent: done as shadow-only Strategy JSON seed generation.
- Five-dimensional signal plan and 30+ structured parameters: done in the intent plan.
- Entry-latency diagnosis: done.
- Evolution/personality lock: done.
- Segment-style GA reflection report: done as local archive evidence.
- Cent-account opportunity sampling: done.
- Hyperliquid/Moss follow lane: done only as read-only shadow mapping, with optional local profile JSON metrics.
- 24/7-style loop: done only as safe local evidence generation.

The article's real-money wallet authorization, agent-wallet private-key custody, copy-trade execution, pair-code upload, and 24/7 live deployment are not implemented. They are intentionally blocked until a separately reviewed execution lane exists.

## Article Feature Matrix

| Article item | Current state | Evidence | Remaining action |
|---|---|---|---|
| Install a Codex trading skill | Done | `QuantGodBackend/.codex/skills/quantgod-trading-agent/SKILL.md`; installed copy at `~/.codex/skills/quantgod-trading-agent` | Keep skill guard green |
| Use plain language to define trading style | Done, safe scope | `tools/strategy_ga_factory/intent_builder.py`; `/api/strategy-ga-factory/intent-plan/build` | Expand parser only if new Strategy JSON families are needed |
| Generate structured strategy parameters | Done, safe USDJPY scope | intent plan emits `structuredParameters` with 30+ fields, locked keys, mutable families | Add more Strategy JSON families only when needed |
| Five-dimensional signal system | Done as planning layer | intent plan emits trend, momentum, mean reversion, volume, volatility weights | Execution remains mapped to QuantGod USDJPY strategy modules |
| Automatic backtest/evolution | Done for USDJPY | `tools/run_strategy_ga.py`; `tools/run_strategy_ga_factory.py`; personality-lock audit | Pipeline remains shadow/tester/paper-live-sim only |
| Segment-by-segment reflection | Done as factory reflection archive | `runtime/ga_factory/QuantGod_GAFactoryReflectionReport.json`; `tools/strategy_ga_factory/factory_runner.py` | Add true walk-forward segment text if deeper replay slices are introduced |
| Upload/pair with Moss platform | Not done | No pair-code endpoint or credential storage exists | Requires external Moss contract and safe credential design |
| Deploy 24/7 real-time Moss agent | Not done | No live Moss deployment writer exists | Deliberately blocked; only local loop/read-only evidence is allowed |
| Follow leaderboard agent | Read-only shadow only | `tools/hyperliquid_shadow_lane/` parses `moss.site/agent/agt...` URL and optional local profile JSON | Public API fetch can be added if Moss publishes a stable endpoint |
| Generate Hyperliquid agent wallet | Not done | Safety fields set `walletAuthorizationAllowed=false` | Deliberately blocked; private-key custody is out of scope |
| Sign Hyperliquid Agent/Builder authorization | Not done | No signing or wallet code in shadow lane | Deliberately blocked until execution lane review |
| Copy-trade execution and auto flatten | Not done | `copyTradeExecutionAllowed=false`; follow ratio and notional are zero | Deliberately blocked |
| 3% price-difference protection | Done as metadata | `tools/hyperliquid_shadow_lane/builder.py` emits `priceDiffProtectionPct=3.0` | Enforce only if a future execution lane exists |
| Natural-language management commands | Partial | CLI/API/front-end actions exist for safe lanes | No command parser for "状态/暂停/恢复/切换 Agent" because execution is blocked |
| Risk disclaimers and safety boundaries | Done | Skill, API contract, docs, tests enforce no live execution | Keep guards updated |

## Safe Next Backlog

These can be implemented without enabling live money:

1. Add more Strategy JSON families to the plain-language parser when the research universe expands.
2. Add direct Moss public API fetch only if the API is stable and requires no credentials.
3. Add deeper walk-forward segment text when replay outputs expose per-segment trade attribution.
4. Add push-only status text for local loop health if operators need periodic summaries.

## Safe 24/7 Local Loop

The safe replacement for the article's always-on live trader is a local evidence loop:

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 tools/run_automation_chain.py --runtime-dir ./runtime --symbols USDJPYc loop --interval-seconds 300
```

This keeps diagnostics and reports fresh. It does not deploy to Moss, authorize Hyperliquid, generate wallets, or send orders.

## Execution-Lane Blockers

These must not be added as normal coding tasks:

1. Wallet generation or private-key custody.
2. Hyperliquid authorization signing.
3. Real order placement, closing, canceling, or flattening.
4. Moss pair-code upload/deploy that can create live trading behavior.
5. Copy-trade execution from leaderboard signals.

Before any of these exists, QuantGod needs a separate execution-lane specification, threat model, credential store design, kill switch, audit log, replay simulator, and explicit operator approval flow.
