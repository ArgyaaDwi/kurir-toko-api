ROOT_RESPONSE_EXAMPLE = {
    "service": "kurir-toko-api",
    "version": "0.1.0",
    "docs": "/docs",
}

HEALTH_RESPONSE_EXAMPLE = {
    "status": "ok",
}

ORDER_SAMPLE_1 = {
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
    "total_amount": 120000,
}

ORDER_SAMPLE_2 = {
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
    "total_amount": 85000,
}

ROUTING_REQUEST_EXAMPLES = {
    "basic": {
        "summary": "Optimasi rute 2 order",
        "description": "Contoh payload untuk optimasi urutan pengiriman dari cabang SUB.",
        "value": {
            "branch": {
                "code": "SUB",
            },
            "orders": [
                ORDER_SAMPLE_1,
                ORDER_SAMPLE_2,
            ],
            "kurir_toko_only": True,
            "algorithm": "cluster",
        },
    }
}

ROUTING_RESPONSE_EXAMPLE = {
    "branch": {
        "code": "SUB",
        "name": "Surabaya",
        "lat": -7.317566,
        "lng": 112.764234,
    },
    "totals": {
        "orders_processed": 2,
        "eligible_orders": 2,
        "failed_geocodes": 0,
        "excluded_orders": 0,
        "total_distance_km": 21.37,
        "total_duration_seconds": 1556.0,
        "total_cost": 21370.0,
    },
    "motor": {
        "vehicle_type": "MOTOR",
        "stop_count": 2,
        "total_distance_km": 21.37,
        "total_duration_seconds": 1556.0,
        "return_distance_km": 6.41,
        "return_duration_seconds": 493.5,
        "total_cost": 21370.0,
        "route": [
            {
                "order": {
                    **ORDER_SAMPLE_1,
                    "lat": -7.3279011,
                    "lng": 112.751305,
                    "geocode_source": "LocationIQ",
                    "accuracy": "tinggi",
                    "vehicle_type": "MOTOR",
                    "distance_from_branch_km": 1.83,
                },
                "segment_distance_km": 4.19,
                "segment_duration_seconds": 405.5,
                "segment_duration_text": "6 mnt",
            },
            {
                "order": {
                    **ORDER_SAMPLE_2,
                    "lat": -7.2782163,
                    "lng": 112.7572735,
                    "geocode_source": "LocationIQ",
                    "accuracy": "tinggi",
                    "vehicle_type": "MOTOR",
                    "distance_from_branch_km": 4.44,
                },
                "segment_distance_km": 10.77,
                "segment_duration_seconds": 657.0,
                "segment_duration_text": "10 mnt",
            },
        ],
    },
    "mobil": {
        "vehicle_type": "MOBIL",
        "stop_count": 0,
        "total_distance_km": 0.0,
        "total_duration_seconds": 0.0,
        "return_distance_km": 0.0,
        "return_duration_seconds": 0.0,
        "total_cost": 0.0,
        "route": [],
    },
    "excluded": [],
    "failed_geocodes": [],
}

PRICING_REQUEST_EXAMPLES = {
    "motor": {
        "summary": "Hitung biaya kirim berdasarkan kendaraan",
        "description": "Contoh payload ongkir dari koordinat gudang ke customer dengan kendaraan MOTOR.",
        "value": {
            "origin": {
                "lat": -7.317566,
                "lng": 112.764234,
            },
            "destination": {
                "lat": -7.2782163,
                "lng": 112.7572735,
            },
            "vehicle_type": "MOTOR",
        },
    }
}

PRICING_RESPONSE_EXAMPLE = {
    "origin": {
        "lat": -7.317566,
        "lng": 112.764234,
    },
    "destination": {
        "lat": -7.2782163,
        "lng": 112.7572735,
    },
    "vehicle_type": "MOTOR",
    "distance_km": 6.41,
    "duration_seconds": 493.5,
    "cost_per_km": 1000.0,
    "total_cost": 6410.0,
    "provider": "OSRM",
    "status": "osrm",
}

GLOBAL_PRICING_REQUEST_EXAMPLES = {
    "global": {
        "summary": "Hitung biaya kirim global",
        "description": "Contoh payload ongkir global tanpa vehicle_type dari request.",
        "value": {
            "origin": {
                "lat": -7.317566,
                "lng": 112.764234,
            },
            "destination": {
                "lat": -7.2782163,
                "lng": 112.7572735,
            },
        },
    }
}

GLOBAL_PRICING_RESPONSE_EXAMPLE = {
    "origin": {
        "lat": -7.317566,
        "lng": 112.764234,
    },
    "destination": {
        "lat": -7.2782163,
        "lng": 112.7572735,
    },
    "distance_km": 6.41,
    "duration_seconds": 493.5,
    "base_fee": 0.0,
    "cost_per_km": 1500.0,
    "minimum_fee": 0.0,
    "total_cost": 9615.0,
    "provider": "OSRM",
    "status": "osrm",
}

