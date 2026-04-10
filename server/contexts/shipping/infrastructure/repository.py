from contexts.shipping.domain import (
    ShipmentRecord,
    ShipmentStatusTransition,
    UpdateShipmentStatusCommand,
)
from data.bootstrap_loader import load_bootstrap_json

_shipment_store: list[ShipmentRecord] | None = None


def _get_shipment_store() -> list[ShipmentRecord]:
    global _shipment_store
    if _shipment_store is None:
        _shipment_store = [
            ShipmentRecord(**entry)
            for entry in load_bootstrap_json("shipping_shipments.json")
        ]
    return _shipment_store


def list_seed_shipments() -> list[ShipmentRecord]:
    return [record.model_copy(deep=True) for record in _get_shipment_store()]


def transition_seed_shipment_status(
    shipment_id: str, command: UpdateShipmentStatusCommand
) -> ShipmentStatusTransition:
    records = _get_shipment_store()
    for index, record in enumerate(records):
        if record.shipment_id != shipment_id:
            continue

        updated_record = record.model_copy(
            update={
                "status": command.status,
                "last_event": command.last_event,
                "eta": command.eta or record.eta,
                "delivered_today": command.status == "Delivered",
            }
        )
        records[index] = updated_record
        return ShipmentStatusTransition(
            shipment_id=updated_record.shipment_id,
            previous_status=record.status,
            status=updated_record.status,
            previous_last_event=record.last_event,
            last_event=updated_record.last_event,
        )

    raise LookupError(f"Shipment {shipment_id} not found")
