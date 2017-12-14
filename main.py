import logging

from api_observer import ApiObserver
from bot.bot import YobitBot
from settings import BOT_TOKEN, LOGGER_NAME
from models import User, IgnoreCurrency
from utils import setup_logger


def init_db():
  if not User.table_exists():
    User.create_table()
  if not IgnoreCurrency.table_exists():
    IgnoreCurrency.create_table()


if __name__ == '__main__':
  init_db()
  setup_logger()
  logger = logging.getLogger(LOGGER_NAME)
  bot = YobitBot(BOT_TOKEN, logger)
  bot.start()

  observer = ApiObserver(bot, logger)
  observer.observe()
