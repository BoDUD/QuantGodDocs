# QuantGodDocs

QuantGodDocs is the documentation and contract hub for the QuantGod four-repository system.

This repository is the source of truth for architecture, API contracts, runbooks, safety boundaries, and phase history. It does not contain backend runtime code, Vue source, deployment automation, credentials, MT5 account data, Telegram tokens, DeepSeek keys, wallet keys, or generated runtime evidence.

## System Summary

QuantGod v2.6 is a local-first USDJPY autonomous research and execution-governance system with an auditable Strategy JSON GA evolution trace:

```text
Live Lane: USDJPYc / RSI_Reversal / LONG / cent account
MT5 Shadow Lane: USDJPY multi-strategy simulation and tester research
HFM Crypto CFD Shadow Lane: local HFM symbol evidence, Moss backtest profile mapping, and shadow-only research
Agent: autonomous daily todo, daily review, promotion, demotion, rollback
GA Trace: Strategy JSON seeds, generations, fitness, blockers, elites, mutation, and crossover
Hard guards: runtime freshness, fastlane quality, spread, high-impact news, loss, and rollback
```

Core principle:

```text
Live narrow. Simulation broad. Promotion fast. Rollback hard.
```

## Repository Map

| Repository | Responsibility | Must not contain |
|---|---|---|
| `QuantGodBackend` | MT5 assets, local API, Agent tools, USDJPY replay/walk-forward/lifecycle, Telegram push | Vue source, Cloudflare source, long-form docs hub |
| `QuantGodFrontend` | Vue operator workbench and `/api/*` client modules | MT5 source, Python tools, direct runtime file reads |
| `QuantGodInfra` | Workspace automation, launchd, Docker local, dist sync, optional Cloudflare/Cloud Sync | Trading logic, live preset policy, product docs hub |
| `QuantGodDocs` | Architecture, API contracts, runbooks, safety, maintenance records | Runtime output, credentials, execution code |

## Start Reading

| Topic | Document |
|---|---|
| Four-repo architecture | [Repo split architecture](docs/architecture/repo-split.md) |
| Module boundaries | [Module boundaries](docs/architecture/module-boundaries.md) |
| Repo linkage contract | [Linkage contract](docs/architecture/linkage-contract.md) |
| API contract | [Backend API contract](docs/backend/api-contract.md) |
| Safety boundaries | [Backend safety boundaries](docs/backend/safety-boundaries.md) |
| Local runbook | [Local runbook](docs/ops/runbook-local.md) |
| Frontend workbench | [Frontend workbench](docs/frontend/workbench.md) |
| Infra automation | [Workspace automation](docs/infra/workspace-automation.md) |

## Current v2.6 Operating Documents

| Area | Document |
|---|---|
| Autonomous multi-lane Agent | [QuantGod v2.5 three-lane Agent](docs/ops/usdjpy-cent-autonomous-multilane-agent.md) |
| Strategy JSON GA trace | [Strategy JSON GA evolution trace](docs/ops/strategy-json-ga-evolution-trace.md) |
| Strategy GA Factory | [Strategy GA Factory](docs/ops/strategy-ga-factory.md) |
| Trading Agent article gap audit | [Trading Agent Article Gap Audit](docs/ops/trading-agent-article-gap-audit.md) |
| USDJPY GA Factory | [USDJPY GA Factory](docs/ops/usdjpy-ga-factory.md) |
| Telegram Gateway observability | [Telegram Gateway observability](docs/ops/telegram-gateway-observability.md) |
| Strategy JSON USDJPY backtest | [Strategy JSON USDJPY backtest](docs/ops/strategy-json-usdjpy-backtest.md) |
| Strategy JSON → EA contract | [Strategy JSON EA contract adapter](docs/ops/strategy-json-ea-contract-adapter.md) |
| USDJPY Evidence OS | [USDJPY Evidence OS](docs/ops/usdjpy-evidence-os.md) |
| Production evidence validation | [Production Evidence Validation](docs/ops/production-evidence-validation.md) |
| Execution feedback coverage | [Execution Feedback Coverage](docs/ops/execution-feedback-coverage.md) |
| Execution feedback producer | [Execution Feedback Producer](docs/ops/execution-feedback-producer.md) |
| News gate simplification | [News gate simplification](docs/ops/news-gate-simplification.md) |
| USDJPY autonomous governance | [USDJPY autonomous Agent](docs/ops/usdjpy-autonomous-agent.md) |
| USDJPY live loop and daily autopilot | [USDJPY live loop daily autopilot](docs/ops/usdjpy-live-loop-daily-autopilot.md) |
| USDJPY strategy policy lab | [USDJPY strategy policy lab](docs/ops/usdjpy-strategy-policy-lab.md) |
| USDJPY runtime evolution core | [USDJPY runtime evolution core](docs/ops/usdjpy-runtime-evolution-core.md) |
| Causal replay simulator | [USDJPY bar replay simulator](docs/ops/usdjpy-bar-replay-simulator.md) |
| Strategy lab API | [USDJPY strategy lab API](docs/backend/usdjpy-strategy-lab-api.md) |
| EA lab runbook | [USDJPY EA lab runbook](docs/ops/usdjpy-ea-lab-runbook.md) |

