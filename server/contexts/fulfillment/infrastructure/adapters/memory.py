from contexts.fulfillment.domain import (
    FulfillmentEvent,
    FulfillmentNote,
    FulfillmentTaskRecord,
)


class MemoryFulfillmentRepository:
    def __init__(self) -> None:
        self._tasks: dict[str, FulfillmentTaskRecord] = {}
        self._events: list[FulfillmentEvent] = []
        self._notes: list[FulfillmentNote] = []

    def initialize(self) -> None:
        return None

    def seed_tasks(self, tasks: list[FulfillmentTaskRecord]) -> None:
        self._tasks = {task.id: task for task in tasks}

    def seed_events(self, events: list[FulfillmentEvent]) -> None:
        self._events = list(events)

    def seed_notes(self, notes: list[FulfillmentNote]) -> None:
        self._notes = list(notes)

    def list_tasks(self) -> list[FulfillmentTaskRecord]:
        return list(self._tasks.values())

    def list_events(self) -> list[FulfillmentEvent]:
        return list(self._events)

    def list_notes(self) -> list[FulfillmentNote]:
        return list(self._notes)

    def update_task_status(
        self, task_id: str, status: str
    ) -> FulfillmentTaskRecord | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(update={"status": status})
        self._tasks[task_id] = updated
        return updated
