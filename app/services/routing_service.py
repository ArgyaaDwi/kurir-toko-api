from math import atan2, cos, radians, sin, sqrt
from typing import List, Tuple

from fastapi import HTTPException

from app.domain.branches import get_branch_by_code
from app.domain.vehicles import VEHICLE_CONFIG
from app.integrations.routing_providers import graphhopper_route, ors_route, osrm_route
from app.schemas.order import GeocodedOrder
from app.schemas.routing import (
    BranchInput,
    ExcludedOrder,
    OptimizeRouteRequest,
    OptimizeRouteResponse,
    RouteStop,
    VehicleRoute,
)
from app.services.geocoding_service import geocode_address
from app.services.vehicle_service import classify_vehicle, is_kurir_toko


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    earth_radius_km = 6371
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return earth_radius_km * 2 * atan2(sqrt(a), sqrt(1 - a))


def format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "0 mnt"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours} jam {minutes} mnt" if hours > 0 else f"{minutes} mnt"


def get_route(coords: tuple, vehicle_type: str) -> dict:
    if len(coords) < 2:
        return {"distance_km": 0.0, "duration_seconds": 0.0, "geometry": [], "provider": "None", "status": "failed"}

    vehicle_config = VEHICLE_CONFIG[vehicle_type]
    result = graphhopper_route(coords, vehicle_config["gh_profile"])
    if result and result.get("geometry"):
        return result

    result = ors_route(coords, vehicle_config["ors_profile"])
    if result and result.get("geometry"):
        return result

    result = osrm_route(coords, vehicle_config["osrm_profile"])
    if result and result.get("geometry"):
        return result

    distance_km = haversine(coords[0][0], coords[0][1], coords[1][0], coords[1][1])
    factor = 1.15 if vehicle_type == "MOTOR" else 1.25
    adjusted_km = round(distance_km * factor, 2)
    speed = vehicle_config["kecepatan"]
    return {
        "distance_km": adjusted_km,
        "duration_seconds": adjusted_km * 3600 / speed,
        "geometry": [list(coords[0]), list(coords[1])],
        "provider": "Estimasi",
        "status": "haversine_fallback",
    }


