import os

from models import IgnoreCurrency

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INFO_URL = 'https://yobit.net/api/3/info'

CURRENCY_PAIRS_KEY = 'pairs'
CURRENCY_VOLUME_KEY = 'vol'
CURRENCY_LAST_PRICE_KEY = 'last'

MAX_ALLOWED_VOLUME = None
VALUE_RAISE_BOUND = 1

BOT_TOKEN = '395068991:AAHuDPRWP1nOdjPIlPA6Qvr0yWIBETBSoPE'

LOGGER_NAME = "DEBUG_LOG"
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGER_FILE_PATH = os.path.join(BASE_DIR, 'log')
LOGGER_UPDATE_VALUE = "d"
LOGGER_UPDATE_INTERVAL = 1
LOGGER_BACKUP_COUNT = 1

ADMIN_PASSWORD = 'your_admin_password'
