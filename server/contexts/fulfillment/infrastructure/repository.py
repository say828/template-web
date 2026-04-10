from datetime import datetime

from contexts.fulfillment.domain import (
    FulfillmentEvent,
    FulfillmentNote,
    FulfillmentTaskRecord,
    FulfillmentTaskStatusTransition,
    FulfillmentTaskStatusTransitionCommand,
)
from data.bootstrap_loader import load_bootstrap_json

_task_store: list[FulfillmentTaskRecord] | None = None
_event_store: list[FulfillmentEvent] | None = None
_note_store: list[FulfillmentNote] | None = None


def _get_task_store() -> list[FulfillmentTaskRecord]:
    global _task_store
    if _task_store is None:
        _task_store = [
            FulfillmentTaskRecord(**entry)
            for entry in load_bootstrap_json("fulfillment_tasks.json")
        ]
    return _task_store


def _get_event_store() -> list[FulfillmentEvent]:
    global _event_store
    if _event_store is None:
        _event_store = [
            FulfillmentEvent(**entry)
            for entry in load_bootstrap_json("fulfillment_events.json")
        ]
    return _event_store


def _get_note_store() -> list[FulfillmentNote]:
    global _note_store
    if _note_store is None:
        _note_store = [
            FulfillmentNote(**entry)
            for entry in load_bootstrap_json("fulfillment_notes.json")
        ]
    return _note_store


def list_seed_fulfillment_tasks() -> list[FulfillmentTaskRecord]:
    return [task.model_copy(deep=True) for task in _get_task_store()]


def list_seed_fulfillment_events() -> list[FulfillmentEvent]:
    return [event.model_copy(deep=True) for event in _get_event_store()]


def list_seed_fulfillment_notes() -> list[FulfillmentNote]:
    return [note.model_copy(deep=True) for note in _get_note_store()]


def transition_seed_fulfillment_task_status(
    task_id: str, command: FulfillmentTaskStatusTransitionCommand
) -> FulfillmentTaskStatusTransition:
    tasks = _get_task_store()
    for index, task in enumerate(tasks):
        if task.id != task_id:
            continue

        updated_task = task.model_copy(
            update={"status": command.status, "stage": command.stage or task.stage}
        )
        tasks[index] = updated_task
        _get_event_store().insert(
            0,
            FulfillmentEvent(
                time=datetime.now().strftime("%H:%M"),
                title=f"{updated_task.order_id} {updated_task.title} -> {updated_task.status}",
                tone=_map_event_tone(updated_task.status),
            ),
        )
        return FulfillmentTaskStatusTransition(
            task_id=updated_task.id,
            previous_status=task.status,
            status=updated_task.status,
            previous_stage=task.stage,
            stage=updated_task.stage,
        )

    raise LookupError(f"Fulfillment task {task_id} not found")


def _map_event_tone(status: str) -> str:
    tone_map = {
        "Queued": "accent",
        "In progress": "warning",
        "Blocked": "warning",
        "Completed": "success",
    }
    return tone_map.get(status, "neutral")
