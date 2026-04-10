from collections import Counter

from contexts.fulfillment.domain import (
    FulfillmentBoardItem,
    FulfillmentBoardPayload,
    FulfillmentOverview,
    FulfillmentStageLoad,
    FulfillmentStat,
    FulfillmentTaskStatusTransition,
    FulfillmentTaskStatusTransitionCommand,
)
from contexts.fulfillment.infrastructure import (
    list_seed_fulfillment_events,
    list_seed_fulfillment_notes,
    list_seed_fulfillment_tasks,
    transition_seed_fulfillment_task_status,
)


def get_fulfillment_overview() -> FulfillmentOverview:
    tasks = list_seed_fulfillment_tasks()
    stage_counts = Counter(task.stage for task in tasks if task.status != "Completed")
    blocked_count = sum(1 for task in tasks if task.status == "Blocked")
    active_count = sum(
        1 for task in tasks if task.status in {"Queued", "In progress", "Blocked"}
    )
    outbound_count = sum(
        1 for task in tasks if task.stage == "Outbound" and task.status != "Completed"
    )

    return FulfillmentOverview(
        throughput_total=str(sum(task.units for task in tasks)),
        stats=[
            FulfillmentStat(
                label="Open tasks", value=str(active_count), tone="text-[#22314d]"
            ),
            FulfillmentStat(
                label="Blocked",
                value=str(blocked_count),
                tone="text-[var(--app-danger)]",
            ),
            FulfillmentStat(
                label="Outbound ready",
                value=str(outbound_count),
                tone="text-[var(--app-accent)]",
            ),
        ],
        timeline=list_seed_fulfillment_events(),
        stage_load=[
            FulfillmentStageLoad(label=label, value=f"{count}건")
            for label, count in stage_counts.items()
        ],
    )


def get_fulfillment_board() -> FulfillmentBoardPayload:
    tasks = list_seed_fulfillment_tasks()
    return FulfillmentBoardPayload(
        tasks=[
            FulfillmentBoardItem(
                id=task.id,
                order_id=task.order_id,
                title=task.title,
                assignee=task.assignee,
                stage=task.stage,
                status=task.status,
                priority=task.priority,
                sla=f"{task.sla_minutes} min",
            )
            for task in tasks
        ],
        notes=list_seed_fulfillment_notes(),
    )


def transition_fulfillment_task_status(
    task_id: str, command: FulfillmentTaskStatusTransitionCommand
) -> FulfillmentTaskStatusTransition:
    return transition_seed_fulfillment_task_status(task_id, command)


def prepare_fulfillment_store() -> None:
    list_seed_fulfillment_tasks()
    list_seed_fulfillment_events()
    list_seed_fulfillment_notes()
