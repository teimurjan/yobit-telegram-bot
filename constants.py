import logging

INFO_URL = 'https://yobit.net/api/3/info'

CURRENCY_PAIRS_KEY = 'pairs'
CURRENCY_VOLUME_KEY = 'vol_cur'

MAX_PERMISSABLE_VOLUME = 150
VALUE_RAISE_BOUND = 1

BOT_TOKEN = '395068991:AAHuDPRWP1nOdjPIlPA6Qvr0yWIBETBSoPE'

LOGGING_CONFIGS = {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   'filename': 'log.txt', 'filemode': 'w', 'level': logging.INFO}

DB_NAME = 'yobit_bot_db'
DB_USER = 'root'
DB_PASS = 'root'


def get_ticker_url(currencies_names):
  return 'https://yobit.net/api/3/ticker/%s' % '-'.join(currencies_names)
