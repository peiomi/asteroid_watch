import unittest
import json
import os
from src.etl.cloud_storage import CloudStorage


class TestCloudStorage(unittest.TestCase):
    def test_upload_json(self):
        storage = CloudStorage()
        data = {"test": "value"}
        storage.upload_json(data, "test.json")

        self.assertTrue(os.path.exists("test.json"))

        with open("test.json", "r") as f:
            loaded_data = json.load(f)

        self.assertEqual(loaded_data, data)

        os.remove("test.json")


if __name__ == "__main__":
    unittest.main()
