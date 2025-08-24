import discord
from discord.ext import commands

from utils import logger
from utils.database import connect_to_db
from utils.welcome_card import generate_welcome_card


class OnMemberJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        c = connect_to_db("databases/configs.db")
        c.execute(
            "SELECT welcome_channel_id, welcome_message FROM guild_config WHERE guild_id = ?",
            (member.guild.id,),
        )
        row = c.fetchone()
        c.close()

        variables = {
            "{member.username}": member.name,
            "{member.name}": member.display_name,
            "{member.mention}": member.mention,
            "{server.name}": member.guild.name,
            "{server.member_count}": str(member.guild.member_count),
        }

        if row:
            channel_id, message = row
            channel = member.guild.get_channel(channel_id)
            for k in variables:
                message = message.replace(k, variables[k])

            try:
                status_text = None
                for activity in member.activities:
                    if isinstance(activity, discord.CustomActivity):
                        status_text = activity.name or None
                if status_text:
                    image = await generate_welcome_card(
                        name=member.display_name,
                        members_count=member.guild.member_count,
                        status=member.status,
                        status_text=status_text,
                    )
                else:
                    image = await generate_welcome_card(
                        name=member.display_name,
                        members_count=member.guild.member_count,
                        status=member.status,
                    )
                if channel:
                    return await channel.send(
                        message,
                        file=discord.File(
                            fp=image, filename=f"{member.id}-welcome.png"
                        ),
                    )
            except Exception as e:
                image = None
                if channel:
                    return await channel.send(message)
                logger.logger.error(e)


def setup(bot: commands.Bot):
    bot.add_cog(OnMemberJoin(bot))
