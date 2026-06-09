# v2.5.1 News Gate Simplification

This maintenance step changes USDJPY news gating from a routine hard block into a staged risk control.

## Scope

Backend:

```text
tools/news_gate/
tools/usdjpy_strategy_lab/policy_builder.py
tools/usdjpy_bar_replay/
tools/daily_autopilot_v2/
tests/test_news_gate.py
```

Frontend:

```text
src/workspaces/mt5/mt5Model.js
src/components/USDJPYEvolutionPanel.vue
```

Docs:

```text
docs/ops/news-gate-simplification.md
docs/maintenance/v2-5-1-news-gate.md
```

## Behavior

```text
普通新闻：不阻断，只降仓/降级。
高冲击新闻：继续硬阻断 live。
新闻源未知：不阻断，只轻微降仓并写入日报。
```

## Safety

This change does not add order execution, close, cancel, order modification, Telegram command receiving, external real-money market trading, or live preset mutation.

Hard guards remain active for runtime freshness, fastlane quality, spread, loss streak, daily loss, symbol/strategy scope, and max lot.

## Validation

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend
python3 -m unittest tests.test_news_gate tests.test_usdjpy_bar_replay -v
python3 -m unittest tests.test_usdjpy_strategy_lab tests.test_autonomous_lifecycle tests.test_usdjpy_autonomous_agent -v

cd /Users/bowen/Desktop/Quard/QuantGodFrontend
npm test
```

