# Nearest Warehouse

Endpoint untuk mencari warehouse terdekat dari koordinat user.

## Endpoint

```text
POST /api/v1/nearest-wh
```

## Request

```json
{
  "latitude": -7.9825,
  "longitude": 112.6255
}
```

`latitude` harus berada di antara `-90` dan `90`, sedangkan `longitude` harus berada di antara `-180` dan `180`.

## Response

```json
{
  "success": true,
  "data": {
    "warehouse_code": "F - MLG",
    "warehouse_name": "Malang",
    "address": "Jl. Pulau Sayang No.16, Kasin",
    "latitude": -7.982,
    "longitude": 112.625,
    "distance_km": 0.18
  }
}
```

## Perhitungan Jarak

API menghitung rute dari koordinat user ke masing-masing warehouse menggunakan kendaraan mobil. Provider digunakan berurutan:

1. GraphHopper dengan profile `car`
2. OpenRouteService dengan profile `driving-car`
3. OSRM dengan profile `driving`
4. Fallback Haversine dengan faktor estimasi mobil jika semua provider tidak tersedia

Nilai `distance_km` adalah jarak rute dalam kilometer dan dibulatkan menjadi dua angka desimal. Warehouse dengan jarak paling kecil dikembalikan.

## Daftar Warehouse

Data warehouse saat ini di-hardcode pada `app/domain/warehouses.py` dan dapat diubah tanpa mengubah logic endpoint.

## Error Validasi

Payload dengan koordinat di luar batas valid akan menghasilkan HTTP `422` dari FastAPI.
