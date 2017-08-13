from bot import YobitBot
from constants import BOT_TOKEN, LOGGING_CONFIGS, JOB_FINISHED_LOG, JOB_STARTED_LOG
from models import Chat
from scrappy import CurrencyScrappy
import logging


def main():
  logging.basicConfig(**LOGGING_CONFIGS)

  if not Chat.table_exists():
    Chat.create_table()

  bot = YobitBot(BOT_TOKEN)
  bot.start()

  scrappy = CurrencyScrappy()

  while True:
    logging.info(JOB_STARTED_LOG)
    scrappy.grab_currencies_names()
    scrappy.check_currencies(bot)
    logging.info(JOB_FINISHED_LOG)


if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    logging.error(e)
