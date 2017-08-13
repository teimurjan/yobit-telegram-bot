def get_value_raised_msg(currency_name, prev_value, next_value):
  return 'Value for %s raised from %s BTC to %s BTC' % (currency_name, prev_value, next_value)


def get_invalid_value_msg(currency_name, value):
  return 'Wrong value for %s = %s' % (currency_name, value)


def get_new_currency_msg(currency_name):
  return 'Found new currency %s' % currency_name
