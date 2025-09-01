# flake8: noqa: F722
import re

import discord
from discord.commands.permissions import default_permissions
from discord.errors import Forbidden
from discord.ext import commands
from discord.role import RoleColours


class SlashRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_hex(self, hex: str):
        return bool(re.match(r"^#([A-Fa-f0-9]{6})$", hex))

    def format_hex(self, hex: str):
        if hex.startswith("#"):
            hex = hex[1:]
        return hex

    role = discord.SlashCommandGroup("role", "Role related commands")

    @role.command(name="color", description="Change the color of a role")
    @default_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def color(
        self,
        ctx: discord.ApplicationContext,
        role: discord.Option(
            discord.Role, description="The role to change the color of", required=True
        ),
        primary: discord.Option(
            str,
            description="Primary color in hex format (e.g., #FF0000)",
            required=True,
        ),
        secondary: discord.Option(
            str,
            description="Secondary color in hex format (e.g., #00FF00)",
            required=False,
        ) = None,
        holographic: discord.Option(
            bool, description="Holographic role color", required=False
        ) = False,
    ):
        if not self.is_hex(primary) or (secondary and not self.is_hex(secondary)):
            return await ctx.respond("❌ Invalid color format.")
        primary = discord.Colour(int(self.format_hex(primary), 16))
        secondary = (
            discord.Colour(int(self.format_hex(secondary), 16)) if secondary else None
        )

        try:
            if holographic:
                await role.edit(holographic=RoleColours.holographic())
            else:
                await role.edit(
                    colours=RoleColours(primary=primary, secondary=secondary)
                )
            return await ctx.respond("✅ Role color changed successfully.")
        except Forbidden:
            return await ctx.respond(
                "❌ Failed to change the color of the role:\n> `Missing Permissions`"
            )
        except Exception:
            return await ctx.respond("❌ Failed to change the color of the role.")


def setup(bot: commands.Bot):
    bot.add_cog(SlashRole(bot))
