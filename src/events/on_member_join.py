import discord
from discord.ext import commands
from sqlmodel import Session, select

from models.server_model import Server
from services.database_service import engine
from utils.logging import logger
from utils.welcome_card import generate_welcome_card


class OnMemberJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            with Session(engine) as session:
                statement = select(Server).where(Server.server_id == member.guild.id)
                server = session.exec(statement).one()
                if (
                    server.greetings is False
                    or server.greetings_channel_id is None
                    or server.greetings_message is None
                ):
                    return
                channel_id = server.greetings_channel_id
                channel = member.guild.get_channel(channel_id)

                message = server.greetings_message
                variables = {
                    "{member.username}": member.name,
                    "{member.name}": member.display_name,
                    "{member.mention}": member.mention,
                    "{server.name}": member.guild.name,
                    "{server.member_count}": str(member.guild.member_count),
                }
                for k in variables:
                    message = message.replace(k, variables[k])

                if server.greetings_card:
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

                    if channel:
                        return await channel.send(
                            content=message,
                            file=discord.File(
                                fp=image, filename=f"{member.id}-welcome.png"
                            ),
                        )
                else:
                    if channel:
                        return await channel.send(
                            content=message,
                        )

        except Exception as e:
            return logger.error(e)


def setup(bot: commands.Bot):
    bot.add_cog(OnMemberJoin(bot))
