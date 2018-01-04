INFO_URL = 'https://yobit.net/api/3/info'
CURRENCY_PAIRS_KEY = 'pairs'
CURRENCY_VOLUME_KEY = 'vol'
CURRENCY_LAST_PRICE_KEY = 'last'


def get_currency_name_from_pair(currency_pair):
  return currency_pair.replace('_btc', '')


def is_pair_with_btc(currency_pair):
  return '_btc' in currency_pair


def get_ticker_url(currencies_names):
  return 'https://yobit.net/api/3/ticker/%s' % '-'.join(currencies_names)
