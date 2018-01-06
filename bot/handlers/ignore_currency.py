from json import dumps

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import RegexHandler

from bot.handlers.base import login_required, unfold_groupdict
from bot.utils import DELETE_CURRENCY_ACTION_KEY
from messages import CURRENCY_ALREADY_EXISTS, CURRENCY_ADD_SUCCESS, DELETE_CURRENCY_HELP_TEXT, SHOW_IGNORED_CURRENCIES, \
  CURRENCY_DELETE_SUCCESS, CURRENCY_NOT_EXISTS
from models import IgnoredCurrency


@login_required
@unfold_groupdict
def _add_ignore_currency(bot, update, user, currency) -> None:
  currency, created = IgnoredCurrency.get_or_create(value=currency.lower(), user=user)
  update.message.reply_text(CURRENCY_ALREADY_EXISTS if not created else CURRENCY_ADD_SUCCESS)


@login_required
def _show_ignore_currencies(bot, update, user) -> None:
  currencies = [[InlineKeyboardButton(text="Currency", callback_data='{]'),
                 InlineKeyboardButton(text="Action", callback_data='{]')]]
  for currency in IgnoredCurrency.select().where(IgnoredCurrency.user == user):
    delete_callback_data = dumps({DELETE_CURRENCY_ACTION_KEY: {'currency': currency.value, 'user_id': user.id}})
    currencies.append([InlineKeyboardButton(text=currency.value, callback_data='{]'),
                       InlineKeyboardButton(text='Delete', callback_data=delete_callback_data)])
  reply_markup = InlineKeyboardMarkup(currencies, n_cols=2)
  update.message.reply_text(DELETE_CURRENCY_HELP_TEXT, reply_markup=reply_markup)


@login_required
def delete_ignore_currency_handler(bot, update, user, currency, user_id) -> None:
  reply = lambda text: bot.edit_message_text(text=text, chat_id=update.callback_query.message.chat_id,
                                             message_id=update.callback_query.message.message_id)
  ignore_currency = IgnoredCurrency.select().where(
    (IgnoredCurrency.value == currency) & (IgnoredCurrency.user == user_id))
  if ignore_currency.exists():
    IgnoredCurrency.delete().where((IgnoredCurrency.value == currency) & (IgnoredCurrency.user == user_id)).execute()
    reply(CURRENCY_DELETE_SUCCESS)
  else:
    reply(CURRENCY_NOT_EXISTS)


add_ignore_currency_handler = RegexHandler(r'^(I|i)gnore (?P<currency>.{1,})$',
                                           _add_ignore_currency, pass_groupdict=True)
show_ignore_currencies_handler = RegexHandler(r'^({})|((S|s)ig)$'.format(SHOW_IGNORED_CURRENCIES),
                                              _show_ignore_currencies)
