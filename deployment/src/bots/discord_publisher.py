import discord
from discord import app_commands
from src.analytics.risk_analytics import RiskAnalytics
from src.etl.secrets_manager import SecretsManager

analytics = RiskAnalytics()
secrets = SecretsManager()
TOKEN = secrets.get_secret("discord_bot_token")


class AsteroidBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"logged in as {self.user}")


bot = AsteroidBot()


@bot.tree.command()
async def asteroid(interaction: discord.Interaction):
    await interaction.response.send_message("Asteroid data incoming")


@bot.tree.command(name="highest-risk")
async def highest_risk(interaction: discord.Interaction):
    asteroid = analytics.get_highest_risk()

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
    avg = analytics.get_average_risk()

    await interaction.response.send_message(f"average risk score: {avg:.2f}")


@bot.tree.command(name="hazards")
async def hazardous_asteroids(interaction: discord.Interaction):
    hazards = analytics.get_hazardous_count()

    await interaction.response.send_message(
        f"Number of Hazardous Objects Near Earth today: {hazards}"
    )


bot.run(TOKEN)
