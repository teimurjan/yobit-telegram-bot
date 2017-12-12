def get_grabbed_currencies_amount_msg(amount):
  return 'Grabbed %s currencies' % amount


def get_value_raised_msg(currency_name, prev_value, next_value):
  return 'Value for %s raised from %s BTC to %s BTC' % (currency_name, prev_value, next_value)


def get_handled_currencies_amount_msg(amount):
  return 'Handled %s currencies' % amount


NOT_FOUND = 'Unknown command'

REGISTRATION_SUCCESS_MSG = 'Registration completed successfully!'
ALREADY_REGISTERED_MSG = 'You have already registered'
ADMIN_EXISTS = 'You are already an admin'
BECOME_ADMIN_SUCCESS = 'Now you are an admin'
LOG_IN_NOT_ALLOWED = 'You are not allowed to log in.'
NO_LOGIN = 'You have no username or haven\'t sent your phone number'


NO_LOGIN_SENT = 'You\'ve not sent a login to add'
USER_ALREADY_EXISTS = 'User with such login already exists'
USER_NOT_EXISTS = 'There is no user with such login'
ADD_SUCCESS = 'User was successfully added'
DELETE_SUCCESS = 'User was successfully deleted'