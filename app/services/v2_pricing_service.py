from app.core.config import Settings, get_settings
from app.schemas.v2_pricing import (
    V2GlobalDeliveryCostRequest,
    V2GlobalDeliveryCostResponse,
)
from app.services.routing_service import get_route


def _select_vehicle(request: V2GlobalDeliveryCostRequest, settings: Settings) -> tuple[str, str]:
    for item in request.items:
        if item.panjang_cm > settings.v2_pricing_motor_max_panjang_cm:
            return (
                "MOBIL",
                f"SKU {item.sku} memiliki panjang {item.panjang_cm:g} cm, "
                f"melebihi batas motor {settings.v2_pricing_motor_max_panjang_cm:g} cm.",
            )
        if item.lebar_cm > settings.v2_pricing_motor_max_lebar_cm:
            return (
                "MOBIL",
                f"SKU {item.sku} memiliki lebar {item.lebar_cm:g} cm, "
                f"melebihi batas motor {settings.v2_pricing_motor_max_lebar_cm:g} cm.",
            )
        if item.tinggi_cm > settings.v2_pricing_motor_max_tinggi_cm:
            return (
                "MOBIL",
                f"SKU {item.sku} memiliki tinggi {item.tinggi_cm:g} cm, "
                f"melebihi batas motor {settings.v2_pricing_motor_max_tinggi_cm:g} cm.",
            )
        if item.berat_kg > settings.v2_pricing_motor_max_berat_kg:
            return (
                "MOBIL",
                f"SKU {item.sku} memiliki berat {item.berat_kg:g} kg, "
                f"melebihi batas motor {settings.v2_pricing_motor_max_berat_kg:g} kg.",
            )

    total_weight_kg = sum(item.berat_kg * item.qty for item in request.items)
    if total_weight_kg > settings.v2_pricing_motor_max_berat_kg:
        return (
            "MOBIL",
            f"Total berat invoice {total_weight_kg:g} kg, "
            f"melebihi kapasitas motor {settings.v2_pricing_motor_max_berat_kg:g} kg.",
        )

    return "MOTOR", "Semua item dan total beban invoice memenuhi kapasitas motor."


def _pricing_for_vehicle(vehicle_type: str, settings: Settings) -> tuple[float, float, float]:
    if vehicle_type == "MOTOR":
        return (
            float(settings.v2_pricing_motor_base_fee),
            float(settings.v2_pricing_motor_cost_per_km),
            float(settings.v2_pricing_motor_minimum_fee),
        )
    return (
        float(settings.v2_pricing_mobil_base_fee),
        float(settings.v2_pricing_mobil_cost_per_km),
        float(settings.v2_pricing_mobil_minimum_fee),
    )


def calculate_v2_global_delivery_cost(
    request: V2GlobalDeliveryCostRequest,
) -> V2GlobalDeliveryCostResponse:
    settings = get_settings()
    vehicle_type, vehicle_reason = _select_vehicle(request, settings)
    route = get_route(
        (
            (request.origin.lat, request.origin.lng),
            (request.destination.lat, request.destination.lng),
        ),
        vehicle_type,
    )

    distance_km = float(route["distance_km"])
    duration_seconds = float(route["duration_seconds"])
    base_fee, cost_per_km, minimum_fee = _pricing_for_vehicle(vehicle_type, settings)
    total_cost = max(minimum_fee, round(base_fee + (distance_km * cost_per_km), 2))

    return V2GlobalDeliveryCostResponse(
        origin=request.origin,
        destination=request.destination,
        vehicle_type=vehicle_type,
        vehicle_reason=vehicle_reason,
        distance_km=distance_km,
        duration_seconds=duration_seconds,
        base_fee=base_fee,
        cost_per_km=cost_per_km,
        minimum_fee=minimum_fee,
        total_cost=total_cost,
        provider=str(route["provider"]),
        status=str(route["status"]),
    )
