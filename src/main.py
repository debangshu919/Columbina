import asyncio

from classes.Client import BotClient
from configs.env import BOT_TOKEN
from utils import logger


async def main():
    bot = BotClient()
    with open("banner.txt", "r") as f:
        print(f.read())
    logger.logger.info("ℹ️  Starting bot...")
    try:
        await bot.load_extensions()
        await bot.start(BOT_TOKEN)
    except KeyboardInterrupt:
        logger.logger.info("Shutting down bot...")
    except asyncio.CancelledError:
        logger.logger.info("Bot connection cancelled, shutting down...")
    finally:
        if not bot.is_closed():
            await bot.close()
        logger.logger.info("Bot shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
