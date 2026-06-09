# P3-3 Maintenance: DeepSeek Telegram Fusion

## Gate definition

P3-3 is re-scoped for the single-user QuantGod workflow:

```text
MT5/HFM runtime evidence
+ local AI Analysis V2
+ DeepSeek Chinese advisory review
+ Telegram push-only delivery
+ SQLite evidence
```

It replaces the earlier multi-market broker-adapter idea.  It does not introduce
multi-user accounts, billing, broker execution, external market trading, wallet
integration, webhook receivers, or Telegram command execution.

## Files owned by this gate

Backend:

```text
tools/ai_analysis/deepseek_validator.py
tools/ai_analysis/advisory_fusion.py
tools/run_ai_advisory_fusion.py
tests/test_ai_advisory_fusion.py
tests/node/test_deepseek_telegram_guard.mjs
tools/run_mt5_ai_telegram_monitor.py  # patched to call fusion after DeepSeek
```

Docs:

```text
docs/ops/deepseek-telegram-fusion.md
docs/maintenance/p3-3-deepseek-telegram-fusion.md
README.md  # link only
```

## Acceptance checks

Backend:

```powershell
python -m py_compile tools\ai_analysis\deepseek_validator.py tools\ai_analysis\advisory_fusion.py tools\run_ai_advisory_fusion.py
python -m unittest discover tests -v
node --test tests\node\test_deepseek_telegram_guard.mjs
python tools\run_ai_advisory_fusion.py config
python tools\run_ai_advisory_fusion.py scan-once --runtime-dir .\runtime --symbols USDJPYc --no-deepseek --delivery-preview
```

Docs:

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

Runtime/Telegram acceptance:

```text
1. Existing MT5 monitor still runs.
2. Telegram message uses safe effective DeepSeek advice.
3. fallback=true or runtimeFresh=false forces HOLD / observation-only.
4. DeepSeek execution-like text is downgraded before message rendering.
5. Local-vs-DeepSeek conflict forces HOLD.
6. SQLite notification evidence still records Telegram delivery.
```

## Safety invariants

These must remain false:

```text
orderSendAllowed
closeAllowed
cancelAllowed
credentialStorageAllowed
livePresetMutationAllowed
canOverrideKillSwitch
telegramCommandExecutionAllowed
telegramWebhookReceiverAllowed
webhookReceiverAllowed
emailDeliveryAllowed
multiUserAllowed
billingAllowed
```

## What to watch after deployment

- Excessive downgrades caused by DeepSeek wording.  If safe wording gets
  downgraded, update `SAFE_NEGATED_EXECUTION_PHRASES` rather than weakening the
  execution patterns globally.
- Repeated `deepseek_not_available`.  Check only local `.env.deepseek.local`; do
  not commit keys or add repo-level secrets for local-only usage.
- Direction conflicts between local agents and DeepSeek.  These are expected;
  the safe outcome is `finalAction=HOLD`.
- Telegram verbosity.  The full monitor keeps the rich Chinese report; the new
  CLI provides compact smoke messages only.

## Next possible gates

After this gate, useful single-user improvements are:

```text
P3-4 AI journal / outcome scoring
P3-5 external market read-only context watcher
P3-6 Vibe Coding DeepSeek research-only generator
```

Do not reopen the multi-market broker adapter or P4 billing path unless the
product scope changes.
