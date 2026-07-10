from app.core.config import get_settings
from app.domain.vehicles import VEHICLE_CONFIG
from app.schemas.global_pricing import GlobalDeliveryCostRequest, GlobalDeliveryCostResponse
from app.services.routing_service import get_route


def calculate_global_delivery_cost(request: GlobalDeliveryCostRequest) -> GlobalDeliveryCostResponse:
    settings = get_settings()
    routing_vehicle_type = str(settings.global_pricing_route_vehicle_type).upper()
    if routing_vehicle_type not in VEHICLE_CONFIG:
        routing_vehicle_type = "MOBIL"

    route = get_route(
        (
            (request.origin.lat, request.origin.lng),
            (request.destination.lat, request.destination.lng),
        ),
        routing_vehicle_type,
    )

    distance_km = float(route["distance_km"])
    duration_seconds = float(route["duration_seconds"])
    base_fee = float(settings.global_pricing_base_fee)
    cost_per_km = float(settings.global_pricing_cost_per_km)
    minimum_fee = float(settings.global_pricing_minimum_fee)
    total_cost = max(minimum_fee, round(base_fee + (distance_km * cost_per_km), 2))

    return GlobalDeliveryCostResponse(
        origin=request.origin,
        destination=request.destination,
        distance_km=distance_km,
        duration_seconds=duration_seconds,
        base_fee=base_fee,
        cost_per_km=cost_per_km,
        minimum_fee=minimum_fee,
        total_cost=total_cost,
        provider=str(route["provider"]),
        status=str(route["status"]),
    )
