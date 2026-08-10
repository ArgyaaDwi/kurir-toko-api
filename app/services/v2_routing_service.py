from app.schemas.v2_routing import (
    V2FailedRouteOrder,
    V2OptimizeRouteRequest,
    V2OptimizeRouteResponse,
    V2RouteStop,
    V2RouteTotals,
)
from app.services.routing_service import compute_route, get_route


VEHICLE_TYPE = "MOBIL"


def optimize_v2_route(request: V2OptimizeRouteRequest) -> V2OptimizeRouteResponse:
    packages = []
    failed = []

    for order in request.orders:
        if order.latitude is None or order.longitude is None:
            failed.append(
                V2FailedRouteOrder(
                    route_order_id=order.route_order_id,
                    order_id=order.order_id,
                    invoice_no=order.invoice_no,
                    reason="Order coordinate is missing.",
                )
            )
            continue

        packages.append(
            {
                "route_order_id": order.route_order_id,
                "order_id": order.order_id,
                "invoice_no": order.invoice_no,
                "customer_name": order.customer_name,
                "phone": order.phone,
                "address": order.address,
                "lat": float(order.latitude),
                "lng": float(order.longitude),
                "weight": float(order.weight),
            }
        )

    route, route_km, route_seconds = compute_route(
        request.warehouse.latitude,
        request.warehouse.longitude,
        packages,
        request.algorithm,
        VEHICLE_TYPE,
    )

    return_distance_km = 0.0
    return_duration_seconds = 0.0
    if request.return_to_warehouse and route:
        last = route[-1]
        return_segment = get_route(
            (
                (last["lat"], last["lng"]),
                (request.warehouse.latitude, request.warehouse.longitude),
            ),
            VEHICLE_TYPE,
        )
        return_distance_km = float(return_segment["distance_km"])
        return_duration_seconds = float(return_segment["duration_seconds"])

    cumulative_distance_km = 0.0
    cumulative_duration_seconds = 0.0
    stops = []
    for index, item in enumerate(route, start=1):
        segment_distance_km = float(item["segment_distance_km"])
        segment_duration_seconds = float(item["segment_duration_seconds"])
        cumulative_distance_km = round(cumulative_distance_km + segment_distance_km, 2)
        cumulative_duration_seconds += segment_duration_seconds
        stops.append(
            V2RouteStop(
                sequence=index,
                route_order_id=item["route_order_id"],
                order_id=item["order_id"],
                invoice_no=item["invoice_no"],
                customer_name=item["customer_name"],
                phone=item["phone"],
                address=item["address"],
                latitude=item["lat"],
                longitude=item["lng"],
                weight=item["weight"],
                segment_distance_km=segment_distance_km,
                segment_duration_seconds=segment_duration_seconds,
                segment_duration_text=item["segment_duration_text"],
                cumulative_distance_km=cumulative_distance_km,
                cumulative_duration_seconds=cumulative_duration_seconds,
            )
        )

    total_distance_km = round(route_km + return_distance_km, 2)
    total_duration_seconds = route_seconds + return_duration_seconds

    return V2OptimizeRouteResponse(
        route_id=request.route_id,
        delivery_date=request.delivery_date,
        session=request.session,
        warehouse=request.warehouse,
        return_to_warehouse=request.return_to_warehouse,
        vehicle_type=VEHICLE_TYPE,
        totals=V2RouteTotals(
            total_orders=len(request.orders),
            optimized_orders=len(stops),
            failed_orders=len(failed),
            total_distance_km=total_distance_km,
            total_duration_seconds=total_duration_seconds,
            return_distance_km=return_distance_km,
            return_duration_seconds=return_duration_seconds,
        ),
        route=stops,
        failed=failed,
    )
