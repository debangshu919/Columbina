import discord
from discord.ext import commands
from sqlmodel import Session, select

from models.server_model import Server
from services.database_service import engine
from utils.logging import logger


class OnGuildRemove(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):

        try:
            with Session(engine) as session:
                statement = select(Server).where(Server.server_id == guild.id)
                server = session.exec(statement).one()
                session.delete(server)
                session.commit()
        except Exception as e:
            logger.error(e)

        return


def setup(bot: commands.Bot):
    bot.add_cog(OnGuildRemove(bot))
