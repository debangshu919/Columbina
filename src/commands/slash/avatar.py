import discord
from discord.ext import commands

from classes import ErrorEmbed, SuccessEmbed


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
        try:
            user = user or ctx.user
            embed = SuccessEmbed(
                title=f"{user.display_name}'s avatar",
                show_timestamp=True,
                footer_icon=ctx.author.avatar.url,
                footer_text=f"Requested by {ctx.author.name}",
            )
            if server:
                embed.set_image(
                    url=(
                        user.display_avatar.url
                        if user.avatar
                        else user.default_avatar.url
                    )
                )
            else:
                embed.set_image(
                    url=user.avatar.url if user.avatar else user.default_avatar.url
                )
            return await ctx.respond(embed=embed)
        except Exception:
            return await ctx.respond(embed=ErrorEmbed("Unable to fetch avatar."))


def setup(bot: commands.Bot):
    bot.add_cog(SlashAvatar(bot))
