import discord
from discord.ext import commands

from utils.welcome_card import generate_welcome_card


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="welcome")
    async def welcome(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        status_text = None
        avatar = await member.display_avatar.read()
        for activity in member.activities:
            if isinstance(activity, discord.CustomActivity):
                status_text = activity.name or None
        if status_text:
            image = await generate_welcome_card(
                name=member.display_name,
                members_count=member.guild.member_count,
                status=str(member.status),
                avatar=avatar,
                status_text=status_text,
            )
        else:
            image = await generate_welcome_card(
                name=member.display_name,
                members_count=member.guild.member_count,
                status=str(member.status),
                avatar=avatar,
            )
        return await ctx.reply(
            file=discord.File(fp=image, filename=f"{member.id}-welcome.png")
        )


def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
