import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)

# File handler (rotating log file, 5MB per file, keep 5 backups)
file_handler = RotatingFileHandler(
    "logs/bot.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)
file_handler.setFormatter(file_formatter)

# Attach handlers (avoid duplicates if reloaded)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
