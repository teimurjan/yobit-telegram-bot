from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from bot.commands import START_COMMAND, LIST_USERS_COMMAND, ADD_USER_COMMAND, DELETE_USER_COMMAND, BECOME_ADMIN_COMMAND
from messages import NOT_FOUND
from models import User
from services.auth import register, become_admin
from services.users import add, show, delete
from bot.constants import REGISTER_WITH_PHONE_BTN_TEXT, REGISTER_WITH_USERNAME_BTN_TEXT, \
  LOGIN_WITH_USERNAME_REGEX, REGISTRATION_INFO_TEXT


def admin_required(func):
  def wrapper(self, bot, update, **kwargs):
    user_id = update.message.from_user.id
    try:
      user = User.get(telegram_user_id=user_id)
      if not user.is_admin:
        raise User.DoesNotExist()
      return func(self, bot, update, **kwargs)
    except User.DoesNotExist:
      return bot.send_message(chat_id=update.message.chat_id, text=NOT_FOUND)

  return wrapper


class YobitBot(object):
  def __init__(self, token):
    self.token = token
    self.msg_router = {
      LOGIN_WITH_USERNAME_REGEX: self._register_with_username
    }

  def start(self) -> None:
    self.updater_ = Updater(token=self.token)
    self._init_commands_handlers()
    self.updater_.start_polling(poll_interval=1)

  def _init_commands_handlers(self) -> None:
    dispatcher = self.updater_.dispatcher
    msg_handler = MessageHandler(Filters.text, self._handle_plain_text_update)
    login_with_phone_handler = MessageHandler(Filters.contact, self._register_with_phone)
    start_handler = CommandHandler(START_COMMAND, self._handle_start)
    list_users_handler = CommandHandler(LIST_USERS_COMMAND, self._list_users)
    add_user_handler = CommandHandler(ADD_USER_COMMAND, self._add_user)
    delete_user_handler = CommandHandler(DELETE_USER_COMMAND, self._delete_user)
    become_admin_handler = CommandHandler(BECOME_ADMIN_COMMAND, self._become_admin)
    dispatcher.add_handler(msg_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_users_handler)
    dispatcher.add_handler(add_user_handler)
    dispatcher.add_handler(delete_user_handler)
    dispatcher.add_handler(login_with_phone_handler)
    dispatcher.add_handler(become_admin_handler)

  def _handle_plain_text_update(self, bot, update) -> None:
    import re
    for msg_template, handler in self.msg_router.items():
      pattern = re.compile(msg_template)
      match = pattern.match(update.message.text)
      if match:
        return handler(bot, update, **match.groupdict())
    return self._handle_not_found(bot, update)

  def _handle_start(self, bot, update) -> None:
    phone_button = KeyboardButton(REGISTER_WITH_PHONE_BTN_TEXT, request_contact=True)
    username_button = KeyboardButton(REGISTER_WITH_USERNAME_BTN_TEXT)
    keyboard = ReplyKeyboardMarkup([[phone_button], [username_button]], row_width=1, resize_keyboard=True)
    update.message.reply_text(REGISTRATION_INFO_TEXT, reply_markup=keyboard)

  def _register_with_phone(self, bot, update) -> None:
    msg = register(update)
    update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())

  def _register_with_username(self, bot, update) -> None:
    msg = register(update, by='username')
    update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())

  def _handle_not_found(self, bot, update) -> None:
    update.message.reply_text(NOT_FOUND)

  @admin_required
  def _list_users(self, bot, update) -> None:
    update.message.reply_text(show(), reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

  @admin_required
  def _add_user(self, bot, update) -> None:
    login = update.message.text.split(' ')[1]
    update.message.reply_text(add(login), reply_markup=ReplyKeyboardRemove())

  def _become_admin(self, bot, update):
    update.message.reply_text(become_admin(update), reply_markup=ReplyKeyboardRemove())

  @admin_required
  def _delete_user(self, bot, update) -> None:
    login = update.message.text.split(' ')[1]
    update.message.reply_text(delete(login), reply_markup=ReplyKeyboardRemove())

  def send_msg(self, msg) -> None:
    bot = self.updater_.dispatcher.bot
    for user in User.select().where(User.is_active is True):
      bot.send_message(user.chat_id, text=msg)
