from typing import Optional

import polyline as polyline_lib
import requests

from app.core.config import get_settings


def graphhopper_route(coords: tuple, profile: str) -> Optional[dict]:
    settings = get_settings()
    if not settings.graphhopper_api_key or len(coords) < 2:
        return None
    points_list = [f"{lat},{lng}" for lat, lng in coords]
    params = {
        "key": settings.graphhopper_api_key,
        "profile": profile,
        "point": points_list,
        "instructions": False,
        "points_encoded": False,
        "locale": "id",
        "calc_points": True,
    }
    try:
        response = requests.get(f"{settings.graphhopper_base}/route", params=params, timeout=20)
        if response.status_code == 200:
            data = response.json()
            if data.get("paths"):
                path = data["paths"][0]
                raw_coords = path.get("points", {}).get("coordinates", [])
                geometry = [[coord[1], coord[0]] for coord in raw_coords] if raw_coords else []
                return {
                    "distance_km": round(path["distance"] / 1000, 2),
                    "duration_seconds": path["time"] / 1000,
                    "geometry": geometry,
                    "provider": "GraphHopper",
                    "status": "graphhopper",
                }
    except Exception:
        return None
    return None


def ors_route(coords: tuple, profile: str) -> Optional[dict]:
    settings = get_settings()
    if not settings.ors_api_key or len(coords) < 2:
        return None
    headers = {
        "Accept": "application/json",
        "Authorization": settings.ors_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "coordinates": [[lng, lat] for lat, lng in coords],
        "instructions": False,
        "geometry": True,
        "format": "json",
        "units": "km",
    }
    try:
        response = requests.post(
            f"{settings.ors_base}/directions/{profile}",
            json=payload,
            headers=headers,
            timeout=20,
        )
        if response.status_code == 200:
            features = response.json().get("features", [])
            if features:
                route = features[0]
                summary = route["properties"]["summary"]
                geometry = [[coord[1], coord[0]] for coord in route["geometry"]["coordinates"]]
                return {
                    "distance_km": round(summary["distance"], 2),
                    "duration_seconds": summary["duration"],
                    "geometry": geometry,
                    "provider": "OpenRouteService",
                    "status": "ors",
                }
    except Exception:
        return None
    return None


def osrm_route(coords: tuple, profile: str) -> Optional[dict]:
    settings = get_settings()
    if len(coords) < 2:
        return None
    coord_str = ";".join(f"{lng},{lat}" for lat, lng in coords)
    try:
        response = requests.get(
            f"{settings.osrm_base}/{profile}/{coord_str}",
            params={"overview": "full", "geometries": "polyline"},
            timeout=15,
        )
        data = response.json()
        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            geometry = polyline_lib.decode(route.get("geometry", "")) if route.get("geometry") else []
            return {
                "distance_km": round(route["distance"] / 1000, 2),
                "duration_seconds": route["duration"],
                "geometry": geometry,
                "provider": "OSRM",
                "status": "osrm",
            }
    except Exception:
        return None
    return None

