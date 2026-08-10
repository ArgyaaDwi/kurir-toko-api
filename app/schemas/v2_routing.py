from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class V2WarehouseInput(BaseModel):
    id: int
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class V2RouteOrderInput(BaseModel):
    route_order_id: int
    order_id: int
    invoice_no: str
    customer_name: str
    phone: str
    address: str
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    weight: float = Field(default=0, ge=0)


class V2OptimizeRouteRequest(BaseModel):
    route_id: int
    warehouse: V2WarehouseInput
    delivery_date: str
    session: str
    return_to_warehouse: bool = True
    orders: List[V2RouteOrderInput] = Field(..., min_length=1)
    algorithm: Literal["cluster", "nn"] = "cluster"


class V2RouteStop(BaseModel):
    sequence: int
    route_order_id: int
    order_id: int
    invoice_no: str
    customer_name: str
    phone: str
    address: str
    latitude: float
    longitude: float
    weight: float
    segment_distance_km: float
    segment_duration_seconds: float
    segment_duration_text: str
    cumulative_distance_km: float
    cumulative_duration_seconds: float


class V2FailedRouteOrder(BaseModel):
    route_order_id: int
    order_id: int
    invoice_no: str
    reason: str


class V2RouteTotals(BaseModel):
    total_orders: int
    optimized_orders: int
    failed_orders: int
    total_distance_km: float
    total_duration_seconds: float
    return_distance_km: float
    return_duration_seconds: float


class V2OptimizeRouteResponse(BaseModel):
    route_id: int
    delivery_date: str
    session: str
    warehouse: V2WarehouseInput
    return_to_warehouse: bool
    vehicle_type: str
    totals: V2RouteTotals
    route: List[V2RouteStop]
    failed: List[V2FailedRouteOrder]
