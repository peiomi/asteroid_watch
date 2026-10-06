import json
from google.cloud import storage
from datetime import datetime, UTC

from src.etl.serializer import Serializer


class CloudStorage:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_json(self, data, filename):
        blob = self.bucket.blob(filename)

        blob.upload_from_string(json.dumps(data), content_type="application/json")

    def save_failed_batch(self, records, name):
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        rows = Serializer.serialize_records(records)

        blob_name = f"failed_batches/" f"{name}_batch_{timestamp}.json"

        blob = self.bucket.blob(blob_name)

        blob.upload_from_string(json.dumps(rows), content_type="application/json")

        return blob_name

    def load_json(self, blob_name):
        blob = self.bucket.blob(blob_name)
        data = blob.download_as_text()
        return json.loads(data)

    def list_failed_batches(self):
        return self.bucket.list_blobs(prefix="failed_batches/")
