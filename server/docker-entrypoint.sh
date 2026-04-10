#!/usr/bin/env bash
set -Eeuo pipefail

cd /app/server

python - <<'PY'
import os
import socket
import time
from urllib.parse import urlparse


DEFAULT_PORTS = {
    "postgresql": 5432,
    "postgresql+psycopg": 5432,
    "mysql": 3306,
    "mongodb": 27017,
}


def wait_for(url: str, label: str, timeout: float = 60.0) -> None:
    parsed = urlparse(url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or DEFAULT_PORTS.get(parsed.scheme, 80)
    deadline = time.time() + timeout
    last_error = None

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError as exc:
            last_error = exc
            time.sleep(1)

    raise SystemExit(f"Timed out waiting for {label} at {host}:{port}: {last_error}")


backend = os.environ.get("DATABASE_BACKEND", "memory").lower()
urls = {
    "postgres": os.environ.get("POSTGRES_URL", ""),
    "mysql": os.environ.get("MYSQL_URL", ""),
    "mariadb": os.environ.get("MARIADB_URL", ""),
    "mongodb": os.environ.get("MONGODB_URL", ""),
}

target_url = urls.get(backend)
if backend != "memory" and target_url:
    wait_for(target_url, backend)
PY

exec uvicorn api.http.app:app \
    --host 0.0.0.0 \
    --port "${SERVER_HTTP_PORT:-8000}" \
    --reload \
    --reload-dir /app/server
