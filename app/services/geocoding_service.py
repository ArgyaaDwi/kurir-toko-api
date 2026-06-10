import re
from typing import Tuple

from app.domain.region_fallback import REGION_FALLBACK
from app.integrations.geocoders import gentle_delay, locationiq, nominatim, photon


SINGKATAN = {
    r"\bJl\.?\b": "Jalan",
    r"\bJln\.?\b": "Jalan",
    r"\bNo\.?\s*": "Nomor ",
    r"\bKec\.?\b": "Kecamatan",
    r"\bKel\.?\b": "Kelurahan",
    r"\bKab\.?\b": "Kabupaten",
    r"\bRT\.?\s*\d+\s*[/,]?\s*RW\.?\s*\d+\b": "",
    r"\bRT\.?\s*\d+\b": "",
    r"\bRW\.?\s*\d+\b": "",
    r"\bGg\.?\b": "Gang",
    r"\bPerum\.?\b": "Perumahan",
}


def extract_coords(text: str) -> Tuple[float | None, float | None]:
    match = re.search(r"\(?(-[1-9]\d?\.\d{3,})\s*,\s*(1[0-2]\d\.\d{3,})\)?", str(text))
    if match:
        lat, lng = float(match.group(1)), float(match.group(2))
        if -11 <= lat <= 6 and 94 <= lng <= 141:
            return lat, lng
    return None, None


def clean_address(raw: str) -> str:
    address = raw
    for pattern, replacement in SINGKATAN.items():
        address = re.sub(pattern, replacement, address, flags=re.IGNORECASE)
    address = re.sub(r"\bIndonesia\b", "", address, flags=re.IGNORECASE)
    address = re.sub(r"\b\d{5}\b", "", address)
    address = re.sub(r"\s{2,}", " ", address).strip()
    parts = [part.strip() for part in address.split(",") if len(part.strip()) > 2]
    unique_parts = []
    seen = set()
    for part in parts:
        key = part.lower()
        if key not in seen:
            seen.add(key)
            unique_parts.append(part)
    return ", ".join(unique_parts[:6])


def region_fallback(raw: str) -> Tuple[float | None, float | None]:
    text = raw.lower()
    for key in sorted(REGION_FALLBACK, key=len, reverse=True):
        if key in text:
            return REGION_FALLBACK[key]
    return None, None


def geocode_address(raw: str) -> tuple:
    lat, lng = extract_coords(raw)
    if lat is not None and lng is not None:
        return lat, lng, "Koordinat langsung", "tinggi"

    cleaned = clean_address(raw)
    lat, lng = locationiq(f"{cleaned}, Indonesia")
    if lat is not None and lng is not None:
        return lat, lng, "LocationIQ", "tinggi"

    gentle_delay()
    lat, lng = nominatim(f"{cleaned}, Indonesia")
    if lat is not None and lng is not None:
        return lat, lng, "Nominatim", "tinggi"

    gentle_delay()
    lat, lng = photon(f"{cleaned} Indonesia")
    if lat is not None and lng is not None:
        return lat, lng, "Photon", "tinggi"

    gentle_delay()
    lat, lng = region_fallback(raw)
    if lat is not None and lng is not None:
        return lat, lng, "Estimasi wilayah", "sedang"

    return None, None, "Gagal", "gagal"

