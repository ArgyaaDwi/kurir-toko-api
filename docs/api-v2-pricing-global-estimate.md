# API v2 Global Pricing Estimate

Endpoint ini menentukan kendaraan pengiriman dari isi satu invoice, kemudian menghitung ongkir berdasarkan tarif kendaraan tersebut. Endpoint v1 tetap tersedia dan tidak berubah.

```http
POST /api/v2/pricing/global-estimate
```

## Aturan kendaraan

- Satu invoice dikirim dengan satu kendaraan.
- Jika satu SKU memiliki panjang lebih dari 100 cm, lebar lebih dari 80 cm, tinggi lebih dari 90 cm, atau berat per barang lebih dari 30 kg, seluruh invoice menggunakan `MOBIL`.
- Jika setiap SKU memenuhi batas motor tetapi total `berat_kg * qty` seluruh invoice lebih dari 30 kg, seluruh invoice menggunakan `MOBIL`.
- Selain itu invoice menggunakan `MOTOR`.

Batas kapasitas dan tarif ditentukan melalui environment variable, jadi dapat diubah tanpa mengubah payload API.

## Request body

`berat_kg` dan dimensi pada setiap item adalah ukuran untuk satu barang. Nilai `qty` dipakai untuk menghitung akumulasi berat invoice.

```json
{
  "origin": { "lat": -7.317566, "lng": 112.764234 },
  "destination": { "lat": -7.2782163, "lng": 112.7572735 },
  "items": [
    {
      "sku": "LAMP-LED-12W",
      "qty": 2,
      "panjang_cm": 20,
      "lebar_cm": 15,
      "tinggi_cm": 10,
      "berat_kg": 0.5
    }
  ]
}
```

## Response body

```json
{
  "origin": { "lat": -7.317566, "lng": 112.764234 },
  "destination": { "lat": -7.2782163, "lng": 112.7572735 },
  "vehicle_type": "MOTOR",
  "vehicle_reason": "Semua item dan total beban invoice memenuhi kapasitas motor.",
  "distance_km": 6.41,
  "duration_seconds": 493.5,
  "base_fee": 0,
  "cost_per_km": 1000,
  "minimum_fee": 0,
  "total_cost": 6410,
  "provider": "OSRM",
  "status": "osrm"
}
```

`cost_per_km`, `base_fee`, dan `minimum_fee` pada respons selalu merupakan tarif kendaraan yang dipilih pada `vehicle_type`.

## Environment variable

```env
V2_PRICING_MOTOR_BASE_FEE=0
V2_PRICING_MOTOR_COST_PER_KM=1000
V2_PRICING_MOTOR_MINIMUM_FEE=0
V2_PRICING_MOBIL_BASE_FEE=0
V2_PRICING_MOBIL_COST_PER_KM=2500
V2_PRICING_MOBIL_MINIMUM_FEE=0
V2_PRICING_MOTOR_MAX_PANJANG_CM=100
V2_PRICING_MOTOR_MAX_LEBAR_CM=80
V2_PRICING_MOTOR_MAX_TINGGI_CM=90
V2_PRICING_MOTOR_MAX_BERAT_KG=30
```
