import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
DEBUG = bool(os.environ.get('DEBUG', 'False'))

HEROKU_BASE_URL = os.environ.get('HEROKU_BASE_URL')

LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGER_FILE_PATH = os.path.join(BASE_DIR, 'log')
LOGGER_UPDATE_VALUE = "d"
LOGGER_UPDATE_INTERVAL = 1
LOGGER_BACKUP_COUNT = 1

ADMIN_PASSWORD = 'your_admin_password'
