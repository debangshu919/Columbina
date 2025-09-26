import os

import discord
from discord.ext import commands

from configs.config import CONFIG
from utils.loader import load_cogs
from utils.logging import logger


class BotClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.presences = True
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__(
            command_prefix=CONFIG["prefix"], intents=intents, help_command=None
        )

    async def load_extensions(self):
        base_dir = os.path.join(os.getcwd(), "src")

        # Load commands
        logger.info("ℹ️ Loading commands...")
        commands_dir = os.path.join(base_dir, "commands")
        await load_cogs(self, commands_dir, "commands")
        logger.info("✅ Commands loaded successfully.")

        # Load events
        logger.info("ℹ️ Loading events...")
        events_dir = os.path.join(base_dir, "events")
        await load_cogs(self, events_dir, "events")
        logger.info("✅ Events loaded successfully.")

        logger.info("✅ All cogs loaded successfully")
