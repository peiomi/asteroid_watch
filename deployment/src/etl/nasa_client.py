import requests


class NasaClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch(self):
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {"start_date": "2026-08-27", "api_key": self.api_key}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        return response.json()
