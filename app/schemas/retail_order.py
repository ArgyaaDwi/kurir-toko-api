from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class RetailAddress(BaseModel):
    name: str = "-"
    phone: str = "-"
    address_1: str
    address_2: str = ""
    sub_district: str = "-"
    district: str = "-"
    city: str = "-"
    province: str = "-"
    country: str = "Indonesia"
    postal_code: str = "-"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def empty_coordinate_to_none(cls, value):
        if value == "":
            return None
        return value


class RetailWarehouseSplit(BaseModel):
    warehouse_id: int
    warehouse_name: str = "-"
    qty: int = Field(default=1, ge=1)


class RetailItemLine(BaseModel):
    local_id: str = "-"
    variant_id: int = 0
    sku: str = "-"
    name: str = "-"
    price: float = 0
    sale_price: float = 0
    quantity: int = Field(default=1, ge=1)
    weight: float = Field(default=0, ge=0)
    warehouse_splits: List[RetailWarehouseSplit] = Field(default_factory=list)
    item_type: str = "regular"


class RetailPayment(BaseModel):
    status_payment: str = "-"
    payment_method: str = "-"


class RetailOrder(BaseModel):
    local_id: str
    order_batch_code: Optional[str] = None
    ordered_at: str
    shipping_price: float = 0
    shipping_provider: str
    nextday: bool = False
    note: str = "-"
    internal_note: str = "-"
    warehouse_id: int
    totalWeight: float = 0
    address: RetailAddress
    item_lines: List[RetailItemLine] = Field(default_factory=list)
    payment: Optional[RetailPayment] = None

    @field_validator("shipping_price", "totalWeight", mode="before")
    @classmethod
    def empty_number_to_zero(cls, value):
        if value in ("", None):
            return 0
        return value


class RetailOrderData(BaseModel):
    account_id: int
    order: RetailOrder


class RetailOrderEstimateRequest(BaseModel):
    data: RetailOrderData


class WarehouseSummary(BaseModel):
    warehouse_id: int
    code: str
    name: str
    lat: float
    lng: float


class DestinationSummary(BaseModel):
    name: str
    phone: str
    address: str
    lat: float
    lng: float


class RetailOrderEstimateResponse(BaseModel):
    account_id: int
    order_local_id: str
    shipping_provider: str
    eligible: bool
    warehouse: WarehouseSummary
    destination: DestinationSummary
    total_weight_kg: float
    item_count: int
    distance_km: float
    duration_seconds: float
    base_fee: float
    cost_per_km: float
    minimum_fee: float
    current_shipping_price: float
    calculated_shipping_price: float
    price_difference: float
    shipping_price_changed: bool
    provider: str
    status: str
