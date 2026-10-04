import unittest
from unittest.mock import MagicMock, patch
from deployment.src.etl.cloud_storage import CloudStorage


class TestCloudStorage(unittest.TestCase):
    @patch("src.etl.cloud_storage.storage.Client")
    def test_upload_json(self, mock_client):
        mock_blob = MagicMock()
        mock_bucket = MagicMock()

        mock_bucket.blob.return_value = mock_blob
        mock_client.return_value.bucket.return_value = mock_bucket

        storage = CloudStorage("test-bucket")

        storage.upload_json({"test": "value"}, "raw/test.json")

        mock_bucket.blob.assert_called_once_with("raw/test.json")
        mock_blob.upload_from_string.assert_called_once()


if __name__ == "__main__":
    unittest.main()
