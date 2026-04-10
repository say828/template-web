from pydantic import BaseModel


class AlertItem(BaseModel):
    id: str
    source: str
    title: str
    message: str
    tone: str
    created_at: str
    read: bool


class AlertRecord(AlertItem):
    pass


class AlertReadResult(AlertItem):
    pass


class AlertsPayload(BaseModel):
    unread_count: int
    items: list[AlertItem]


class AlertsReadAllResult(BaseModel):
    updated_count: int
    unread_count: int
