from json import dumps

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import RegexHandler

from bot.handlers.base import admin_required, login_required, unfold_groupdict
from bot.utils import DELETE_USER_ACTION_KEY
from messages import USER_ALREADY_EXISTS, USER_ADD_SUCCESS, USER_UPDATE_SUCCESS, DELETE_USER_HELP_TEXT, SHOW_USERS, \
  USER_NOT_EXISTS, USER_DELETE_SUCCESS, MIN_RAISE_LIMIT, MIN_ALLOWED_VOLUME
from models import User


@admin_required
@unfold_groupdict
def _add_user(bot, update, user, login) -> None:
  user, created = User.get_or_create(login=login)
  update.message.reply_text(USER_ALREADY_EXISTS if not created else USER_ADD_SUCCESS)


@login_required
def _show_yourself(bot, update, user) -> None:
  update.message.reply_text(user.about)


@login_required
@unfold_groupdict
def _set_user_max_volume(bot, update, user, volume) -> None:
  if volume > 0:
    user.max_allowed_volume = volume
    user.save()
    update.message.reply_text(USER_UPDATE_SUCCESS)
  else:
    update.message.reply_text()


@login_required
@unfold_groupdict
def _set_user_raise_limit(bot, update, user, limit) -> None:
  if limit > 0.5:
    user.volume_raise_limit = limit
    user.save()
    update.message.reply_text(USER_UPDATE_SUCCESS)
  else:
    update.message.reply_text(MIN_ALLOWED_VOLUME)


@admin_required
def _show_users(bot, update, user) -> None:
  users = [[InlineKeyboardButton(text="Login", callback_data='{}'),
            InlineKeyboardButton(text="Active", callback_data='{}'),
            InlineKeyboardButton(text="Action", callback_data='{}')]]
  for user in User.select():
    delete_callback_data = dumps({DELETE_USER_ACTION_KEY: {'login': user.login}})
    users.append([InlineKeyboardButton(text=user.login, callback_data='{}'),
                  InlineKeyboardButton(text='Yes' if user.is_active else 'No', callback_data='{}'),
                  InlineKeyboardButton(text='Delete', callback_data=delete_callback_data)])
  reply_markup = InlineKeyboardMarkup(users, n_cols=3)
  update.message.reply_text(DELETE_USER_HELP_TEXT, reply_markup=reply_markup)


@admin_required
def delete_user_handler(bot, update, user, login) -> None:
  reply = lambda text: bot.edit_message_text(text=text, chat_id=update.callback_query.message.chat_id,
                                             message_id=update.callback_query.message.message_id)
  found_user = User.select().where(User.login == login)
  if not found_user.exists():
    reply(USER_NOT_EXISTS)
  else:
    User.delete().where(User.login == login).execute()
    reply(USER_DELETE_SUCCESS)


add_user_handler = RegexHandler(r'^(A|a)dd user (?P<login>.{5,})$', _add_user, pass_groupdict=True)
show_yourself_handler = RegexHandler(r'^(M|m)e$', _show_yourself)
set_user_max_volume_handler = RegexHandler(r'^(S|s)et max volume (?P<volume>\d+)$',
                                           _set_user_max_volume, pass_groupdict=True)
set_user_raise_limit_handler = RegexHandler(r'^(S|s)et raise limit (?P<limit>\d+(\.\d+)?)$',
                                            _set_user_raise_limit, pass_groupdict=True)
show_users_handler = RegexHandler(r'^{}$'.format(SHOW_USERS), _show_users)
