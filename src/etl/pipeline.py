from etl.bigquery_writer import BigQueryWriter
from etl.cloud_storage import CloudStorage
from etl.nasa_client import NasaClient
from etl.normalizer import Normalizer
from etl.risk_scorer import RiskScorer
from etl.secrets_manager import SecretsManager


class ETLPipeline:
    def __init__(self):
        self.secrets = SecretsManager()
        self.nasa = NasaClient()
        self.storage = CloudStorage()
        self.normalizer = Normalizer()
        self.scorer = RiskScorer()
        self.bigquery = BigQueryWriter()

    def run(self):
        data = self.nasa.fetch()
        self.storage.store(data)
        records = self.normalizer.normalize(data)
        risk_score = self.scorer.score_risk(records)
        self.bigquery.write(risk_score)
