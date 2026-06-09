# Strategy JSON USDJPY Backtest

QuantGod Perfect Edition starts by making Strategy JSON executable in a read-only research plane.

This module reads a safe `quantgod.strategy.v1` seed, runs a deterministic USDJPY Strategy JSON backtest against local SQLite bars, and writes GA-readable evidence:

```text
runtime/backtest/usdjpy.sqlite
runtime/backtest/QuantGod_StrategyBacktestReport.json
runtime/backtest/QuantGod_StrategyTrades.csv
runtime/backtest/QuantGod_StrategyEquityCurve.csv
runtime/backtest/QuantGod_USDJPYHistoricalKlineSyncReport.json
runtime/backtest/QuantGod_USDJPYHistoryProductionStatus.json
```

## What It Does

- Keeps scope fixed to `USDJPYc`.
- Validates Strategy JSON through the existing Strategy JSON validator.
- Runs every supported USDJPY MT5 shadow strategy family through the Strategy JSON runner:
  `RSI_Reversal`, `MA_Cross`, `BB_Triple`, `MACD_Divergence`, `SR_Breakout`,
  `USDJPY_TOKYO_RANGE_BREAKOUT`, `USDJPY_NIGHT_REVERSION_SAFE`, and
  `USDJPY_H4_TREND_PULLBACK`.
- Loads all available USDJPY SQLite timeframes (`M1`, `M5`, `M15`, `H1`, `H4`, `D1`) and lets the runner pick the primary execution timeframe from the Strategy JSON.
- Syncs production history from MT5 Python when available, or from real MT5 `MQL5/Files/backtest/exported_klines` CopyRates CSV exports on macOS.
- Writes a production status report that checks M1/M5/M15/H1 coverage depth, density, and latest-bar lag before GA treats the history as production-grade evidence.
- Adds `historyProductionStatus` to GA fitness; if production status is not `PASS`, GA candidates are downgraded to shadow/tester evidence and blocked from promotion.
- Applies a deterministic research cost model for spread, slippage, and commission pips.
- Produces `netR`, pips, profit factor, win rate, max drawdown R, Sharpe, Sortino, loss streak, MFE/MAE and profit capture ratio.
- Persists each run into SQLite `strategy_runs`, `strategy_trades`, and `equity_curves` tables.
- Feeds per-seed Strategy JSON backtest evidence into GA fitness, so GA candidates are not all scored against one stale latest report.
- Emits a parity vector so the Evidence OS can compare Strategy JSON, Python replay, and MQL5 EA evidence.
- Exposes read-only API endpoints under `/api/usdjpy-strategy-lab/strategy-backtest/*`.

## Safety

The backtest layer does not:

- place orders
- close positions
- cancel orders
- mutate live preset
- write MT5 order requests
- connect a external wallet
- receive Telegram trade commands

It only writes local research evidence under `runtime/backtest`.

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime sample --overwrite
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime sync-klines --months 12 --timeframes M1,M5,M15,H1
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime production-status
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime quality
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime run --write
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime status
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime telegram-text --refresh
```

## API

```text
GET  /api/usdjpy-strategy-lab/strategy-backtest/status
POST /api/usdjpy-strategy-lab/strategy-backtest/sample
POST /api/usdjpy-strategy-lab/strategy-backtest/run
GET  /api/usdjpy-strategy-lab/strategy-backtest/telegram-text
POST /api/usdjpy-strategy-lab/strategy-backtest/sync-klines
GET  /api/usdjpy-strategy-lab/strategy-backtest/production-status
```

All endpoints are local, USDJPY-only, and research-only.

## Current Limits

This is the first complete USDJPY Strategy JSON research runner, not a broker execution engine.

Current remaining limits:

- It is still a deterministic Python research runner, not a MetaTrader Strategy Tester replacement.
- It does not place orders or mutate live presets.
- Tick-level fill modeling and broker-specific slippage distributions remain future work.
- Strategy JSON / Python Replay / MQL5 EA parity must stay green before any candidate can advance.
