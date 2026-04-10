from datetime import date

from contexts.orders.domain import (
    CreateOrderCommand,
    OrderRecord,
    OrderStatusTransition,
    UpdateOrderStatusCommand,
)
from data.bootstrap_loader import load_bootstrap_json

_order_store: list[OrderRecord] | None = None


def _get_order_store() -> list[OrderRecord]:
    global _order_store
    if _order_store is None:
        _order_store = [
            OrderRecord(**entry) for entry in load_bootstrap_json("orders.json")
        ]
    return _order_store


def _copy_orders(records: list[OrderRecord]) -> list[OrderRecord]:
    return [record.model_copy(deep=True) for record in records]


def _next_order_number(records: list[OrderRecord]) -> int:
    return max((int(record.id.split("-")[-1]) for record in records), default=24050) + 1


def _derive_fulfillment_status(status: str, current_status: str | None = None) -> str:
    fulfillment_status_map = {
        "Pending": "Queued",
        "Paid": "Picking",
        "At risk": "Exception",
        "Completed": "Delivered",
        "Cancelled": "Cancelled",
    }
    return fulfillment_status_map.get(status, current_status or "Queued")


def _derive_risk(status: str, current_risk: str | None = None) -> str:
    if status == "At risk":
        return "risk"
    if status in {"Approved", "Completed"}:
        return "ok"
    return current_risk or "ok"


def list_seed_orders() -> list[OrderRecord]:
    return _copy_orders(_get_order_store())


def create_seed_order(command: CreateOrderCommand) -> OrderRecord:
    records = _get_order_store()
    next_order_number = _next_order_number(records)
    today = date.today().strftime("%Y.%m.%d")
    record = OrderRecord(
        id=f"ORD-{next_order_number:05d}",
        product_id=command.product_id,
        product_name=command.product_name,
        customer_name=command.customer_name,
        seller_name=command.seller_name,
        status=command.status,
        fulfillment_status=command.fulfillment_status,
        created_at=today,
        amount_krw=command.amount_krw,
        risk=_derive_risk(command.status),
        stage=command.stage,
        sla=command.sla,
        is_new_today=True,
    )
    records.insert(0, record)
    return record.model_copy(deep=True)


def update_seed_order_status(
    order_id: str, command: UpdateOrderStatusCommand
) -> OrderStatusTransition:
    records = _get_order_store()
    for index, record in enumerate(records):
        if record.id != order_id:
            continue

        updated_record = record.model_copy(
            update={
                "status": command.status,
                "fulfillment_status": command.fulfillment_status
                or _derive_fulfillment_status(command.status, record.fulfillment_status),
                "risk": _derive_risk(command.status, record.risk),
                "stage": command.stage or record.stage,
            }
        )
        records[index] = updated_record
        return OrderStatusTransition(
            id=updated_record.id,
            previous_status=record.status,
            status=updated_record.status,
            fulfillment_status=updated_record.fulfillment_status,
            risk=updated_record.risk,
            stage=updated_record.stage,
        )

    raise LookupError(f"Order {order_id} not found")
