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
            endpoints = [{"path": f"/api/example/{idx}"} for idx in range(100)]
            endpoints.append(
                {
                    "path": "/api/hfm-crypto/status",
                    "queryVariants": [
                        {
                            "query": "view=summary",
                            "description": "Preserves operatorChecklist, brokerSymbolDiagnostics and safety for compact first paint.",
                        }
                    ],
                    "description": "HFM status includes operatorChecklist and brokerSymbolDiagnostics.",
                }
            )
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

    def test_api_contract_rejects_missing_hfm_summary_contract(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/contracts").mkdir(parents=True)
            endpoints = [{"path": f"/api/example/{idx}"} for idx in range(100)]
            endpoints.append({"path": "/api/hfm-crypto/status"})
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
            self.assertTrue(any("status?view=summary" in error for error in errors))

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