V2_GLOBAL_PRICING_REQUEST_EXAMPLES = {
    "motor": {
        "summary": "Invoice yang dapat dikirim motor",
        "description": "Semua SKU dan total berat invoice memenuhi kapasitas motor.",
        "value": {
            "origin": {
                "lat": -7.317566,
                "lng": 112.764234,
            },
            "destination": {
                "lat": -7.2782163,
                "lng": 112.7572735,
            },
            "items": [
                {
                    "sku": "LAMP-LED-12W",
                    "qty": 2,
                    "panjang_cm": 20,
                    "lebar_cm": 15,
                    "tinggi_cm": 10,
                    "berat_kg": 0.5,
                },
                {
                    "sku": "KABEL-USB-C-2M",
                    "qty": 1,
                    "panjang_cm": 15,
                    "lebar_cm": 10,
                    "tinggi_cm": 5,
                    "berat_kg": 0.2,
                },
            ],
        },
    },
    "mobil": {
        "summary": "Invoice yang wajib dikirim mobil",
        "description": "Satu SKU melebihi batas panjang motor sehingga seluruh invoice dikirim mobil.",
        "value": {
            "origin": {
                "lat": -7.317566,
                "lng": 112.764234,
            },
            "destination": {
                "lat": -7.2782163,
                "lng": 112.7572735,
            },
            "items": [
                {
                    "sku": "MEJA-LIPAT-120",
                    "qty": 1,
                    "panjang_cm": 110,
                    "lebar_cm": 60,
                    "tinggi_cm": 75,
                    "berat_kg": 18,
                }
            ],
        },
    },
}

V2_GLOBAL_PRICING_RESPONSE_EXAMPLE = {
    "origin": {
        "lat": -7.317566,
        "lng": 112.764234,
    },
    "destination": {
        "lat": -7.2782163,
        "lng": 112.7572735,
    },
    "vehicle_type": "MOBIL",
    "vehicle_reason": (
        "SKU MEJA-LIPAT-120 memiliki panjang 110 cm, melebihi batas motor 100 cm."
    ),
    "distance_km": 6.41,
    "duration_seconds": 554.0,
    "base_fee": 0.0,
    "cost_per_km": 2500.0,
    "minimum_fee": 0.0,
    "total_cost": 16025.0,
    "provider": "OSRM",
    "status": "osrm",
}

BATCH_REQUEST_EXAMPLES = {
    "basic": {
        "summary": "Bagi order ke batch pengiriman",
        "description": "Contoh payload batching order berdasarkan cutoff time.",
        "value": {
            "branch_code": "SUB",
            "windows": [
                {"name": "PAGI", "cutoff_time": "09:00"},
                {"name": "SIANG", "cutoff_time": "13:00"},
                {"name": "SORE", "cutoff_time": "16:00"},
            ],
            "orders": [
                ORDER_SAMPLE_1,
                ORDER_SAMPLE_2,
            ],
            "kurir_toko_only": True,
            "algorithm": "cluster",
        },
    }
}

BATCH_RESPONSE_EXAMPLE = {
    "branch_code": "SUB",
    "batch_count": 1,
    "batches": [
        {
            "batch_name": "SIANG",
            "cutoff_time": "13:00",
            "order_count": 2,
            "routing_result": ROUTING_RESPONSE_EXAMPLE,
        }
    ],
}

V2_OPTIMIZE_ROUTE_REQUEST_EXAMPLES = {
    "laravel_route": {
        "summary": "Payload route Laravel/Omni",
        "description": "Contoh payload route berisi 5 order Kurir Toko Retail dari Laravel.",
        "value": {
            "route_id": 12,
            "warehouse": {
                "id": 1,
                "name": "Surabaya",
                "latitude": -7.317566,
                "longitude": 112.764234,
            },
            "delivery_date": "2026-08-11",
            "session": "siang",
            "return_to_warehouse": True,
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
                    "weight": 4.8,
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
                    "weight": 2.1,
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
                    "weight": 1.5,
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
                    "weight": 3.2,
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
                    "weight": 0.8,
                },
            ],
        },
    }
}

V2_OPTIMIZE_ROUTE_RESPONSE_EXAMPLE = {
    "route_id": 12,
    "delivery_date": "2026-08-11",
    "session": "siang",
    "warehouse": {
        "id": 1,
        "name": "Surabaya",
        "latitude": -7.317566,
        "longitude": 112.764234,
    },
    "return_to_warehouse": True,
    "vehicle_type": "MOBIL",
    "totals": {
        "total_orders": 5,
        "optimized_orders": 5,
        "failed_orders": 0,
        "total_distance_km": 26.63,
        "total_duration_seconds": 2739.085714285714,
        "return_distance_km": 8.69,
        "return_duration_seconds": 893.8285714285714,
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
            "cumulative_duration_seconds": 235.54285714285714,
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
            "cumulative_duration_seconds": 652.1142857142856,
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
            "cumulative_duration_seconds": 1143.7714285714285,
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
            "cumulative_duration_seconds": 1557.2571428571428,
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
            "segment_duration_seconds": 288.0,
            "segment_duration_text": "4 mnt",
            "cumulative_distance_km": 17.94,
            "cumulative_duration_seconds": 1845.2571428571428,
        },
    ],
    "failed": [],
}
