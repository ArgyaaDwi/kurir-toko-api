import time
from typing import Optional, Tuple

import requests
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from app.core.config import get_settings


def locationiq(query: str) -> Tuple[Optional[float], Optional[float]]:
    settings = get_settings()
    if not settings.locationiq_api_key:
        return None, None
    try:
        params = {
            "key": settings.locationiq_api_key,
            "q": query,
            "format": "json",
            "limit": 1,
            "countrycodes": "id",
            "accept-language": "id",
        }
        response = requests.get(f"{settings.locationiq_base}/search.php", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        return None, None
    return None, None


def nominatim(query: str) -> Tuple[Optional[float], Optional[float]]:
    try:
        loc = Nominatim(user_agent="kurir_toko_api", timeout=10).geocode(query)
        if loc:
            return loc.latitude, loc.longitude
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None
    return None, None


def photon(query: str) -> Tuple[Optional[float], Optional[float]]:
    try:
        response = requests.get(
            "https://photon.komoot.io/api/",
            params={"q": query, "limit": 1, "lang": "id"},
            timeout=10,
        )
        features = response.json().get("features", [])
        if features:
            coords = features[0]["geometry"]["coordinates"]
            return coords[1], coords[0]
    except Exception:
        return None, None
    return None, None


def gentle_delay() -> None:
    settings = get_settings()
    time.sleep(settings.geocode_delay)

