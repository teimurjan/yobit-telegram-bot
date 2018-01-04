import logging
from logging.handlers import TimedRotatingFileHandler

from settings import LOGGER_FORMAT, LOGGER_FILE_PATH, LOGGER_UPDATE_VALUE, LOGGER_UPDATE_INTERVAL, \
  LOGGER_BACKUP_COUNT


def setup_logger(name):
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter(LOGGER_FORMAT)
  handler = TimedRotatingFileHandler(LOGGER_FILE_PATH,
                                     when=LOGGER_UPDATE_VALUE,
                                     interval=LOGGER_UPDATE_INTERVAL,
                                     backupCount=LOGGER_BACKUP_COUNT)
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger

