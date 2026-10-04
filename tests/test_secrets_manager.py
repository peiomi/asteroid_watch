import unittest
from unittest.mock import MagicMock, patch
from deployment.src.etl.secrets_manager import SecretsManager
from google.api_core.exceptions import (
    PermissionDenied,
)


class TestSecretsManager(unittest.TestCase):

    @patch("src.etl.secrets_manager.secretmanager.SecretManagerServiceClient")
    def test_get_secret_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.payload.data = b"super_secret"

        mock_client.return_value.access_secret_version.return_value = mock_response

        manager = SecretsManager()
        secret = manager.get_secret("nasa_api_key")

        self.assertEqual(secret, "super_secret")

    @patch("src.etl.secrets_manager.Settings")
    def test_project_id_missing(self, mock_settings):
        mock_settings.PROJECT_ID = None
        manager = SecretsManager()

        with self.assertRaises(ValueError):
            manager.get_secret("nasa_api_key")

    @patch("src.etl.secrets_manager.secretmanager.SecretManagerServiceClient")
    def test_get_secret_permission_denied(self, mock_client):
        mock_client.return_value.access_secret_version.side_effect = PermissionDenied(
            "No access"
        )

        manager = SecretsManager()

        with self.assertRaises(RuntimeError):
            manager.get_secret("nasa_api_key")


if __name__ == "__main__":
    unittest.main()
