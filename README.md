# Kurir Toko API

POC backend untuk integrasi `Kurir Toko` ke sistem omnichannel memakai `FastAPI` dan `Docker`.

## Fitur awal

- `GET /health`
- `POST /api/v1/routes/optimize`
- `POST /api/v1/batches/plan`
- Geocoding alamat
- Klasifikasi motor vs mobil
- Filter order `Kurir Toko`
- Optimasi rute sederhana tanpa database

## Jalankan lokal

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Jalankan dengan Docker

```bash
copy .env.example .env
docker compose up --build
```

## Request contoh

```json
{
  "branch": { "code": "SUB" },
  "kurir_toko_only": true,
  "algorithm": "cluster",
  "orders": [
    {
      "invoice_no": "INV-001",
      "recipient_name": "Budi",
      "recipient_phone": "08123456789",
      "shipping_address": "Jl. Rungkut Industri, Surabaya",
      "shipping_courier": "Kurir Toko",
      "items_name": "Lampu",
      "items_quantity": 1,
      "panjang_cm": 20,
      "lebar_cm": 20,
      "tinggi_cm": 20,
      "berat_kg": 2
    }
  ]
}
```
