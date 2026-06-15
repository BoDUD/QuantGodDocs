# Strategy GA Factory

P4-4 productionizes the Strategy JSON GA trace as a factory layer. It does not create a new trading strategy. It organizes existing GA candidates, Case Memory seeds, fitness results, elite selections, blocker outcomes, and lineage into stable archives.

## Flow

```text
Strategy JSON seeds
→ GA generation trace
→ fitness and blocker evidence
→ elite archive
→ strategy graveyard
→ lineage tree
→ next generation production status
```

## Runtime Outputs

```text
runtime/ga_factory/QuantGod_GAFactoryState.json
runtime/ga_factory/QuantGod_GAEliteArchive.json
runtime/ga_factory/QuantGod_GAStrategyGraveyard.json
runtime/ga_factory/QuantGod_GALineageTree.json
runtime/ga_factory/QuantGod_GAFactoryReflectionReport.json
runtime/ga_factory/QuantGod_GAFactoryLedger.csv
runtime/ga_factory/QuantGod_GAFactoryArtifactManifest.json
runtime/ga_factory/QuantGod_StrategyFactoryIntentPlan.json
runtime/hyperliquid_shadow/QuantGod_HyperliquidShadowLane.json
```

The artifact manifest is the audit index for the archive. It keeps workspace-relative paths plus sha256 hashes for the GA Factory state, elite archive, strategy graveyard, lineage tree, reflection report and ledger, so promotion reviews can compare exact files instead of trusting stale absolute paths.

The factory reads from:

```text
runtime/ga/QuantGod_GAStatus.json
runtime/ga/QuantGod_GACandidateRuns.jsonl
runtime/ga/QuantGod_GAEliteStrategies.json
runtime/ga/QuantGod_GALineage.json
```

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime status
python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime build --write
python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime intent-plan --write --prompt "USDJPY 震荡短线，多空都做，低风险，回撤超过百分之十停手"
python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime telegram-text --refresh
python3 tools/run_hyperliquid_shadow_lane.py --runtime-dir ./runtime build --write --target-agent-url "https://moss.site/agent/agt..."
python3 tools/run_hyperliquid_shadow_lane.py --runtime-dir ./runtime build --write --target-agent-url "https://moss.site/agent/agt..." --target-agent-profile-json ./runtime/moss_agent_profile.json
python3 tools/run_automation_chain.py --runtime-dir ./runtime --symbols USDJPYc loop --interval-seconds 300
```

Smoke test:

```bash
tmp="$(mktemp -d)"
python3 tools/run_strategy_ga_factory.py --runtime-dir "$tmp" sample --overwrite
python3 tools/run_strategy_ga_factory.py --runtime-dir "$tmp" build --write
python3 tools/run_strategy_ga_factory.py --runtime-dir "$tmp" telegram-text --refresh
```

## API

```text
GET  /api/strategy-ga-factory/status
POST /api/strategy-ga-factory/build
GET  /api/strategy-ga-factory/intent-plan
POST /api/strategy-ga-factory/intent-plan/build?prompt=...
GET  /api/strategy-ga-factory/hyperliquid-shadow
POST /api/strategy-ga-factory/hyperliquid-shadow/build?targetAgentUrl=...
POST /api/strategy-ga-factory/hyperliquid-shadow/build?targetAgentUrl=...&targetAgentProfileJson=...
GET  /api/strategy-ga-factory/telegram-text
```

The `/api/ga-factory/*` routes are aliases for the same factory state.

## Safety

GA Factory can only classify candidates into:

```text
SHADOW
FAST_SHADOW
TESTER_ONLY
PAPER_LIVE_SIM
```

It cannot place orders, close positions, cancel orders, modify MT5 live presets, write MT5 `OrderRequest`, receive Telegram trading commands, or connect a external wallet real-money path.

## Plain-Language Factory

`intent-plan` is the safe version of the article-style "tell Codex what trader you want" flow:

- It infers strategy family, direction, entry posture and risk profile from plain language.
- It emits a five-dimensional signal plan: trend, momentum, mean reversion, volume and volatility.
- It emits 30+ structured parameters with locked personality keys and mutable tactical families.
- It writes valid USDJPY Strategy JSON seeds only into `MT5_SHADOW`.
- It emits `lockedPersonality` and `evolutionPolicy`.
- It keeps direction bias, symbol, strategy family, lane and risk kernel locked.
- GA mutation/crossover can only mutate tactical parameters and records a personality-lock audit.
- GA Factory writes a reflection report after archive build so winners, losers, blockers and next-generation scope are visible.

This is intentionally not a live trading shortcut. The generated seeds still need GA replay, walk-forward, factory archive and separate governance before any promotion.

## Hyperliquid Shadow Lane

The Hyperliquid/Moss bridge is currently a read-only shadow lane. Given a `moss.site/agent/agt...` URL, it writes a local mapping plan with 3% price-diff protection metadata, but:

If a public Moss profile has been exported to local JSON, pass `--target-agent-profile-json`.
The lane will read ROI, max drawdown, runtime, liquidation count and trade count into the report for screening.

- does not authorize a wallet;
- does not store credentials;
- does not place, close, cancel or flatten orders;
- sets follow ratio and max notional to zero;
- requires a separate future execution-lane approval before real copy trading.

## Safe Local Loop

For 24/7-style evidence generation without order execution, run the automation chain loop:

```bash
python3 tools/run_automation_chain.py --runtime-dir ./runtime --symbols USDJPYc loop --interval-seconds 300
```

This refreshes local evidence and reports only. It does not deploy to Moss, sign Hyperliquid authorization, or write MT5 orders.
