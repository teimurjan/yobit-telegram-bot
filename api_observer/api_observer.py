import time
import traceback
from json import JSONDecodeError

import requests

from bot.message import Message
from messages import get_grabbed_currencies_amount_msg, get_handled_currencies_amount_msg
from api_observer.utils import is_pair_with_btc, get_ticker_url, INFO_URL, CURRENCY_PAIRS_KEY, CURRENCY_VOLUME_KEY, \
  get_currency_name_from_pair


class ApiObserver:
  def __init__(self, bot, logger):
    self.bot = bot
    self.previous_values = dict()
    self.logger = logger

  def observe(self):
    while True:
      try:
        self._collect_data()
        time.sleep(40)
      except Exception:
        self.logger.error(traceback.format_exc())

  def _collect_data(self):
    self._collect_currencies_pairs()
    self.logger.info(get_grabbed_currencies_amount_msg(len(self.currencies_pairs_)))
    self._collect_values_with_matching()
    self.logger.info(get_handled_currencies_amount_msg(len(self.previous_values)))

  def _collect_currencies_pairs(self):
    response = requests.get(INFO_URL)
    try:
      payload = response.json()
      currencies_pairs = payload[CURRENCY_PAIRS_KEY].keys()
      self.currencies_pairs_ = [currency_pair for currency_pair in currencies_pairs if is_pair_with_btc(currency_pair)]
    except JSONDecodeError as e:
      self.logger.error('Could not get currencies pairs. {}. Response: {}'.format(str(e), response.text))

  def _collect_values_with_matching(self):
    self._split_currencies_pairs()
    for currencies_pairs_chunk in self.currencies_pairs_:
      url = get_ticker_url(currencies_pairs_chunk)
      response = requests.get(url)
      try:
        payload = response.json()
        for currency_pair, currency_info in payload.items():
          currency_name = get_currency_name_from_pair(currency_pair)
          prev_volume = self.previous_values.get(currency_name)
          msg = Message(currency_name, currency_info, prev_volume)
          self.bot.dispatch_message(msg)
          self.previous_values[currency_name] = currency_info[CURRENCY_VOLUME_KEY]
        time.sleep(1)
      except JSONDecodeError as e:
        self.logger.error('{}. Could not get ticket by url {}. Response: {}'.format(str(e), url, response.text))

  def _split_currencies_pairs(self, chunk_size=50):
    splitted_pairs = list()
    for i in range(0, len(self.currencies_pairs_), chunk_size):
      splitted_pairs.append(self.currencies_pairs_[i:i + chunk_size])
    self.currencies_pairs_ = splitted_pairs
