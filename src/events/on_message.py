from venv import logger

import discord
from discord.ext import commands
from sqlmodel import Session, select

from configs.config import CONFIG
from models.server_model import Server
from services.cache_service import redis_client
from services.database_service import engine
from utils.chat import chatbot
from utils.functions.redis_type_conversions import (deserialize_from_redis,
                                                    serialize_for_redis)


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return

        try:
            cache = redis_client.hgetall(f"server:{message.author.guild.id}")
            if cache:
                cache_data = deserialize_from_redis(cache)
                server = Server(**cache_data)
            else:
                with Session(engine) as session:
                    statement = select(Server).where(
                        Server.server_id == message.author.guild.id
                    )
                    server = session.exec(statement).one()

                redis_client.hset(
                    f"server:{message.author.guild.id}",
                    mapping=serialize_for_redis(server.model_dump()),
                )

            if (
                server.chatbot is False
                or server.chatbot_channel_id is None
                or server.chatbot_response is None
            ):
                return

            channel_id = server.chatbot_channel_id
            channel = message.author.guild.get_channel(channel_id)

            if channel is None or message.channel.id != channel_id:
                return

            if server.chatbot_response == "all":
                async with channel.typing():
                    response = await chatbot(
                        message.content.strip(),
                        uid=message.author.id,
                        username=message.author.name,
                    )
                await channel.send(response)

            elif server.chatbot_response == "mentions":
                if (f"<@{CONFIG['bot_id']}>") in message.content:
                    async with channel.typing():
                        response = await chatbot(
                            message.content.strip(),
                            uid=message.author.id,
                            username=message.author.name,
                        )
                    await channel.send(response)
            elif server.chatbot_response == "replies":
                if message.reference and message.reference.resolved.author.id == int(
                    CONFIG["bot_id"]
                ):
                    async with channel.typing():
                        response = await chatbot(
                            message.content.strip(),
                            uid=message.author.id,
                            username=message.author.name,
                        )
                    await channel.send(response)
            elif server.chatbot_response == "default":
                if (f"<@{CONFIG['bot_id']}") in message.content or (
                    message.reference
                    and message.reference.resolved.author.id == int(CONFIG["bot_id"])
                ):
                    async with channel.typing():
                        response = await chatbot(
                            message.content.strip(),
                            uid=message.author.id,
                            username=message.author.name,
                        )
                    await channel.send(response)

        except Exception as e:
            logger.exception(e)


def setup(bot: commands.Bot):
    bot.add_cog(OnMessage(bot))
