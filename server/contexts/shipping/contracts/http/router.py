from fastapi import APIRouter, Depends, HTTPException

from contexts.auth.contracts.http.dependencies import require_authenticated_user
from contexts.shipping.application import (
    get_shipment_list,
    get_shipping_overview,
    transition_shipment_status,
)
from contexts.shipping.domain import (
    ShippingOverview,
    ShipmentStatusTransition,
    ShipmentSummary,
    UpdateShipmentStatusCommand,
)

router = APIRouter(
    prefix="/shipping",
    tags=["shipping"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.get("/overview", response_model=ShippingOverview)
def shipping_overview() -> ShippingOverview:
    return get_shipping_overview()


@router.get("/shipments", response_model=list[ShipmentSummary])
def list_shipments() -> list[ShipmentSummary]:
    return get_shipment_list()


@router.patch("/shipments/{shipment_id}/status", response_model=ShipmentStatusTransition)
def patch_shipment_status(
    shipment_id: str, command: UpdateShipmentStatusCommand
) -> ShipmentStatusTransition:
    try:
        return transition_shipment_status(shipment_id, command)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
