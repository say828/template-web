from fastapi import APIRouter

from contexts.health.application import get_status_payload

router = APIRouter(tags=["health"])


@router.get("/status")
def status() -> dict[str, str]:
    return get_status_payload()
