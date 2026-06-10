from typing import List

from pydantic import BaseModel, Field

from app.schemas.order import OrderInput
from app.schemas.routing import OptimizeRouteResponse


class BatchWindow(BaseModel):
    name: str
    cutoff_time: str


class BatchPlanRequest(BaseModel):
    branch_code: str = "SUB"
    windows: List[BatchWindow] = Field(default_factory=lambda: [
        BatchWindow(name="PAGI", cutoff_time="09:00"),
        BatchWindow(name="SIANG", cutoff_time="13:00"),
        BatchWindow(name="SORE", cutoff_time="16:00"),
    ])
    orders: List[OrderInput]
    kurir_toko_only: bool = True
    algorithm: str = Field(default="cluster", pattern="^(cluster|nn)$")


class BatchPlanItem(BaseModel):
    batch_name: str
    cutoff_time: str
    order_count: int
    routing_result: OptimizeRouteResponse


class BatchPlanResponse(BaseModel):
    branch_code: str
    batch_count: int
    batches: List[BatchPlanItem]

