from atproto import Client


class BlueSkyPublisher:
    def __init__(self, username, password):
        self.client = Client()
        self.client.login(username, password)

    def post(self, message):
        self.client.send_post(message)
