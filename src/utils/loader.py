import os

from utils.logging import logger


async def load_cogs(bot, base_dir: str, package: str):
    """
    Recursively load all cogs (commands/events) in base_dir.

    Args:
        bot: The discord bot client
        base_dir (str): Base directory (absolute path to scan)
        package (str): Python package root (e.g., "commands")
    """
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Convert file path into a Python module path
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                module = f"{package}.{rel_path.replace(os.sep, '.')[:-3]}"
                try:
                    bot.load_extension(module)
                    logger.info(f"✅ Loaded {module.split(".")[0][:-1]}: {module}")
                except Exception:
                    logger.exception(f"❌ Failed to load {module}")
