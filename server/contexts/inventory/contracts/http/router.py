from fastapi import APIRouter, Depends, Query

from contexts.auth.contracts.http.dependencies import require_admin_user
from contexts.inventory.application import (
    adjust_inventory_level_or_404,
    get_inventory_level_or_404,
    list_inventory_levels,
    release_inventory_level_or_404,
    reserve_inventory_or_404,
    set_inventory_level_or_404,
)
from contexts.inventory.domain import (
    AdjustInventoryCommand,
    InventoryAvailabilityStatus,
    InventoryLevel,
    InventoryMutationReceipt,
    ReleaseInventoryCommand,
    ReserveInventoryCommand,
    SetInventoryLevelCommand,
)

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(require_admin_user)],
)


@router.get("/levels", response_model=list[InventoryLevel])
def list_levels(
    sku: str | None = Query(default=None),
    product_id: str | None = Query(default=None),
    location_id: str | None = Query(default=None),
    status: InventoryAvailabilityStatus | None = Query(default=None),
) -> list[InventoryLevel]:
    return list_inventory_levels(
        sku=sku,
        product_id=product_id,
        location_id=location_id,
        availability_status=status,
    )


@router.get("/levels/{sku}/{location_id}", response_model=InventoryLevel)
def get_level(sku: str, location_id: str) -> InventoryLevel:
    return get_inventory_level_or_404(sku, location_id)


@router.post("/levels/{sku}/{location_id}/adjustments", response_model=InventoryMutationReceipt)
def post_adjustment(
    sku: str,
    location_id: str,
    command: AdjustInventoryCommand,
) -> InventoryMutationReceipt:
    return adjust_inventory_level_or_404(sku, location_id, command)


@router.post("/levels/{sku}/{location_id}/reservations", response_model=InventoryMutationReceipt)
def post_reservation(
    sku: str,
    location_id: str,
    command: ReserveInventoryCommand,
) -> InventoryMutationReceipt:
    return reserve_inventory_or_404(sku, location_id, command)


@router.post("/levels/{sku}/{location_id}/releases", response_model=InventoryMutationReceipt)
def post_release(
    sku: str,
    location_id: str,
    command: ReleaseInventoryCommand,
) -> InventoryMutationReceipt:
    return release_inventory_level_or_404(sku, location_id, command)


@router.put("/levels/{sku}/{location_id}", response_model=InventoryMutationReceipt)
def put_level(
    sku: str,
    location_id: str,
    command: SetInventoryLevelCommand,
) -> InventoryMutationReceipt:
    return set_inventory_level_or_404(sku, location_id, command)
