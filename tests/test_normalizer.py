import unittest
from src.etl.normalizer import Normalizer

asteroid1 = {
    "id": "123",
    "name": "Apollo",
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 1.0,
            "estimated_diameter_max": 2.0,
        }
    },
    "close_approach_data": [
        {
            "miss_distance": {"kilometers": "1000"},
            "relative_velocity": {"kilometers_per_second": "25"},
            "close_approach_date": "2025-01-01",
        }
    ],
    "is_potentially_hazardous_asteroid": True,
}

asteroid2 = {
    "id": "456",
    "name": "Athena",
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 1.0,
            "estimated_diameter_max": 2.0,
        }
    },
    "close_approach_data": [
        {
            "miss_distance": {"kilometers": "1000"},
            "relative_velocity": {"kilometers_per_second": "25"},
            "close_approach_date": "2025-01-01",
        }
    ],
    "is_potentially_hazardous_asteroid": True,
}

asteroid_missing_data = {
    "id": "123",
    "name": "Apollo",
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 1.0,
            "estimated_diameter_max": 2.0,
        }
    },
    "is_potentially_hazardous_asteroid": True,
}


class TestNormalizer(unittest.TestCase):
    def test_normalize_single_asteroid(self):
        data = {"near_earth_objects": {"2025-01-01": [asteroid1]}}

        result = Normalizer().normalize(data)

        record = result[0]
        self.assertEqual(record.id, "123")
        self.assertEqual(record.name, "Apollo")
        self.assertEqual(record.diameter_min, 1.0)
        self.assertEqual(record.diameter_max, 2.0)
        self.assertEqual(record.miss_distance_km, 1000.0)
        self.assertEqual(record.relative_velocity_km_s, 25.0)
        self.assertEqual(record.is_hazardous, True)
        self.assertEqual(record.close_approach_date, "2025-01-01")

    def test_normalize_multiple_asteroids(self):
        data = {"near_earth_objects": {"2025-01-01": [asteroid1, asteroid2]}}

        result = Normalizer().normalize(data)
        record1 = result[0]
        record2 = result[1]

        self.assertNotEqual(record1.id, record2.id)
        self.assertEqual(len(result), 2)
        self.assertEqual(record1.id, "123")
        self.assertEqual(record2.id, "456")

    def test_empty_data(self):
        data = {"near_earth_objects": {}}
        result = Normalizer().normalize(data)
        self.assertEqual(result, [])

    def test_missing_data(self):
        data = {"near_earth_objects": {"2025-01-01": [asteroid_missing_data]}}
        result = Normalizer().normalize(data)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
