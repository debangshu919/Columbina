import discord
from discord.ext import commands
from sqlmodel import Session

from models.server_model import Server
from services.database_service import engine
from utils.logging import logger


class OnGuildJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        # Adds the server into the DB
        server = Server(server_id=guild.id)

        try:
            with Session(engine) as session:
                session.add(server)
                session.commit()
        except Exception as e:
            logger.error(e)

        return


def setup(bot: commands.Bot):
    bot.add_cog(OnGuildJoin(bot))
