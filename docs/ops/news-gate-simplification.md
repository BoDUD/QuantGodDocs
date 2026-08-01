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

| Level | Meaning | Shadow Advisory behavior |
|---|---|---|
| `NONE` | No news risk | No effect |
| `SOFT` | Ordinary or medium-risk news | Downgrade research stage and suggested weight |
| `HARD` | BOJ/FOMC/CPI/NFP/rate-decision style high-impact window | Block a fresh advisory; replay may continue |
| `UNKNOWN` | News source unavailable or parse failed | Mark data quality warning and lower advisory confidence |

## 当前 Shadow Advisory 边界

当前没有 Live Lane；RSI LONG 也不例外：

```text
executionLaneExists=false
existingEaOwnsExecution=false
```

News behavior only changes research/advisory evidence:

```text
SOFT + NONE      -> no change
SOFT + SOFT      -> STANDARD_ENTRY becomes OPPORTUNITY_ENTRY; lot is multiplied by QG_NEWS_SOFT_LOT_MULTIPLIER
SOFT + HARD      -> BLOCKED
SOFT + UNKNOWN   -> no block; light lot downgrade
HARD             -> any source news block remains BLOCKED
OFF              -> news is recorded only
```

## Shadow And Replay

MT5 Shadow Lane and replay continue under ordinary news. They may retain this compatibility field:

```text
newsRiskLevel
newsImpactTag
wouldBlockLive  # historical schema name; does not imply a current live lane
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
broker mutation primitives present
executionLaneExists != false
external market real-money
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
