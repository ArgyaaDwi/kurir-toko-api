# Kurir Toko API

backend API untuk integrasi `Kurir Toko` memakai `FastAPI` dan `Docker (kalo mau wkwkw)`.

## Fitur awal

- `GET /health`
- `POST /api/v1/routes/optimize`
- `POST /api/v1/batches/plan`
- `POST /api/v1/pricing/estimate`
- `POST /api/v1/pricing/global-estimate`
- Geocoding alamat
- Klasifikasi motor vs mobil
- Filter order `Kurir Toko`
- Optimasi rute
- Hitung biaya kirim dari koordinat asal ke tujuan
- Hitung biaya kirim global tanpa `vehicle_type`

## Jalankan lokal

```bash
copy .env.example .env
isi .env dengan API_KEY
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Jalankan dengan Docker

```bash
copy .env.example .env
isi .env dengan API_KEY
docker compose up --build
```

## Variabel biaya global

Atur di `.env` kalau mau ubah ongkir global endpoint terpisah:

```env
GLOBAL_PRICING_BASE_FEE=0
GLOBAL_PRICING_COST_PER_KM=1500
GLOBAL_PRICING_MINIMUM_FEE=0
GLOBAL_PRICING_ROUTE_VEHICLE_TYPE=MOBIL
```

## Request contoh banyak Order untuk cari rute

```json
{
  "branch": {
    "code": "SUB"
  },
  "orders": [
    {
      "invoice_no": "INV-001",
      "so_number": "SO-001",
      "order_date": "2026-06-10 09:10:00",
      "recipient_name": "Budi",
      "recipient_phone": "08111111111",
      "shipping_address": "Jl. Rungkut Industri, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Lampu LED",
      "items_quantity": 1,
      "panjang_cm": 20,
      "lebar_cm": 15,
      "tinggi_cm": 10,
      "berat_kg": 2,
      "kendaraan_override": "",
      "total_amount": 120000
    },
    {
      "invoice_no": "INV-002",
      "so_number": "SO-002",
      "order_date": "2026-06-10 09:20:00",
      "recipient_name": "Siti",
      "recipient_phone": "08222222222",
      "shipping_address": "Jl. Gubeng Kertajaya, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Sabun",
      "items_quantity": 2,
      "panjang_cm": 25,
      "lebar_cm": 20,
      "tinggi_cm": 15,
      "berat_kg": 4,
      "kendaraan_override": "",
      "total_amount": 85000
    },
    {
      "invoice_no": "INV-003",
      "so_number": "SO-003",
      "order_date": "2026-06-10 09:35:00",
      "recipient_name": "Andi",
      "recipient_phone": "08333333333",
      "shipping_address": "Jl. Jemursari, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Sprei",
      "items_quantity": 1,
      "panjang_cm": 80,
      "lebar_cm": 60,
      "tinggi_cm": 30,
      "berat_kg": 12,
      "kendaraan_override": "",
      "total_amount": 350000
    },
    {
      "invoice_no": "INV-004",
      "so_number": "SO-004",
      "order_date": "2026-06-10 09:50:00",
      "recipient_name": "Rina",
      "recipient_phone": "08444444444",
      "shipping_address": "Jl. Wiyung Asri, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Kursi Lipat",
      "items_quantity": 1,
      "panjang_cm": 100,
      "lebar_cm": 70,
      "tinggi_cm": 60,
      "berat_kg": 25,
      "kendaraan_override": "",
      "total_amount": 500000
    },
    {
      "invoice_no": "INV-005",
      "so_number": "SO-005",
      "order_date": "2026-06-10 10:05:00",
      "recipient_name": "Doni",
      "recipient_phone": "08555555555",
      "shipping_address": "Jl. Tandes Lor, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Galon",
      "items_quantity": 1,
      "panjang_cm": 35,
      "lebar_cm": 35,
      "tinggi_cm": 40,
      "berat_kg": 18,
      "kendaraan_override": "",
      "total_amount": 95000
    },
    {
      "invoice_no": "INV-006",
      "so_number": "SO-006",
      "order_date": "2026-06-10 10:20:00",
      "recipient_name": "Maya",
      "recipient_phone": "08666666666",
      "shipping_address": "Jl. Wonokromo, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Buku",
      "items_quantity": 3,
      "panjang_cm": 18,
      "lebar_cm": 12,
      "tinggi_cm": 8,
      "berat_kg": 1,
      "kendaraan_override": "",
      "total_amount": 65000
    }
  ],
  "kurir_toko_only": true,
  "algorithm": "cluster"
}
```

## Request contoh hitung biaya kirim

```json
{
  "origin": {
    "lat": -7.317566,
    "lng": 112.764234
  },
  "destination": {
    "lat": -7.2782163,
    "lng": 112.7572735
  },
  "vehicle_type": "MOTOR"
}
```

## Response contoh hitung biaya kirim

```json
{
  "origin": {
    "lat": -7.317566,
    "lng": 112.764234
  },
  "destination": {
    "lat": -7.2782163,
    "lng": 112.7572735
  },
  "vehicle_type": "MOTOR",
  "distance_km": 6.41,
  "duration_seconds": 493.5,
  "cost_per_km": 1000,
  "total_cost": 6410,
  "provider": "OSRM",
  "status": "osrm"
}
```

## Request contoh hitung biaya kirim global

```json
{
  "origin": {
    "lat": -7.317566,
    "lng": 112.764234
  },
  "destination": {
    "lat": -7.2782163,
    "lng": 112.7572735
  }
}
```

## Response contoh hitung biaya kirim global

```json
{
  "origin": {
    "lat": -7.317566,
    "lng": 112.764234
  },
  "destination": {
    "lat": -7.2782163,
    "lng": 112.7572735
  },
  "routing_vehicle_type": "MOBIL",
  "distance_km": 6.41,
  "duration_seconds": 493.5,
  "base_fee": 0,
  "cost_per_km": 1500,
  "minimum_fee": 0,
  "total_cost": 9615,
  "provider": "OSRM",
  "status": "osrm"
}
```
