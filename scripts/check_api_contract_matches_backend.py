#!/usr/bin/env python3
"""Validate QuantGodDocs API contract and optionally compare it to Backend routes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PATH_RE = re.compile(r"/api/[A-Za-z0-9_./:-]+")

PLACEHOLDER_PATHS = {
    "/api/ai-analysis/history/:id",
    "/api/ai-analysis-v2/history/:id",
    "/api/vibe-coding/strategy/:id",
    "/api/usdjpy-strategy-lab/ga/candidate/:seedId",
    "/api/paramlab/auto-tester/:action",
    "/api/mt5-platform/:endpoint",
    "/api/mt5-trading/:endpoint",
    "/api/mt5/order/:ticket",
    "/api/mt5-readonly/:endpoint",
    "/api/mt5-readonly-secondary/:endpoint",
    "/api/mt5-symbol-registry/:endpoint",
    "/api/mt5/:endpoint",
}

REQUIRED_SAFETY_FALSE_KEYS = [
    "orderSendAllowed",
    "closeAllowed",
    "cancelAllowed",
    "credentialStorageAllowed",
    "livePresetMutationAllowed",
    "canOverrideKillSwitch",
]

OPTIONAL_SAFETY_FALSE_KEYS = [
    "canMutateGovernanceDecision",
    "telegramCommandExecutionAllowed",
]

REQUIRED_ENDPOINT_GROUPS = {
    "backend-core-and-control",
    "hfm-crypto-cfd",
    "live-automation-readiness",
    "mt5-readonly",
    "ai-analysis-v1",
    "phase2-file-facade",
    "notify",
    "phase3-vibe-ai-kline",
}

ALLOWED_ENDPOINT_MODES = {
    "advisory",
    "guarded-control",
    "local-advisory-control",
    "push-only",
    "push-preview",
    "read-only",
    "read-only-csv",
    "research-only",
    "review-only-build",
}

BACKEND_ROUTE_FILES = [
    "Dashboard/phase1_api_routes.js",
    "Dashboard/phase2_api_routes.js",
    "Dashboard/phase3_api_routes.js",
    "Dashboard/state_api_routes.js",
    "Dashboard/dashboard_server.js",
    "Dashboard/automation_chain_api_routes.js",
    "Dashboard/usdjpy_strategy_lab_api_routes.js",
    "Dashboard/case_memory_api_routes.js",
    "Dashboard/strategy_ga_factory_api_routes.js",
    "Dashboard/ga_factory_api_routes.js",
    "Dashboard/telegram_gateway_ops_api_routes.js",
    "Dashboard/hfm_crypto_cfd_api_routes.js",
    "Dashboard/live_automation_readiness_api_routes.js",
    "Dashboard/production_evidence_validation_api_routes.js",
]

ALIAS_PREFIX_COVERAGE = {
    "/api/ga-factory/": "/api/ga-factory",
}


def load_contract(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contract root must be object")
    return data


def endpoint_groups(contract: dict) -> list[dict]:
    groups = contract.get("endpointGroups")
    if not isinstance(groups, list):
        raise ValueError("endpointGroups must be a list")
    return groups


def contract_endpoints(contract: dict) -> set[str]:
    endpoints: set[str] = set()
    for group in endpoint_groups(contract):
        if not isinstance(group, dict):
            raise ValueError("endpoint group must be object")
        for endpoint in group.get("endpoints", []):
            path = endpoint.get("path")
            method = endpoint.get("method")
            if not isinstance(path, str) or not path.startswith("/api/"):
                raise ValueError(f"invalid endpoint path: {path!r}")
            if not isinstance(method, str) or method.upper() not in {
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "ANY",
            }:
                raise ValueError(f"invalid method for {path}: {method!r}")
            endpoints.add(path)
    return endpoints


def check_required_groups(contract: dict) -> list[str]:
    group_names = {
        group.get("name")
        for group in endpoint_groups(contract)
        if isinstance(group, dict)
    }
    missing = sorted(REQUIRED_ENDPOINT_GROUPS - group_names)
    return [f"missing endpoint group: {name}" for name in missing]


def check_safety(contract: dict) -> list[str]:
    errors: list[str] = []
    safety = contract.get("safetyDefaults", {})
    if safety.get("localOnly") is not True:
        errors.append("safetyDefaults.localOnly must be true")

    for key in REQUIRED_SAFETY_FALSE_KEYS:
        if safety.get(key) is not False:
            errors.append(f"safetyDefaults.{key} must be false")

    for key in OPTIONAL_SAFETY_FALSE_KEYS:
        if key in safety and safety.get(key) is not False:
            errors.append(f"safetyDefaults.{key} must be false when present")

    return errors


def check_hfm_summary_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    status_endpoint = None
    for group in endpoint_groups(contract):
        if not isinstance(group, dict):
            continue
        for endpoint in group.get("endpoints", []):
            if isinstance(endpoint, dict) and endpoint.get("path") == "/api/hfm-crypto/status":
                status_endpoint = endpoint
                break
        if status_endpoint:
            break

    if not isinstance(status_endpoint, dict):
        return ["missing /api/hfm-crypto/status endpoint"]

    variants = status_endpoint.get("queryVariants") or []
    summary_variant = next(
        (
            variant
            for variant in variants
            if isinstance(variant, dict) and variant.get("query") == "view=summary"
        ),
        None,
    )
    if not summary_variant:
        errors.append("missing /api/hfm-crypto/status?view=summary query variant")
    status_text = json.dumps(status_endpoint, ensure_ascii=False)
    summary_text = json.dumps(summary_variant or {}, ensure_ascii=False)
    if "brokerSymbolDiagnostics" not in status_text or "brokerSymbolDiagnostics" not in summary_text:
        errors.append("HFM summary contract must preserve brokerSymbolDiagnostics")
    if "operatorChecklist" not in status_text or "operatorChecklist" not in summary_text:
        errors.append("HFM summary contract must preserve operatorChecklist")
    if "safety" not in summary_text:
        errors.append("HFM summary contract must preserve safety flags")
    return errors


def check_endpoint_modes(contract: dict) -> list[str]:
    errors: list[str] = []
    for group in endpoint_groups(contract):
        group_name = group.get("name") if isinstance(group, dict) else "unknown"
        for endpoint in group.get("endpoints", []):
            if not isinstance(endpoint, dict):
                continue
            path = endpoint.get("path")
            mode = endpoint.get("mode")
            if not isinstance(mode, str) or not mode.strip():
                errors.append(f"{group_name}:{path}: endpoint mode is required")
                continue
            if mode not in ALLOWED_ENDPOINT_MODES:
                errors.append(
                    f"{group_name}:{path}: invalid endpoint mode {mode!r}; "
                    f"expected one of {sorted(ALLOWED_ENDPOINT_MODES)}"
                )
    return errors


def normalize_backend_path(path: str) -> str:
    clean = path.rstrip("/") or path

    if clean.startswith("/api/ai-analysis/history/"):
        return "/api/ai-analysis/history/:id"
    if clean.startswith("/api/ai-analysis-v2/history/"):
        return "/api/ai-analysis-v2/history/:id"
    if clean.startswith("/api/vibe-coding/strategy/"):
        return "/api/vibe-coding/strategy/:id"
    if clean.startswith("/api/usdjpy-strategy-lab/ga/candidate/"):
        return "/api/usdjpy-strategy-lab/ga/candidate/:seedId"
    if clean.startswith("/api/paramlab/auto-tester/"):
        return "/api/paramlab/auto-tester/:action"
    if clean.startswith("/api/mt5-platform/"):
        return "/api/mt5-platform/:endpoint"
    if clean.startswith("/api/mt5-trading/"):
        return "/api/mt5-trading/:endpoint"
    if clean.startswith("/api/mt5/order/"):
        return "/api/mt5/order/:ticket"
    if clean.startswith("/api/mt5-readonly/"):
        return "/api/mt5-readonly/:endpoint"
    if clean.startswith("/api/mt5-readonly-secondary/"):
        return "/api/mt5-readonly-secondary/:endpoint"
    if clean.startswith("/api/mt5-symbol-registry/"):
        return "/api/mt5-symbol-registry/:endpoint"
    if clean.startswith("/api/mt5/"):
        return "/api/mt5/:endpoint"

    return clean


def scan_backend_route_files(backend_root: Path) -> set[str]:
    found: set[str] = set()
    for rel in BACKEND_ROUTE_FILES:
        path = backend_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in PATH_RE.finditer(text):
            raw = match.group(0).rstrip("/") or match.group(0)
            normalized = normalize_backend_path(raw)
            found.add(raw)
            found.add(normalized)
    return found


def backend_route_registry_paths(backend_root: Path) -> set[str] | None:
    registry_script = backend_root / "tools" / "api_route_registry.py"
    if not registry_script.exists():
        return None

    result = subprocess.run(
        [
            sys.executable,
            str(registry_script),
            "--backend-root",
            str(backend_root),
            "--format",
            "json",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Backend API route registry failed: "
            + (result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}")
        )

    payload = json.loads(result.stdout)
    paths = payload.get("paths")
    if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
        raise ValueError("Backend API route registry must expose a string list at `paths`")
    return set(paths)


def backend_paths(backend_root: Path) -> set[str]:
    registry_paths = backend_route_registry_paths(backend_root)
    if registry_paths is not None:
        return registry_paths
    return scan_backend_route_files(backend_root)


def path_is_covered_by_alias(path: str, actual: set[str]) -> bool:
    for prefix, base in ALIAS_PREFIX_COVERAGE.items():
        if path.startswith(prefix) and base in actual:
            return True
    return False


def compare_backend_routes(contract: dict, backend_root: Path, strict_extra: bool) -> list[str]:
    documented = contract_endpoints(contract)
    actual = backend_paths(backend_root)
    errors: list[str] = []

    # For the "missing from contract" check, skip backend paths whose normalized form
    # is a known wildcard placeholder. Raw literal paths (e.g. /api/mt5-readonly/kline)
    # are expected to be covered by wildcard placeholders (e.g. /api/mt5-readonly/:endpoint).
    missing = sorted(
        path for path in actual
        if path not in documented
        and path not in PLACEHOLDER_PATHS
        and normalize_backend_path(path) not in PLACEHOLDER_PATHS
    )
    if missing:
        errors.append(
            "backend route(s) missing from docs contract: " + ", ".join(missing[:50])
        )

    if strict_extra:
        extra_contract_paths: list[str] = []
        for path in sorted(documented):
            if path in actual:
                continue
            if path in PLACEHOLDER_PATHS:
                continue
            if path_is_covered_by_alias(path, actual):
                continue
            # A literal contract path (e.g. /api/mt5-readonly/account) is covered
            # if the corresponding wildcard (e.g. /api/mt5-readonly/:endpoint) is in
            # the observed backend paths.
            covered_by_wildcard = any(
                wildcard in actual
                for wildcard in PLACEHOLDER_PATHS
                if path.startswith(wildcard.replace(":endpoint", "").replace(":id", "").replace(":ticket", "").replace(":action", ""))
            )
            if not covered_by_wildcard:
                extra_contract_paths.append(path)
        if extra_contract_paths:
            errors.append(
                "docs contract path(s) not observed in backend route files: "
                + ", ".join(extra_contract_paths[:50])
            )

    return errors


def validate_contract(contract: dict, min_endpoints: int = 100) -> list[str]:
    errors: list[str] = []
    documented = contract_endpoints(contract)

    if len(documented) < min_endpoints:
        errors.append(
            f"contract looks too small: only {len(documented)} endpoints; "
            f"expected at least {min_endpoints}"
        )

    errors.extend(check_required_groups(contract))
    errors.extend(check_safety(contract))
    errors.extend(check_endpoint_modes(contract))
    errors.extend(check_hfm_summary_contract(contract))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="docs/contracts/api-contract.json")
    parser.add_argument(
        "--backend",
        default=None,
        help="Optional QuantGodBackend root for route comparison",
    )
    parser.add_argument(
        "--strict-extra",
        action="store_true",
        help="Also fail when contract contains paths not seen in backend route files",
    )
    parser.add_argument(
        "--min-endpoints",
        type=int,
        default=100,
        help="Minimum documented endpoint count expected in the contract",
    )
    args = parser.parse_args(argv)

    contract_path = Path(args.contract).resolve()
    contract = load_contract(contract_path)
    errors = validate_contract(contract, min_endpoints=args.min_endpoints)

    if args.backend:
        errors.extend(compare_backend_routes(contract, Path(args.backend).resolve(), args.strict_extra))

    if errors:
        print("QuantGod API contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "QuantGod API contract check OK "
        f"({len(contract_endpoints(contract))} documented endpoints)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
