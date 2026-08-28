from etl.secrets_manager import SecretsManager
import requests


class NasaClient:
    def __init__(self):
        self.secrets = SecretsManager()
        self.api_key = self.secrets.get_secret("nasa_api_key")

    def fetch(self):
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {"start_date": "2026-08-27", "api_key": self.api_key}
        response = requests.get(url, params=params, timeout=5)
        return response.json()
