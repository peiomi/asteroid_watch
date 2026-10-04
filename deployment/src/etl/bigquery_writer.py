import logging
from dataclasses import asdict
from google.cloud import bigquery

logger = logging.getLogger(__name__)


class BigQueryWriter:
    def __init__(self):
        self.client = bigquery.Client()

    def write(self, records, table_id):
        rows = []

        for record in records:
            row = asdict(record)
            row["processed_at"] = row["processed_at"].isoformat()
            rows.append(row)

        logger.info("attempting to insert %d rows into %s", len(rows), table_id)

        # will return empty list if success
        errors = self.client.insert_rows_json(table_id, rows)
        # if not empty returns list off errors
        if errors:
            logger.error("Failed to insert rows %s. Errors: %s", table_id, errors)
            raise RuntimeError(f"BigQuery insert failed: {errors}")

        logger.info("Successfully inserted %d rows into %s", len(rows), table_id)
