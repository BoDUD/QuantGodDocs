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

    def test_markdown_compression_is_rejected(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "README.md"
            target.write_text("# Title long compressed document", encoding="utf-8")
            errors = []
            module.check_markdown_readability(root, errors)
            self.assertTrue(any("too short" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
