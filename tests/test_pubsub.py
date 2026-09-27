import json
import unittest
from unittest.mock import patch

from src.etl.pubsub_publisher import PubSubPublisher


class TestPubSubPublisher(unittest.TestCase):

    @patch("src.etl.pubsub_publisher.pubsub_v1.PublisherClient")
    def test_publish(self, mock_client):

        mock_client.return_value.topic_path.return_value = (
            "projects/test/topics/etl-events"
        )

        publisher = PubSubPublisher(project_id="test", topic_name="etl-events")

        payload = {"event": "etl_completed"}

        publisher.publish(payload)

        mock_client.return_value.publish.assert_called_once_with(
            "projects/test/topics/etl-events", json.dumps(payload).encode("utf-8")
        )


if __name__ == "__main__":
    unittest.main()
