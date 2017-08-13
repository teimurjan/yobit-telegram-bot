from lxml import html
import requests
from bot import YobitBot
from constants import get_currency_url, BASE_URL, CURRENCIES_NAMES_XPATH, CURRENCY_VALUE_XPATH, format_currency_value
from messages import get_value_raised_msg, get_invalid_value_msg, get_grabbed_currencies_amount_msg, \
  get_checking_currency_msg
import logging


class CurrencyScrappy:
  def __init__(self):
    self.previous_values = dict()

  def grab_currencies_names(self):
    page_source = html.fromstring(requests.get(BASE_URL).text)
    self.currencies_names_ = page_source.xpath(CURRENCIES_NAMES_XPATH)
    logging.info(get_grabbed_currencies_amount_msg(len(self.currencies_names_)))

  def check_currencies(self, bot: YobitBot):
    i = 0
    for currency_name in self.currencies_names_:
      i += 1
      logging.info(get_checking_currency_msg(currency_name, i))
      page_source = html.fromstring(requests.get(get_currency_url(currency_name)).text)
      value = page_source.xpath(CURRENCY_VALUE_XPATH)[0]
      formatted_value = self._format_value(currency_name, value)
      if formatted_value:
        try:
          previous_value = self.previous_values[currency_name]
          if self._did_value_raised(previous_value, formatted_value):
            bot.send_msg(get_value_raised_msg(currency_name, previous_value, formatted_value))
        except KeyError:
          pass
        self.previous_values[currency_name] = formatted_value

  def _did_value_raised(self, prev_value, next_value):
    raise_bound = 1
    if next_value - prev_value >= raise_bound:
      return True
    return False

  def _format_value(self, currency_name, value):
    try:
      formatted_value = format_currency_value(value)
      return formatted_value
    except Exception:
      logging.error(get_invalid_value_msg(currency_name, value))
