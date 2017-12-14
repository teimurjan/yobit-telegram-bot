from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from settings import ADMIN_PASSWORD
from models import User
from messages import REGISTRATION_SUCCESS_MSG, ALREADY_REGISTERED_MSG, \
  ADMIN_EXISTS, BECOME_ADMIN_SUCCESS, \
  LOG_IN_NOT_ALLOWED, NO_LOGIN, NOT_FOUND
from utils import get_from_list


def register(login, message) -> str:
  if login is None:
    return NO_LOGIN
  chat_id = message.chat_id
  t_id = message.from_user.id
  name = message.from_user.name
  try:
    user_with_login = User.select().where(User.login == login).get()
    user_with_same_id_exists = User.select().where(User.t_id == t_id).exists()
    if user_with_login.is_active or user_with_same_id_exists:
      return ALREADY_REGISTERED_MSG
    else:
      User.update(chat_id=chat_id, t_id=t_id, name=name).where(User.login == login).execute()
      return REGISTRATION_SUCCESS_MSG
  except User.DoesNotExist:
    return LOG_IN_NOT_ALLOWED


def become_admin(message) -> dict:
  try:
    keyboard = ReplyKeyboardMarkup([['Покажи всех пользователей'], ['Покажи игнорируемые валюты']])
    answer = lambda text, markup=keyboard: {'text': text, 'reply_markup': markup}
    user_id = message.from_user.id
    if User.select().where(User.t_id == user_id).exists():
      return answer(ADMIN_EXISTS)
    password = get_from_list(message.text.split(' '), 1)
    if password != ADMIN_PASSWORD:
      return answer(NOT_FOUND, ReplyKeyboardRemove)
    User.create(login='admin{}'.format(user_id), t_id=user_id,
                name=message.from_user.name,
                chat_id=message.chat_id, is_admin=True)
    return answer(BECOME_ADMIN_SUCCESS)
  except(User.DoesNotExist, IndexError):
    return NOT_FOUND
