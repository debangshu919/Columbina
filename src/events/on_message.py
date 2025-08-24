import discord
from discord.ext import commands

from configs.config import CONFIG
from utils.chat import chatbot


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ALLOWED_CHANNEL_IDS = CONFIG["chatbot_channel_ids"]

        if message.author == self.bot.user:
            return

        if (f"<@{CONFIG['bot_id']}>" in message.content or message.reference) and str(
            message.channel.id
        ) in ALLOWED_CHANNEL_IDS:
            if message.reference and message.reference.resolved.author == self.bot.user:
                async with message.channel.typing():
                    response = await chatbot(
                        message.content.strip(),
                        uid=message.author.id,
                        username=message.author.name,
                    )
            else:
                async with message.channel.typing():
                    response = await chatbot(
                        query=message.content.strip()
                        .split(f"<@{CONFIG['bot_id']}>")[0]
                        .strip(),
                        uid=message.author.id,
                        username=message.author.name,
                    )

            await message.reply(response)


def setup(bot: commands.Bot):
    bot.add_cog(OnMessage(bot))
