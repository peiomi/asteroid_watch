import logging

from src.etl.settings import Settings
from src.etl.bigquery_writer import BigQueryWriter
from src.etl.cloud_storage import CloudStorage

logger = logging.getLogger(__name__)


class RecoveryService:
    def __init__(self):
        self.storage = CloudStorage(Settings.BUCKET_NAME)
        self.bigquery = BigQueryWriter()

    def replay_failed_batches(self):
        failed_batches = list(self.storage.list_failed_batches())

        if not failed_batches:
            logger.info("No failed batches found. Nothing to recover.")
            return

        logger.info("Found %d failed batches to recover", len(failed_batches))

        for blob in failed_batches:
            records = self.storage.load_json(blob.name)

            if "asteroid_batch" in blob.name:
                table_id = Settings.ASTEROID_TABLE

            elif "scored_batch" in blob.name:
                table_id = Settings.RISK_TABLE

            else:
                logger.warning("Unknown batch type: %s", blob.name)
                continue

            try:
                self.bigquery.write(records=records, table_id=table_id)

                blob.delete()

                logger.info(
                    "Successfully recovered %s",
                    blob.name,
                )
            except Exception:
                logger.exception("Failed recovering %s", blob.name)
