import datetime

import discord
from discord.ext import commands

from configs.config import CONFIG


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="avatar")
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        color = CONFIG["colors"]["primary"]
        embed = discord.Embed(
            title=f"{member.display_name}'s avatar",
            color=discord.Color.from_rgb(color[0], color[1], color[2]),
            timestamp=datetime.datetime.now(),
        )
        embed.set_image(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )
        return await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Avatar(bot))