## Phase and Maintenance Records

| Phase | Document |
|---|---|
| Phase 1 | [Phase 1](docs/phases/phase1.md) |
| Phase 2 | [Phase 2](docs/phases/phase2.md) |
| Phase 3 | [Phase 3](docs/phases/phase3.md) |
| USDJPY strategy factory | [USDJPY EA strategy factory](docs/phases/usdjpy-ea-strategy-factory.md) |
| Completion matrix | [Docs completion matrix](docs/maintenance/docs-completion-matrix.md) |
| Changelog | [Changelog](docs/maintenance/changelog.md) |

Recent maintenance records:

- [P3-17 USDJPY evolution core](docs/maintenance/p3-17-usdjpy-evolution-core.md)
- [P3-18 replay fidelity hardening](docs/maintenance/p3-18-replay-fidelity-hardening.md)
- [P3-19 bar replay simulator](docs/maintenance/p3-19-usdjpy-bar-replay-simulator.md)
- [P3-20 autonomous walk-forward promotion gate](docs/maintenance/p3-20-autonomous-walk-forward-promotion-gate.md)
- [P3-21 three-lane autonomous lifecycle](docs/maintenance/p3-21-usdjpy-cent-autonomous-multilane-agent.md)
- [v2.5.1 news gate simplification](docs/maintenance/v2-5-1-news-gate.md)
- [v2.6 Strategy JSON GA trace](docs/maintenance/v2-6-strategy-json-ga-trace.md)
- [v2.6.1 Strategy JSON USDJPY backtest](docs/maintenance/v2-6-1-strategy-json-usdjpy-backtest.md)
- [v2.7 USDJPY Evidence OS](docs/maintenance/v2-7-usdjpy-evidence-os.md)
- [v2.8 Strategy JSON EA contract adapter](docs/maintenance/v2-8-strategy-json-ea-contract-adapter.md)
- [P4-3 Case Memory strategy candidate](docs/maintenance/p4-3-case-memory-strategy-candidate.md)
- [P4-4 Strategy GA Factory](docs/maintenance/p4-4-strategy-ga-factory.md)
- [P4-4 GA Factory productionization](docs/maintenance/p4-4-ga-factory-productionization.md)
- [P4-5 Telegram Gateway observability](docs/maintenance/p4-5-telegram-gateway-observability.md)
- [P4-6 Production Evidence Validation](docs/maintenance/p4-6-production-evidence-validation.md)
- [P4-7 Case Memory strategy structure productionization](docs/maintenance/p4-7-case-memory-strategy-structure-productionization.md)
- [P4-8A Strategy Family Parity Matrix](docs/maintenance/p4-8a-strategy-family-parity-matrix.md)
- [P4-8B Execution Feedback Sampling Coverage](docs/maintenance/p4-8b-execution-feedback-coverage.md)
- [P4-8B.1 Execution Feedback Producer](docs/maintenance/p4-8b-1-execution-feedback-producer.md)

## API and Contract Files

- [API contract JSON](docs/contracts/api-contract.json)
- [API contract markdown](docs/backend/api-contract.md)
- [Repo manifest schema](docs/contracts/repo-manifest.schema.json)

When a backend `/api/*` endpoint changes, update:

1. `docs/contracts/api-contract.json`
2. `docs/backend/api-contract.md`
3. Any affected frontend or ops documentation

## Safety Doctrine

Documentation should consistently reflect these constraints:

- Live Lane is limited to `USDJPYc / RSI_Reversal / LONG`.
- MT5 Shadow Lane may simulate and rank multiple USDJPY strategies, but cannot seize the live route.
- HFM Crypto CFD is shadow-only; no broker order send, close, cancel, live preset mutation, wallet signing, or credential custody.
- Telegram is push-only; Telegram command execution is out of scope.
- DeepSeek explains, summarizes, and reviews; it does not approve live execution or override rollback.
- `QG_AUTO_MAX_LOT=2.0` is an upper bound, not a fixed lot size.
- Runtime stale, fastlane degraded, high-impact news, abnormal spread, daily loss, and loss streak gates remain hard stops.
- Ordinary news is a soft risk adjustment by default: it can downgrade stage or reduce lot, but should not by itself block USDJPY RSI LONG.
- Agent may write controlled patch evidence through staged governance; it must not mutate source code or live preset directly.
- GA may generate and score Strategy JSON candidates for shadow/tester/paper research, but it must not directly enter live execution or mutate live preset.

## Local Checks

```bash
cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python3 -m unittest discover tests -v
```

For contract-only validation:

```bash
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json
```

## Maintenance Rules

1. Use readable multi-line Markdown and Python; do not compress whole files into one long line.
2. Keep relative links valid.
3. Keep contract JSON parseable and synchronized with backend routes.
4. Safety documentation takes precedence over feature descriptions.
5. Do not document future work as completed. Strategy JSON GA trace is implemented for shadow/tester research; Telegram Gateway is push-only observability, not a command channel.
6. Do not include credentials, runtime evidence, account identifiers, wallet keys, or tokens.
7. Prefer natural-language operator wording over internal endpoint names in user-facing docs.
- [GA 多代稳定性证据](docs/ops/ga-multi-generation-stability.md)
