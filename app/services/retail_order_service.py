from fastapi import HTTPException

from app.core.config import get_settings
from app.domain.warehouses import get_warehouse_by_id
from app.schemas.retail_order import (
    DestinationSummary,
    RetailAddress,
    RetailOrderEstimateRequest,
    RetailOrderEstimateResponse,
    WarehouseSummary,
)
from app.services.geocoding_service import geocode_address
from app.services.routing_service import get_route


def _is_kurir_toko_retail(provider: str) -> bool:
    normalized = str(provider).lower().replace(" ", "").replace("_", "").replace("-", "")
    return "kurirtokoretail" in normalized


def _format_address(address: RetailAddress) -> str:
    raw_parts = [
        address.address_1,
        address.address_2,
        address.sub_district,
        address.district,
        address.city,
        address.province,
        address.postal_code,
        address.country,
    ]
    parts = []
    seen = set()
    for raw_part in raw_parts:
        for part in str(raw_part).split(","):
            cleaned = part.strip()
            key = cleaned.lower()
            if cleaned and key not in seen:
                seen.add(key)
                parts.append(cleaned)
    return ", ".join(parts)


def _resolve_destination(address: RetailAddress) -> tuple[float, float]:
    if address.latitude is not None and address.longitude is not None:
        return float(address.latitude), float(address.longitude)

    lat, lng, _, _ = geocode_address(_format_address(address))
    if lat is None or lng is None:
        raise HTTPException(status_code=422, detail="Destination coordinate could not be resolved.")
    return float(lat), float(lng)


def estimate_retail_order_shipping(request: RetailOrderEstimateRequest) -> RetailOrderEstimateResponse:
    settings = get_settings()
    order = request.data.order

    try:
        warehouse = get_warehouse_by_id(order.warehouse_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    destination_lat, destination_lng = _resolve_destination(order.address)
    route = get_route(
        (
            (float(warehouse["lat"]), float(warehouse["lng"])),
            (destination_lat, destination_lng),
        ),
        "MOBIL",
    )

    distance_km = float(route["distance_km"])
    duration_seconds = float(route["duration_seconds"])
    base_fee = float(settings.global_pricing_base_fee)
    cost_per_km = float(settings.global_pricing_cost_per_km)
    minimum_fee = float(settings.global_pricing_minimum_fee)
    calculated_shipping_price = max(minimum_fee, round(base_fee + (distance_km * cost_per_km), 2))
    current_shipping_price = float(order.shipping_price)

    return RetailOrderEstimateResponse(
        account_id=request.data.account_id,
        order_local_id=order.local_id,
        shipping_provider=order.shipping_provider,
        eligible=_is_kurir_toko_retail(order.shipping_provider),
        warehouse=WarehouseSummary(**warehouse),
        destination=DestinationSummary(
            name=order.address.name,
            phone=order.address.phone,
            address=_format_address(order.address),
            lat=destination_lat,
            lng=destination_lng,
        ),
        total_weight_kg=float(order.totalWeight),
        item_count=sum(item.quantity for item in order.item_lines),
        distance_km=distance_km,
        duration_seconds=duration_seconds,
        base_fee=base_fee,
        cost_per_km=cost_per_km,
        minimum_fee=minimum_fee,
        current_shipping_price=current_shipping_price,
        calculated_shipping_price=calculated_shipping_price,
        price_difference=round(calculated_shipping_price - current_shipping_price, 2),
        shipping_price_changed=round(calculated_shipping_price, 2) != round(current_shipping_price, 2),
        provider=str(route["provider"]),
        status=str(route["status"]),
    )
