from json import JSONDecodeError
from time import sleep

import requests

INFO_URL = 'https://yobit.net/api/3/info'
CURRENCY_PAIRS_KEY = 'pairs'
CURRENCY_VOLUME_KEY = 'vol'
CURRENCY_LAST_PRICE_KEY = 'last'


def get_currency_name_from_pair(currency_pair):
  return currency_pair.replace('_btc', '')


def is_pair_with_btc(currency_pair):
  return '_btc' in currency_pair


def get_with_retry(url, max_retry=3, try_number=0):
  if try_number > max_retry:
    return None
  try:
    return requests.get(url).json()
  except JSONDecodeError:
    sleep(1)
    return get_with_retry(url, max_retry, try_number + 1)
