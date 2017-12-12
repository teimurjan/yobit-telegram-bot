import logging
from logging.handlers import TimedRotatingFileHandler

from settings import LOGGER_NAME, LOGGER_FORMAT, LOGGER_FILE_PATH, LOGGER_UPDATE_VALUE, LOGGER_UPDATE_INTERVAL, \
  LOGGER_BACKUP_COUNT


def get_currency_name_from_pair(currency_pair):
  return currency_pair.replace('_btc', '').upper()


def is_pair_with_btc(currency_pair):
  return '_btc' in currency_pair


def get_ticker_url(currencies_names):
  return 'https://yobit.net/api/3/ticker/%s' % '-'.join(currencies_names)


def setup_logger():
  logger = logging.getLogger(LOGGER_NAME)
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter(LOGGER_FORMAT)
  handler = TimedRotatingFileHandler(LOGGER_FILE_PATH,
                                     when=LOGGER_UPDATE_VALUE,
                                     interval=LOGGER_UPDATE_INTERVAL,
                                     backupCount=LOGGER_BACKUP_COUNT)
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger
