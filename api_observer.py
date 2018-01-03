import time

import requests

from messages import get_grabbed_currencies_amount_msg, get_handled_currencies_amount_msg
from settings import INFO_URL, CURRENCY_PAIRS_KEY, CURRENCY_VOLUME_KEY
from utils import is_pair_with_btc, get_ticker_url


class ApiObserver(object):
  def __init__(self, bot, logger):
    self.bot = bot
    self.previous_values = dict()
    self.logger = logger

  def observe(self):
    while True:
      try:
        self._collect_data()
        time.sleep(40)
      except Exception as e:
        self.logger.error('API_OBSERVER: {}'.format(str(e)))

  def _collect_data(self):
    self._collect_currencies_pairs()
    self.logger.info(get_grabbed_currencies_amount_msg(len(self.currencies_pairs_)))
    self._collect_values_with_matching()
    self.logger.info(get_handled_currencies_amount_msg(len(self.previous_values)))

  def _collect_currencies_pairs(self):
    response = requests.get(INFO_URL).json()
    currencies_pairs = response[CURRENCY_PAIRS_KEY].keys()
    self.currencies_pairs_ = [currency_pair for currency_pair in currencies_pairs if is_pair_with_btc(currency_pair)]

  def _collect_values_with_matching(self):
    self._split_currencies_pairs()
    for currencies_pairs_chunk in self.currencies_pairs_:
      response = requests.get(get_ticker_url(currencies_pairs_chunk)).json()
      for currency_pair, currency_info in response.items():
        prev_volume = self.previous_values.get(currency_pair)
        self.bot.send_msg(currency_pair, currency_info, prev_volume)
        self.previous_values[currency_pair] = currency_info[CURRENCY_VOLUME_KEY]

  def _split_currencies_pairs(self, chunk_size=50):
    splitted_pairs = list()
    for i in range(0, len(self.currencies_pairs_), chunk_size):
      splitted_pairs.append(self.currencies_pairs_[i:i + chunk_size])
    self.currencies_pairs_ = splitted_pairs
