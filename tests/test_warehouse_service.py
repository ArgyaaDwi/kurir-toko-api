import unittest
from unittest.mock import patch

from app.schemas.warehouses import NearestWarehouseRequest
from app.services import warehouse_service
from app.services.warehouse_service import find_nearest_warehouse


def route_by_destination(distances_by_latitude, status="graphhopper"):
    def fake_get_route(coords, vehicle_type, timeout=None):
        return {"distance_km": distances_by_latitude[coords[1][0]], "geometry": [], "status": status}

    return fake_get_route


class NearestWarehouseServiceTests(unittest.TestCase):
    def setUp(self):
        warehouse_service._cache.clear()

    @patch("app.services.warehouse_service.get_route")
    def test_returns_warehouse_with_shortest_car_route(self, get_route):
        # Tiga gudang Surabaya terdekat secara garis lurus; rute terpendek bukan yang terdekat garis lurus.
        get_route.side_effect = route_by_destination({-7.2640: 5.49, -7.31757: 6.1, -7.2412: 4.9})

        response = find_nearest_warehouse(NearestWarehouseRequest(latitude=-7.2856, longitude=112.7758))

        self.assertTrue(response.success)
        self.assertEqual(response.data.warehouse_code, "A - ITC")
        self.assertEqual(response.data.warehouse_name, "Surabaya-ITC")
        self.assertEqual(response.data.distance_km, 4.9)
        self.assertTrue(all(call.args[1] == "MOBIL" for call in get_route.call_args_list))

    @patch("app.services.warehouse_service.get_route")
    def test_routes_only_top_three_straight_line_candidates(self, get_route):
        get_route.side_effect = route_by_destination({-7.2640: 5.49, -7.31757: 6.1, -7.2412: 4.9})

        find_nearest_warehouse(NearestWarehouseRequest(latitude=-7.2856, longitude=112.7758))

        self.assertEqual(get_route.call_count, 3)
        routed = {call.args[0][1][0] for call in get_route.call_args_list}
        self.assertEqual(routed, {-7.2640, -7.31757, -7.2412})

    @patch("app.services.warehouse_service.get_route")
    def test_second_request_for_same_coordinate_uses_cache(self, get_route):
        get_route.side_effect = route_by_destination({-7.2640: 5.49, -7.31757: 6.1, -7.2412: 4.9})

        first = find_nearest_warehouse(NearestWarehouseRequest(latitude=-7.2856, longitude=112.7758))
        second = find_nearest_warehouse(NearestWarehouseRequest(latitude=-7.28561, longitude=112.77579))

        self.assertEqual(get_route.call_count, 3)
        self.assertEqual(first.data, second.data)

    def test_fallback_provider_result_is_not_cached(self):
        for status in ("osrm", "haversine_fallback"):
            with self.subTest(status=status), patch("app.services.warehouse_service.get_route") as get_route:
                warehouse_service._cache.clear()
                get_route.side_effect = route_by_destination({-7.2640: 5.49, -7.31757: 6.1, -7.2412: 4.9}, status=status)

                find_nearest_warehouse(NearestWarehouseRequest(latitude=-7.2856, longitude=112.7758))
                find_nearest_warehouse(NearestWarehouseRequest(latitude=-7.2856, longitude=112.7758))

                self.assertEqual(get_route.call_count, 6)

    def test_rejects_coordinates_outside_valid_bounds(self):
        with self.assertRaises(ValueError):
            NearestWarehouseRequest(latitude=91, longitude=112)


if __name__ == "__main__":
    unittest.main()
