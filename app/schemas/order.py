from typing import Optional

from pydantic import BaseModel, Field


class OrderInput(BaseModel):
    invoice_no: str = Field(default="-")
    so_number: str = Field(default="-")
    order_date: Optional[str] = None
    recipient_name: str = Field(default="-")
    recipient_phone: str = Field(default="-")
    shipping_address: str
    shipping_courier: str = Field(default="-")
    items_name: str = Field(default="-")
    items_quantity: int = Field(default=1, ge=1)
    panjang_cm: float = Field(default=0, ge=0)
    lebar_cm: float = Field(default=0, ge=0)
    tinggi_cm: float = Field(default=0, ge=0)
    berat_kg: float = Field(default=0, ge=0)
    kendaraan_override: str = Field(default="")
    total_amount: float = Field(default=0, ge=0)


class GeocodedOrder(OrderInput):
    lat: Optional[float] = None
    lng: Optional[float] = None
    geocode_source: str = "Gagal"
    accuracy: str = "gagal"
    vehicle_type: Optional[str] = None
    distance_from_branch_km: Optional[float] = None

