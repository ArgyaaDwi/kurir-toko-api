from app.domain.vehicles import KURIR_TOKO_KEYWORDS, VEHICLE_CONFIG


def is_kurir_toko(value: str) -> bool:
    if not value or str(value).strip() == "":
        return False
    normalized = str(value).lower().replace(" ", "").replace("_", "")
    return any(keyword.replace(" ", "") in normalized for keyword in KURIR_TOKO_KEYWORDS)


def classify_vehicle(
    panjang_cm: float,
    lebar_cm: float,
    tinggi_cm: float,
    berat_kg: float,
    qty: int,
    override: str = "",
) -> str:
    normalized_override = str(override).strip().upper()
    if normalized_override in ("MOTOR", "MOBIL"):
        return normalized_override

    motor = VEHICLE_CONFIG["MOTOR"]
    if panjang_cm == 0 and lebar_cm == 0 and tinggi_cm == 0 and berat_kg == 0:
        return "MOTOR"

    is_motor = (
        panjang_cm <= motor["max_panjang"]
        and lebar_cm <= motor["max_lebar"]
        and tinggi_cm <= motor["max_tinggi"]
        and berat_kg <= motor["max_berat"]
        and qty <= motor["max_qty"]
    )
    return "MOTOR" if is_motor else "MOBIL"

