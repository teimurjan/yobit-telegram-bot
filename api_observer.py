import logging

import requests
import time

from constants import INFO_URL, CURRENCY_PAIRS_KEY, CURRENCY_VOLUME_KEY, MAX_PERMISSABLE_VOLUME, \
  VALUE_RAISE_BOUND, IGNORE_CURRENCIES
from messages import get_value_raised_msg, get_grabbed_currencies_amount_msg, get_handled_currencies_amount_msg
from utils import get_currency_name_from_pair, is_pair_with_btc, get_ticker_url


class ApiObserver(object):
  def __init__(self, bot):
    self.bot = bot
    self.previous_values = dict()

  def observe(self):
    while True:
      try:
        self._collect_data()
        time.sleep(40)
      except Exception as e:
        logging.error(e)

  def _collect_data(self):
    self._collect_currencies_pairs()
    logging.info(get_grabbed_currencies_amount_msg(len(self.currencies_pairs_)))
    self._collect_values_with_matching()
    logging.info(get_handled_currencies_amount_msg(len(self.previous_values)))

  def _collect_currencies_pairs(self):
    response = requests.get(INFO_URL).json()
    currencies_pairs = response[CURRENCY_PAIRS_KEY].keys()
    self.currencies_pairs_ = [currency_pair for currency_pair in currencies_pairs if is_pair_with_btc(currency_pair)]

  def _collect_values_with_matching(self):
    self._split_currencies_pairs()
    for currencies_pairs_chunk in self.currencies_pairs_:
      response = requests.get(get_ticker_url(currencies_pairs_chunk)).json()
      for name, value in response.items():
        if get_currency_name_from_pair(name).lower() in IGNORE_CURRENCIES:
          continue
        volume = value[CURRENCY_VOLUME_KEY]
        if volume > MAX_PERMISSABLE_VOLUME:
          continue
        self._match_with_prev(name, volume)
        self.previous_values[name] = volume

  def _match_with_prev(self, currency_pair, currency_volume):
    try:
      prev_volume = self.previous_values[currency_pair]
      has_value_raised = currency_volume - prev_volume >= VALUE_RAISE_BOUND
      if has_value_raised:
        msg = get_value_raised_msg(get_currency_name_from_pair(currency_pair), prev_volume, currency_volume)
        self.bot.send_msg(msg)
        logging.info(msg)
    except KeyError:
      pass

  def _split_currencies_pairs(self, chunk_size=50):
    splitted_pairs = list()
    for i in range(0, len(self.currencies_pairs_), chunk_size):
      splitted_pairs.append(self.currencies_pairs_[i:i + chunk_size])
    self.currencies_pairs_ = splitted_pairs
