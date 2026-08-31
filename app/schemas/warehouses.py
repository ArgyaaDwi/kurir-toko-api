from pydantic import BaseModel, Field


class NearestWarehouseRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class NearestWarehouse(BaseModel):
    warehouse_code: str
    warehouse_name: str
    address: str
    latitude: float
    longitude: float
    distance_km: float


class NearestWarehouseResponse(BaseModel):
    success: bool
    data: NearestWarehouse
