from discord.ext import commands

from utils.summarize import summarize


class Summarize(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="summarize")
    async def summarize(self, ctx: commands.Context, message_id: int = None):
        messages = []
        participants = []

        if ctx.message.reference:  # if command is used as a reply
            ref_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            async for msg in ctx.channel.history(after=ref_msg, limit=None):
                messages.append(
                    {"author": msg.author.display_name, "message": msg.content}
                )

                if msg.author.display_name not in participants:
                    participants.append(msg.author.display_name)

        elif message_id:  # after a specific message ID
            ref_msg = await ctx.channel.fetch_message(message_id)
            async for msg in ctx.channel.history(after=ref_msg, limit=None):
                messages.append(
                    {"author": msg.author.display_name, "message": msg.content}
                )

                if msg.author.display_name not in participants:
                    participants.append(msg.author.display_name)

        else:
            async for msg in ctx.channel.history(limit=50):
                # if msg.author.bot:
                #     continue
                messages.append(
                    {"author": msg.author.display_name, "message": msg.content}
                )

                if msg.author.display_name not in participants:
                    participants.append(msg.author.display_name)

            messages = messages[::-1]

        context = {"participants": participants, "messages": messages}
        async with ctx.message.channel.typing():
            summary = await summarize(context=context)

        return await ctx.reply(f"{summary}\n\n-# This is an AI generated summary.")


def setup(bot: commands.Bot):
    bot.add_cog(Summarize(bot))
