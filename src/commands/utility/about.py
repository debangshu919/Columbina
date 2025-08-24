import datetime

import discord
from discord.ext import commands

from configs.config import CONFIG


class About(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="about")
    async def about(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        color = CONFIG["colors"]["secondary"]
        embed = discord.Embed(
            description=CONFIG["description"],
            color=discord.Color.from_rgb(color[0], color[1], color[2]),
            timestamp=datetime.datetime.now(),
        )
        embed.add_field(name="Version", value=f"v{CONFIG['version']}", inline=True)
        embed.add_field(name="Ping", value=f"{latency}ms", inline=True)
        embed.add_field(name="Written in", value="Python", inline=True)
        embed.add_field(
            name="Author",
            value=f"[{CONFIG['author']['username']}](https://discord.com/users/{CONFIG['author']['user_id']})",
            inline=True,
        )
        embed.add_field(
            name="Developer",
            value=f"[{CONFIG['developer']['username']}](https://discord.com/users/{CONFIG['developer']['user_id']})",
            inline=True,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )
        embed.set_author(name=CONFIG["name"], icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        view = discord.ui.View()
        button = discord.ui.Button(
            label="Join our Discord Server",
            url=CONFIG["server"]["invite"],
            style=discord.ButtonStyle.link,
        )
        invite_button = discord.ui.Button(
            label="Invite Bot",
            url="https://discord.com/oauth2/authorize?client_id=1407769283148251248&permissions=8&integration_type=0&scope=bot",
            style=discord.ButtonStyle.link,
        )
        view.add_item(button)
        view.add_item(invite_button)

        return await ctx.send(
            content="-# ⓘ You can join our **Discord Server** to give feedback.",
            embed=embed,
            view=view,
        )


def setup(bot: commands.Bot):
    bot.add_cog(About(bot))
