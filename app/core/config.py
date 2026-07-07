from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Kurir Toko API"
    app_env: str = "development"
    graphhopper_api_key: Optional[str] = None
    graphhopper_base: str = "https://graphhopper.com/api/1"
    ors_api_key: Optional[str] = None
    ors_base: str = "https://api.openrouteservice.org/v2"
    osrm_base: str = "http://router.project-osrm.org/route/v1"
    locationiq_api_key: Optional[str] = None
    locationiq_base: str = "https://us1.locationiq.com/v1"
    geocode_delay: float = 0.3
    global_pricing_base_fee: float = 0
    global_pricing_cost_per_km: float = 1500
    global_pricing_minimum_fee: float = 0
    global_pricing_route_vehicle_type: str = "MOBIL"


@lru_cache
def get_settings() -> Settings:
    return Settings()
