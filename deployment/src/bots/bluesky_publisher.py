from atproto import Client
from src.analytics.risk_analytics import RiskAnalytics
from src.etl.secrets_manager import SecretsManager
from src.etl.settings import Settings

analytics = RiskAnalytics()
secrets = SecretsManager()


class BlueSkyPublisher:
    def __init__(self):
        self.client = Client()
        self.client.login(
            Settings.BLUESKY_USERNAME, secrets.get_secret("bluesky_password")
        )

    def generate_post(self):
        asteroid = analytics.get_highest_risk()
        hazards = analytics.get_hazardous_count()

        if asteroid is None:
            return "No asteroid data available."

        message = f"""
🚨 Asteroid Watch Daily Update
Highest Risk Asteroid: {asteroid.name}
Risk Score: {asteroid.risk_score}/100
Risk Level: {asteroid.risk_level}
Size: {asteroid.size}
Speed: {asteroid.speed}
Distance: {asteroid.distance}

Hazardous Objects Today: {hazards}

Source: NASA NEO API
"""
        return message

    def post(self, message):
        self.client.send_post(message)
