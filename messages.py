def get_grabbed_currencies_amount_msg(amount):
  return 'Grabbed {} currencies'.format(amount)


def get_value_raised_msg(currency_name, prev_value, next_value, last_price):
  return 'Value for {} raised from {} BTC to {} BTC. Last price was {}.'.format(
    currency_name, prev_value, next_value, last_price)


def get_handled_currencies_amount_msg(amount):
  return 'Handled {} currencies'.format(amount)


NOT_FOUND = 'Непонятно'

REGISTRATION_SUCCESS_MSG = 'Добро пожаловать!'
ALREADY_REGISTERED_MSG = 'Но ты уже зарегистрирован.'
ADMIN_EXISTS = 'Ты уже админ :)'
BECOME_ADMIN_SUCCESS = 'Теперь ты админ!'
LOG_IN_NOT_ALLOWED = 'Сначала получи разрешение.'
NO_LOGIN = 'Представьтесь, пожалуйста.'

USER_ALREADY_EXISTS = 'Так он уже добавлен :)'
USER_NOT_EXISTS = 'Нет такого пользователя.'
USER_ADD_SUCCESS = 'Пользователь добавлен'
USER_DELETE_SUCCESS = 'Пользователь удален'

CURRENCY_DELETE_SUCCESS = "Валюта больше не игнорируется"
CURRENCY_ADD_SUCCESS = 'Валюта добавлена в игнорируемые'
CURRENCY_ALREADY_EXISTS = 'Такая валюта уже игнорируется'

