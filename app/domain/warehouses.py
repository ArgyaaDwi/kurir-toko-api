WAREHOUSES_DEFAULT = [
    {"warehouse_id": 759, "code": "SUB", "name": "Surabaya", "lat": -7.317566, "lng": 112.764234},
]


def get_warehouse_by_id(warehouse_id: int) -> dict:
    for warehouse in WAREHOUSES_DEFAULT:
        if warehouse["warehouse_id"] == warehouse_id:
            return warehouse
    raise ValueError(f"Unknown warehouse_id: {warehouse_id}")
