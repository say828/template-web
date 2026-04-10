from contexts.alerts.domain import AlertRecord
from data.bootstrap_loader import load_bootstrap_json

_alert_store: list[AlertRecord] | None = None


def _get_alert_store() -> list[AlertRecord]:
    global _alert_store
    if _alert_store is None:
        _alert_store = [
            AlertRecord(**entry) for entry in load_bootstrap_json("alerts.json")
        ]
    return _alert_store


def list_seed_alerts() -> list[AlertRecord]:
    return [record.model_copy(deep=True) for record in _get_alert_store()]


def mark_seed_alert_read(alert_id: str) -> AlertRecord:
    records = _get_alert_store()
    for index, record in enumerate(records):
        if record.id != alert_id:
            continue

        updated_record = record.model_copy(update={"read": True})
        records[index] = updated_record
        return updated_record.model_copy(deep=True)

    raise LookupError(f"Alert {alert_id} not found")


def mark_all_seed_alerts_read() -> int:
    records = _get_alert_store()
    updated_count = 0
    for index, record in enumerate(records):
        if record.read:
            continue
        records[index] = record.model_copy(update={"read": True})
        updated_count += 1
    return updated_count
