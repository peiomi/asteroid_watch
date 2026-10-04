import json
from google.cloud import pubsub_v1


class PubSubPublisher:
    def __init__(self, project_id, topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish(self, payload):
        self.publisher.publish(self.topic_path, json.dumps(payload).encode("utf-8"))
