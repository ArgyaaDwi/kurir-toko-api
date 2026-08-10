# API v2 Route Optimize

Endpoint ini dipakai oleh Laravel/Omni untuk mengoptimasi urutan pengiriman Kurir Toko Retail dari satu warehouse ke banyak alamat customer.

Endpoint ini khusus rute. Endpoint ini tidak menghitung biaya kirim karena biaya sudah ditangani endpoint pricing yang lain.

## Endpoint

```http
POST /api/v2/routes/optimize
```

Contoh production:

```http
POST https://kurir-toko.argyadwi.site/api/v2/routes/optimize
```

## Kapan Dipakai

Pakai endpoint ini ketika Laravel sudah punya satu route plan berisi beberapa order yang siap diantar dalam satu sesi, misalnya sesi `siang`.

Flow rekomendasi:

1. Laravel membuat route header.
2. Laravel mengumpulkan order Kurir Toko Retail dalam route tersebut.
3. Laravel mengirim payload route ke endpoint ini.
4. API mengembalikan urutan pengiriman hasil optimasi.
5. Laravel update `sequence`, jarak segmen, dan durasi segmen ke setiap `route_order_id`.

## Catatan Perhitungan

- Semua order v2 dihitung sebagai `MOBIL`.
- Field `weight` diterima untuk kebutuhan data, tapi belum dipakai dalam perhitungan rute.
- API memakai koordinat dari `warehouse.latitude`, `warehouse.longitude`, `orders[].latitude`, dan `orders[].longitude`.
- Kalau `return_to_warehouse=true`, total jarak dan durasi akan menambahkan perjalanan dari stop terakhir kembali ke warehouse.
- Endpoint ini tidak melakukan geocoding alamat karena payload Laravel sudah membawa koordinat.
- Urutan output `route` bisa berbeda dari urutan input karena sudah dioptimasi.

## Request Body

```json
{
  "route_id": 12,
  "warehouse": {
    "id": 1,
    "name": "Surabaya",
    "latitude": -7.317566,
    "longitude": 112.764234
  },
  "delivery_date": "2026-08-11",
  "session": "siang",
  "return_to_warehouse": true,
  "orders": [
    {
      "route_order_id": 101,
      "order_id": 9001,
      "invoice_no": "WEB260806E713",
      "customer_name": "dilaaa",
      "phone": "086656556544",
      "address": "Jalan Gubeng Kertajaya Gang IX, Surabaya",
      "latitude": -7.27491971,
      "longitude": 112.75754175,
      "weight": 4.8
    },
    {
      "route_order_id": 102,
      "order_id": 9002,
      "invoice_no": "WEB260806A111",
      "customer_name": "Budi",
      "phone": "081222222222",
      "address": "Jl. Kertajaya Indah Timur, Surabaya",
      "latitude": -7.280411,
      "longitude": 112.786184,
      "weight": 2.1
    },
    {
      "route_order_id": 103,
      "order_id": 9003,
      "invoice_no": "WEB260806B222",
      "customer_name": "Sari",
      "phone": "081333333333",
      "address": "Jl. Ngagel Jaya Selatan, Surabaya",
      "latitude": -7.3025131,
      "longitude": 112.7368934,
      "weight": 1.5
    },
    {
      "route_order_id": 104,
      "order_id": 9004,
      "invoice_no": "WEB260806C333",
      "customer_name": "Raka",
      "phone": "081444444444",
      "address": "Jl. Mulyosari, Surabaya",
      "latitude": -7.260672,
      "longitude": 112.790337,
      "weight": 3.2
    },
    {
      "route_order_id": 105,
      "order_id": 9005,
      "invoice_no": "WEB260806D444",
      "customer_name": "Nadia",
      "phone": "081555555555",
      "address": "Jl. Tenggilis Mejoyo, Surabaya",
      "latitude": -7.3279011,
      "longitude": 112.751305,
      "weight": 0.8
    }
  ]
}
```

## Optional Field

`algorithm` boleh dikirim kalau ingin eksplisit.

```json
{
  "algorithm": "cluster"
}
```

Nilai yang tersedia:

- `cluster`: default, cocok untuk order banyak.
- `nn`: nearest neighbor langsung, cocok untuk order sedikit atau testing.

## Response Body

Jika 5 order valid, maka `route` akan berisi 5 stop.

