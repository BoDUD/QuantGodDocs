#!/usr/bin/env python3
"""QuantGodDocs readability and completion quality gate.

This guard is intentionally repository-local. It does not enforce legal policy or
open-source licensing. It only verifies that the Docs repository is a readable,
structured documentation hub before the project advances to the next roadmap item.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

REQUIRED_DOCS = [
    "README.md",
    "docs/architecture/repo-split.md",
    "docs/architecture/module-boundaries.md",
    "docs/architecture/linkage-contract.md",
    "docs/backend/README.md",
    "docs/backend/api-contract.md",
    "docs/backend/safety-boundaries.md",
    "docs/frontend/README.md",
    "docs/frontend/workbench.md",
    "docs/frontend/api-client.md",
    "docs/infra/README.md",
    "docs/infra/workspace-automation.md",
    "docs/infra/deployment-local.md",
    "docs/ops/runbook-local.md",
    "docs/ops/mt5-hfm-live-pilot.md",
    "docs/ops/telegram.md",
    "docs/phases/phase1.md",
    "docs/phases/phase2.md",
    "docs/phases/phase3.md",
    "docs/contracts/api-contract.json",
    "docs/contracts/repo-manifest.schema.json",
    "docs/maintenance/contribution.md",
    "docs/maintenance/changelog.md",
    "scripts/check_docs_links.py",
    "scripts/check_api_contract_matches_backend.py",
]

CORE_MARKDOWN = [
    "README.md",
    "docs/architecture/repo-split.md",
    "docs/architecture/module-boundaries.md",
    "docs/architecture/linkage-contract.md",
    "docs/backend/api-contract.md",
    "docs/backend/safety-boundaries.md",
    "docs/frontend/api-client.md",
    "docs/infra/workspace-automation.md",
    "docs/ops/runbook-local.md",
    "docs/phases/phase1.md",
    "docs/phases/phase2.md",
    "docs/phases/phase3.md",
]

EXECUTION_FALSE_FIELDS = [
    "orderSendAllowed",
    "closeAllowed",
    "cancelAllowed",
    "credentialStorageAllowed",
    "livePresetMutationAllowed",
    "canOverrideKillSwitch",
    "telegramCommandExecutionAllowed",
]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"OPENROUTER_API_KEY\s*=\s*['\"][^'\"]+['\"]", re.I),
    re.compile(r"TELEGRAM_BOT_TOKEN\s*=\s*['\"][^'\"]+['\"]", re.I),
]

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def all_markdown_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        yield path


def check_required_files(root: Path, errors: list[str]) -> None:
    for rel in REQUIRED_DOCS:
        if not (root / rel).exists():
            fail(errors, f"required file missing: {rel}")


def check_markdown_readability(root: Path, errors: list[str]) -> None:
    for rel in CORE_MARKDOWN:
        path = root / rel
        if not path.exists():
            continue
        text = read_text(path)
        lines = text.splitlines()
        if len(lines) < 8:
            fail(errors, f"{rel} is too short or likely compressed; line_count={len(lines)}")
        if not any(line.startswith("# ") for line in lines[:8]):
            fail(errors, f"{rel} should have a top-level H1 heading near the beginning")
        headings = [line for line in lines if line.startswith("#")]
        if len(headings) < 2:
            fail(errors, f"{rel} should contain multiple headings for readability")
        longest = max((len(line) for line in lines), default=0)
        if longest > 1400:
            fail(errors, f"{rel} has an overlong line ({longest} chars); likely compressed")


def check_all_markdown_basic(root: Path, errors: list[str]) -> None:
    for path in all_markdown_files(root):
        rel = path.relative_to(root).as_posix()
        text = read_text(path)
        if not text.strip():
            fail(errors, f"markdown file is empty: {rel}")
        if "\r" in text:
            fail(errors, f"markdown file contains CR characters: {rel}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(errors, f"possible secret in markdown file: {rel}")


def collect_endpoints(contract: dict) -> list[str]:
    endpoints: list[str] = []
    groups = contract.get("endpointGroups", [])
    if isinstance(groups, dict):
        groups = groups.values()
    for group in groups:
        if not isinstance(group, dict):
            continue
        entries = group.get("endpoints", [])
        if isinstance(entries, dict):
            entries = entries.values()
        for entry in entries:
            if isinstance(entry, str):
                endpoints.append(entry)
            elif isinstance(entry, dict):
                path = entry.get("path") or entry.get("endpoint")
                if path:
                    endpoints.append(str(path))
    flat = contract.get("endpoints", [])
    if isinstance(flat, dict):
        flat = flat.values()
    for entry in flat:
        if isinstance(entry, str):
            endpoints.append(entry)
        elif isinstance(entry, dict):
            path = entry.get("path") or entry.get("endpoint")
            if path:
                endpoints.append(str(path))
    return sorted(set(endpoints))


def check_api_contract(root: Path, errors: list[str]) -> None:
    path = root / "docs/contracts/api-contract.json"
    if not path.exists():
        fail(errors, "api contract is missing")
        return
    try:
        contract = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        fail(errors, f"api contract is invalid JSON: {exc}")
        return

    endpoints = collect_endpoints(contract)
    if len(endpoints) < 100:
        fail(errors, f"api contract endpoint count too low: {len(endpoints)} < 100")
    invalid = [endpoint for endpoint in endpoints if not endpoint.startswith("/api/")]
    if invalid:
        fail(errors, f"api contract contains non-/api endpoint(s): {invalid[:5]}")
    hfm_status = None
    for group in contract.get("endpointGroups", []):
        if not isinstance(group, dict):
            continue
        for endpoint in group.get("endpoints", []):
            if isinstance(endpoint, dict) and endpoint.get("path") == "/api/hfm-crypto/status":
                hfm_status = endpoint
                break
        if hfm_status:
            break
    if not isinstance(hfm_status, dict):
        fail(errors, "api contract must include /api/hfm-crypto/status")
    else:
        variants = hfm_status.get("queryVariants") or []
        summary = next(
            (
                variant
                for variant in variants
                if isinstance(variant, dict) and variant.get("query") == "view=summary"
            ),
            None,
        )
        if not summary:
            fail(errors, "api contract must document /api/hfm-crypto/status?view=summary")
        summary_text = json.dumps(summary or {}, ensure_ascii=False)
        status_text = json.dumps(hfm_status, ensure_ascii=False)
        if "brokerSymbolDiagnostics" not in status_text or "brokerSymbolDiagnostics" not in summary_text:
            fail(errors, "HFM summary contract must preserve brokerSymbolDiagnostics")
        if "operatorChecklist" not in status_text or "operatorChecklist" not in summary_text:
            fail(errors, "HFM summary contract must preserve operatorChecklist")
        if "safety" not in summary_text:
            fail(errors, "HFM summary contract must preserve safety flags")

    safety = contract.get("safetyDefaults") or contract.get("safety") or {}
    if not isinstance(safety, dict):
        fail(errors, "api contract safety defaults must be an object")
        return
    for field in EXECUTION_FALSE_FIELDS:
        if safety.get(field) is not False:
            fail(errors, f"api contract safety default must be false: {field}")


def check_phase_docs(root: Path, errors: list[str]) -> None:
    expected_terms = {
        "docs/phases/phase1.md": ["AI", "K", "CI"],
        "docs/phases/phase2.md": ["Vue", "API", "Telegram", "CI"],
        "docs/phases/phase3.md": ["Vibe", "Agent", "K"],
    }
    for rel, terms in expected_terms.items():
        path = root / rel
        if not path.exists():
            continue
        text = read_text(path)
        for term in terms:
            if term.lower() not in text.lower():
                fail(errors, f"{rel} should mention {term}")
        if "安全" not in text and "safety" not in text.lower():
            fail(errors, f"{rel} should describe safety boundaries")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check QuantGodDocs readability and completion")
    parser.add_argument("--root", default=".", help="QuantGodDocs root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    check_required_files(root, errors)
    check_markdown_readability(root, errors)
    check_all_markdown_basic(root, errors)
    check_api_contract(root, errors)
    check_phase_docs(root, errors)

    if errors:
        print("QuantGodDocs quality gate failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("QuantGodDocs quality gate OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
