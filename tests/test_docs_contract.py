from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import check_api_contract_matches_backend as api_check
from scripts import check_docs_links as docs_check
from scripts import format_docs_readability as formatter


class DocsContractTests(unittest.TestCase):
    def test_overlay_scripts_are_not_collapsed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for rel in [
            "scripts/check_docs_links.py",
            "scripts/check_api_contract_matches_backend.py",
            "scripts/render_api_contract_markdown.py",
            "scripts/format_docs_readability.py",
            "tests/test_docs_contract.py",
            ".github/workflows/ci.yml",
        ]:
            text = (root / rel).read_text(encoding="utf-8")
            self.assertGreater(len(text.splitlines()), 10, rel)

    def test_docs_ci_resolves_matching_backend_pr_branch_before_strict_contract_check(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")

        self.assertIn("DOCS_HEAD_REF: ${{ github.head_ref }}", workflow)
        self.assertIn("git ls-remote --exit-code --heads", workflow)
        self.assertIn('"refs/heads/$DOCS_HEAD_REF"', workflow)
        self.assertIn("explicitly falling back to Backend main", workflow)
        self.assertIn("ref: ${{ steps.backend-ref.outputs.ref }}", workflow)
        self.assertIn("--strict-extra", workflow)

    def test_contract_endpoint_counter(self) -> None:
        contract = {
            "endpointGroups": [
                {
                    "name": "core",
                    "endpoints": [
                        {"method": "GET", "path": "/api/latest"},
                        {"method": "POST", "path": "/api/notify/test"},
                        {"method": "GET", "path": "/healthz"},
                        {"method": "GET", "path": "/readyz"},
                    ],
                }
            ]
        }
        self.assertEqual(
            api_check.contract_endpoints(contract),
            {"/api/latest", "/api/notify/test", "/healthz", "/readyz"},
        )

    def test_safety_defaults_require_false_for_trading_fields(self) -> None:
        errors = api_check.check_safety(
            {
                "safetyDefaults": {
                    "localOnly": True,
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                }
            }
        )
        self.assertEqual(errors, [])

    def test_endpoint_modes_are_required_and_limited(self) -> None:
        valid = {
            "endpointGroups": [
                {
                    "name": "core",
                    "endpoints": [
                        {"method": "GET", "path": "/api/latest", "mode": "read-only"},
                        {"method": "POST", "path": "/api/run", "mode": "research-only"},
                    ],
                }
            ]
        }
        self.assertEqual(api_check.check_endpoint_modes(valid), [])

        missing = {
            "endpointGroups": [
                {"name": "core", "endpoints": [{"method": "GET", "path": "/api/latest"}]}
            ]
        }
        self.assertTrue(any("mode is required" in error for error in api_check.check_endpoint_modes(missing)))

        invalid = {
            "endpointGroups": [
                {
                    "name": "core",
                    "endpoints": [
                        {"method": "GET", "path": "/api/latest", "mode": "maybe-live"}
                    ],
                }
            ]
        }
        self.assertTrue(any("invalid endpoint mode" in error for error in api_check.check_endpoint_modes(invalid)))

    def test_contract_rejects_crypto_only_groups_and_routes(self) -> None:
        errors = api_check.check_forex_only_contract(
            {
                "endpointGroups": [
                    {
                        "name": "hfm-crypto-cfd",
                        "endpoints": [
                            {
                                "method": "GET",
                                "path": "/api/hfm-crypto/status",
                            }
                        ],
                    }
                ]
            }
        )
        self.assertTrue(any("endpoint group" in error for error in errors))
        self.assertTrue(any("endpoint is forbidden" in error for error in errors))

    def test_contract_accepts_hfm_forex_routes(self) -> None:
        errors = api_check.check_forex_only_contract(
            {
                "endpointGroups": [
                    {
                        "name": "mt5-forex",
                        "endpoints": [
                            {
                                "method": "GET",
                                "path": "/api/mt5-hfm/status",
                            }
                        ],
                    }
                ]
            }
        )
        self.assertEqual(errors, [])

    def test_contract_rejects_nested_crypto_route(self) -> None:
        errors = api_check.check_forex_only_contract(
            {
                "endpointGroups": [
                    {
                        "name": "autonomous-agent",
                        "endpoints": [
                            {
                                "method": "GET",
                                "path": "/api/usdjpy-strategy-lab/autonomous-agent/hfm-crypto-shadow",
                            }
                        ],
                    }
                ]
            }
        )
        self.assertTrue(any("endpoint is forbidden" in error for error in errors))

    def test_docs_checker_detects_collapsed_python(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            bad = root / "scripts" / "check_docs_links.py"
            bad.write_text(
                "#!/usr/bin/env python3 def main(): return 0 " * 30,
                encoding="utf-8",
            )
            errors = docs_check.check_python_not_collapsed(root)
            self.assertTrue(any("collapsed" in error or "shebang" in error for error in errors))

    def test_formatter_repairs_collapsed_markdown(self) -> None:
        text = (
            "# Title This is a long intro. ## Section - [Link](docs/x.md) "
            "1. Step one. 2. Step two. ```powershell echo ok ```"
        ) * 20
        repaired = formatter.repair_markdown_text(text)
        self.assertGreater(len(repaired.splitlines()), 6)
        self.assertIn("\n\n## Section", repaired)

    def test_json_roundtrip_contract_shape(self) -> None:
        payload = {
            "schemaVersion": 1,
            "safetyDefaults": {
                "localOnly": True,
                "orderSendAllowed": False,
                "closeAllowed": False,
                "cancelAllowed": False,
                "credentialStorageAllowed": False,
                "livePresetMutationAllowed": False,
                "canOverrideKillSwitch": False,
            },
            "endpointGroups": [
                {
                    "name": "backend-core-and-control",
                    "endpoints": [{"method": "GET", "path": "/api/x"}],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "api-contract.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            loaded = api_check.load_contract(path)
            self.assertEqual(api_check.contract_endpoints(loaded), {"/api/x"})

    def test_backend_route_scan_includes_production_evidence_validation(self) -> None:
        root = Path(__file__).resolve().parents[1]
        backend = root.parent / "QuantGodBackend"
        paths = api_check.backend_paths(backend)

        self.assertIn("/api/production-evidence-validation/status", paths)
        self.assertIn("/api/production-evidence-validation/run", paths)
        self.assertIn("/api/production-evidence-validation/telegram-text", paths)

    def test_backend_paths_requires_backend_route_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            backend = Path(tmp)
            (backend / "Dashboard").mkdir()
            (backend / "Dashboard" / "dashboard_server.js").write_text(
                "app.get('/api/from-fallback-scan', handler)",
                encoding="utf-8",
            )

            with self.assertRaises(FileNotFoundError):
                api_check.backend_paths(backend)

    def test_backend_paths_uses_backend_route_registry_as_single_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            backend = Path(tmp)
            (backend / "tools").mkdir()
            (backend / "Dashboard").mkdir()
            (backend / "Dashboard" / "dashboard_server.js").write_text(
                "app.get('/api/from-fallback-scan', handler)",
                encoding="utf-8",
            )
            (backend / "tools" / "api_route_registry.py").write_text(
                "\n".join(
                    [
                        "import json",
                        "print(json.dumps({",
                        '  "schema": "quantgod.backend_api_route_registry.v1",',
                        '  "paths": ["/api/from-backend-registry"],',
                        '  "placeholderPaths": [],',
                        '  "aliasPrefixCoverage": {}',
                        "}))",
                    ]
                ),
                encoding="utf-8",
            )

            paths = api_check.backend_paths(backend)

            self.assertEqual(paths, {"/api/from-backend-registry"})

    def test_ga_factory_alias_children_are_covered_by_base_route(self) -> None:
        actual = {"/api/ga-factory"}
        alias_prefix_coverage = {"/api/ga-factory/": "/api/ga-factory"}

        self.assertTrue(
            api_check.path_is_covered_by_alias(
                "/api/ga-factory/status",
                actual,
                alias_prefix_coverage,
            )
        )
        self.assertTrue(
            api_check.path_is_covered_by_alias(
                "/api/ga-factory/build",
                actual,
                alias_prefix_coverage,
            )
        )
        self.assertFalse(
            api_check.path_is_covered_by_alias(
                "/api/strategy-ga-factory/status",
                actual,
                alias_prefix_coverage,
            )
        )

    def test_dynamic_backend_routes_require_documented_placeholder(self) -> None:
        documented = {"/api/mt5-readonly/:endpoint"}
        placeholder_paths = {"/api/mt5-readonly/:endpoint"}

        self.assertTrue(
            api_check.path_is_documented(
                "/api/mt5-readonly/account",
                documented,
                placeholder_paths,
            )
        )
        self.assertFalse(
            api_check.path_is_documented(
                "/api/mt5-readonly/account",
                set(),
                placeholder_paths,
            )
        )


if __name__ == "__main__":
    unittest.main()
