import json
from google.cloud import storage


class CloudStorage:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_json(self, data, filename):
        blob = self.bucket.blob(filename)

        blob.upload_from_string(json.dumps(data), content_type="application/json")
