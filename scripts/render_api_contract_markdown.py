#!/usr/bin/env python3
"""Render docs/backend/api-contract.md from docs/contracts/api-contract.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_contract(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def endpoint_rows(endpoints: list[dict]) -> list[str]:
    rows = ["| Method | Path | Mode | Notes |", "|---|---|---|---|"]
    for endpoint in endpoints:
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "")
        mode = endpoint.get("mode", "read-only")
        notes = endpoint.get("description") or endpoint.get("source") or ""
        variants = endpoint.get("queryVariants") or []
        if isinstance(variants, list) and variants:
            rendered_variants = []
            for variant in variants:
                if not isinstance(variant, dict):
                    continue
                query = variant.get("query")
                description = variant.get("description") or variant.get("mode") or ""
                if query:
                    rendered_variants.append(f"`?{query}`: {description}")
            if rendered_variants:
                notes = f"{notes} Query variants: {'; '.join(rendered_variants)}"
        rows.append(f"| {method} | `{path}` | `{mode}` | {notes} |")
    return rows


def render(contract: dict) -> str:
    groups = contract.get("endpointGroups", [])
    total = sum(len(group.get("endpoints", [])) for group in groups)
    safety = contract.get("safetyDefaults", {})

    lines: list[str] = [
        "# QuantGod Backend API Contract",
        "",
        "本文由 `docs/contracts/api-contract.json` 渲染生成，用于人工 review。",
        "机器可读版本仍以 JSON contract 为准。",
        "",
        "## Contract 摘要",
        "",
        f"- Endpoint 总数：`{total}`。",
        f"- Backend API base：`{contract.get('backendApiBaseUrl', 'http://127.0.0.1:8080/api')}`。",
        "- Backend `/api/*` route surface 以 `QuantGodBackend/tools/api_route_registry.py` 输出为准。",
        "- 任何新增、删除或重命名 `/api/*` route，都必须同步更新 JSON contract、本文档和 Frontend service wrapper。",
        "",
        "## 通用安全语义",
        "",
        "Phase 1/2/3 的 API contract 必须保持本地优先和安全受控：",
        "",
        "| 字段 | 期望值 | 含义 |",
        "|---|---:|---|",
    ]

    for key in [
        "localOnly",
        "advisoryOnly",
        "readOnlyDataPlane",
        "orderSendAllowed",
        "closeAllowed",
        "cancelAllowed",
        "credentialStorageAllowed",
        "livePresetMutationAllowed",
        "canOverrideKillSwitch",
        "canMutateGovernanceDecision",
        "telegramCommandExecutionAllowed",
    ]:
        if key in safety:
            value = str(safety.get(key)).lower()
            lines.append(f"| `{key}` | `{value}` | Contract default |")

    lines.extend(
        [
            "",
            "`guarded-control` 不代表开放交易权限。它只表示 endpoint 是受控动作面，",
            "仍必须受 Backend、EA、dryRun、Kill Switch 和手动授权约束。",
            "",
            "## Endpoint Groups",
            "",
        ]
    )

    for group in groups:
        name = group.get("name", "unnamed")
        phase = group.get("phase", "unknown")
        endpoints = group.get("endpoints", [])
        lines.extend(
            [
                f"### {name}",
                "",
                f"- Phase / Domain：`{phase}`。",
                f"- Endpoint 数量：`{len(endpoints)}`。",
                "",
            ]
        )
        lines.extend(endpoint_rows(endpoints))
        lines.append("")

    lines.extend(
        [
            "## 更新清单",
            "",
            "Backend route surface 变化时，按下面顺序维护：",
            "",
            "1. 先更新 Backend route 和 Node/Python contract tests。",
            "2. 运行 `python ../QuantGodBackend/tools/api_route_registry.py --format json` 确认 Backend route registry 已暴露新路由。",
            "3. 再更新 `docs/contracts/api-contract.json`。",
            "4. 运行 `python scripts/render_api_contract_markdown.py` 重新生成本文。",
            "5. 更新 Frontend service wrapper，确保前端仍只走 `/api/*`。",
            "6. 运行跨仓库对齐检查：",
            "",
            "```powershell",
            "python scripts\\check_api_contract_matches_backend.py `",
            "  --contract docs\\contracts\\api-contract.json `",
            "  --backend ..\\QuantGodBackend",
            "```",
            "",
        ]
    )

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="docs/contracts/api-contract.json")
    parser.add_argument("--output", default="docs/backend/api-contract.md")
    args = parser.parse_args(argv)

    contract_path = Path(args.contract)
    output_path = Path(args.output)
    contract = load_contract(contract_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(contract), encoding="utf-8")
    print(f"Rendered {output_path} from {contract_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
