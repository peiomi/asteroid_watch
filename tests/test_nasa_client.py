import unittest
from unittest.mock import MagicMock, patch
from deployment.src.etl.nasa_client import NasaClient


class TestNasaClient(unittest.TestCase):
    def test_client_creation(self):
        client = NasaClient(api_key="test")
        self.assertIsNotNone(client)

    @patch("src.etl.nasa_client.requests.get")
    def test_fetch_returns_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = NasaClient(api_key="test")
        data = client.fetch()

        self.assertEqual(data, {"test": "data"})


if __name__ == "__main__":
    unittest.main()
