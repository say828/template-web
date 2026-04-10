import json
from pathlib import Path
from typing import Any


DATA_ROOT = Path(__file__).resolve().parent
BOOTSTRAP_ROOT = DATA_ROOT / "bootstrap"


def load_bootstrap_json(filename: str) -> list[dict[str, Any]]:
    with (BOOTSTRAP_ROOT / filename).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"{filename} must contain a JSON list")
    return payload
