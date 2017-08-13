import logging

BASE_URL = 'https://yobit.net/ru/'
CURRENCIES_NAMES_XPATH = '//*[@id="trade_market"]//tbody//tr//*[@class="first"]/text()'
CURRENCY_VALUE_XPATH = '//*[@class="top_center_list"]//li[@class="c_5"]//span/text()'

BOT_TOKEN = '395068991:AAHuDPRWP1nOdjPIlPA6Qvr0yWIBETBSoPE'

LOGGING_CONFIGS = {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   'filename': 'log.txt', 'filemode': 'w', 'level': logging.INFO}
JOB_STARTED_LOG = 'Job started'
JOB_FINISHED_LOG = 'Job finished'

DB_NAME = 'yobit_bot_db'
DB_USER = 'root'
DB_PASS = 'root'


def get_currency_url(currency_name):
  return 'https://yobit.net/ru/trade/{}/BTC?_pjax=%23data-pjax-container'.format(currency_name)


def format_currency_value(raw_value):
  currency_abbreviation = ' BTC'
  return float(raw_value.replace(currency_abbreviation, ''))
