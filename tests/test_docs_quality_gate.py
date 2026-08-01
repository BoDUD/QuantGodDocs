from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_docs_quality_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_docs_quality_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DocsQualityGateTests(unittest.TestCase):
    def test_script_is_real_multiline_python(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertGreater(len(text.splitlines()), 100)
        self.assertIn("def check_api_contract", text)
        self.assertNotIn("\r", text)

    def test_collect_endpoints_from_grouped_contract(self):
        module = load_module()
        contract = {
            "endpointGroups": [
                {"name": "core", "endpoints": [{"path": "/api/latest"}, {"path": "/api/status"}]},
                {"name": "extra", "endpoints": ["/api/example"]},
            ]
        }
        self.assertEqual(
            module.collect_endpoints(contract),
            ["/api/example", "/api/latest", "/api/status"],
        )

    def test_api_contract_requires_false_execution_defaults(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            endpoints = [{"path": f"/api/example/{idx}", "mode": "read-only"} for idx in range(100)]
            contract = {
                "endpointGroups": [{"name": "example", "endpoints": endpoints}],
                "safetyDefaults": {
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                    "telegramCommandExecutionAllowed": False,
                },
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            errors = []
            module.check_api_contract(root, errors)
            self.assertEqual(errors, [])

    def test_api_contract_allows_standard_local_health_endpoints(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            endpoints = [{"path": f"/api/example/{idx}", "mode": "read-only"} for idx in range(100)]
            endpoints.extend([
                {"path": "/healthz", "mode": "read-only"},
                {"path": "/readyz", "mode": "read-only"},
            ])
            contract = {
                "endpointGroups": [{"name": "example", "endpoints": endpoints}],
                "safetyDefaults": {
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                    "telegramCommandExecutionAllowed": False,
                },
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            errors = []
            module.check_api_contract(root, errors)
            self.assertEqual(errors, [])

    def test_api_contract_rejects_crypto_only_endpoint(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            endpoints = [{"path": f"/api/example/{idx}", "mode": "read-only"} for idx in range(100)]
            endpoints.append({"path": "/api/hfm-crypto/status", "mode": "read-only"})
            contract = {
                "endpointGroups": [{"name": "example", "endpoints": endpoints}],
                "safetyDefaults": {
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                    "telegramCommandExecutionAllowed": False,
                },
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            errors = []
            module.check_api_contract(root, errors)
            self.assertTrue(any("crypto-only endpoint" in error for error in errors))

    def test_api_contract_rejects_crypto_only_group(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            contract = {
                "endpointGroups": [
                    {
                        "name": "bitcoin-research",
                        "endpoints": [
                            {"path": f"/api/example/{idx}", "mode": "read-only"}
                            for idx in range(100)
                        ],
                    }
                ],
                "safetyDefaults": {
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                    "telegramCommandExecutionAllowed": False,
                },
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            errors = []
            module.check_api_contract(root, errors)
            self.assertTrue(any("crypto-only group" in error for error in errors))

    def test_api_contract_requires_endpoint_modes(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            endpoints = [{"path": f"/api/example/{idx}", "mode": "read-only"} for idx in range(100)]
            endpoints.append({"path": "/api/example/no-mode"})
            contract = {
                "endpointGroups": [{"name": "example", "endpoints": endpoints}],
                "safetyDefaults": {
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                    "telegramCommandExecutionAllowed": False,
                },
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            errors = []
            module.check_api_contract(root, errors)
            self.assertTrue(any("endpoint mode missing" in error for error in errors))

    def test_live_lane_doctrine_accepts_permanent_shadow_boundary(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            safety = root / "docs/backend/safety-boundaries.md"
            safety.parent.mkdir(parents=True)
            safety.write_text(
                "\n".join(
                    [
                        "# Backend 安全边界",
                        "当前没有 live lane，executionLaneExists=false。",
                        "USDJPYc / RSI_Reversal / LONG 也不例外，只能生成 topAdvisoryPolicy。",
                        "MA_Cross 与 USDJPY_NIGHT_REVERSION_SAFE 只能保留在 SHADOW、TESTER_ONLY、PAPER_LIVE_SIM。",
                        "活动 EA 已物理移除 broker mutation 原语。",
                        "未来必须单独执行 lane RFC，且 order-send 与 live-preset-mutation 继续为 false。",
                    ]
                ),
                encoding="utf-8",
            )
            errors = []
            module.check_live_lane_doctrine(root, errors)
            self.assertEqual(errors, [])

    def test_live_lane_doctrine_rejects_retired_live_route_boundary(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            safety = root / "docs/backend/safety-boundaries.md"
            safety.parent.mkdir(parents=True)
            safety.write_text(
                "# Backend 安全边界\n当前唯一允许保留为 live 的路线是 USDJPYc / RSI_Reversal / LONG，其他策略经过治理后可进入实盘。\n",
                encoding="utf-8",
            )
            errors = []
            module.check_live_lane_doctrine(root, errors)
            self.assertTrue(
                any("Shadow-only doctrine" in error or "retired live-route doctrine" in error for error in errors)
            )

    def test_active_shadow_doctrine_accepts_current_runbooks(self):
        module = load_module()
        errors = []

        module.check_active_shadow_doctrine(ROOT, errors)

        self.assertEqual(errors, [])

    def test_active_shadow_doctrine_rejects_live_lane_and_auto_lot_instructions(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text(
                "\n".join(
                    [
                        "# QuantGodDocs",
                        "Shadow / ReadOnly research with executionLaneExists=false.",
                        "Live Lane: USDJPYc / RSI_Reversal / LONG",
                        "QG_AUTO_MAX_LOT=2.0",
                    ]
                ),
                encoding="utf-8",
            )
            errors = []

            module.check_active_shadow_doctrine(root, errors)

            self.assertTrue(any("retired active-execution doctrine" in error for error in errors))

    def test_retired_live_runbook_requires_bilingual_retired_marker(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runbook = root / "docs/ops/mt5-hfm-live-pilot.md"
            runbook.parent.mkdir(parents=True)
            runbook.write_text("# MT5 / HFM Live Pilot\n\nCurrent operations.\n", encoding="utf-8")
            errors = []

            module.check_active_shadow_doctrine(root, errors)

            self.assertTrue(any("Historical / Retired" in error for error in errors))

    def test_api_contract_markdown_sync_accepts_rendered_markdown(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            (root / "docs/backend").mkdir(parents=True)
            contract = {
                "backendApiBaseUrl": "http://127.0.0.1:8080/api",
                "safetyDefaults": {"orderSendAllowed": False},
                "endpointGroups": [
                    {
                        "name": "core",
                        "phase": "backend",
                        "endpoints": [{"method": "GET", "path": "/api/latest", "mode": "read-only"}],
                    }
                ],
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            (root / "docs/backend/api-contract.md").write_text(
                module.render_api_contract_markdown(contract),
                encoding="utf-8",
            )

            errors = []
            module.check_api_contract_markdown_sync(root, errors)

            self.assertEqual(errors, [])

    def test_api_contract_markdown_sync_rejects_stale_markdown(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            (root / "docs/backend").mkdir(parents=True)
            contract = {
                "endpointGroups": [
                    {
                        "name": "core",
                        "endpoints": [{"method": "GET", "path": "/api/latest"}],
                    }
                ],
            }
            (root / "docs/contracts/api-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            (root / "docs/backend/api-contract.md").write_text("# Stale API contract\n", encoding="utf-8")

            errors = []
            module.check_api_contract_markdown_sync(root, errors)

            self.assertTrue(any("api-contract.md is not synchronized" in error for error in errors))

    def test_markdown_compression_is_rejected(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "README.md"
            target.write_text("# Title long compressed document", encoding="utf-8")
            errors = []
            module.check_markdown_readability(root, errors)
            self.assertTrue(any("too short" in error for error in errors))

    def test_case_memory_coverage_queue_is_documented(self):
        case_memory = (ROOT / "docs/ops/usdjpy-case-memory.md").read_text(encoding="utf-8")
        production = (ROOT / "docs/ops/production-evidence-validation.md").read_text(encoding="utf-8")
        combined = f"{case_memory}\n{production}"

        for marker in [
            "coveragePlan.nextCollectionQueue",
            "coveragePlan.missingRows",
            "caseMemoryCoverage.nextCollectionQueue",
            "caseMemoryCoverage.missingRows",
            "targetSampleCount",
            "remainingTargetSampleCount",
            "/api/usdjpy-strategy-lab/evidence-os/execution-feedback",
            "/api/usdjpy-strategy-lab/bar-replay/entry",
            "BAD_ENTRY",
            "MISSED_OPPORTUNITY",
            "EARLY_EXIT",
            "NEWS_DAMAGE",
            "GA_OVERFIT",
            "orderSendAllowed=false",
        ]:
            self.assertIn(marker, combined)

        self.assertIn("Do not satisfy these gaps by editing live presets", case_memory)
        self.assertIn("They must not place orders", production)

    def test_history_freshness_recovery_queue_is_documented(self):
        production = (ROOT / "docs/ops/production-evidence-validation.md").read_text(encoding="utf-8")

        for marker in [
            "historyProduction.staleTimeframes",
            "historyProduction.freshnessRecoveryQueue",
            "historyProduction.nextRecoveryActionZh",
            "sync-klines --months 12 --timeframes M1,M5,M15,H1",
            "production-status --months 12 --max-latest-lag-hours 96",
            "freshnessOk=true",
            "historyTargetSatisfied=true",
            "orderSendAllowed=false",
        ]:
            self.assertIn(marker, production)

        self.assertIn("must not place orders", production)


if __name__ == "__main__":
    unittest.main()
