import unittest
from unittest.mock import patch
from deployment.src.etl.bigquery_writer import BigQueryWriter
from tests.mock_records import MOCK_RECORDS


class TestBigQuery(unittest.TestCase):

    @patch("src.etl.bigquery_writer.bigquery.Client")
    def test_write_calls_insert(self, mock_client):
        mock_client.return_value.insert_rows_json.return_value = []
        writer = BigQueryWriter()

        records = MOCK_RECORDS

        writer.write(records=records, table_id="asteroid_records")

        mock_client.return_value.insert_rows_json.assert_called_once()

    @patch("src.etl.bigquery_writer.bigquery.Client")
    def test_write_failure(self, mock_client):
        mock_client.return_value.insert_rows_json.return_value = [{"error": "bad row"}]

        writer = BigQueryWriter()

        with self.assertRaises(RuntimeError):
            writer.write(records=MOCK_RECORDS, table_id="asteroid_records")


if __name__ == "__main__":
    unittest.main()
