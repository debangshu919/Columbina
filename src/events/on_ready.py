import discord
from discord.ext import commands

from configs.config import CONFIG
from utils import logger


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=CONFIG["activity"]["name"]
            ),
            status=discord.Status.idle,
        )
        logger.logger.info(f"✅ {self.bot.user.display_name} is online.")


def setup(bot: commands.Bot):
    bot.add_cog(OnReady(bot))