```json
{
  "route_id": 12,
  "delivery_date": "2026-08-11",
  "session": "siang",
  "warehouse": {
    "id": 1,
    "name": "Surabaya",
    "latitude": -7.317566,
    "longitude": 112.764234
  },
  "return_to_warehouse": true,
  "vehicle_type": "MOBIL",
  "totals": {
    "total_orders": 5,
    "optimized_orders": 5,
    "failed_orders": 0,
    "total_distance_km": 26.63,
    "total_duration_seconds": 2739.085714285714,
    "return_distance_km": 8.69,
    "return_duration_seconds": 893.8285714285714
  },
  "route": [
    {
      "sequence": 1,
      "route_order_id": 105,
      "order_id": 9005,
      "invoice_no": "WEB260806D444",
      "customer_name": "Nadia",
      "phone": "081555555555",
      "address": "Jl. Tenggilis Mejoyo, Surabaya",
      "latitude": -7.3279011,
      "longitude": 112.751305,
      "weight": 0.8,
      "segment_distance_km": 2.29,
      "segment_duration_seconds": 235.54285714285714,
      "segment_duration_text": "3 mnt",
      "cumulative_distance_km": 2.29,
      "cumulative_duration_seconds": 235.54285714285714
    },
    {
      "sequence": 2,
      "route_order_id": 103,
      "order_id": 9003,
      "invoice_no": "WEB260806B222",
      "customer_name": "Sari",
      "phone": "081333333333",
      "address": "Jl. Ngagel Jaya Selatan, Surabaya",
      "latitude": -7.3025131,
      "longitude": 112.7368934,
      "weight": 1.5,
      "segment_distance_km": 4.05,
      "segment_duration_seconds": 416.57142857142856,
      "segment_duration_text": "6 mnt",
      "cumulative_distance_km": 6.34,
      "cumulative_duration_seconds": 652.1142857142856
    },
    {
      "sequence": 3,
      "route_order_id": 101,
      "order_id": 9001,
      "invoice_no": "WEB260806E713",
      "customer_name": "dilaaa",
      "phone": "086656556544",
      "address": "Jalan Gubeng Kertajaya Gang IX, Surabaya",
      "latitude": -7.27491971,
      "longitude": 112.75754175,
      "weight": 4.8,
      "segment_distance_km": 4.78,
      "segment_duration_seconds": 491.65714285714284,
      "segment_duration_text": "8 mnt",
      "cumulative_distance_km": 11.12,
      "cumulative_duration_seconds": 1143.7714285714285
    },
    {
      "sequence": 4,
      "route_order_id": 102,
      "order_id": 9002,
      "invoice_no": "WEB260806A111",
      "customer_name": "Budi",
      "phone": "081222222222",
      "address": "Jl. Kertajaya Indah Timur, Surabaya",
      "latitude": -7.280411,
      "longitude": 112.786184,
      "weight": 2.1,
      "segment_distance_km": 4.02,
      "segment_duration_seconds": 413.4857142857142,
      "segment_duration_text": "6 mnt",
      "cumulative_distance_km": 15.14,
      "cumulative_duration_seconds": 1557.2571428571428
    },
    {
      "sequence": 5,
      "route_order_id": 104,
      "order_id": 9004,
      "invoice_no": "WEB260806C333",
      "customer_name": "Raka",
      "phone": "081444444444",
      "address": "Jl. Mulyosari, Surabaya",
      "latitude": -7.260672,
      "longitude": 112.790337,
      "weight": 3.2,
      "segment_distance_km": 2.8,
      "segment_duration_seconds": 288,
      "segment_duration_text": "4 mnt",
      "cumulative_distance_km": 17.94,
      "cumulative_duration_seconds": 1845.2571428571428
    }
  ],
  "failed": []
}
```

## Field Penting Untuk Laravel

- `route[].sequence`: urutan pengiriman hasil optimasi.
- `route[].route_order_id`: ID baris route order yang harus di-update di Laravel.
- `route[].segment_distance_km`: jarak dari titik sebelumnya ke stop ini.
- `route[].segment_duration_seconds`: durasi dari titik sebelumnya ke stop ini.
- `route[].cumulative_distance_km`: akumulasi jarak sampai stop ini.
- `totals.total_distance_km`: total jarak rute, termasuk return trip kalau `return_to_warehouse=true`.
- `totals.return_distance_km`: jarak dari stop terakhir balik ke warehouse.
- `failed`: order yang tidak bisa dioptimasi, misalnya koordinat kosong.

## Response Failed Order

Kalau ada order tanpa koordinat, order tersebut tidak dimasukkan ke `route`, tapi masuk ke `failed`.

```json
{
  "totals": {
    "total_orders": 5,
    "optimized_orders": 4,
    "failed_orders": 1,
    "total_distance_km": 20.1,
    "total_duration_seconds": 2500,
    "return_distance_km": 4.5,
    "return_duration_seconds": 500
  },
  "failed": [
    {
      "route_order_id": 105,
      "order_id": 9005,
      "invoice_no": "WEB260806D444",
      "reason": "Order coordinate is missing."
    }
  ]
}
```

## Contoh cURL

```bash
curl -X POST "https://kurir-toko.argyadwi.site/api/v2/routes/optimize" \
  -H "Content-Type: application/json" \
  -d @payload.json
```
