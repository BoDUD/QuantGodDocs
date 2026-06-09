# News Gate Simplification

QuantGod v2.5.1 changes the USDJPY news gate from a常态硬阻断变量 to a风险调节变量.

The rule is:

```text
普通新闻不挡单，高冲击新闻才挡单。
```

## Defaults

```text
QG_NEWS_GATE_MODE=SOFT
QG_NEWS_HARD_BLOCK_ONLY_HIGH_IMPACT=1
QG_NEWS_SOFT_LOT_MULTIPLIER=0.5
QG_NEWS_SOFT_STAGE_DOWNGRADE=1
QG_NEWS_HARD_BLOCK_MINUTES_BEFORE=30
QG_NEWS_HARD_BLOCK_MINUTES_AFTER=30
```

## Risk Levels

| Level | Meaning | Live Lane behavior |
|---|---|---|
| `NONE` | No news risk | No effect |
| `SOFT` | Ordinary or medium-risk news | Do not block; downgrade stage and reduce lot |
| `HARD` | BOJ/FOMC/CPI/NFP/rate-decision style high-impact window | Block live entry; shadow and replay continue |
| `UNKNOWN` | News source unavailable or parse failed | Do not block; light lot downgrade and record data quality issue |

## Live Lane

The Live Lane remains limited to:

```text
USDJPYc / RSI_Reversal / LONG
```

News behavior:

```text
SOFT + NONE      -> no change
SOFT + SOFT      -> STANDARD_ENTRY becomes OPPORTUNITY_ENTRY; lot is multiplied by QG_NEWS_SOFT_LOT_MULTIPLIER
SOFT + HARD      -> BLOCKED
SOFT + UNKNOWN   -> no block; light lot downgrade
HARD             -> any source news block remains BLOCKED
OFF              -> news is recorded only
```

## Shadow And Replay

MT5 Shadow Lane and replay continue under ordinary news. They record:

```text
newsRiskLevel
newsImpactTag
wouldBlockLive
```

Replay writes:

```text
runtime/replay/usdjpy/QuantGod_USDJPYNewsGateReplayReport.json
```

with variants:

```text
current_news_gate
soft_news_gate_v1
hard_only_news_gate_v1
news_off_shadow
```

## Hard Boundaries

News simplification does not soften these hard guards:

```text
runtime stale
fastlane DEGRADED
spread abnormal
lossStreak >= 2
dailyLossR <= -1R
non-USDJPY live
non-RSI live
external market real-money
maxLot > 2.0
```

## Telegram And Frontend

All operator-facing text should use Chinese wording:

```text
新闻风险
普通新闻
高冲击新闻
软提示
硬阻断
仓位降档
不阻断
```

Avoid legacy wording that implies every news flag is a hard block.

