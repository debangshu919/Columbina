import discord
from discord.ext import commands

from configs.config import CONFIG


class SlashPing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Check bot latency")
    async def ping(self, ctx: discord.ApplicationContext):
        latency = round(self.bot.latency * 1000)

        # Get color based on latency
        if latency < 500:
            color_values = CONFIG["colors"]["success"]
        else:
            color_values = CONFIG["colors"]["warning"]

        embed = discord.Embed(
            title="Pong",
            color=discord.Color.from_rgb(
                color_values[0], color_values[1], color_values[2]
            ),
        )
        embed.add_field(name="Bot Latency", value=f"```{latency} ms```")
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url,
        )
        return await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SlashPing(bot))
