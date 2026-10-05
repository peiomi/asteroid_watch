import requests
import time
from datetime import date


class NasaClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch(self):
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {"start_date": date.today().isoformat(), "api_key": self.api_key}
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                response = requests.get(url, params=params, timeout=5)
                response.raise_for_status()

                return response.json()

            except requests.RequestException:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(2**attempt)
