import discord
from discord import app_commands
import logging

from deployment.src.analytics.risk_analytics import RiskAnalytics
from deployment.src.etl.secrets_manager import SecretsManager

logging.basicConfig(level=logging.INFO)


class AsteroidBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.analytics = RiskAnalytics()

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        logging.info("Logged in as %s", self.user)


bot = AsteroidBot()


@bot.tree.command()
async def asteroid(interaction: discord.Interaction):
    await interaction.response.send_message("Asteroid data incoming")


@bot.tree.command(name="highest-risk")
async def highest_risk(interaction: discord.Interaction):
    asteroid = bot.analytics.get_highest_risk()

    if asteroid is None:
        await interaction.response.send_message("No asteroid data found.")
        return

    await interaction.response.send_message(f"""
🚨 Highest Risk Asteroid\n
Name: {asteroid.name}\n
Risk Score: {asteroid.risk_score}/100
Risk Level: {asteroid.risk_level}
Size: {asteroid.size}
Speed: {asteroid.speed}
Distance: {asteroid.distance}
""")


@bot.tree.command(name="average-risk")
async def average_risk(interaction: discord.Interaction):
    avg = bot.analytics.get_average_risk()

    await interaction.response.send_message(f"average risk score: {avg:.2f}")


@bot.tree.command(name="hazards")
async def hazardous_asteroids(interaction: discord.Interaction):
    hazards = bot.analytics.get_hazardous_count()

    await interaction.response.send_message(
        f"Number of Hazardous Objects Near Earth today: {hazards}"
    )


@bot.tree.command(name="rwgd")
async def are_we_gunna_die(interaction: discord.Interaction):
    await interaction.response.send_message("Probably not today 😎")


if __name__ == "__main__":
    secrets = SecretsManager()
    TOKEN = secrets.get_secret("discord_bot_token")
    bot.run(TOKEN)
