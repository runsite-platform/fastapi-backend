import logging
import sys

from app.config.settings import settings

logger = logging.getLogger(settings.SERVICE_NAME)
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logger.level)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
