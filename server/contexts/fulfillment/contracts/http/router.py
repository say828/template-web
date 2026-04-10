from fastapi import APIRouter, Depends, HTTPException

from contexts.auth.contracts.http.dependencies import require_authenticated_user
from contexts.fulfillment.application import (
    get_fulfillment_board,
    get_fulfillment_overview,
    transition_fulfillment_task_status,
)
from contexts.fulfillment.domain import (
    FulfillmentBoardPayload,
    FulfillmentOverview,
    FulfillmentTaskStatusTransition,
    FulfillmentTaskStatusTransitionCommand,
)

router = APIRouter(
    prefix="/fulfillment",
    tags=["fulfillment"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.get("/overview", response_model=FulfillmentOverview)
def fulfillment_overview() -> FulfillmentOverview:
    return get_fulfillment_overview()


@router.get("/board", response_model=FulfillmentBoardPayload)
def fulfillment_board() -> FulfillmentBoardPayload:
    return get_fulfillment_board()


@router.patch("/tasks/{task_id}/status", response_model=FulfillmentTaskStatusTransition)
def transition_task_status(
    task_id: str, command: FulfillmentTaskStatusTransitionCommand
) -> FulfillmentTaskStatusTransition:
    try:
        return transition_fulfillment_task_status(task_id, command)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
