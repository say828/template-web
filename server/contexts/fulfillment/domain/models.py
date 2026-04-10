from pydantic import BaseModel


class FulfillmentTaskRecord(BaseModel):
    id: str
    order_id: str
    title: str
    assignee: str
    stage: str
    status: str
    priority: str
    channel: str
    sla_minutes: int
    units: int


class FulfillmentEvent(BaseModel):
    time: str
    title: str
    tone: str


class FulfillmentNote(BaseModel):
    id: str
    note: str
    emphasis: str


class FulfillmentStat(BaseModel):
    label: str
    value: str
    tone: str | None = None


class FulfillmentStageLoad(BaseModel):
    label: str
    value: str


class FulfillmentOverview(BaseModel):
    throughput_total: str
    stats: list[FulfillmentStat]
    timeline: list[FulfillmentEvent]
    stage_load: list[FulfillmentStageLoad]


class FulfillmentBoardItem(BaseModel):
    id: str
    order_id: str
    title: str
    assignee: str
    stage: str
    status: str
    priority: str
    sla: str


class FulfillmentBoardPayload(BaseModel):
    tasks: list[FulfillmentBoardItem]
    notes: list[FulfillmentNote]


class FulfillmentTaskStatusTransitionCommand(BaseModel):
    status: str
    stage: str | None = None


class FulfillmentTaskStatusTransition(BaseModel):
    task_id: str
    previous_status: str
    status: str
    previous_stage: str
    stage: str
