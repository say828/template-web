from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCREEN_SPEC = ROOT / "sdd/01_planning/02_screen/mobile_screen_spec.pdf"
OUTPUT_DIR = ROOT / "sdd/99_toolchain/03_templates/generated_assets"

# Template example output lives under `03_templates/generated_assets`.
# Replace this path with the consuming project's runtime asset directory.


ASSET_RECIPES = [
    {
        "id": "example-brand-lockup-source",
        "source": {"kind": "pdf_page", "path": SCREEN_SPEC, "page": 2, "dpi": 150},
        "crop_box": (294, 750, 738, 1151),
        "transparent_white_threshold": 245,
        "trim": True,
        "children": [
            {
                "id": "example-brand-lockup",
                "output": OUTPUT_DIR / "example-brand-lockup.svg",
            },
            {
                "id": "example-brand-mark",
                "crop_box": (123, 0, 288, 180),
                "output": OUTPUT_DIR / "example-brand-mark.svg",
            },
            {
                "id": "example-brand-wordmark",
                "crop_box": (50, 324, 363, 381),
                "output": OUTPUT_DIR / "example-brand-wordmark.svg",
            },
        ],
    }
]
