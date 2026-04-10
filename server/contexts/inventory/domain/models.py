from typing import Literal, TypeAlias

from pydantic import BaseModel, Field, model_validator

InventoryAvailabilityStatus = Literal["in_stock", "low_stock", "out_of_stock"]
InventoryMutationAction = Literal["adjusted", "reserved", "released", "set"]


class InventoryLevelRecord(BaseModel):
    sku: str = Field(min_length=1)
    product_id: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    variant_name: str = Field(min_length=1)
    location_id: str = Field(min_length=1)
    location_name: str = Field(min_length=1)
    on_hand: int = Field(ge=0)
    reserved: int = Field(ge=0)
    safety_stock: int = Field(ge=0)
    reorder_point: int = Field(ge=0)
    updated_at: str

    @model_validator(mode="after")
    def validate_stock_levels(self) -> "InventoryLevelRecord":
        if self.reserved > self.on_hand:
            raise ValueError("reserved stock cannot exceed on-hand stock")
        return self


class InventoryLevelView(BaseModel):
    sku: str
    product_id: str
    product_name: str
    variant_name: str
    location_id: str
    location_name: str
    on_hand: int
    reserved: int
    available_to_sell: int
    safety_stock: int
    reorder_point: int
    needs_reorder: bool
    status: InventoryAvailabilityStatus
    updated_at: str


class AdjustInventoryCommand(BaseModel):
    quantity_delta: int
    reason: str = Field(min_length=1)
    reference_id: str | None = Field(default=None, min_length=1)


class ReserveInventoryCommand(BaseModel):
    quantity: int = Field(gt=0)
    reference_id: str = Field(min_length=1)
    channel: str | None = Field(default=None, min_length=1)


class ReleaseInventoryCommand(BaseModel):
    quantity: int = Field(gt=0)
    reference_id: str = Field(min_length=1)
    reason: str | None = Field(default=None, min_length=1)


class SetInventoryLevelCommand(BaseModel):
    on_hand: int = Field(ge=0)
    reserved: int = Field(ge=0)
    safety_stock: int = Field(ge=0)
    reorder_point: int = Field(ge=0)
    reason: str | None = Field(default=None, min_length=1)
    reference_id: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_stock_levels(self) -> "SetInventoryLevelCommand":
        if self.reserved > self.on_hand:
            raise ValueError("reserved stock cannot exceed on-hand stock")
        return self


class InventoryMutationReceipt(BaseModel):
    action: InventoryMutationAction
    sku: str
    location_id: str
    quantity: int
    reference_id: str | None = None
    reason: str | None = None
    level: InventoryLevelView


InventoryLevel = InventoryLevelView
InventoryAdjustmentCommand: TypeAlias = AdjustInventoryCommand
InventoryReservationCommand: TypeAlias = ReserveInventoryCommand
InventoryReleaseCommand: TypeAlias = ReleaseInventoryCommand
InventorySetLevelCommand: TypeAlias = SetInventoryLevelCommand