def cluster_packages(packages: List[dict], n: int | None = None) -> List[List[dict]]:
    if len(packages) <= 3:
        return [packages]
    n = n or max(2, min(len(packages) // 6, 8))
    n = min(n, len(packages))
    coords = [(pkg["lat"], pkg["lng"]) for pkg in packages]
    centers = [coords[0]]
    for _ in range(n - 1):
        best_coord = None
        best_distance = -1
        for coord in coords:
            distance = min(haversine(coord[0], coord[1], center[0], center[1]) for center in centers)
            if distance > best_distance:
                best_distance = distance
                best_coord = coord
        if best_coord:
            centers.append(best_coord)

    assignments = [0] * len(coords)
    for _ in range(30):
        assignments = [
            min(range(n), key=lambda center_index: haversine(coord[0], coord[1], centers[center_index][0], centers[center_index][1]))
            for coord in coords
        ]
        new_centers = []
        for center_index in range(n):
            points = [coords[index] for index, assignment in enumerate(assignments) if assignment == center_index]
            if points:
                new_centers.append(
                    (
                        sum(point[0] for point in points) / len(points),
                        sum(point[1] for point in points) / len(points),
                    )
                )
            else:
                new_centers.append(centers[center_index])
        if new_centers == centers:
            break
        centers = new_centers

    clusters = [[] for _ in range(n)]
    for index, pkg in enumerate(packages):
        clusters[assignments[index]].append(pkg)
    return [cluster for cluster in clusters if cluster]


def order_clusters(branch_lat: float, branch_lng: float, clusters: List[List[dict]]) -> List[List[dict]]:
    remaining = list(range(len(clusters)))
    ordered = []
    current_lat, current_lng = branch_lat, branch_lng
    while remaining:
        best_index = None
        best_distance = float("inf")
        for candidate in remaining:
            cluster = clusters[candidate]
            center_lat = sum(item["lat"] for item in cluster) / len(cluster)
            center_lng = sum(item["lng"] for item in cluster) / len(cluster)
            distance = haversine(current_lat, current_lng, center_lat, center_lng)
            if distance < best_distance:
                best_distance = distance
                best_index = candidate
        ordered.append(clusters[best_index])
        current_lat = sum(item["lat"] for item in clusters[best_index]) / len(clusters[best_index])
        current_lng = sum(item["lng"] for item in clusters[best_index]) / len(clusters[best_index])
        remaining.remove(best_index)
    return ordered


def nearest_neighbor_segment(
    start_lat: float,
    start_lng: float,
    packages: List[dict],
    home_lat: float,
    home_lng: float,
    is_last_segment: bool,
    vehicle_type: str,
) -> Tuple[List[dict], float, float]:
    remaining = packages.copy()
    route = []
    total_km = 0.0
    total_seconds = 0.0
    current_lat, current_lng = start_lat, start_lng

    while remaining:
        if is_last_segment and 1 < len(remaining) <= 3:
            best_index = 0
            best_cost = float("inf")
            for index, package in enumerate(remaining):
                cost = (
                    haversine(current_lat, current_lng, package["lat"], package["lng"]) * 1.3
                    + haversine(package["lat"], package["lng"], home_lat, home_lng) * 1.04
                )
                if cost < best_cost:
                    best_cost = cost
                    best_index = index
        else:
            best_index = min(
                range(len(remaining)),
                key=lambda index: haversine(current_lat, current_lng, remaining[index]["lat"], remaining[index]["lng"]),
            )

        chosen = remaining.pop(best_index).copy()
        segment = get_route(((current_lat, current_lng), (chosen["lat"], chosen["lng"])), vehicle_type)
        chosen["segment_distance_km"] = float(segment["distance_km"])
        chosen["segment_duration_seconds"] = float(segment["duration_seconds"])
        chosen["segment_duration_text"] = format_duration(chosen["segment_duration_seconds"])
        chosen["route_provider"] = segment["provider"]
        route.append(chosen)
        total_km += chosen["segment_distance_km"]
        total_seconds += chosen["segment_duration_seconds"]
        current_lat, current_lng = chosen["lat"], chosen["lng"]

    return route, round(total_km, 2), total_seconds


def compute_route(branch_lat: float, branch_lng: float, packages: List[dict], algorithm: str, vehicle_type: str) -> Tuple[List[dict], float, float]:
    if not packages:
        return [], 0.0, 0.0
    if algorithm == "cluster" and len(packages) > 4:
        clusters = order_clusters(branch_lat, branch_lng, cluster_packages(packages))
        full_route = []
        total_km = 0.0
        total_seconds = 0.0
        current_lat, current_lng = branch_lat, branch_lng
        for index, cluster in enumerate(clusters):
            segment_route, segment_km, segment_seconds = nearest_neighbor_segment(
                current_lat,
                current_lng,
                cluster,
                branch_lat,
                branch_lng,
                index == len(clusters) - 1,
                vehicle_type,
            )
            full_route.extend(segment_route)
            total_km += segment_km
            total_seconds += segment_seconds
            if segment_route:
                current_lat, current_lng = segment_route[-1]["lat"], segment_route[-1]["lng"]
        return full_route, round(total_km, 2), total_seconds
    return nearest_neighbor_segment(branch_lat, branch_lng, packages, branch_lat, branch_lng, True, vehicle_type)


def resolve_branch(branch: BranchInput) -> BranchInput:
    if branch.lat is not None and branch.lng is not None:
        return branch
    base = get_branch_by_code(branch.code)
    return BranchInput(code=base["kode"], name=base["nama"], lat=base["lat"], lng=base["lng"])


def geocode_and_split_orders(request: OptimizeRouteRequest) -> tuple:
    branch = resolve_branch(request.branch)
    source_orders = request.orders
    if request.kurir_toko_only:
        source_orders = [order for order in source_orders if is_kurir_toko(order.shipping_courier)]

    if not source_orders:
        raise HTTPException(status_code=400, detail="No eligible orders to process.")

    motor_packages = []
    mobil_packages = []
    excluded = []
    failed = []

    for order in source_orders:
        lat, lng, geocode_source, accuracy = geocode_address(order.shipping_address)
        if lat is None or lng is None:
            failed.append({"invoice_no": order.invoice_no, "shipping_address": order.shipping_address})
            continue

        vehicle_type = classify_vehicle(
            order.panjang_cm,
            order.lebar_cm,
            order.tinggi_cm,
            order.berat_kg,
            order.items_quantity,
            order.kendaraan_override,
        )
        distance_from_branch = round(haversine(branch.lat, branch.lng, lat, lng), 2)
        payload = GeocodedOrder(
            **order.model_dump(),
            lat=lat,
            lng=lng,
            geocode_source=geocode_source,
            accuracy=accuracy,
            vehicle_type=vehicle_type,
            distance_from_branch_km=distance_from_branch,
        )
        max_radius = VEHICLE_CONFIG[vehicle_type]["max_radius"]
        if distance_from_branch > max_radius:
            excluded.append(
                ExcludedOrder(
                    invoice_no=order.invoice_no,
                    recipient_name=order.recipient_name,
                    shipping_address=order.shipping_address,
                    vehicle_type=vehicle_type,
                    distance_from_branch_km=distance_from_branch,
                    max_radius_km=max_radius,
                )
            )
            continue

        target = motor_packages if vehicle_type == "MOTOR" else mobil_packages
        target.append(payload.model_dump())

    return branch, motor_packages, mobil_packages, excluded, failed


def build_vehicle_route(branch: BranchInput, packages: List[dict], algorithm: str, vehicle_type: str) -> VehicleRoute:
    route, route_km, route_seconds = compute_route(branch.lat, branch.lng, packages, algorithm, vehicle_type)
    return_distance_km = 0.0
    return_duration_seconds = 0.0
    if route:
        last = route[-1]
        return_segment = get_route(((last["lat"], last["lng"]), (branch.lat, branch.lng)), vehicle_type)
        return_distance_km = float(return_segment["distance_km"])
        return_duration_seconds = float(return_segment["duration_seconds"])

    total_distance = round(route_km + return_distance_km, 2)
    total_seconds = route_seconds + return_duration_seconds
    total_cost = round(total_distance * VEHICLE_CONFIG[vehicle_type]["cost_per_km"], 2)

    return VehicleRoute(
        vehicle_type=vehicle_type,
        stop_count=len(route),
        total_distance_km=total_distance,
        total_duration_seconds=total_seconds,
        return_distance_km=return_distance_km,
        return_duration_seconds=return_duration_seconds,
        total_cost=total_cost,
        route=[
            RouteStop(
                order=GeocodedOrder(**item),
                segment_distance_km=item["segment_distance_km"],
                segment_duration_seconds=item["segment_duration_seconds"],
                segment_duration_text=item["segment_duration_text"],
            )
            for item in route
        ],
    )


def optimize_routes(request: OptimizeRouteRequest) -> OptimizeRouteResponse:
    branch, motor_packages, mobil_packages, excluded, failed = geocode_and_split_orders(request)
    motor = build_vehicle_route(branch, motor_packages, request.algorithm, "MOTOR")
    mobil = build_vehicle_route(branch, mobil_packages, request.algorithm, "MOBIL")

    total_distance = round(motor.total_distance_km + mobil.total_distance_km, 2)
    total_duration_seconds = motor.total_duration_seconds + mobil.total_duration_seconds
    total_cost = round(motor.total_cost + mobil.total_cost, 2)

    return OptimizeRouteResponse(
        branch=branch,
        totals={
            "orders_processed": len(request.orders),
            "eligible_orders": len(motor_packages) + len(mobil_packages) + len(excluded),
            "failed_geocodes": len(failed),
            "excluded_orders": len(excluded),
            "total_distance_km": total_distance,
            "total_duration_seconds": total_duration_seconds,
            "total_cost": total_cost,
        },
        motor=motor,
        mobil=mobil,
        excluded=excluded,
        failed_geocodes=failed,
    )

