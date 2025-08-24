import discord
from discord.ext import commands

from configs.config import CONFIG


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)

        # Get color based on latency
        if latency < 500:
            color = CONFIG["colors"]["success"]
        else:
            color = CONFIG["colors"]["warning"]

        embed = discord.Embed(
            title="Pong",
            color=discord.Color.from_rgb(color[0], color[1], color[2]),
        )
        embed.add_field(name="Bot Latency", value=f"```{latency} ms```")
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url,
        )
        return await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
