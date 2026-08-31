from app.domain.warehouses import WAREHOUSES
from app.schemas.warehouses import (
    NearestWarehouse,
    NearestWarehouseRequest,
    NearestWarehouseResponse,
)
from app.services.routing_service import get_route


def find_nearest_warehouse(request: NearestWarehouseRequest) -> NearestWarehouseResponse:
    user_coords = (request.latitude, request.longitude)
    nearest = None

    for warehouse in WAREHOUSES:
        route = get_route(
            (user_coords, (warehouse["latitude"], warehouse["longitude"])),
            "MOBIL",
        )
        candidate = NearestWarehouse(
            warehouse_code=warehouse["code"],
            warehouse_name=warehouse["name"],
            address=warehouse["address"],
            latitude=warehouse["latitude"],
            longitude=warehouse["longitude"],
            distance_km=round(float(route["distance_km"]), 2),
        )
        if nearest is None or candidate.distance_km < nearest.distance_km:
            nearest = candidate

    return NearestWarehouseResponse(success=True, data=nearest)
