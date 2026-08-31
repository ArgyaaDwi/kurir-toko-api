import unittest
from unittest.mock import patch

from app.schemas.warehouses import NearestWarehouseRequest
from app.services.warehouse_service import find_nearest_warehouse


class NearestWarehouseServiceTests(unittest.TestCase):
    @patch("app.services.warehouse_service.get_route")
    def test_returns_warehouse_with_shortest_car_route(self, get_route):
        distances = [12.0, 8.5, 4.25, 3.75, 0.18, 6.0, 5.0]
        get_route.side_effect = [
            {"distance_km": distance, "geometry": []} for distance in distances
        ]

        response = find_nearest_warehouse(
            NearestWarehouseRequest(latitude=-7.9825, longitude=112.6255)
        )

        self.assertTrue(response.success)
        self.assertEqual(response.data.warehouse_code, "F - MLG")
        self.assertEqual(response.data.warehouse_name, "Malang")
        self.assertEqual(response.data.distance_km, 0.18)
        self.assertTrue(all(call.args[1] == "MOBIL" for call in get_route.call_args_list))

    def test_rejects_coordinates_outside_valid_bounds(self):
        with self.assertRaises(ValueError):
            NearestWarehouseRequest(latitude=91, longitude=112)


if __name__ == "__main__":
    unittest.main()
