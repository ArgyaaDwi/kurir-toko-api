from app.schemas.pricing import CoordinateInput
from pydantic import BaseModel


class GlobalDeliveryCostRequest(BaseModel):
    origin: CoordinateInput
    destination: CoordinateInput


class GlobalDeliveryCostResponse(BaseModel):
    origin: CoordinateInput
    destination: CoordinateInput
    distance_km: float
    duration_seconds: float
    base_fee: float
    cost_per_km: float
    minimum_fee: float
    total_cost: float
    provider: str
    status: str
