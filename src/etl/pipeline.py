from datetime import date
import logging

from etl.bigquery_writer import BigQueryWriter
from etl.cloud_storage import CloudStorage
from etl.nasa_client import NasaClient
from etl.normalizer import Normalizer
from etl.risk_scorer import RiskScorer
from etl.secrets_manager import SecretsManager
from etl.settings import Settings

logger = logging.getLogger(__name__)


class ETLPipeline:
    def __init__(self):
        self.secrets = SecretsManager()
        self.nasa = NasaClient(api_key=self.secrets.get_secret("nasa_api_key"))
        self.storage = CloudStorage(Settings.BUCKET_NAME)
        self.normalizer = Normalizer()
        self.scorer = RiskScorer()
        self.bigquery = BigQueryWriter()

    def run(self):
        logger.info("Fetching NASA data")
        data = self.nasa.fetch()

        logger.info("Uploading raw json")
        filename = f"raw/{date.today()}.json"
        self.storage.upload_json(data=data, filename=filename)

        logger.info("Received NASA response")
        records = self.normalizer.normalize(data)
        logger.info("Normalized %d asteroid records", len(records))

        self.bigquery.write(
            records=records,
            table_id=Settings.ASTEROID_TABLE,
        )

        risk_scores = self.scorer.score_risk(records)
        logger.info("Generated %d risk scores", len(risk_scores))

        self.bigquery.write(
            records=risk_scores,
            table_id=Settings.RISK_TABLE,
        )
