from telegram import ReplyKeyboardRemove
from telegram.ext import RegexHandler

from bot.handlers.base import unfold_groupdict
from bot.utils import USER_KEYBOARD, ADMIN_KEYBOARD
from messages import NO_LOGIN, ALREADY_REGISTERED_MSG, REGISTRATION_SUCCESS_MSG, LOG_IN_NOT_ALLOWED, NOT_FOUND, \
  ADMIN_EXISTS, BECOME_ADMIN_SUCCESS
from models import User
from settings import ADMIN_PASSWORD


@unfold_groupdict
def _log_in(bot, update, login) -> None:
  reply = lambda text, markup=USER_KEYBOARD: update.message.reply_text(text, markup=markup)
  if login is None:
    reply(NO_LOGIN, ReplyKeyboardRemove())
  chat_id = update.message.chat_id
  telegram_user_id = update.message.from_user.id
  name = update.message.from_user.name
  try:
    user_with_same_login = User.select().where(User.login == login).get()
    user_with_same_id_exists = User.select().where(User.telegram_user_id == telegram_user_id).exists()
    if user_with_same_login.is_active or user_with_same_id_exists:
      reply(ALREADY_REGISTERED_MSG)
    else:
      User.update(chat_id=chat_id, telegram_user_id=telegram_user_id, name=name).where(User.login == login).execute()
      reply(REGISTRATION_SUCCESS_MSG)
  except User.DoesNotExist:
    reply(LOG_IN_NOT_ALLOWED, ReplyKeyboardRemove())


@unfold_groupdict
def _become_admin(bot, update, password) -> None:
  reply = lambda text, markup=ADMIN_KEYBOARD: update.message.reply_text(text, markup=markup)
  if password != ADMIN_PASSWORD:
    return reply(NOT_FOUND, ReplyKeyboardRemove())
  telegram_user_id = update.message.from_user.id
  if User.select().where(User.telegram_user_id == telegram_user_id).exists():
    reply(ADMIN_EXISTS)
  else:
    User.create(login='admin_{}'.format(telegram_user_id), telegram_user_id=telegram_user_id,
                name=update.message.from_user.name, chat_id=update.message.chat_id, is_admin=True)
    reply(BECOME_ADMIN_SUCCESS)


log_in_handler = RegexHandler(r'^(L|l)og in (?P<login>.{5,})$', _log_in, pass_groupdict=True)
become_admin_handler = RegexHandler(r'^(A|a)dmin (?P<password>.{5,})$', _become_admin, pass_groupdict=True)
