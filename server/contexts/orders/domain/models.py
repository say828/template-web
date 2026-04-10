from pydantic import BaseModel


class OrderRecord(BaseModel):
    id: str
    product_id: str
    product_name: str
    customer_name: str
    seller_name: str
    status: str
    fulfillment_status: str
    created_at: str
    amount_krw: int
    risk: str
    stage: str
    sla: str
    is_new_today: bool


class DashboardStat(BaseModel):
    label: str
    value: str
    tone: str | None = None


class OrderActivity(BaseModel):
    order_id: str
    date: str
    customer: str
    status: str


class OrderDetail(BaseModel):
    product_name: str
    customer_name: str
    status: str
    amount: str


class OrderOverview(BaseModel):
    stats: list[DashboardStat]
    recent_activity: list[OrderActivity]
    selected_order: OrderDetail


class OrderSummary(BaseModel):
    id: str
    product_name: str
    customer_name: str
    status: str


class StageStatus(BaseModel):
    label: str
    value: str


class AdminOrderOverview(BaseModel):
    cards: list[DashboardStat]
    stage_statuses: list[StageStatus]


class AdminQueueItem(BaseModel):
    order_id: str
    product_name: str
    customer_name: str
    status: str
    sla: str


class CreateOrderCommand(BaseModel):
    product_id: str
    product_name: str
    customer_name: str
    seller_name: str
    amount_krw: int
    stage: str = "결제 대기"
    status: str = "Pending"
    fulfillment_status: str = "Queued"
    sla: str = "55 min"


class UpdateOrderStatusCommand(BaseModel):
    status: str
    fulfillment_status: str | None = None
    stage: str | None = None


class OrderStatusTransition(BaseModel):
    id: str
    previous_status: str
    status: str
    fulfillment_status: str
    risk: str
    stage: str
