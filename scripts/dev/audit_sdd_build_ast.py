#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SERVICE_DOCS = {
    "mobile": ROOT / "sdd/03_build/01_feature/service/mobile_surface.md",
    "web": ROOT / "sdd/03_build/01_feature/service/web_surface.md",
    "admin": ROOT / "sdd/03_build/01_feature/service/admin_surface.md",
    "landing": ROOT / "sdd/03_build/01_feature/service/landing_surface.md",
}

BUILD_AST_DOC = ROOT / "sdd/03_build/03_architecture/build_ast_runtime_tree_governance.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def score(value: float, maximum: float) -> int:
    if maximum <= 0:
        return 0
    scaled = round((value / maximum) * 10)
    return max(0, min(10, scaled))


def contains_all(text: str, needles: list[str]) -> bool:
    return all(needle in text for needle in needles)


def ast_similarity() -> tuple[int, list[str]]:
    findings: list[str] = []
    points = 0.0
    maximum = 10.0

    mobile = read(SERVICE_DOCS["mobile"])
    if contains_all(
        mobile,
        [
            "client/mobile/src/main.tsx",
            "AuthProvider",
            "BrowserRouter",
            "client/mobile/src/app/App.tsx",
            "ProtectedRoute",
            "InShell",
            "DashboardPage",
            "FulfillmentPage",
            "ShippingPage",
        ],
    ):
        points += 2.5
    else:
        findings.append("mobile surface summary does not reflect the real provider/router/shell chain.")

    web = read(SERVICE_DOCS["web"])
    if contains_all(
        web,
        [
            "client/web/src/main.tsx",
            "AuthProvider",
            "BrowserRouter",
            "client/web/src/app/App.tsx",
            "ProtectedRoute",
            "AppShell",
            "DashboardPage",
            "OrdersPage",
        ],
    ):
        points += 2.5
    else:
        findings.append("web surface summary does not reflect the real app shell route tree.")

    admin = read(SERVICE_DOCS["admin"])
    if contains_all(
        admin,
        [
            "client/admin/src/main.tsx",
            "AuthProvider",
            "BrowserRouter",
            "client/admin/src/app/App.tsx",
            "ProtectedRoute",
            "AdminShell",
            "AdminDashboardPage",
            "AdminQueuePage",
            "AdminSupportPage",
        ],
    ):
        points += 2.5
    else:
        findings.append("admin surface summary does not reflect the real admin shell route tree.")

    landing = read(SERVICE_DOCS["landing"])
    if contains_all(
        landing,
        [
            "client/landing/src/main.tsx",
            "AuthProvider",
            "BrowserRouter",
            "client/landing/src/App.tsx",
            "LandingHomePage",
            "LandingLoginPage",
            "ProtectedRoute",
            "LandingShell",
            "LandingWorkspacePage",
        ],
    ):
        points += 2.5
    else:
        findings.append("landing surface summary does not reflect the public and gated route assembly.")

    return score(points, maximum), findings


def implementation_traceability() -> tuple[int, list[str]]:
    findings: list[str] = []
    points = 0.0
    maximum = 10.0

    mobile = read(SERVICE_DOCS["mobile"])
    if contains_all(
        mobile,
        [
            "server/main.py",
            "server/api/http/app.py",
            "server/api/http/router.py",
            "contexts/auth/contracts/http/router.py",
            "contexts/fulfillment/contracts/http/router.py",
            "contexts/shipping/contracts/http/router.py",
        ],
    ):
        points += 2.0
    else:
        findings.append("mobile surface summary does not trace route leaves to backend contract leaves.")

    web = read(SERVICE_DOCS["web"])
    if contains_all(
        web,
        [
            "server/main.py",
            "server/api/http/app.py",
            "server/api/http/router.py",
            "contexts/auth/contracts/http/router.py",
            "contexts/catalog/contracts/http/router.py",
            "contexts/orders/contracts/http/router.py",
        ],
    ):
        points += 2.0
    else:
        findings.append("web surface summary does not trace dashboard and orders routes to backend contracts.")

    admin = read(SERVICE_DOCS["admin"])
    if contains_all(
        admin,
        [
            "server/main.py",
            "server/api/http/app.py",
            "server/api/http/router.py",
            "contexts/alerts/contracts/http/router.py",
            "contexts/inventory/contracts/http/router.py",
            "contexts/support/contracts/http/router.py",
        ],
    ):
        points += 2.0
    else:
        findings.append("admin surface summary does not trace admin routes to backend contracts.")

    landing = read(SERVICE_DOCS["landing"])
    if contains_all(
        landing,
        [
            "server/main.py",
            "server/api/http/app.py",
            "server/api/http/router.py",
            "contexts/catalog/contracts/http/router.py",
            "contexts/health/contracts/http/router.py",
            "contexts/user/contracts/http/router.py",
        ],
    ):
        points += 2.0
    else:
        findings.append("landing surface summary does not trace public/workspace routes to backend contracts.")

    architecture = read(BUILD_AST_DOC)
    if contains_all(
        architecture,
        [
            ".agent/ralph.sh",
            ".claude/agents/",
            ".codex/skills/SKILL.md",
            "infra/terraform/README.md",
        ],
    ):
        points += 2.0
    else:
        findings.append("build AST architecture summary does not retain the canonical harness and infra roots.")

    return score(points, maximum), findings


def human_agent_readability() -> tuple[int, list[str]]:
    findings: list[str] = []
    points = 10.0
    maximum = 10.0

    build_md_files = sorted((ROOT / "sdd/03_build").rglob("*.md"))
    combined = "\n".join(read(path) for path in build_md_files)

    pattern_penalties = [
        (r"## Current Build Note", 2.0, "build docs still use a Current Build Note section instead of current-state structure."),
        (r"\bRalph\b", 2.0, "build docs still contain Ralph loop narrative."),
        (r"2026-\d{2}-\d{2}", 2.0, "build docs still contain dated history markers."),
        (r"이번 턴", 1.0, "build docs still contain turn-specific execution narrative."),
        (r"run `\d+", 1.0, "build docs still contain run-id style execution narrative."),
        (r"\biteration\b", 1.0, "build docs still contain iteration-oriented loop narrative."),
    ]

    for pattern, penalty, message in pattern_penalties:
        if re.search(pattern, combined):
            points -= penalty
            findings.append(message)

    for path in SERVICE_DOCS.values():
        if len(read(path).splitlines()) > 80:
            points -= 0.5
            findings.append(f"{path.name} is too large to serve as a concise runtime tree summary.")

    if points < 0:
        points = 0

    return score(points, maximum), findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, default=None)
    args = parser.parse_args()

    ast_score, ast_findings = ast_similarity()
    trace_score, trace_findings = implementation_traceability()
    readability_score, readability_findings = human_agent_readability()

    payload = {
        "scores": {
            "ast_similarity": ast_score,
            "implementation_traceability": trace_score,
            "human_agent_readability": readability_score,
        },
        "all_ten": ast_score == 10 and trace_score == 10 and readability_score == 10,
        "findings": {
            "ast_similarity": ast_findings,
            "implementation_traceability": trace_findings,
            "human_agent_readability": readability_findings,
        },
    }

    output = json.dumps(payload, ensure_ascii=False, indent=2)
    print(output)

    if args.write is not None:
        target = args.write
        if not target.is_absolute():
            target = ROOT / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output + "\n", encoding="utf-8")

    return 0 if payload["all_ten"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
