import logging
import traceback
import requests
import time
from settings import INFO_URL, CURRENCY_PAIRS_KEY, CURRENCY_VOLUME_KEY, \
  VALUE_RAISE_BOUND, IGNORE_CURRENCIES, LOGGER_NAME, MAX_ALLOWED_VOLUME, CURRENCY_LAST_PRICE_KEY
from messages import get_value_raised_msg, get_grabbed_currencies_amount_msg, get_handled_currencies_amount_msg
from utils import get_currency_name_from_pair, is_pair_with_btc, get_ticker_url


def _should_ignore(currency_name, currency_volume):
  return currency_name.lower() in IGNORE_CURRENCIES or \
         (MAX_ALLOWED_VOLUME and currency_volume > MAX_ALLOWED_VOLUME)


class ApiObserver(object):
  def __init__(self, bot):
    self.bot = bot
    self.previous_values = dict()
    self.logger = logging.getLogger(LOGGER_NAME)

  def observe(self):
    while True:
      try:
        self._collect_data()
        time.sleep(40)
      except Exception:
        self.logger.error(traceback.print_exc())

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
        self._match_currency(currency_pair, currency_info)

  def _match_currency(self, currency_pair, currency_info):
    currency_name = get_currency_name_from_pair(currency_pair)
    currency_volume = currency_info[CURRENCY_VOLUME_KEY]
    if _should_ignore(currency_name, currency_volume):
      return
    prev_volume = self.previous_values.get(currency_pair)
    if prev_volume is not None:
      volume_raised = currency_volume - prev_volume >= VALUE_RAISE_BOUND
      if volume_raised:
        last_price = currency_info[CURRENCY_LAST_PRICE_KEY]
        msg = get_value_raised_msg(currency_name, prev_volume, currency_volume, last_price)
        self.bot.send_msg(msg)
        self.logger.info(msg)
    self.previous_values[currency_pair] = currency_volume

  def _split_currencies_pairs(self, chunk_size=50):
    splitted_pairs = list()
    for i in range(0, len(self.currencies_pairs_), chunk_size):
      splitted_pairs.append(self.currencies_pairs_[i:i + chunk_size])
    self.currencies_pairs_ = splitted_pairs
