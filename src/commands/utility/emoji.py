import re

from discord.ext import commands

from classes.Embed import ErrorEmbed, PrimaryEmbed
from configs.config import CONFIG


class Emoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="emoji")
    async def emoji(self, ctx: commands.Context, emj: str = None):
        if emj is None:
            embed = ErrorEmbed(
                error=f"Please provide an emoji!\nUsage: `{CONFIG["prefix"][0]}emoji <emoji>`"
            )
        else:
            try:
                custom_emoji = re.match(r"<a?:(\w+):(\d+)>", emj)
                if custom_emoji:
                    emoji_name = custom_emoji.group(1)
                    emoji_id = custom_emoji.group(2)
                    is_animated = emj.startswith("<a:")

                    extension = "gif" if is_animated else "png"
                    emoji_url = (
                        f"https://cdn.discordapp.com/emojis/{emoji_id}.{extension}"
                    )
                    embed = PrimaryEmbed(
                        title="Enlarged Emoji",
                        description=f"Emoji: `{emoji_name}`",
                        footer_text=f"Emoji ID: {emoji_id}",
                    )
                    embed.set_image(url=emoji_url)

                else:
                    embed = ErrorEmbed(
                        error=f"Please provide a valid emoji (not discord emojis)\nUsage: `{CONFIG["prefix"][0]}emoji <emoji>`"
                    )
            except Exception as e:
                embed = ErrorEmbed()
                print(e)
                return await ctx.send(embed=embed)

        return await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Emoji(bot))
