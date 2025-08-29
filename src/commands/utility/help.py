import datetime

import discord
from discord.ext import commands

from configs.commands import COMMANDS
from configs.config import CONFIG


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        color = CONFIG["colors"]["secondary"]

        embed = discord.Embed(
            title="Commands",
            color=discord.Color.from_rgb(color[0], color[1], color[2]),
            timestamp=datetime.datetime.now(),
        )

        for cmds in COMMANDS["commands"]:
            embed.add_field(
                name=cmds["name"],
                value=f"> {cmds['description']}\nexample: `{cmds['example']}`",
                inline=False,
            )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url,
        )
        return await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
