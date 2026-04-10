from datetime import datetime, timezone
from functools import lru_cache

from fastapi import HTTPException, status as http_status

from contexts.inventory.domain import (
    AdjustInventoryCommand,
    InventoryAvailabilityStatus,
    InventoryLevel,
    InventoryLevelRecord,
    InventoryMutationReceipt,
    ReleaseInventoryCommand,
    ReserveInventoryCommand,
    SetInventoryLevelCommand,
)
from contexts.inventory.infrastructure import get_inventory_repository
from data.bootstrap_loader import load_bootstrap_json


def list_inventory_levels(
    sku: str | None = None,
    product_id: str | None = None,
    location_id: str | None = None,
    availability_status: InventoryAvailabilityStatus | None = None,
) -> list[InventoryLevel]:
    prepare_inventory_store()
    repository = get_inventory_repository()
    levels = repository.list_levels()

    if sku is not None:
        normalized_sku = sku.strip().casefold()
        levels = [level for level in levels if level.sku.casefold() == normalized_sku]
    if product_id is not None:
        normalized_product_id = product_id.strip().casefold()
        levels = [level for level in levels if level.product_id.casefold() == normalized_product_id]
    if location_id is not None:
        normalized_location_id = location_id.strip().casefold()
        levels = [level for level in levels if level.location_id.casefold() == normalized_location_id]
    if availability_status is not None:
        levels = [level for level in levels if _availability_status(level) == availability_status]

    return [_to_level(level) for level in levels]


def get_inventory_level_or_404(sku: str, location_id: str) -> InventoryLevel:
    prepare_inventory_store()
    repository = get_inventory_repository()
    level = repository.get_level(sku, location_id)
    if level is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Inventory level not found")
    return _to_level(level)


def adjust_inventory_level_or_404(
    sku: str,
    location_id: str,
    command: AdjustInventoryCommand,
) -> InventoryMutationReceipt:
    prepare_inventory_store()
    repository = get_inventory_repository()
    level = repository.get_level(sku, location_id)
    if level is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Inventory level not found")
    if command.quantity_delta == 0:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Adjustment delta must not be zero")

    next_on_hand = level.on_hand + command.quantity_delta
    if next_on_hand < level.reserved:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Adjustment would reduce on-hand stock below reserved stock",
        )

    updated = level.model_copy(update={"on_hand": next_on_hand, "updated_at": _now_iso()})
    repository.upsert_level(updated)
    return InventoryMutationReceipt(
        action="adjusted",
        sku=updated.sku,
        location_id=updated.location_id,
        quantity=command.quantity_delta,
        reference_id=command.reference_id,
        reason=command.reason,
        level=_to_level(updated),
    )


def reserve_inventory_or_404(
    sku: str,
    location_id: str,
    command: ReserveInventoryCommand,
) -> InventoryMutationReceipt:
    prepare_inventory_store()
    repository = get_inventory_repository()
    level = repository.get_level(sku, location_id)
    if level is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Inventory level not found")
    available_to_sell = level.on_hand - level.reserved
    if command.quantity > available_to_sell:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail="Not enough available stock to reserve")

    updated = level.model_copy(update={"reserved": level.reserved + command.quantity, "updated_at": _now_iso()})
    repository.upsert_level(updated)
    return InventoryMutationReceipt(
        action="reserved",
        sku=updated.sku,
        location_id=updated.location_id,
        quantity=command.quantity,
        reference_id=command.reference_id,
        reason=command.channel,
        level=_to_level(updated),
    )


def release_inventory_level_or_404(
    sku: str,
    location_id: str,
    command: ReleaseInventoryCommand,
) -> InventoryMutationReceipt:
    prepare_inventory_store()
    repository = get_inventory_repository()
    level = repository.get_level(sku, location_id)
    if level is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Inventory level not found")
    if command.quantity > level.reserved:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail="Release quantity exceeds reserved stock")

    updated = level.model_copy(update={"reserved": level.reserved - command.quantity, "updated_at": _now_iso()})
    repository.upsert_level(updated)
    return InventoryMutationReceipt(
        action="released",
        sku=updated.sku,
        location_id=updated.location_id,
        quantity=command.quantity,
        reference_id=command.reference_id,
        reason=command.reason,
        level=_to_level(updated),
    )


def set_inventory_level_or_404(
    sku: str,
    location_id: str,
    command: SetInventoryLevelCommand,
) -> InventoryMutationReceipt:
    prepare_inventory_store()
    repository = get_inventory_repository()
    current = repository.get_level(sku, location_id)
    if current is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Inventory level not found")

    updated = current.model_copy(
        update={
            "on_hand": command.on_hand,
            "reserved": command.reserved,
            "safety_stock": command.safety_stock,
            "reorder_point": command.reorder_point,
            "updated_at": _now_iso(),
        }
    )
    repository.upsert_level(updated)
    return InventoryMutationReceipt(
        action="set",
        sku=updated.sku,
        location_id=updated.location_id,
        quantity=updated.on_hand - current.on_hand,
        reference_id=command.reference_id,
        reason=command.reason,
        level=_to_level(updated),
    )


def prepare_inventory_store() -> None:
    _seed_inventory_store()


@lru_cache
def _seed_inventory_store() -> None:
    repository = get_inventory_repository()
    repository.initialize()
    levels = [InventoryLevelRecord(**entry) for entry in load_bootstrap_json("inventory_levels.json")]
    repository.seed_levels(levels)


def _to_level(level: InventoryLevelRecord) -> InventoryLevel:
    available_to_sell = max(level.on_hand - level.reserved, 0)
    return InventoryLevel(
        sku=level.sku,
        product_id=level.product_id,
        product_name=level.product_name,
        variant_name=level.variant_name,
        location_id=level.location_id,
        location_name=level.location_name,
        on_hand=level.on_hand,
        reserved=level.reserved,
        available_to_sell=available_to_sell,
        safety_stock=level.safety_stock,
        reorder_point=level.reorder_point,
        needs_reorder=available_to_sell <= level.reorder_point,
        status=_availability_status(level),
        updated_at=level.updated_at,
    )


def _availability_status(level: InventoryLevelRecord) -> InventoryAvailabilityStatus:
    available_to_sell = max(level.on_hand - level.reserved, 0)
    if available_to_sell == 0:
        return "out_of_stock"
    if available_to_sell <= level.reorder_point:
        return "low_stock"
    return "in_stock"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
