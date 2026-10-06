import unittest

from deployment.src.etl.serializer import Serializer
from tests.mock_records import MOCK_RECORDS


class TestSerializer(unittest.TestCase):
    def test_serialize_dataclass_records(self):
        rows = Serializer.serialize_records(records=MOCK_RECORDS)

        self.assertEqual(len(rows), len(MOCK_RECORDS))
        self.assertIsInstance(rows[0], dict)
        self.assertIn("processed_at", rows[0])
        self.assertIsInstance(rows[0]["processed_at"], str)

    def test_serialize_dict_records(self):
        records = [
            {
                "id": "123",
                "name": "Apophis",
                "processed_at": "2026-01-01T00:00:00+00:00",
            }
        ]
        rows = Serializer.serialize_records(records)
        self.assertEqual(rows, records)


if __name__ == "__main__":
    unittest.main()
