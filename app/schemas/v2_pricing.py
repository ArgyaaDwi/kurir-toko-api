from typing import Literal, List

from pydantic import BaseModel, Field

from app.schemas.pricing import CoordinateInput


class InvoiceItemInput(BaseModel):
    sku: str = Field(..., min_length=1)
    qty: int = Field(..., ge=1)
    panjang_cm: float = Field(..., ge=0)
    lebar_cm: float = Field(..., ge=0)
    tinggi_cm: float = Field(..., ge=0)
    berat_kg: float = Field(..., ge=0)


class V2GlobalDeliveryCostRequest(BaseModel):
    origin: CoordinateInput
    destination: CoordinateInput
    items: List[InvoiceItemInput] = Field(..., min_length=1)


class V2GlobalDeliveryCostResponse(BaseModel):
    origin: CoordinateInput
    destination: CoordinateInput
    vehicle_type: Literal["MOTOR", "MOBIL"]
    vehicle_reason: str
    distance_km: float
    duration_seconds: float
    base_fee: float
    cost_per_km: float
    minimum_fee: float
    total_cost: float
    provider: str
    status: str
