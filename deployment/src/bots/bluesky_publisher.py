from atproto import Client
from deployment.src.analytics.risk_analytics import RiskAnalytics
from deployment.src.etl.secrets_manager import SecretsManager
from deployment.src.etl.settings import Settings
from PIL import Image

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
        asteroid_data = analytics.get_asteroid_data(asteroid_name=asteroid.name)
        hazards = analytics.get_hazardous_count()

        if asteroid is None:
            return "No asteroid data available."

        message = f"""
☄️ Asteroid Watch Daily Update ☄️

Highest Risk Asteroid: {asteroid.name}
Risk Score: {asteroid.risk_score}/100
Risk Level: {asteroid.risk_level.title()}
Size: {asteroid.size.title()} / {asteroid_data.diameter_max:.2f} km
Speed: {asteroid.speed.title()} / {asteroid_data.relative_velocity_km_s:.2f} km/s
Distance: {asteroid.distance.title()} / {asteroid_data.miss_distance_km:.2f} km

Hazardous Objects Today: {hazards}

Source: NASA NEO API
"""
        return message

    def get_chart_image(self):
        with open("deployment/src/notebooks/dashboard.png", "rb") as image_file:
            image_data = image_file.read()

        image = self.client.upload_blob(image_data)

        return image

    def post(self, message, image):
        self.client.send_post(
            text=message,
            embed={
                "$type": "app.bsky.embed.images",
                "images": [
                    {"alt": "asteroid risk distribution chart", "image": image.blob}
                ],
            },
        )


# just for local testing, run: python -m deployment.src.bots.bluesky_publisher

""" if __name__ == "__main__":
    publisher = BlueSkyPublisher()
    message = publisher.generate_post()
    image = publisher.get_chart_image()
    print("Generated post:")
    print(message)

    publisher.post(message=message, image=image) """
