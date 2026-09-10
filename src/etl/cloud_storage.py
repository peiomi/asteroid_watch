import json


class CloudStorage:
    def upload_json(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
