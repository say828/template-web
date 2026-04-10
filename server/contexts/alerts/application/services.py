from contexts.alerts.domain import (
    AlertItem,
    AlertReadResult,
    AlertsPayload,
    AlertsReadAllResult,
)
from contexts.alerts.infrastructure import (
    list_seed_alerts,
    mark_all_seed_alerts_read,
    mark_seed_alert_read,
)


def _to_alert_item(record: AlertItem) -> AlertItem:
    return AlertItem(**record.model_dump())


def get_alerts() -> AlertsPayload:
    records = list_seed_alerts()
    return AlertsPayload(
        unread_count=sum(1 for record in records if not record.read),
        items=[_to_alert_item(record) for record in records],
    )


def mark_alert_read(alert_id: str) -> AlertReadResult:
    record = mark_seed_alert_read(alert_id)
    return AlertReadResult(**record.model_dump())


def mark_all_alerts_read() -> AlertsReadAllResult:
    updated_count = mark_all_seed_alerts_read()
    unread_count = sum(1 for record in list_seed_alerts() if not record.read)
    return AlertsReadAllResult(
        updated_count=updated_count,
        unread_count=unread_count,
    )


def prepare_alert_store() -> None:
    list_seed_alerts()
