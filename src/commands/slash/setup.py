import discord
from discord.commands.permissions import default_permissions
from discord.ext import commands
from sqlmodel import Session, select

from models.server_model import Server
from services.cache_service import redis_client
from services.database_service import engine
from utils.functions.redis_type_conversions import serialize_for_redis
from utils.logging import logger
from utils.welcome_card import generate_welcome_card


class SlashSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    setup = discord.SlashCommandGroup("setup", "Bot setup related commands")
    disable = setup.create_subgroup("disable", "Disable a feature")

    @setup.command(name="greetings", description="Setup greetings message")
    @default_permissions(administrator=True)
    async def greetings(
        self,
        ctx: discord.ApplicationContext,
        message: str,
        channel: discord.TextChannel,
        card: bool,
    ):
        guild_id = ctx.guild_id
        channel_id = channel.id

        await ctx.defer()

        try:
            with Session(engine) as session:
                statement = select(Server).where(Server.server_id == guild_id)
                server = session.exec(statement).one()
                server.greetings = True
                server.greetings_card = card
                server.greetings_channel_id = channel_id
                server.greetings_message = message
                session.add(server)
                session.commit()
                server = session.exec(statement).one()

            redis_client.hset(
                f"server:{guild_id}", mapping=serialize_for_redis(server.model_dump())
            )
            embed = discord.Embed(
                title="Success",
                description=f"Greetings configured successfully!\nGreetings messages will be sent to <#{channel_id}>",
                color=discord.Color.green(),
            )
            await ctx.send_followup(embed=embed)

            variables = {
                "{member.username}": ctx.user.name,
                "{member.name}": ctx.user.display_name,
                "{member.mention}": ctx.user.mention,
                "{server.name}": ctx.user.guild.name,
                "{server.member_count}": str(ctx.user.guild.member_count),
            }
            for k in variables:
                message = message.replace(k, variables[k])

            if card is False:
                return await ctx.send_followup(content=message, ephemeral=True)
            else:
                member = ctx.author
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
                return await ctx.send_followup(
                    content=message,
                    file=discord.File(fp=image, filename=f"{member.id}-welcome.png"),
                    ephemeral=True,
                )

        except Exception as e:
            embed = discord.Embed(
                color=discord.Color.red(), description="Something went wrong..."
            )
            logger.error(e)
            return await ctx.send_followup(embed=embed)

    @setup.command(name="chatbot", description="Setup AI chatbot")
    async def chatbot(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        response: discord.Option(
            str,
            description="Responds to",
            choices=["all", "mentions", "replies", "both"],
        ),
    ):
        guild_id = ctx.guild_id
        channel_id = channel.id

        await ctx.defer()

        try:
            with Session(engine) as session:
                statement = select(Server).where(Server.server_id == guild_id)
                server = session.exec(statement).one()
                server.chatbot = True
                server.chatbot_response = response
                server.chatbot_channel_id = channel_id
                session.add(server)
                session.commit()

            embed = discord.Embed(
                title="Success",
                description=f"Chatbot configured successfully!\nYou can interact with the chatbot in <#{channel_id}>",
                color=discord.Color.green(),
            )
            await ctx.send_followup(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                color=discord.Color.red(), description="Something went wrong..."
            )
            logger.error(e)
            return await ctx.send_followup(embed=embed)

    @disable.command(name="chatbot", description="Disable AI chatbot")
    async def disable_chatbot(self, ctx: discord.ApplicationContext):
        guild_id = ctx.guild_id
        await ctx.defer()
        try:
            with Session(engine) as session:
                statement = select(Server).where(Server.server_id == guild_id)
                server = session.exec(statement).one()
                server.chatbot = False
                session.add(server)
                session.commit()

            embed = discord.Embed(
                title="Success",
                description="Chatbot disabled successfully!",
                color=discord.Color.green(),
            )
            return await ctx.send_followup(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                color=discord.Color.red(), description="Something went wrong..."
            )
            logger.error(e)
            return await ctx.send_followup(embed=embed)

    @disable.command(name="greetings", description="Disable greetings")
    async def disable_greetings(self, ctx: discord.ApplicationContext):
        guild_id = ctx.guild_id
        await ctx.defer()
        try:
            with Session(engine) as session:
                statement = select(Server).where(Server.server_id == guild_id)
                server = session.exec(statement).one()
                server.greetings = False
                session.add(server)
                session.commit()

            embed = discord.Embed(
                title="Success",
                description="Greetings disabled successfully!",
                color=discord.Color.green(),
            )
            return await ctx.send_followup(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                color=discord.Color.red(), description="Something went wrong..."
            )
            logger.error(e)
            return await ctx.send_followup(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SlashSetup(bot))
