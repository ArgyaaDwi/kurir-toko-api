from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from app.domain.warehouses import WAREHOUSES
from app.schemas.warehouses import (
    NearestWarehouse,
    NearestWarehouseRequest,
    NearestWarehouseResponse,
)
from app.services.routing_service import get_route, haversine

# Gudang terdekat menurut rute mobil hampir selalu ada di antara beberapa terdekat menurut garis lurus.
TOP_CANDIDATES = 3
# Timeout per penyedia routing; Omni hanya menunggu 10 detik untuk seluruh request.
PROVIDER_TIMEOUT_SECONDS = 3
CACHE_MAX_SIZE = 4096
CACHEABLE_STATUS = "graphhopper"

_cache: dict[tuple[float, float], NearestWarehouse] = {}
_cache_lock = Lock()


def _route_candidate(warehouse: dict, user_coords: tuple) -> tuple[NearestWarehouse, str]:
    route = get_route(
        (user_coords, (warehouse["latitude"], warehouse["longitude"])),
        "MOBIL",
        timeout=PROVIDER_TIMEOUT_SECONDS,
    )
    candidate = NearestWarehouse(
        warehouse_code=warehouse["code"],
        warehouse_name=warehouse["name"],
        address=warehouse["address"],
        latitude=warehouse["latitude"],
        longitude=warehouse["longitude"],
        distance_km=round(float(route["distance_km"]), 2),
    )
    return candidate, route.get("status", "")


def find_nearest_warehouse(request: NearestWarehouseRequest) -> NearestWarehouseResponse:
    user_coords = (round(request.latitude, 3), round(request.longitude, 3))
    with _cache_lock:
        cached = _cache.get(user_coords)
    if cached is not None:
        return NearestWarehouseResponse(success=True, data=cached)

    shortlist = sorted(
        WAREHOUSES,
        key=lambda warehouse: haversine(user_coords[0], user_coords[1], warehouse["latitude"], warehouse["longitude"]),
    )[:TOP_CANDIDATES]
    with ThreadPoolExecutor(max_workers=len(shortlist)) as pool:
        results = list(pool.map(lambda warehouse: _route_candidate(warehouse, user_coords), shortlist))

    nearest = min((candidate for candidate, _ in results), key=lambda candidate: candidate.distance_km)

    # Hanya hasil GraphHopper yang disimpan: hasil cadangan (OSRM/haversine, mis. saat GraphHopper kena 429)
    # jaraknya berbeda, jadi request berikutnya mencoba GraphHopper lagi.
    if all(status == CACHEABLE_STATUS for _, status in results):
        with _cache_lock:
            if len(_cache) >= CACHE_MAX_SIZE:
                _cache.pop(next(iter(_cache)))
            _cache[user_coords] = nearest

    return NearestWarehouseResponse(success=True, data=nearest)
