from api_observer.utils import CURRENCY_VOLUME_KEY, CURRENCY_LAST_PRICE_KEY


class Message:
  def __init__(self, currency_name, currency_info, prev_volume):
    self._currency_name = currency_name
    self._current_volume = currency_info[CURRENCY_VOLUME_KEY]
    self._last_price = currency_info[CURRENCY_LAST_PRICE_KEY]
    self._prev_volume = prev_volume

  def get_currency_name(self):
    return self._currency_name

  def get_current_volume(self):
    return self._current_volume

  def get_last_price(self):
    return self._last_price

  def get_prev_volume(self):
    return self._prev_volume

  def __str__(self):
    return 'Value for {} raised from {} BTC to {} BTC. Last price was {}.'.format(
      self._currency_name.upper(), self._prev_volume, self._current_volume, self._last_price)
