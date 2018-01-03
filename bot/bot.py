import json

from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler

from bot.utils import DELETE_CURRENCY_ACTION_KEY, DELETE_USER_ACTION_KEY
from messages import NOT_FOUND, DELETE_USER_HELP_TEXT, DELETE_CURRENCY_HELP_TEXT, SHOW_USERS, SHOW_IGNORED_CURRENCIES, \
  get_value_raised_msg
from models import User, IgnoredCurrency
from services.auth import become_admin, register
from services.ignore_currency import delete as delete_currency, add as add_currency, show as show_currencies
from services.users import add as add_user, show as show_users, delete as delete_user, update as update_user
from settings import CURRENCY_VOLUME_KEY, CURRENCY_LAST_PRICE_KEY
from utils import get_currency_name_from_pair


def admin_required(func):
  def wrapper(self, bot, update, **kwargs):
    user_id = update.message.from_user.id
    try:
      user = User.get(t_id=user_id)
      if not user.is_admin:
        raise User.DoesNotExist()
      return func(self, bot, update, **kwargs)
    except User.DoesNotExist:
      return update.reply_text(NOT_FOUND, reply_markup=ReplyKeyboardRemove())

  return wrapper


def inject_user(func):
  def wrapper(self, bot, update, **kwargs):
    user_id = update.message.from_user.id
    try:
      user = User.get(t_id=user_id)
      return func(self, bot, update, user, **kwargs)
    except User.DoesNotExist:
      return update.reply_text(NOT_FOUND, reply_markup=ReplyKeyboardRemove())

  return wrapper


class YobitBot(object):
  def __init__(self, token, logger):
    self.token = token
    self.text_msg_router = {
      r'^(A|a)dd user (?P<login>.{5,})$': self._add_user,
      r'^(I|i)gnore (?P<currency>.{1,})$': self._add_currency,
      r'^(L|l)ogin (?P<login>.{5,})$': self._register,
      r'^(M|m)e$': self._about_me,
      r'^(S|s)et max volume (?P<volume>\d+)$': self._set_max_volume,
      r'^(S|s)et raise bound (?P<bound>\d+(\.\d+)?)$': self._set_raise_bound,
      r'^(A|a)dmin (?P<password>.{5,})$': self._become_admin,
      r'^{}$'.format(SHOW_USERS): self._show_users,
      r'^{}$'.format(SHOW_IGNORED_CURRENCIES): self._show_currencies,
    }
    self.action_to_callback = {
      DELETE_CURRENCY_ACTION_KEY: delete_currency,
      DELETE_USER_ACTION_KEY: delete_user
    }
    self.logger = logger
    self.updater = None

  def start(self) -> None:
    self.updater = Updater(token=self.token)
    self._init_commands_handlers()
    self.updater.start_polling(poll_interval=1)

  def _init_commands_handlers(self) -> None:
    dispatcher = self.updater.dispatcher
    text_msg_handler = MessageHandler(Filters.text, self._handle_plain_text_update)
    inline_btn_handler = CallbackQueryHandler(self.inline_btn_callback)
    dispatcher.add_handler(text_msg_handler)
    dispatcher.add_handler(inline_btn_handler)
    dispatcher.add_error_handler(self._handle_error)

  def _handle_error(self, bot, update, error):
    try:
      raise error
    except Exception as e:
      self.logger.error('BOT: {}'.format(str(e)))

  def _handle_plain_text_update(self, bot, update) -> None:
    import re
    for msg_template, handler in self.text_msg_router.items():
      pattern = re.compile(msg_template)
      match = pattern.match(update.message.text)
      if match:
        return handler(bot, update, **match.groupdict())
    return self._not_found(bot, update)

  @staticmethod
  def _register(bot, update, login=None) -> None:
    update.message.reply_text(**register(login, update.message))

  @inject_user
  def _about_me(self, bot, update, user) -> None:
    update.message.reply_text(text=user.about)

  @inject_user
  def _set_max_volume(self, bot, update, user, volume):
    update.message.reply_text(update_user(user, volume=volume))

  @inject_user
  def _set_raise_bound(self, bot, update, user, bound):
    update.message.reply_text(update_user(user, bound=float(bound)))

  @admin_required
  def _add_user(self, bot, update, login=None) -> None:
    update.message.reply_text(add_user(login))

  @admin_required
  def _show_users(self, bot, update) -> None:
    update.message.reply_text(DELETE_USER_HELP_TEXT, reply_markup=show_users())

  @inject_user
  def _add_currency(self, bot, update, user, currency=None) -> None:
    update.message.reply_text(add_currency(currency, user))

  @inject_user
  def _show_currencies(self, bot, update, user) -> None:
    update.message.reply_text(DELETE_CURRENCY_HELP_TEXT, reply_markup=show_currencies(user))

  @staticmethod
  def _not_found(bot, update) -> None:
    update.message.reply_text(NOT_FOUND)

  @staticmethod
  def _become_admin(bot, update, password) -> None:
    update.message.reply_text(**become_admin(update.message, password))

  def inline_btn_callback(self, bot, update) -> None:
    data = json.loads(update.callback_query.data)
    action, action_kwargs = data.popitem()
    if action is not None:
      bot.edit_message_text(text=self.action_to_callback[action](**action_kwargs),
                            chat_id=update.callback_query.message.chat_id,
                            message_id=update.callback_query.message.message_id)

  def send_msg(self, currency_pair, currency_info, prev_volume) -> None:
    bot = self.updater.dispatcher.bot
    for user in User.select().where(User.is_active == True):
      try:
        currency_name = get_currency_name_from_pair(currency_pair).lower()
        if user.should_receive_notification(currency_name, currency_info, prev_volume):
          msg = get_value_raised_msg(currency_name.upper(), prev_volume,
                                     currency_info[CURRENCY_VOLUME_KEY],
                                     currency_info[CURRENCY_LAST_PRICE_KEY])
          bot.send_message(user.chat_id, text=msg)
          self.logger.info(msg)
      except Exception as e:
        self.logger.error('BOT: {}\nCouldn\'t send msg to user {}'.format(str(user), str(e)))
