import discord
from discord.ext import commands

from classes import ErrorEmbed, InfoEmbed, PrimaryEmbed


class SlashBanner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name="banner", description="Display your banner")
    async def banner(
        self, ctx: discord.ApplicationContext, user: discord.Member = None
    ):
        try:
            member = user or ctx.user
            user: discord.User = await self.bot.fetch_user(member.id)

            if user.banner:
                embed = PrimaryEmbed(
                    title=f"{user.display_name}'s banner",
                    show_timestamp=True,
                    footer_icon=ctx.author.avatar.url if ctx.author.avatar else None,
                    footer_text=f"Requested by {ctx.author.name}",
                )
                embed.set_image(url=user.banner.url)
            else:
                embed = InfoEmbed(message=f"{user.display_name} doesn't have a banner.")

            return await ctx.respond(embed=embed)
        except Exception:
            return await ctx.respond(embed=ErrorEmbed("Unable to fetch banner."))


def setup(bot: commands.Bot):
    bot.add_cog(SlashBanner(bot))
