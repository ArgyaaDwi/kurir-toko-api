from fastapi import APIRouter, Body

from app.schemas.warehouses import NearestWarehouseRequest, NearestWarehouseResponse
from app.services.warehouse_service import find_nearest_warehouse


router = APIRouter()


@router.post(
    "/nearest-wh",
    response_model=NearestWarehouseResponse,
    summary="Cari warehouse terdekat",
    description="Mencari warehouse terdekat dari koordinat user menggunakan perhitungan rute mobil.",
)
def nearest_warehouse(
    request: NearestWarehouseRequest = Body(...),
) -> NearestWarehouseResponse:
    return find_nearest_warehouse(request)
