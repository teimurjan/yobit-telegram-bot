def get_grabbed_currencies_amount_msg(amount):
  return 'Grabbed {} currencies'.format(amount)


def get_value_raised_msg(currency_name, prev_value, next_value, last_price):
  return 'Value for {} raised from {} BTC to {} BTC. Last price was {}.'.format(
    currency_name, prev_value, next_value, last_price)


def get_handled_currencies_amount_msg(amount):
  return 'Handled {} currencies'.format(amount)


NOT_FOUND = 'Unclear :('

REGISTRATION_SUCCESS_MSG = 'Welcome!'
ALREADY_REGISTERED_MSG = 'You\'ve already registered.'
ADMIN_EXISTS = 'User with such id already exists'
BECOME_ADMIN_SUCCESS = 'You are an admin now!'
LOG_IN_NOT_ALLOWED = 'Get a permission at first.'
NO_LOGIN = 'Call your login.'

USER_ALREADY_EXISTS = 'This user is already added'
USER_NOT_EXISTS = 'This user doesn\'t exist'
USER_ADD_SUCCESS = 'The user was added'
USER_UPDATE_SUCCESS = 'Your settings were updated'
MIN_RAISE_LIMIT_MSG = 'Min value of raise limit should be greater then 0.5'
MIN_ALLOWED_VOLUME_MSG = 'Min value of max allowed volume should be greater then 1'
USER_DELETE_SUCCESS = 'The user was deleted'

CURRENCY_DELETE_SUCCESS = "The currency is no longer ignored."
CURRENCY_ADD_SUCCESS = 'The currency is ignored now.'
CURRENCY_ALREADY_EXISTS = 'This currency is already ignored.'
CURRENCY_NOT_EXISTS = 'This currency doesn\'t exist'

DELETE_USER_HELP_TEXT = 'Press "Delete" to delete a user.'
DELETE_CURRENCY_HELP_TEXT = 'Press "Delete" to prevent ignoring a currency.'

SHOW_USERS = 'Show users'
SHOW_IGNORED_CURRENCIES = 'Show ignored currencies'
