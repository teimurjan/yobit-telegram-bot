from api_observer import ApiObserver
from bot import YobitBot
from constants import BOT_TOKEN
from models import Chat
from utils import setup_logger

if __name__ == '__main__':
  if not Chat.table_exists():
    Chat.create_table()

  bot = YobitBot(BOT_TOKEN)
  bot.start()

  setup_logger()
  observer = ApiObserver(bot)
  observer.observe()
