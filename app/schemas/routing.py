from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.order import GeocodedOrder, OrderInput


class BranchInput(BaseModel):
    code: str = "SUB"
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class RouteStop(BaseModel):
    order: GeocodedOrder
    segment_distance_km: float
    segment_duration_seconds: float
    segment_duration_text: str


class ExcludedOrder(BaseModel):
    invoice_no: str
    recipient_name: str
    shipping_address: str
    vehicle_type: str
    distance_from_branch_km: float
    max_radius_km: float


class VehicleRoute(BaseModel):
    vehicle_type: str
    stop_count: int
    total_distance_km: float
    total_duration_seconds: float
    return_distance_km: float
    return_duration_seconds: float
    total_cost: float
    route: List[RouteStop]


class OptimizeRouteRequest(BaseModel):
    branch: BranchInput = Field(default_factory=BranchInput)
    orders: List[OrderInput]
    kurir_toko_only: bool = True
    algorithm: str = Field(default="cluster", pattern="^(cluster|nn)$")


class OptimizeRouteResponse(BaseModel):
    branch: BranchInput
    totals: dict
    motor: VehicleRoute
    mobil: VehicleRoute
    excluded: List[ExcludedOrder]
    failed_geocodes: List[dict]

