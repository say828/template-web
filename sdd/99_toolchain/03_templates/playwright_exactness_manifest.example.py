from __future__ import annotations


PLAYWRIGHT_SUITES = [
    {
        "id": "service-screen-batch",
        "spec": "service-screen-batch.spec.js",
        "kind": "screen-exactness",
        "service": "mobile",
        "targets": ["SERVICE-S001", "SERVICE-S002"],
        "description": "example screen exactness batch",
    },
    {
        "id": "shared-shell-regression",
        "spec": "shared-shell-regression.spec.js",
        "kind": "shared-ui-regression",
        "service": "web",
        "targets": ["shared-shell"],
        "description": "example shared shell regression batch",
    },
]
