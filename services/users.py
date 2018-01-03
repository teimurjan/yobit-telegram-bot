from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils import DELETE_USER_ACTION_KEY
from messages import USER_ALREADY_EXISTS, USER_NOT_EXISTS, USER_ADD_SUCCESS, USER_DELETE_SUCCESS, USER_UPDATE_SUCCESS
from models import User
from utils import get_callback_data


def show() -> InlineKeyboardMarkup:
  none_callback_data = get_callback_data()
  users = [[InlineKeyboardButton(text="Login", callback_data=none_callback_data),
            InlineKeyboardButton(text="Active", callback_data=none_callback_data),
            InlineKeyboardButton(text="Action", callback_data=none_callback_data)]]
  for user in User.select():
    delete_callback_data = get_callback_data(DELETE_USER_ACTION_KEY, {'login': user.login})
    users.append([InlineKeyboardButton(text=user.login, callback_data=none_callback_data),
                  InlineKeyboardButton(text='Yes' if user.is_active else 'No', callback_data=none_callback_data),
                  InlineKeyboardButton(text='Delete', callback_data=delete_callback_data)])
  reply_markup = InlineKeyboardMarkup(users, n_cols=3)
  return reply_markup


def add(login) -> str:
  user, created = User.get_or_create(login=login)
  if not created:
    return USER_ALREADY_EXISTS
  else:
    return USER_ADD_SUCCESS


def update(user, volume=None, bound=None) -> str:
  if volume is not None:
    user.max_allowed_volume = volume
  if bound is not None:
    user.volume_raise_bound = bound
  user.save()
  return USER_UPDATE_SUCCESS


def delete(login) -> str:
  found_user = User.select().where(User.login == login)
  if not found_user.exists():
    return USER_NOT_EXISTS
  User.delete().where(User.login == login).execute()
  return USER_DELETE_SUCCESS
