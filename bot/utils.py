from telegram import ReplyKeyboardMarkup

from messages import SHOW_IGNORED_CURRENCIES, SHOW_USERS

DELETE_CURRENCY_ACTION_KEY = 'del_curr'
DELETE_USER_ACTION_KEY = 'del_user'

ADMIN_KEYBOARD = ReplyKeyboardMarkup([[SHOW_USERS], [SHOW_IGNORED_CURRENCIES]])
USER_KEYBOARD = ReplyKeyboardMarkup([[SHOW_IGNORED_CURRENCIES]])