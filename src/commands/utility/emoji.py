import re

import discord
from discord.ext import commands

from configs.config import CONFIG


class Emoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="emoji")
    async def emoji(self, ctx: commands.Context, emj: str = None):
        embed = discord.Embed()
        if emj is None:
            embed.title = "Error"
            embed.description = (
                f"Please provide an emoji!\nUsage: `{CONFIG["prefix"][0]}emoji <emoji>`"
            )
            embed.color = discord.Color.red()
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
                    color = CONFIG["colors"]["primary"]
                    embed.title = "Enlarged Emoji"
                    embed.description = f"Emoji: `{emoji_name}`"
                    embed.set_image(url=emoji_url)
                    embed.set_footer(text=f"Emoji ID: {emoji_id}")
                    embed.color = discord.Color.from_rgb(color[0], color[1], color[2])

                else:
                    embed.title = "Error"
                    embed.description = f"Please provide a valid emoji (not discord emojis)\nUsage: `{CONFIG["prefix"][0]}emoji <emoji>`"
                    embed.color = discord.Color.red()
            except Exception as e:
                embed.title = "Error"
                embed.description = "Something went wrong..."
                embed.color = discord.Color.red()
                print(e)
                return await ctx.send(embed=embed)

        return await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Emoji(bot))
