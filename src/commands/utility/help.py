from discord.ext import commands

from classes import ErrorEmbed, PrimaryEmbed
from configs.commands import COMMANDS


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        try:
            embed = PrimaryEmbed(
                title="Commands",
                show_timestamp=True,
                footer_text=f"Requested by {ctx.author.name}",
                footer_icon_url=ctx.author.display_avatar.url,
            )

            for cmds in COMMANDS["commands"]:
                embed.add_field(
                    name=cmds["name"],
                    value=f"> {cmds['description']}\nexample: `{cmds['example']}`",
                    inline=False,
                )
            return await ctx.send(embed=embed)
        except Exception:
            return await ctx.respond(embed=ErrorEmbed())


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
