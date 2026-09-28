import base64
import json
import logging

logger = logging.getLogger(__name__)


class ETLEventHandler:

    def handle(self, event):
        data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

        logger.info("Received Pub/Sub event: %s", data)
