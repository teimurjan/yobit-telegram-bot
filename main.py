import logging

from api_observer import ApiObserver
from bot.bot import YobitBot
from settings import BOT_TOKEN, LOGGER_NAME
from models import User
from utils import setup_logger

if __name__ == '__main__':
  if not User.table_exists():
    User.create_table()

  setup_logger()
  logger = logging.getLogger(LOGGER_NAME)
  bot = YobitBot(BOT_TOKEN, logger)
  bot.start()

  observer = ApiObserver(bot, logger)
  observer.observe()
