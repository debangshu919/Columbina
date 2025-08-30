import datetime

import discord
from discord.ext import commands

from configs.config import CONFIG


class SlashBanner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name="banner", description="Display your banner")
    async def banner(self, ctx: discord.ApplicationContext, user: discord.User = None):
        user = user or ctx.user
        color = CONFIG["colors"]["primary"]
        embed = discord.Embed(
            title=f"{user.display_name}'s avatar",
            color=discord.Color.from_rgb(color[0], color[1], color[2]),
            timestamp=datetime.datetime.now(),
        )
        embed.set_image(url=user.banner.url if user.banner else None)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        return (
            await ctx.respond(embed=embed)
            if user.banner
            else await ctx.respond(f"{user.display_name} has no banner.")
        )


def setup(bot: commands.Bot):
    bot.add_cog(SlashBanner(bot))
