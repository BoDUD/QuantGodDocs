# P3-5 AI Advisory Outcome Journal Maintenance Note

## Goal

P3-5 is a loss-control and learning layer for QuantGod's single-user MT5 +
DeepSeek + Telegram workflow.

Instead of increasing strategy complexity while Telegram advisories are losing,
this phase makes every advisory measurable:

```text
Telegram advisory
→ local shadow sample
→ later runtime price scoring
→ symbol/direction performance summary
→ signal-level pause when recent outcomes are weak
```

## Acceptance checks

Backend:

```powershell
python -m py_compile tools\run_ai_journal.py tools\ai_journal\schema.py tools\ai_journal\writer.py tools\ai_journal\reader.py tools\ai_journal\price_probe.py tools\ai_journal\scorer.py tools\ai_journal\kill_switch.py tools\ai_journal\summary.py tools\ai_journal\telegram_text.py tools\run_mt5_ai_telegram_monitor.py
python -m unittest discover tests -v
node --test tests\node\test_ai_journal_guard.mjs
python tools\run_ai_journal.py status --runtime-dir .\runtime
python tools\run_ai_journal.py summary --runtime-dir .\runtime --text
```

Docs:

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## Forbidden scope

P3-5 must not add:

- order send
- close or cancel
- live preset mutation
- credential storage
- Telegram command receiver
- webhook receiver
- email delivery
- broker execution
- external wallet or order path
- multi-user accounts
- billing or credits

## Chinese Telegram rule

New user-facing Telegram text must be Chinese. Technical identifiers may appear
only when they are unavoidable, such as symbol names, model IDs, runtime file
names, timestamps, or JSON keys inside machine evidence.

## Phase gate

P3-5 passes when:

- Telegram advisories are recorded to local journal evidence
- scoring CLI can produce outcomes from runtime prices
- weak symbol/direction families can be paused at advisory level
- all new Telegram human-facing output is Chinese
- CI remains green
