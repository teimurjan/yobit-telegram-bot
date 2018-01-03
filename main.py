import logging

from api_observer import ApiObserver
from bot.bot import YobitBot
from settings import BOT_TOKEN, LOGGER_NAME
from models import User, IgnoredCurrency
from utils import setup_logger


def init_db():
  if not User.table_exists():
    User.create_table()
  if not IgnoredCurrency.table_exists():
    IgnoredCurrency.create_table()


if __name__ == '__main__':
  init_db()
  setup_logger()
  logger = logging.getLogger(LOGGER_NAME)
  bot = YobitBot(BOT_TOKEN, logger)
  bot.start()

  observer = ApiObserver(bot, logger)
  observer.observe()
