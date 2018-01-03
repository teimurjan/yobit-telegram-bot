from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils import DELETE_CURRENCY_ACTION_KEY
from messages import CURRENCY_DELETE_SUCCESS, CURRENCY_ALREADY_EXISTS, CURRENCY_ADD_SUCCESS
from models import IgnoredCurrency
from utils import get_callback_data


def show(user):
  none_callback_data = get_callback_data()
  currencies = [[InlineKeyboardButton(text="Currency", callback_data=none_callback_data),
                 InlineKeyboardButton(text="Action", callback_data=none_callback_data)]]
  for currency in IgnoredCurrency.select().where(IgnoredCurrency.user == user):
    delete_callback_data = get_callback_data(DELETE_CURRENCY_ACTION_KEY, {'value': currency.value, 'user_id': user.id})
    currencies.append([InlineKeyboardButton(text=currency.value, callback_data=none_callback_data),
                       InlineKeyboardButton(text='Delete', callback_data=delete_callback_data)])
  reply_markup = InlineKeyboardMarkup(currencies, n_cols=2)
  return reply_markup


def delete(value, user_id):
  IgnoredCurrency.delete().where((IgnoredCurrency.value == value) & (IgnoredCurrency.user == user_id)).execute()
  return CURRENCY_DELETE_SUCCESS


def add(value, user):
  currency, created = IgnoredCurrency.get_or_create(value=value.lower(), user=user)
  if not created:
    return CURRENCY_ALREADY_EXISTS
  else:
    return CURRENCY_ADD_SUCCESS
