import json
import logging
from google.cloud import pubsub_v1

logger = logging.getLogger(__name__)


class PubSubPublisher:
    def __init__(self, project_id, topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish(self, payload):
        future = self.publisher.publish(
            self.topic_path, json.dumps(payload).encode("utf-8")
        )

        message_id = future.result()

        logger.info("Published Pub/Sub message %s", message_id)

        return message_id
