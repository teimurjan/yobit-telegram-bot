import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN = '395068991:AAHuDPRWP1nOdjPIlPA6Qvr0yWIBETBSoPE'

LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGER_FILE_PATH = os.path.join(BASE_DIR, 'log')
LOGGER_UPDATE_VALUE = "d"
LOGGER_UPDATE_INTERVAL = 1
LOGGER_BACKUP_COUNT = 1

ADMIN_PASSWORD = 'your_admin_password'
