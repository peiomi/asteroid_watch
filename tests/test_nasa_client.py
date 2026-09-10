import unittest
from src.etl.nasa_client import NasaClient


class TestNasaClient(unittest.TestCase):
    def test_client_creation(self):
        client = NasaClient()
        self.assertIsNotNone(client)

    def test_fetch_returns_data(self):
        client = NasaClient()
        data = client.fetch()
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
