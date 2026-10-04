import base64
import json
import logging
from src.bots.bluesky_publisher import BlueSkyPublisher

logger = logging.getLogger(__name__)


class ETLEventHandler:

    def handle(self, event):
        data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
        logger.info("Received Pub/Sub event: %s", data)

        event_type = data.get("event")

        if event_type == "etl_completed":
            self._handle_etl_completed()

    def _handle_etl_completed(self):
        try:
            publisher = BlueSkyPublisher()
            message = publisher.generate_post()
            publisher.post(message=message)
            logger.info("Posted asteroid update to Bluesky")
        except Exception as e:
            logger.exception("Failed to publish BlueSky update: %s", e)
            raise
