import base64
import json
import logging
from src.etl.bluesky_publisher import BlueSkyPublisher

logger = logging.getLogger(__name__)


class ETLEventHandler:

    def handle(self, event):
        print("HANDLE START")
        data = json.loads(base64.b64decode(event["message"]["data"]).decode("utf-8"))
        print("MESSAGE DECODED")
        print(data)
        logger.info("Received Pub/Sub event: %s", data)

        event_type = data.get("event")
        print(event_type)

        if event_type == "etl_completed":
            self._handle_etl_completed()

    def _handle_etl_completed(self):
        try:
            bluesky = BlueSkyPublisher()
            print("PUBLISHER CREATED")
            message = bluesky.generate_post()
            image = bluesky.get_chart_image()
            bluesky.post(message=message, image=image)
            logger.info("Posted asteroid update to Bluesky")
            print("POST COMPLETE")
        except Exception as e:
            logger.exception("Failed to publish BlueSky update: %s", e)
            raise
