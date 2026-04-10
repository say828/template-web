from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PLAYWRIGHT_HARNESS_ROOT = ROOT / "research" / "agent-browser" / "pocs" / "playwright-dev-e2e"
PLAYWRIGHT_CONFIG = PLAYWRIGHT_HARNESS_ROOT / "playwright.config.js"
PLAYWRIGHT_PACKAGE = PLAYWRIGHT_HARNESS_ROOT / "package.json"
PLAYWRIGHT_RESULTS_DIR = ROOT / "research" / "agent-browser" / "results"


# Downstream repos should populate this registry with durable suite ids.
PLAYWRIGHT_SUITES: list[dict[str, object]] = []


def get_suite_by_id(suite_id: str) -> dict[str, object]:
    for suite in PLAYWRIGHT_SUITES:
        if suite["id"] == suite_id:
            return suite
    raise KeyError(suite_id)
