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

RETAIL_ORDER_ESTIMATE_REQUEST_EXAMPLES = {
    "web_order": {
        "summary": "Payload real order Web/Omni",
        "description": "Contoh payload dari observer Omni untuk Kurir Toko Retail.",
        "value": {
            "data": {
                "account_id": 10444,
                "order": {
                    "local_id": "WEB260806E713",
                    "order_batch_code": None,
                    "ordered_at": "2026-08-06 15:33:17",
                    "shipping_price": "6350",
                    "shipping_provider": "Kurir Toko Retail - Sesi Siang",
                    "nextday": True,
                    "note": "-",
                    "internal_note": "-",
                    "warehouse_id": 759,
                    "totalWeight": "4.8",
                    "address": {
                        "name": "dilaaa",
                        "phone": "086656556544",
                        "address_1": "Jalan Gubeng Kertajaya Gang IX, RW 04, Airlangga, Gubeng, Surabaya, East Java, 60286, Indonesia",
                        "address_2": "",
                        "sub_district": "Gubeng",
                        "district": "Gubeng",
                        "city": "Kota Surabaya",
                        "province": "Jawa Timur",
                        "country": "Indonesia",
                        "postal_code": "60286",
                        "latitude": "-7.2749197116067",
                        "longitude": "112.75754175306",
                    },
                    "item_lines": [
                        {
                            "local_id": "dbklik5_18108",
                            "variant_id": 0,
                            "sku": "AKBL04",
                            "name": "Keyboard Mouse Wireless Logitech MK220",
                            "price": 300000,
                            "sale_price": 0,
                            "quantity": 4,
                            "weight": 1.2,
                            "warehouse_splits": [
                                {
                                    "warehouse_id": 759,
                                    "warehouse_name": "Surabaya",
                                    "qty": 4,
                                }
                            ],
                            "item_type": "regular",
                        }
                    ],
                    "payment": {
                        "status_payment": "1",
                        "payment_method": "Xendit Va Mandiri",
                    },
                },
            }
        },
    }
}

RETAIL_ORDER_ESTIMATE_RESPONSE_EXAMPLE = {
    "account_id": 10444,
    "order_local_id": "WEB260806E713",
    "shipping_provider": "Kurir Toko Retail - Sesi Siang",
    "eligible": True,
    "warehouse": {
        "warehouse_id": 759,
        "code": "SUB",
        "name": "Surabaya",
        "lat": -7.317566,
        "lng": 112.764234,
    },
    "destination": {
        "name": "dilaaa",
        "phone": "086656556544",
        "address": "Jalan Gubeng Kertajaya Gang IX, RW 04, Airlangga, Gubeng, Surabaya, East Java, 60286, Indonesia, Kota Surabaya, Jawa Timur",
        "lat": -7.2749197116067,
        "lng": 112.75754175306,
    },
    "total_weight_kg": 4.8,
    "item_count": 4,
    "distance_km": 5.79,
    "duration_seconds": 734.301,
    "base_fee": 0.0,
    "cost_per_km": 1500.0,
    "minimum_fee": 0.0,
    "current_shipping_price": 6350.0,
    "calculated_shipping_price": 8685.0,
    "price_difference": 2335.0,
    "shipping_price_changed": True,
    "provider": "GraphHopper",
    "status": "graphhopper",
}
