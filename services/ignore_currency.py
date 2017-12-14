from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from messages import CURRENCY_DELETE_SUCCESS, CURRENCY_ALREADY_EXISTS, CURRENCY_ADD_SUCCESS
from models import IgnoreCurrency
from utils import get_callback_data


def show():
  none_callback_data = get_callback_data()
  currencies = [[InlineKeyboardButton(text="Валюта", callback_data=none_callback_data),
                 InlineKeyboardButton(text="Действие", callback_data=none_callback_data)]]
  for currency in IgnoreCurrency.select():
    delete_callback_data = get_callback_data('delete_currency', {'value': currency.value})
    currencies.append([InlineKeyboardButton(text=currency.value, callback_data=none_callback_data),
                       InlineKeyboardButton(text='Удалить', callback_data=delete_callback_data)])
  reply_markup = InlineKeyboardMarkup(currencies, n_cols=2)
  return reply_markup


def delete(value):
  IgnoreCurrency.delete().where(IgnoreCurrency.value == value).execute()
  return CURRENCY_DELETE_SUCCESS


def add(value):
  currency, created = IgnoreCurrency.get_or_create(value=value.lower())
  if not created:
    return CURRENCY_ALREADY_EXISTS
  else:
    return CURRENCY_ADD_SUCCESS
