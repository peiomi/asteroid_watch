import unittest
from unittest.mock import MagicMock
from deployment.src.etl.recovery_service import RecoveryService


class TestRecoveryService(unittest.TestCase):
    def test_replays_asteroid_batch(self):
        recovery = RecoveryService()
        blob = MagicMock()
        blob.name = "failed_batches/asteroid_batch_123.json"

        recovery.storage = MagicMock()
        recovery.bigquery = MagicMock()

        recovery.storage.list_failed_batches.return_value = [blob]

        recovery.storage.load_json.return_value = [{"id": "123", "name": "Apophis"}]

        recovery.replay_failed_batches()
        recovery.bigquery.write.assert_called_once()
        blob.delete.assert_called_once()


if __name__ == "__main__":
    unittest.main()
