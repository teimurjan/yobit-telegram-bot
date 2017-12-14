import json

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler

from messages import NOT_FOUND
from models import User
from services.auth import become_admin, register
from services.ignore_currency import delete as delete_currency, add as add_currency, show as show_currencies
from services.users import add as add_user, show as show_users, delete as delete_user


def admin_required(func):
  def wrapper(self, bot, update, **kwargs):
    user_id = update.message.from_user.id
    try:
      user = User.get(t_id=user_id)
      if not user.is_admin:
        raise User.DoesNotExist()
      return func(self, bot, update, **kwargs)
    except User.DoesNotExist:
      return update.reply_text(NOT_FOUND)

  return wrapper


class YobitBot(object):
  def __init__(self, token, logger):
    self.token = token
    self.text_msg_router = {
      r'^Добавь(\-ка)? пользователя (?P<login>.{5,})$': self._add_user,
      r'^Игнорируй (?P<currency>.{1,})$': self._add_currency,
      r'^(Привет\,?)?\s?(я|Я)(\s?\-\s?|\s)(?P<login>.{5,})$': self._register,
      r'^Покажи всех пользователей$': self._show_users,
      r'^Покажи игнорируемые валюты$': self._show_currencies,
    }
    self.logger = logger

  def start(self) -> None:
    self.updater_ = Updater(token=self.token)
    self._init_commands_handlers()
    self.updater_.start_polling(poll_interval=1)

  def _init_commands_handlers(self) -> None:
    dispatcher = self.updater_.dispatcher
    text_msg_handler = MessageHandler(Filters.text, self._handle_plain_text_update)
    admin_handler = CommandHandler('admin', self._become_admin)
    inline_btn_handler = CallbackQueryHandler(self.inline_btn_callback)
    dispatcher.add_handler(text_msg_handler)
    dispatcher.add_handler(admin_handler)
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

  def _register(self, bot, update, login=None) -> None:
    update.message.reply_text(register(login, update.message))

  @admin_required
  def _add_user(self, bot, update, login=None) -> None:
    update.message.reply_text(add_user(login))

  @admin_required
  def _show_users(self, bot, update) -> None:
    update.message.reply_text('Чтобы удалить пользователя, нажми "Удалить".', reply_markup=show_users())

  @admin_required
  def _add_currency(self, bot, update, currency=None) -> None:
    update.message.reply_text(add_currency(currency))

  @admin_required
  def _show_currencies(self, bot, update) -> None:
    update.message.reply_text('Чтобы перестать игнорировать валюту, нажми "Удалить".', reply_markup=show_currencies())

  def inline_btn_callback(self, bot, update) -> None:
    data = json.loads(update.callback_query.data)
    action = data['action']
    if action is not None:
      bot.edit_message_text(text=globals()[action](**data['kwargs']),
                            chat_id=update.callback_query.message.chat_id,
                            message_id=update.callback_query.message.message_id)

  def _not_found(self, bot, update) -> None:
    update.message.reply_text(NOT_FOUND)

  def _become_admin(self, bot, update) -> None:
    update.message.reply_text(**become_admin(update.message))

  def send_msg(self, msg) -> None:
    bot = self.updater_.dispatcher.bot
    for user in User.select().where(User.is_active == True):
      try:
        bot.send_message(user.chat_id, text=msg)
      except Exception as e:
        self.logger.error('BOT: {}\nCouldn\'t send msg to user {}'.format(str(user), str(e)))
