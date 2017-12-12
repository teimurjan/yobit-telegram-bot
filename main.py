from api_observer import ApiObserver
from bot.bot import YobitBot
from constants import BOT_TOKEN
from models import User
from utils import setup_logger

if __name__ == '__main__':
  if not User.table_exists():
    User.create_table()

  bot = YobitBot(BOT_TOKEN)
  bot.start()

  setup_logger()
  observer = ApiObserver(bot)
  observer.observe()
