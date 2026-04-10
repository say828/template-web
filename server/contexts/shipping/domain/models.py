from pydantic import BaseModel


class ShippingStat(BaseModel):
    label: str
    value: str
    tone: str | None = None


class ShippingCarrierLoad(BaseModel):
    label: str
    value: str


class ShippingOverview(BaseModel):
    stats: list[ShippingStat]
    carriers: list[ShippingCarrierLoad]
    highlighted_route: str


class ShipmentSummary(BaseModel):
    shipment_id: str
    order_id: str
    carrier: str
    destination: str
    tracking_number: str
    status: str
    eta: str
    last_event: str


class ShipmentRecord(ShipmentSummary):
    route_name: str
    delivered_today: bool


class UpdateShipmentStatusCommand(BaseModel):
    status: str
    last_event: str
    eta: str | None = None


class ShipmentStatusTransition(BaseModel):
    shipment_id: str
    previous_status: str
    status: str
    previous_last_event: str
    last_event: str
