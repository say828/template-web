from fastapi import APIRouter, Depends, HTTPException

from contexts.auth.contracts.http.dependencies import (
    require_admin_user,
    require_authenticated_user,
)
from contexts.orders.application import (
    create_order as create_order_service,
    get_admin_order_overview,
    get_admin_queue,
    get_order_list,
    get_order_overview,
    update_order_status as update_order_status_service,
)
from contexts.orders.domain import (
    AdminOrderOverview,
    AdminQueueItem,
    CreateOrderCommand,
    OrderOverview,
    OrderRecord,
    OrderStatusTransition,
    OrderSummary,
    UpdateOrderStatusCommand,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get(
    "/overview",
    response_model=OrderOverview,
    dependencies=[Depends(require_authenticated_user)],
)
def order_overview() -> OrderOverview:
    return get_order_overview()


@router.get("", response_model=list[OrderSummary], dependencies=[Depends(require_authenticated_user)])
def list_orders() -> list[OrderSummary]:
    return get_order_list()


@router.post(
    "",
    response_model=OrderRecord,
    status_code=201,
    dependencies=[Depends(require_authenticated_user)],
)
def create_order(command: CreateOrderCommand) -> OrderRecord:
    return create_order_service(command)


@router.get(
    "/admin/overview",
    response_model=AdminOrderOverview,
    dependencies=[Depends(require_admin_user)],
)
def admin_order_overview() -> AdminOrderOverview:
    return get_admin_order_overview()


@router.get(
    "/admin/queue",
    response_model=list[AdminQueueItem],
    dependencies=[Depends(require_admin_user)],
)
def admin_queue() -> list[AdminQueueItem]:
    return get_admin_queue()


@router.patch(
    "/{order_id}/status",
    response_model=OrderStatusTransition,
    dependencies=[Depends(require_authenticated_user)],
)
def update_order_status(
    order_id: str, command: UpdateOrderStatusCommand
) -> OrderStatusTransition:
    try:
        return update_order_status_service(order_id, command)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
