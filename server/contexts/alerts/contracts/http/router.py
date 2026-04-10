from fastapi import APIRouter, Depends, HTTPException

from contexts.alerts.application import (
    get_alerts,
    mark_alert_read,
    mark_all_alerts_read,
)
from contexts.alerts.domain import (
    AlertReadResult,
    AlertsPayload,
    AlertsReadAllResult,
)
from contexts.auth.contracts.http.dependencies import require_admin_user

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    dependencies=[Depends(require_admin_user)],
)


@router.get("", response_model=AlertsPayload)
def list_alerts() -> AlertsPayload:
    return get_alerts()


@router.post("/read-all", response_model=AlertsReadAllResult)
def read_all_alerts() -> AlertsReadAllResult:
    return mark_all_alerts_read()


@router.post("/{alert_id}/read", response_model=AlertReadResult)
def read_alert(alert_id: str) -> AlertReadResult:
    try:
        return mark_alert_read(alert_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
