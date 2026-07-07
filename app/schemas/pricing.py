from typing import Literal

from pydantic import BaseModel, Field


class CoordinateInput(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class DeliveryCostRequest(BaseModel):
    origin: CoordinateInput
    destination: CoordinateInput
    vehicle_type: Literal["MOTOR", "MOBIL"]


class DeliveryCostResponse(BaseModel):
    origin: CoordinateInput
    destination: CoordinateInput
    vehicle_type: str
    distance_km: float
    duration_seconds: float
    cost_per_km: float
    total_cost: float
    provider: str
    status: str
