from telegram import ReplyKeyboardRemove

from messages import NOT_FOUND
from models import User


def admin_required(func):
  def wrapper(bot, update, **kwargs):
    user_id = update.effective_user.id
    try:
      user = User.get(telegram_user_id=user_id)
      if not user.is_admin:
        raise User.DoesNotExist()
      return func(bot, update, user=user, **kwargs)
    except User.DoesNotExist:
      return update.reply_text(NOT_FOUND, reply_markup=ReplyKeyboardRemove())

  return wrapper


def login_required(func):
  def wrapper(bot, update, **kwargs):
    user_id = update.effective_user.id
    try:
      user = User.get(telegram_user_id=user_id, is_active=True)
      return func(bot, update, user=user, **kwargs)
    except User.DoesNotExist:
      return update.reply_text(NOT_FOUND, reply_markup=ReplyKeyboardRemove())

  return wrapper


def unfold_groupdict(func):
  def wrapper(bot, update, **kwargs):
    groupdict = kwargs['groupdict']
    del kwargs['groupdict']
    return func(bot, update, **groupdict, **kwargs)

  return wrapper
