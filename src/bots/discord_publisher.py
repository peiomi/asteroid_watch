import requests


class DiscordPublisher:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def post(self, message):
        requests.post(self.webhook_url, json={"content": message})
