from api_observer.api_observer import ApiObserver
from bot.bot import YobitBot
from settings import BOT_TOKEN
from models import User, IgnoredCurrency
from utils import setup_logger


def init_db():
  if not User.table_exists():
    User.create_table()
  if not IgnoredCurrency.table_exists():
    IgnoredCurrency.create_table()


if __name__ == '__main__':
  init_db()

  api_observer_logger = setup_logger(ApiObserver.__name__)
  bot_logger = setup_logger(YobitBot.__name__)

  bot = YobitBot(BOT_TOKEN, bot_logger)
  bot.start()

  observer = ApiObserver(bot, api_observer_logger)
  observer.observe()
