from datetime import datetime, UTC
import logging
from google.api_core.exceptions import GoogleAPIError

from src.etl.bigquery_writer import BigQueryWriter
from src.etl.cloud_storage import CloudStorage
from src.etl.nasa_client import NasaClient
from src.etl.normalizer import Normalizer
from src.etl.risk_scorer import RiskScorer
from src.etl.secrets_manager import SecretsManager
from src.etl.settings import Settings
from src.etl.pubsub_publisher import PubSubPublisher

logger = logging.getLogger(__name__)


class ETLPipeline:
    def __init__(self):
        self.secrets = SecretsManager()
        self.nasa = NasaClient(api_key=self.secrets.get_secret("nasa_api_key"))
        self.storage = CloudStorage(Settings.BUCKET_NAME)
        self.normalizer = Normalizer()
        self.scorer = RiskScorer()
        self.bigquery = BigQueryWriter()
        self.publisher = PubSubPublisher(
            project_id=Settings.PROJECT_ID, topic_name=Settings.TOPIC_NAME
        )

    def run(self):
        logger.info("Fetching NASA data")
        data = self.nasa.fetch()

        logger.info("Uploading raw json")
        ts = datetime.now(UTC)
        filename = f"raw/{ts:%Y/%m/%d}/nasa_{ts:%H%M%S}.json"
        self.storage.upload_json(data=data, filename=filename)

        logger.info("Received NASA response")
        records = self.normalizer.normalize(data)
        logger.info("Normalized %d asteroid records", len(records))

        etl_success = True

        try:
            self.bigquery.write(
                records=records,
                table_id=Settings.ASTEROID_TABLE,
            )
        except GoogleAPIError:
            etl_success = False

            path = self.storage.save_failed_batch(records, "asteroid")
            logger.exception("BigQuery failed. Batch saved to %s", path)

        risk_scores = self.scorer.score_risk(records)
        logger.info("Generated %d risk scores", len(risk_scores))

        try:
            self.bigquery.write(
                records=risk_scores,
                table_id=Settings.RISK_TABLE,
            )
        except GoogleAPIError:
            etl_success = False

            path = self.storage.save_failed_batch(risk_scores, "scored")
            logger.exception("BigQuery failed. Batch saved to %s", path)

        event = "etl_completed" if etl_success else "etl_completed_with_errors"

        self.publisher.publish({"event": event, "records_processed": len(records)})
