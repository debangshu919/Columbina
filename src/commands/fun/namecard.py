from discord.ext import commands

from classes.Embed import ErrorEmbed
from utils.namecard import random_namecard


class Namecard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="namecard")
    async def namecard(self, ctx: commands.Context):
        try:
            return await ctx.send(random_namecard())
        except Exception:
            return await ctx.send(embed=ErrorEmbed())


def setup(bot: commands.Bot):
    bot.add_cog(Namecard(bot))
