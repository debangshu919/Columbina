import datetime

import discord
from discord.ext import commands

from configs.config import CONFIG


class SlashAvatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name="avatar", description="Display your avatar")
    async def avatar(
        self,
        ctx: discord.ApplicationContext,
        user: discord.User = None,
        server: bool = False,
    ):
        user = user or ctx.user
        color = CONFIG["colors"]["primary"]
        embed = discord.Embed(
            title=f"{user.display_name}'s avatar",
            color=discord.Color.from_rgb(color[0], color[1], color[2]),
            timestamp=datetime.datetime.now(),
        )
        if server:
            embed.set_image(
                url=user.display_avatar.url if user.avatar else user.default_avatar.url
            )
        else:
            embed.set_image(
                url=user.avatar.url if user.avatar else user.default_avatar.url
            )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )

        return await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SlashAvatar(bot))
