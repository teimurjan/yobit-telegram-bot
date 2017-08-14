def get_grabbed_currencies_amount_msg(amount):
  return 'Grabbed %s currencies' % amount


def get_value_raised_msg(currency_name, prev_value, next_value):
  return 'Value for %s raised from %s BTC to %s BTC' % (currency_name, prev_value, next_value)


def get_handled_currencies_amount_msg(amount):
  return 'Handled %s currencies' % amount
