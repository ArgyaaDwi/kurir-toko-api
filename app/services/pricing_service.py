from app.domain.vehicles import VEHICLE_CONFIG
from app.schemas.pricing import DeliveryCostRequest, DeliveryCostResponse
from app.services.routing_service import get_route


def calculate_delivery_cost(request: DeliveryCostRequest) -> DeliveryCostResponse:
    route = get_route(
        (
            (request.origin.lat, request.origin.lng),
            (request.destination.lat, request.destination.lng),
        ),
        request.vehicle_type,
    )

    cost_per_km = float(VEHICLE_CONFIG[request.vehicle_type]["cost_per_km"])
    distance_km = float(route["distance_km"])
    duration_seconds = float(route["duration_seconds"])

    return DeliveryCostResponse(
        origin=request.origin,
        destination=request.destination,
        vehicle_type=request.vehicle_type,
        distance_km=distance_km,
        duration_seconds=duration_seconds,
        cost_per_km=cost_per_km,
        total_cost=round(distance_km * cost_per_km, 2),
        provider=str(route["provider"]),
        status=str(route["status"]),
    )
