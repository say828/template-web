from contexts.orders.domain import (
    AdminOrderOverview,
    AdminQueueItem,
    CreateOrderCommand,
    DashboardStat,
    OrderActivity,
    OrderDetail,
    OrderOverview,
    OrderRecord,
    OrderStatusTransition,
    OrderSummary,
    StageStatus,
    UpdateOrderStatusCommand,
)
from contexts.orders.infrastructure import (
    create_seed_order,
    list_seed_orders,
    update_seed_order_status,
)


def get_order_overview() -> OrderOverview:
    records = list_seed_orders()
    at_risk = [record for record in records if record.risk == "risk"]
    revenue_total = sum(record.amount_krw for record in records)
    recent_activity = [
        OrderActivity(
            order_id=record.id,
            date=record.created_at,
            customer=record.customer_name,
            status=record.status,
        )
        for record in records[:3]
    ]
    selected = at_risk[0] if at_risk else records[0]

    return OrderOverview(
        stats=[
            DashboardStat(
                label="Active orders", value=str(len(records)), tone="text-[#22314d]"
            ),
            DashboardStat(
                label="At risk",
                value=str(len(at_risk)),
                tone="text-[var(--app-danger)]",
            ),
            DashboardStat(
                label="Revenue",
                value=f"₩{revenue_total // 1_000_000}M",
                tone="text-[var(--app-accent)]",
            ),
        ],
        recent_activity=recent_activity,
        selected_order=OrderDetail(
            product_name=selected.product_name,
            customer_name=selected.customer_name,
            status=selected.status,
            amount=f"₩{selected.amount_krw:,}",
        ),
    )


def get_order_list() -> list[OrderSummary]:
    return [
        OrderSummary(
            id=record.id,
            product_name=record.product_name,
            customer_name=record.customer_name,
            status=record.status,
        )
        for record in list_seed_orders()
    ]


def get_admin_order_overview() -> AdminOrderOverview:
    records = list_seed_orders()
    pending = sum(1 for record in records if record.status == "Pending")
    risky = sum(1 for record in records if record.risk == "risk")
    new_today = sum(1 for record in records if record.is_new_today)
    stage_counts: dict[str, int] = {}
    for record in records:
        stage_counts[record.stage] = stage_counts.get(record.stage, 0) + 1

    return AdminOrderOverview(
        cards=[
            DashboardStat(label="대기 거래", value=str(pending), tone=None),
            DashboardStat(
                label="위험 거래", value=str(risky), tone="text-[var(--admin-danger)]"
            ),
            DashboardStat(
                label="오늘 신규",
                value=str(new_today),
                tone="text-[var(--admin-accent)]",
            ),
        ],
        stage_statuses=[
            StageStatus(label=label, value=f"{count}건")
            for label, count in stage_counts.items()
        ],
    )


def get_admin_queue() -> list[AdminQueueItem]:
    return [
        AdminQueueItem(
            order_id=record.id,
            product_name=record.product_name,
            customer_name=record.customer_name,
            status=record.fulfillment_status,
            sla=record.sla,
        )
        for record in list_seed_orders()
    ]


def create_order(command: CreateOrderCommand) -> OrderRecord:
    return create_seed_order(command)


def update_order_status(
    order_id: str, command: UpdateOrderStatusCommand
) -> OrderStatusTransition:
    return update_seed_order_status(order_id, command)


def prepare_order_store() -> None:
    list_seed_orders()
