import discord
from discord.ext import commands

from classes import ErrorEmbed, SuccessEmbed


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="avatar")
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        try:
            member = member or ctx.author
            embed = SuccessEmbed(
                title=f"{member.display_name}'s avatar",
                show_timestamp=True,
                footer_icon=ctx.author.avatar.url,
                footer_text=f"Requested by {ctx.author.name}",
            )
            embed.set_image(
                url=member.avatar.url if member.avatar else member.default_avatar.url
            )
            return await ctx.send(embed=embed)
        except Exception:
            return await ctx.send(embed=ErrorEmbed("Unable to fetch avatar."))


def setup(bot: commands.Bot):
    bot.add_cog(Avatar(bot))
