import datetime

import discord
from discord.ext import commands

from configs.config import CONFIG


class Banner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="banner")
    async def banner(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        user = await self.bot.fetch_user(member.id)
        color = CONFIG["colors"]["primary"]
        if user.banner:
            embed = discord.Embed(
                title=f"{user.display_name}'s banner",
                color=discord.Color.from_rgb(color[0], color[1], color[2]),
                timestamp=datetime.datetime.now(),
            )
            embed.set_image(url=user.banner.url)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
            )
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(f"{user.display_name} has no banner.")


def setup(bot: commands.Bot):
    bot.add_cog(Banner(bot))
