import logging

from api_observer import ApiObserver
from bot import YobitBot
from constants import BOT_TOKEN, LOGGING_CONFIGS
from models import Chat


def main():
  logging.basicConfig(**LOGGING_CONFIGS)

  if not Chat.table_exists():
    Chat.create_table()

  bot = YobitBot(BOT_TOKEN)
  bot.start()

  observer = ApiObserver(bot)
  observer.observe()


if __name__ == '__main__':
  main()
