import logging
from google.cloud import bigquery
import time
from google.api_core.exceptions import GoogleAPIError

from src.etl.serializer import Serializer

logger = logging.getLogger(__name__)


class BigQueryWriter:
    def __init__(self):
        self.client = bigquery.Client()

    def write(self, records, table_id):
        max_attempts = 3

        rows = Serializer.serialize_records(records)

        for attempt in range(max_attempts):
            try:
                logger.info("attempting to insert %d rows into %s", len(rows), table_id)

                # will return empty list if success
                errors = self.client.insert_rows_json(table_id, rows)
                # if not empty returns list off errors
                if errors:
                    raise RuntimeError(
                        f"BigQuery insert failed for {table_id}: {errors}"
                    )

                logger.info(
                    "Successfully inserted %d rows into %s", len(rows), table_id
                )

                return

            except GoogleAPIError as e:
                if attempt == max_attempts - 1:
                    raise

                wait = 2**attempt
                logger.warning(
                    "BigQuery API error (%s)."
                    "Retrying in %d seconds "
                    "(attempt %d/%d)",
                    e,
                    wait,
                    attempt + 1,
                    max_attempts,
                )

                time.sleep(wait)
