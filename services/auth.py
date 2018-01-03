from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot.utils import USER_KEYBOARD, ADMIN_KEYBOARD
from settings import ADMIN_PASSWORD
from models import User
from messages import REGISTRATION_SUCCESS_MSG, ALREADY_REGISTERED_MSG, \
  ADMIN_EXISTS, BECOME_ADMIN_SUCCESS, \
  LOG_IN_NOT_ALLOWED, NO_LOGIN, NOT_FOUND, SHOW_USERS, SHOW_IGNORED_CURRENCIES
from utils import get_from_list


def get_answer_with_markup(text: str, markup) -> dict:
  return {'text': text, 'reply_markup': markup}


def register(login, message) -> dict:
  answer = lambda text, markup=USER_KEYBOARD: get_answer_with_markup(text, markup)
  if login is None:
    return answer(NO_LOGIN, ReplyKeyboardRemove())
  chat_id = message.chat_id
  t_id = message.from_user.id
  name = message.from_user.name
  try:
    user_with_login = User.select().where(User.login == login).get()
    user_with_same_id_exists = User.select().where(User.t_id == t_id).exists()
    if user_with_login.is_active or user_with_same_id_exists:
      return answer(ALREADY_REGISTERED_MSG)
    else:
      User.update(chat_id=chat_id, t_id=t_id, name=name).where(User.login == login).execute()
      return answer(REGISTRATION_SUCCESS_MSG)
  except User.DoesNotExist:
    return answer(LOG_IN_NOT_ALLOWED, ReplyKeyboardRemove())


def become_admin(message, password) -> dict:
  answer = lambda text, markup=ADMIN_KEYBOARD: get_answer_with_markup(text, markup)
  if password != ADMIN_PASSWORD:
    return answer(NOT_FOUND, ReplyKeyboardRemove())
  user_id = message.from_user.id
  if User.select().where(User.t_id == user_id).exists():
    return answer(ADMIN_EXISTS)
  User.create(login='admin{}'.format(user_id), t_id=user_id,
              name=message.from_user.name,
              chat_id=message.chat_id, is_admin=True)
  return answer(BECOME_ADMIN_SUCCESS)
